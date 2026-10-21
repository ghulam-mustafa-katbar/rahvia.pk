import React, { useState, useEffect } from 'react';
import { api } from '../../api/client';
import { useAuth } from '../../context/AuthContext';
import { 
  CheckCircle, ArrowRight, ArrowLeft, Clock, AlertCircle, 
  Sparkles, Check, Brain, Compass, BookOpen 
} from 'lucide-react';

export const AssessmentRunner = ({ onComplete, onCancel }) => {
  const { user, isAuthenticated, language } = useAuth();
  const [assessmentId, setAssessmentId] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({}); // { [question_id]: answer_value }
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [secondsElapsed, setSecondsElapsed] = useState(0);
  const [error, setError] = useState(null);

  const isUrdu = language === 'ur';

  // Timer
  useEffect(() => {
    const timer = setInterval(() => {
      setSecondsElapsed((prev) => prev + 1);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  // Initialize Assessment
  useEffect(() => {
    const init = async () => {
      try {
        setLoading(true);
        setError(null);

        // Start session
        const startRes = await api.startAssessment({
          assessment_type: 'COMPREHENSIVE'
        });

        if (!startRes || !startRes.assessment_id) {
          throw new Error(startRes?.error || 'Unable to start assessment session. Please log in first.');
        }

        const aId = startRes.assessment_id;
        setAssessmentId(aId);

        // Fetch questions
        const qRes = await api.getAssessmentQuestions(aId);
        if (qRes && qRes.questions && qRes.questions.length > 0) {
          setQuestions(qRes.questions);
        } else {
          throw new Error('No assessment questions found for this profile.');
        }
      } catch (err) {
        console.error('Assessment init error:', err);
        setError(err.message || 'Error loading assessment');
      } finally {
        setLoading(false);
      }
    };

    init();
  }, []);

  const handleSelectAnswer = (questionId, value) => {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: value,
    }));
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex((prev) => prev + 1);
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex((prev) => prev - 1);
    }
  };

  const handleSubmit = async () => {
    try {
      setSubmitting(true);
      setError(null);

      const formattedAnswers = Object.entries(answers).map(([qId, ans]) => ({
        question_id: qId,
        student_answer: String(ans),
        time_taken_seconds: Math.floor(secondsElapsed / (questions.length || 1)),
      }));

      const submitRes = await api.submitAssessment(assessmentId, {
        answers: formattedAnswers,
        time_spent_seconds: secondsElapsed,
      });

      if (submitRes && submitRes.report_id) {
        onComplete(submitRes.report_id, submitRes);
      } else {
        throw new Error(submitRes?.error || 'Submission failed');
      }
    } catch (err) {
      console.error('Assessment submit error:', err);
      setError(err.message || 'Error submitting test.');
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-3xl mx-auto py-16 px-4 text-center">
        <div className="w-16 h-16 border-4 border-emerald-200 border-t-emerald-700 rounded-full animate-spin mx-auto mb-4" />
        <h3 className="text-xl font-bold text-slate-800">
          {isUrdu ? 'آپ کا ٹیسٹ تیار کیا جا رہا ہے...' : 'Assembling Your Psychometric Assessment...'}
        </h3>
        <p className="text-slate-500 text-sm mt-1">
          {isUrdu ? 'براہ کرم چند سیکنڈ انتظار فرمائیں۔' : 'Configuring cognitive items and Pakistani RIASEC interest inventory'}
        </p>
      </div>
    );
  }

  if (error) {
    const isAuthError =
      error.toLowerCase().includes('log in') ||
      error.toLowerCase().includes('session') ||
      error.toLowerCase().includes('credentials') ||
      error.toLowerCase().includes('authorized');

    return (
      <div className="max-w-xl mx-auto my-12 p-8 bg-white border border-slate-200 rounded-3xl text-center shadow-lg">
        <div className="w-14 h-14 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center mx-auto mb-4 border border-amber-200">
          <AlertCircle className="w-8 h-8" />
        </div>
        <h3 className="text-xl font-bold text-slate-900 mb-2">
          {isAuthError 
            ? (isUrdu ? 'لاگ ان درکار ہے' : 'Student Login Required')
            : (isUrdu ? 'ٹیسٹ شروع کرنے میں مسئلہ پیش آیا' : 'Unable to Start Assessment')}
        </h3>
        <p className="text-slate-600 text-sm mb-6 leading-relaxed">
          {isAuthError
            ? (isUrdu 
                ? 'کیریئر رہنمائی ٹیسٹ شروع کرنے اور اپنا ریکارڈ محفوظ کرنے کے لیے براہ کرم پہلے اپنے اسٹوڈنٹ اکاؤنٹ میں لاگ ان کریں۔'
                : 'To take the diagnostic assessment and save your Sindh Class 11 educational roadmap, please sign in with your student account.')
            : error}
        </p>
        <div className="flex flex-wrap items-center justify-center gap-3">
          <button
            onClick={onCancel}
            className="px-6 py-3 bg-emerald-800 hover:bg-emerald-900 text-white font-bold rounded-xl text-sm transition-all shadow-md shadow-emerald-900/20"
          >
            {isAuthError
              ? (isUrdu ? 'لاگ ان اسکرین پر جائیں' : 'Sign In / Register')
              : (isUrdu ? 'واپس جائیں' : 'Return to Home')}
          </button>
        </div>
      </div>
    );
  }

  const currentQ = questions[currentIndex];
  const progressPercent = Math.round(((currentIndex + 1) / questions.length) * 100);
  const answeredCount = Object.keys(answers).length;
  const isCurrentAnswered = currentQ && answers[currentQ.question_id] !== undefined;
  const isLastQuestion = currentIndex === questions.length - 1;

  // Grade context differentiation
  const studentGrade = user?.student_profile?.current_grade || user?.grade || 'MATRIC_10TH';
  const isClass9 = String(studentGrade).includes('9');

  // Format time MM:SS
  const mins = Math.floor(secondsElapsed / 60);
  const secs = secondsElapsed % 60;
  const formattedTime = `${mins}:${secs < 10 ? '0' : ''}${secs}`;

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6">
      
      {/* Grade Context Alert Banner */}
      <div className={`p-4 rounded-2xl mb-4 border flex items-center justify-between gap-3 text-xs ${
        isClass9 ? 'bg-sky-50 border-sky-200 text-sky-900' : 'bg-emerald-50 border-emerald-200 text-emerald-950'
      }`}>
        <div className="flex items-center gap-2.5">
          <Brain className={`w-4 h-4 ${isClass9 ? 'text-sky-600' : 'text-emerald-700'}`} />
          <span className="font-bold">
            {isClass9 
              ? (isUrdu ? 'نہم جماعت (SSC Part-I) - تشخیصی و فکری استعداد ٹیسٹ' : 'Class 9 (SSC Part-I): Foundational Exploration & Skill Diagnostic')
              : (isUrdu ? 'دہم جماعت (SSC Part-II) - انٹرمیڈیٹ و SECCAP داخلہ رہنمائی ٹیسٹ' : 'Class 10 (SSC Part-II): Class 11 Pathway & SECCAP Preparation Assessment')}
          </span>
        </div>
        <span className="font-semibold text-[11px] opacity-80 hidden sm:inline">
          {isClass9 ? 'Non-punitive diagnostic' : 'College readiness evaluation'}
        </span>
      </div>

      {/* Top Header & Progress */}
      <div className="bg-white rounded-2xl p-6 shadow-xs border border-slate-200 mb-6">
        <div className="flex flex-wrap items-center justify-between gap-4 mb-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider bg-emerald-100 text-emerald-800 border border-emerald-200">
                {currentQ?.category}
              </span>
              <span className="text-xs font-medium text-slate-500">
                {currentQ?.dimension}
              </span>
            </div>
            <h2 className="text-lg font-extrabold text-slate-900 mt-1">
              {isUrdu ? `سوال ${currentIndex + 1} از ${questions.length}` : `Question ${currentIndex + 1} of ${questions.length}`}
            </h2>
          </div>

          <div className="flex items-center gap-4 text-xs font-semibold text-slate-600">
            <div className="flex items-center gap-1.5 bg-slate-100 px-3 py-1.5 rounded-lg">
              <Clock className="w-4 h-4 text-slate-500" />
              <span>{formattedTime}</span>
            </div>
            <div className="flex items-center gap-1.5 bg-emerald-50 text-emerald-800 px-3 py-1.5 rounded-lg border border-emerald-200">
              <Check className="w-3.5 h-3.5 text-emerald-600" />
              <span>{answeredCount} / {questions.length} {isUrdu ? 'مکمل' : 'Answered'}</span>
            </div>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
          <div 
            className="bg-emerald-600 h-full rounded-full transition-all duration-300 ease-out"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
      </div>

      {/* Main Question Card */}
      {currentQ && (
        <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-sm border border-slate-200">
          
          {/* Question Text in English & Urdu */}
          <div className="mb-8">
            <h1 className="text-xl sm:text-2xl font-bold text-slate-900 leading-relaxed mb-3">
              {currentQ.text}
            </h1>
            
            {currentQ.text_urdu && (
              <p className="font-urdu text-lg sm:text-xl text-emerald-950 bg-emerald-50/70 p-4 rounded-xl border border-emerald-100 leading-loose">
                {currentQ.text_urdu}
              </p>
            )}
          </div>

          {/* Options / Scale */}
          <div className="space-y-3">
            {currentQ.options && currentQ.options.map((opt, idx) => {
              const optId = opt.id || String(idx + 1);
              const isSelected = String(answers[currentQ.question_id]) === String(optId);

              return (
                <div
                  key={optId}
                  onClick={() => handleSelectAnswer(currentQ.question_id, optId)}
                  className={`flex items-center justify-between p-4 sm:p-5 rounded-2xl cursor-pointer border-2 transition-all ${
                    isSelected
                      ? 'border-emerald-600 bg-emerald-50/50 shadow-xs ring-2 ring-emerald-500/20'
                      : 'border-slate-200 hover:border-emerald-300 hover:bg-slate-50'
                  }`}
                >
                  <div className="flex items-center gap-4 flex-1">
                    <div className={`w-8 h-8 rounded-xl flex items-center justify-center font-bold text-sm shrink-0 transition-colors ${
                      isSelected
                        ? 'bg-emerald-700 text-white'
                        : 'bg-slate-100 text-slate-600 group-hover:bg-slate-200'
                    }`}>
                      {optId}
                    </div>
                    <span className="text-base font-semibold text-slate-800">
                      {opt.text}
                    </span>
                  </div>

                  {opt.text_urdu && (
                    <span className="font-urdu text-sm font-semibold text-slate-600 pl-4 border-l border-slate-200 ml-4 hidden sm:inline-block">
                      {opt.text_urdu}
                    </span>
                  )}
                </div>
              );
            })}
          </div>

          {/* Question Stepper Bottom Controls */}
          <div className="flex items-center justify-between gap-4 mt-10 pt-6 border-t border-slate-200">
            <button
              onClick={handlePrev}
              disabled={currentIndex === 0}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-bold transition-all ${
                currentIndex === 0
                  ? 'text-slate-300 cursor-not-allowed'
                  : 'text-slate-700 hover:bg-slate-100 border border-slate-200'
              }`}
            >
              <ArrowLeft className="w-4 h-4" />
              <span>{isUrdu ? 'پچھلا سوال' : 'Previous'}</span>
            </button>

            {isLastQuestion ? (
              <button
                onClick={handleSubmit}
                disabled={submitting}
                className="flex items-center gap-2 px-8 py-3 rounded-xl text-sm font-bold text-white bg-emerald-700 hover:bg-emerald-800 shadow-md shadow-emerald-900/20 transition-all disabled:opacity-50"
              >
                {submitting ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    <span>{isUrdu ? 'رپورٹ تیار ہو رہی ہے...' : 'Generating Career Report...'}</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4" />
                    <span>{isUrdu ? 'ٹیسٹ جمع کریں اور نتائج دیکھیں' : 'Submit Test & View Results'}</span>
                  </>
                )}
              </button>
            ) : (
              <button
                onClick={handleNext}
                className="flex items-center gap-2 px-6 py-2.5 rounded-xl text-sm font-bold text-white bg-slate-900 hover:bg-slate-800 transition-all shadow-xs"
              >
                <span>{isUrdu ? 'اگلا سوال' : 'Next'}</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            )}
          </div>

        </div>
      )}

      {/* Mini Question Map for Quick Navigation */}
      <div className="mt-6 bg-white p-4 rounded-2xl border border-slate-200 shadow-xs">
        <p className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
          {isUrdu ? 'تمام سوالات کا خلاصہ:' : 'Question Grid Navigation:'}
        </p>
        <div className="flex flex-wrap gap-2">
          {questions.map((q, idx) => {
            const isAnswered = answers[q.question_id] !== undefined;
            const isCurrent = idx === currentIndex;
            return (
              <button
                key={q.question_id}
                onClick={() => setCurrentIndex(idx)}
                className={`w-8 h-8 rounded-lg text-xs font-bold transition-all ${
                  isCurrent
                    ? 'ring-2 ring-emerald-600 bg-emerald-800 text-white'
                    : isAnswered
                    ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                    : 'bg-slate-100 text-slate-500 hover:bg-slate-200'
                }`}
              >
                {idx + 1}
              </button>
            );
          })}
        </div>
      </div>

    </div>
  );
};
