import React, { useState, useEffect } from 'react';
import { api } from '../../api/client';
import { useAuth } from '../../context/AuthContext';
import { 
  User, ShieldCheck, CheckCircle2, Save, AlertCircle, 
  BookOpen, School, Sparkles, Check 
} from 'lucide-react';

export const StudentProfileView = () => {
  const { user, language } = useAuth();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  const isUrdu = language === 'ur';

  useEffect(() => {
    const loadProfile = async () => {
      try {
        setLoading(true);
        const data = await api.getProfile();
        setProfile(data);
      } catch (err) {
        console.error('Error loading profile:', err);
      } finally {
        setLoading(false);
      }
    };
    loadProfile();
  }, []);

  const handleChange = (field, value) => {
    setProfile((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleScoreChange = (subject, score) => {
    setProfile((prev) => ({
      ...prev,
      academic_scores: {
        ...(prev.academic_scores || {}),
        [subject]: Number(score),
      },
    }));
  };

  const handleSave = async (e) => {
    e.preventDefault();
    try {
      setSaving(true);
      setSuccessMsg('');
      setErrorMsg('');

      const res = await api.updateProfile(profile);
      if (res && res.student_id) {
        setProfile(res);
        setSuccessMsg(isUrdu ? 'پروفائل کامیابی کے ساتھ اپ ڈیٹ ہو گئی!' : 'Profile updated successfully!');
      } else {
        throw new Error(res?.detail || 'Failed to update profile');
      }
    } catch (err) {
      setErrorMsg(err.message || 'Error saving profile');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-3xl mx-auto py-16 text-center">
        <div className="w-10 h-10 border-4 border-emerald-200 border-t-emerald-700 rounded-full animate-spin mx-auto mb-2" />
        <p className="text-slate-500 text-sm">Loading academic profile...</p>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="max-w-md mx-auto py-12 text-center text-slate-500 text-sm">
        Student profile not available. Please ensure you are logged into a student account.
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 space-y-6">
      
      {/* Header */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-xs">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 rounded-2xl bg-emerald-100 text-emerald-800 flex items-center justify-center font-bold">
            <User className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-2xl font-extrabold text-slate-900">
              {isUrdu ? 'طالب علم کا تعلیمی پروفائل' : 'Student Academic Profile'}
            </h1>
            <p className="text-xs text-slate-500">
              {profile.email} • {profile.school_name || 'Independent Student'}
            </p>
          </div>
        </div>
      </div>

      {successMsg && (
        <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-2xl text-emerald-800 text-xs font-bold flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          <span>{successMsg}</span>
        </div>
      )}

      {errorMsg && (
        <div className="p-4 bg-rose-50 border border-rose-200 rounded-2xl text-rose-800 text-xs font-bold flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-rose-600" />
          <span>{errorMsg}</span>
        </div>
      )}

      <form onSubmit={handleSave} className="space-y-6">
        
        {/* Basic Academic Info */}
        <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-xs space-y-5">
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <BookOpen className="w-4 h-4 text-emerald-700" />
            <span>Academic Curriculum & School Board</span>
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Full Name</label>
              <input
                type="text"
                value={profile.name || ''}
                onChange={(e) => handleChange('name', e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-600/20"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Education Board</label>
              <input
                type="text"
                value={profile.board || ''}
                onChange={(e) => handleChange('board', e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-600/20"
                placeholder="e.g. FBISE Islamabad, BISE Lahore"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Current Grade Level</label>
              <select
                value={profile.current_grade || 'MATRIC_10TH'}
                onChange={(e) => handleChange('current_grade', e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm bg-slate-50 focus:outline-none focus:ring-2 focus:ring-emerald-600/20"
              >
                <option value="MATRIC_9TH">Matric 9th Grade</option>
                <option value="MATRIC_10TH">Matric 10th Grade</option>
                <option value="INTER_11TH">Intermediate 1st Year (11th Grade)</option>
                <option value="INTER_12TH">Intermediate 2nd Year (12th Grade)</option>
                <option value="O_LEVELS">Cambridge O-Levels</option>
                <option value="A_LEVELS">Cambridge A-Levels</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Elective Stream</label>
              <select
                value={profile.elective_group || 'SCIENCE_CS'}
                onChange={(e) => handleChange('elective_group', e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm bg-slate-50 focus:outline-none focus:ring-2 focus:ring-emerald-600/20"
              >
                <option value="SCIENCE_CS">Matric Science (Computer Science)</option>
                <option value="SCIENCE_BIO">Matric Science (Biology)</option>
                <option value="ARTS_GENERAL">Matric Arts / General</option>
                <option value="PRE_ENGINEERING">FSc Pre-Engineering</option>
                <option value="PRE_MEDICAL">FSc Pre-Medical</option>
                <option value="ICS_CS">ICS (Computer Science)</option>
                <option value="ICOM">I.Com (Commerce)</option>
                <option value="FA_HUMANITIES">FA Humanities & Arts</option>
              </select>
            </div>

            <div className="sm:col-span-2">
              <label className="block text-xs font-bold text-slate-700 mb-1">
                {isUrdu ? 'تعلیمی ادارہ (اسکول یا کالج)' : 'Educational Institution (School / College)'}
              </label>
              <div className="relative">
                <input
                  type="text"
                  value={profile.school_name || (isUrdu ? 'آزاد امیدوار / کوئی اسکول منسلک نہیں' : 'Independent Candidate / Unaffiliated')}
                  disabled
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-slate-600 text-sm font-medium"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Academic Marks Entry */}
        <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-xs space-y-4">
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-emerald-700" />
            <span>Subject Scores (Out of 100 or Board Percentage)</span>
          </h3>
          <p className="text-xs text-slate-500">
            These scores are integrated into the recommendation algorithm to cross-check aptitude metrics:
          </p>

          <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 pt-2">
            {['Math', 'Physics', 'Chemistry', 'Biology', 'Computer'].map((sub) => (
              <div key={sub} className="bg-slate-50 p-3 rounded-2xl border border-slate-200 text-center">
                <label className="block text-xs font-bold text-slate-700 mb-1">{sub}</label>
                <input
                  type="number"
                  min="0"
                  max="100"
                  value={profile.academic_scores?.[sub] ?? 80}
                  onChange={(e) => handleScoreChange(sub, e.target.value)}
                  className="w-16 mx-auto text-center font-extrabold text-sm py-1.5 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-emerald-600/20"
                />
              </div>
            ))}
          </div>
        </div>

        {/* Parental Consent (Pakistani PDPA Compliance) */}
        <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-xs space-y-4">
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-700" />
            <span>Minors' Data Protection & Parental Consent (PDPA Compliance)</span>
          </h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            In compliance with Pakistani minors' data protection standards, students under age 18 must verify parent/guardian authorization for educational profile recording.
          </p>

          <div className="flex items-start gap-3 p-4 bg-emerald-50/50 rounded-2xl border border-emerald-200">
            <input
              type="checkbox"
              id="consent"
              checked={profile.parent_consent}
              onChange={(e) => handleChange('parent_consent', e.target.checked)}
              className="mt-1 w-4 h-4 rounded text-emerald-700 focus:ring-emerald-600 cursor-pointer"
            />
            <label htmlFor="consent" className="text-xs text-slate-700 leading-normal cursor-pointer font-medium">
              I certify that my parent or legal guardian has reviewed and consented to the career counseling assessment and academic profile storage on Rahvia Platform.
            </label>
          </div>
        </div>

        <div className="text-right">
          <button
            type="submit"
            disabled={saving}
            className="flex items-center gap-2 px-8 py-3 rounded-xl bg-emerald-800 hover:bg-emerald-900 text-white font-bold text-sm shadow-md shadow-emerald-900/20 transition-all disabled:opacity-50 ml-auto"
          >
            <Save className="w-4 h-4" />
            <span>{saving ? 'Saving...' : 'Save Profile Changes'}</span>
          </button>
        </div>

      </form>

    </div>
  );
};
