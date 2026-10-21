import React from 'react';
import { useAuth } from '../context/AuthContext';
import { 
  Compass, Award, BookOpen, School, ShieldCheck, 
  ArrowRight, Sparkles, CheckCircle2, TrendingUp, Users 
} from 'lucide-react';

export const HomeView = ({ onStartAssessment, onExploreCareers, onOpenDashboard }) => {
  const { language } = useAuth();
  const isUrdu = language === 'ur';

  return (
    <div className="space-y-16 pb-16">
      
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-emerald-950 via-emerald-900 to-slate-900 text-white py-16 sm:py-24 px-4 sm:px-6 lg:px-8">
        <div className="max-w-5xl mx-auto text-center space-y-6 relative z-10">
          
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-800/80 border border-emerald-500/30 text-emerald-300 text-xs font-bold tracking-wide">
            <Sparkles className="w-4 h-4 text-emerald-400" />
            <span>{isUrdu ? 'پاکستان کا پہلا سائنسی کیریئر گائیڈنس پلیٹ فارم' : 'Pakistan’s Premier Psychometric Career Guidance Platform'}</span>
          </div>

          <h1 className="text-3xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-tight">
            {isUrdu ? (
              <span className="font-urdu leading-snug">
                میٹرک اور انٹر کے بعد صحیح تعلیمی راستے کا سائنسی انتخاب
              </span>
            ) : (
              <>
                Objective Career Pathways for <br className="hidden sm:inline" />
                <span className="text-emerald-400">Matric & Intermediate</span> Students
              </>
            )}
          </h1>

          <p className="max-w-2xl mx-auto text-sm sm:text-base text-emerald-100/90 leading-relaxed font-normal">
            {isUrdu ? (
              <span className="font-urdu leading-loose">
                محض افواہوں یا روایتی رجحان پر انحصار نہ کریں۔ جدید سائیکومیٹرک ٹیسٹ، ہالینڈ ریاسیک (RIASEC) ماڈل اور پاکستانی جامعات کے داخلہ معیارات کے تحت اپنی قدرتی صلاحیتیں دریافت کریں۔
              </span>
            ) : (
              'Move beyond hearsay and societal pressure. Discover your natural cognitive aptitude and Holland RIASEC interest profile mapped directly to Pakistani intermediate streams (FSc, ICS, I.Com, FA) and university degrees.'
            )}
          </p>

          <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
            <button
              onClick={onStartAssessment}
              className="flex items-center gap-2 px-7 py-3.5 rounded-2xl bg-white text-emerald-950 font-extrabold text-sm hover:bg-emerald-50 transition-all shadow-xl shadow-black/30"
            >
              <span>{isUrdu ? 'ابھی تشخیصی ٹیسٹ شروع کریں' : 'Start Free Assessment'}</span>
              <ArrowRight className="w-4 h-4 text-emerald-800" />
            </button>

            <button
              onClick={onExploreCareers}
              className="px-6 py-3.5 rounded-2xl bg-emerald-800/60 hover:bg-emerald-800 text-emerald-100 font-bold text-sm border border-emerald-600/40 transition-colors"
            >
              {isUrdu ? 'کیریئر انسائیکلوپیڈیا دیکھیں' : 'Browse 500+ Pakistan Careers'}
            </button>
          </div>

          {/* Quick Metrics */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-12 max-w-4xl mx-auto border-t border-emerald-800/60 text-left">
            <div>
              <p className="text-2xl font-extrabold text-emerald-300">500+</p>
              <p className="text-xs text-emerald-200/80">Local Career Fields</p>
            </div>
            <div>
              <p className="text-2xl font-extrabold text-emerald-300">100%</p>
              <p className="text-xs text-emerald-200/80">Pakistani Boards Covered</p>
            </div>
            <div>
              <p className="text-2xl font-extrabold text-emerald-300">RIASEC</p>
              <p className="text-xs text-emerald-200/80">Psychometric Norms</p>
            </div>
            <div>
              <p className="text-2xl font-extrabold text-emerald-300">PDPA</p>
              <p className="text-xs text-emerald-200/80">Minors' Data Protection</p>
            </div>
          </div>

        </div>
      </section>

      {/* 3 Step Assessment Flow */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6">
        <div className="text-center space-y-2 mb-12">
          <span className="text-xs font-bold uppercase tracking-wider text-emerald-800 bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200">
            {isUrdu ? 'طریقہ کار' : 'Structured 3-Step Methodology'}
          </span>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
            How Rahvia Guides Pakistani Students
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-7 rounded-3xl border border-slate-200 shadow-xs space-y-4 hover:border-emerald-400 transition-all">
            <div className="w-12 h-12 rounded-2xl bg-emerald-100 text-emerald-800 flex items-center justify-center font-extrabold text-lg">
              1
            </div>
            <h3 className="text-lg font-bold text-slate-900">
              Interactive Psychometric Test
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              10-15 minute mobile-friendly assessment evaluating numerical problem-solving, verbal logic, spatial visualization, and Holland RIASEC work interest factors.
            </p>
          </div>

          <div className="bg-white p-7 rounded-3xl border border-slate-200 shadow-xs space-y-4 hover:border-emerald-400 transition-all">
            <div className="w-12 h-12 rounded-2xl bg-emerald-100 text-emerald-800 flex items-center justify-center font-extrabold text-lg">
              2
            </div>
            <h3 className="text-lg font-bold text-slate-900">
              Rule-Based Stream Mapping
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Synthesizes psychometric percentiles with academic marks to objectively recommend Pre-Engineering, Pre-Medical, ICS, I.Com, or Humanities.
            </p>
          </div>

          <div className="bg-white p-7 rounded-3xl border border-slate-200 shadow-xs space-y-4 hover:border-emerald-400 transition-all">
            <div className="w-12 h-12 rounded-2xl bg-emerald-100 text-emerald-800 flex items-center justify-center font-extrabold text-lg">
              3
            </div>
            <h3 className="text-lg font-bold text-slate-900">
              Downloadable Pathway PDF Report
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Instant comprehensive narrative report with strengths breakdown, degree recommendations, required entry tests (ECAT, MDCAT, NET, FAST), and university roadmaps.
            </p>
          </div>
        </div>
      </section>

      {/* School Counselor Banner */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6">
        <div className="bg-emerald-50 rounded-3xl p-8 sm:p-12 border border-emerald-200 flex flex-wrap items-center justify-between gap-8">
          <div className="max-w-xl space-y-3">
            <div className="inline-flex items-center gap-2 text-emerald-800 text-xs font-bold uppercase tracking-wider">
              <School className="w-4 h-4" />
              <span>For Schools & Colleges</span>
            </div>
            <h3 className="text-2xl font-extrabold text-emerald-950">
              Institutional Dashboards & Batch Analytics
            </h3>
            <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
              Principals and counselors can batch-enroll full student classes, schedule assessments, and monitor cohort distribution heatmaps to identify at-risk students and guide subject streaming.
            </p>
          </div>

          <button
            onClick={onOpenDashboard}
            className="px-6 py-3 rounded-xl bg-emerald-800 hover:bg-emerald-900 text-white font-bold text-sm shadow-md shadow-emerald-900/20 transition-all"
          >
            Access Counselor Portal
          </button>
        </div>
      </section>

      {/* Compliance / Privacy Callout */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6">
        <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 flex items-start gap-4">
          <div className="w-10 h-10 rounded-2xl bg-slate-100 text-slate-700 flex items-center justify-center shrink-0">
            <ShieldCheck className="w-5 h-5 text-emerald-700" />
          </div>
          <div className="space-y-1">
            <h4 className="text-sm font-bold text-slate-900">
              Privacy by Design (Pakistani PDPA Compliance)
            </h4>
            <p className="text-xs text-slate-500 leading-relaxed">
              Rahvia Platform strictly adheres to local data protection principles: verifiable parental consent for minors, encrypted storage of educational records, zero third-party commercial advertising, and data minimization standards.
            </p>
          </div>
        </div>
      </section>

    </div>
  );
};
