import React, { useState, useEffect } from 'react';
import { api } from '../../api/client';
import { useAuth } from '../../context/AuthContext';
import {
  User,
  School,
  ShieldCheck,
  Building2,
  Mail,
  Phone,
  Calendar,
  Save,
  CheckCircle2,
  AlertCircle,
  ExternalLink,
  Users,
  Award,
  Sparkles
} from 'lucide-react';

export const CounselorProfileView = ({ onOpenDashboard }) => {
  const { user, updateUser, language } = useAuth();
  const isUrdu = language === 'ur';

  const [firstName, setFirstName] = useState(user?.first_name || '');
  const [lastName, setLastName] = useState(user?.last_name || '');
  const [phone, setPhone] = useState(user?.phone_number || '');
  const [assignedSchools, setAssignedSchools] = useState(user?.assigned_schools || []);

  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  // Refresh user data & assigned schools from /auth/me on mount
  useEffect(() => {
    let isMounted = true;
    const fetchUserData = async () => {
      try {
        setLoading(true);
        const me = await api.getCurrentUser();
        if (isMounted && me) {
          updateUser(me);
          setFirstName(me.first_name || '');
          setLastName(me.last_name || '');
          setPhone(me.phone_number || '');
          if (Array.isArray(me.assigned_schools)) {
            setAssignedSchools(me.assigned_schools);
          }
        }
      } catch (err) {
        console.error('Failed to load counselor details:', err);
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    fetchUserData();
    return () => {
      isMounted = false;
    };
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setSuccessMsg('');
    setErrorMsg('');

    try {
      const res = await api.updateCurrentUser({
        first_name: firstName.trim(),
        last_name: lastName.trim(),
        phone_number: phone.trim(),
      });

      if (res && res.email) {
        updateUser(res);
        if (Array.isArray(res.assigned_schools)) {
          setAssignedSchools(res.assigned_schools);
        }
        setSuccessMsg(
          isUrdu
            ? 'کونسلر پروفائل کامیابی کے ساتھ اپ ڈیٹ ہو گئی!'
            : 'Counselor profile updated successfully!'
        );
      } else {
        throw new Error('Failed to update profile');
      }
    } catch (err) {
      setErrorMsg(err.message || 'Error updating profile');
    } finally {
      setSaving(false);
    }
  };

  const displayName =
    firstName || lastName
      ? `${firstName} ${lastName}`.trim()
      : isUrdu
      ? 'اسکول کونسلر'
      : 'School Counselor';

  return (
    <div className={`max-w-4xl mx-auto py-8 px-4 sm:px-6 space-y-6 ${isUrdu ? 'rtl text-right' : 'ltr text-left'}`}>
      
      {/* Header Banner */}
      <div className="bg-gradient-to-br from-emerald-900 via-teal-900 to-slate-900 rounded-3xl p-6 sm:p-8 text-white shadow-xl relative overflow-hidden">
        <div className="absolute top-0 right-0 w-80 h-80 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
        
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 relative z-10">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-2xl bg-white/10 border border-white/20 backdrop-blur-md flex items-center justify-center text-emerald-300 font-extrabold text-2xl shadow-inner">
              {firstName ? firstName.charAt(0).toUpperCase() : <School className="w-8 h-8" />}
            </div>
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-black tracking-wider uppercase bg-emerald-400/20 text-emerald-300 border border-emerald-400/30">
                  {isUrdu ? 'اسکول کونسلر اور ایڈوائزر' : 'Designated School Counselor'}
                </span>
                <span className="inline-flex items-center gap-1 text-[11px] text-emerald-200">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                  {isUrdu ? 'تصدیق شدہ' : 'Verified'}
                </span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
                {displayName}
              </h1>
              <p className="text-emerald-200/80 text-sm mt-0.5 flex items-center gap-2">
                <Mail className="w-3.5 h-3.5" />
                {user?.email}
              </p>
            </div>
          </div>

          {onOpenDashboard && (
            <button
              onClick={onOpenDashboard}
              className="inline-flex items-center justify-center gap-2 px-5 py-3 rounded-2xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-sm transition-all duration-150 shadow-lg shadow-emerald-950/40 hover:scale-[1.02] active:scale-[0.98]"
            >
              <Users className="w-4 h-4" />
              <span>{isUrdu ? 'اسکول کوہورٹ ڈیش بورڈ کھولیں' : 'Open Cohort Dashboard'}</span>
              <ExternalLink className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>

      {/* Assigned Institutions Section */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-xs space-y-4">
        <div className="flex items-center justify-between pb-4 border-b border-slate-100">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-emerald-50 text-emerald-700 flex items-center justify-center">
              <Building2 className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-slate-900">
                {isUrdu ? 'منسلک تعلیمی ادارہ (اسکول / کالج)' : 'Designated Educational Institution'}
              </h2>
              <p className="text-xs text-slate-500">
                {isUrdu
                  ? 'آپ کا اکاؤنٹ صرف اس ادارے کے رجسٹرڈ طلباء کے ڈیٹا تک رسائی رکھتا ہے'
                  : 'Institutional multi-tenant isolation ensures data access is restricted to this campus.'}
              </p>
            </div>
          </div>
        </div>

        {assignedSchools && assignedSchools.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
            {assignedSchools.map((school) => (
              <div
                key={school.school_id}
                className="p-5 rounded-2xl border border-emerald-100 bg-gradient-to-br from-emerald-50/50 to-white hover:border-emerald-300 transition-all shadow-xs"
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-extrabold text-slate-900 text-base">
                        {school.name}
                      </span>
                    </div>
                    <span className="inline-block mt-1 font-mono text-xs font-bold text-emerald-800 bg-emerald-100/70 px-2 py-0.5 rounded-md">
                      {isUrdu ? 'کوڈ:' : 'Code:'} {school.code}
                    </span>
                  </div>
                  {school.verified && (
                    <span className="px-2 py-0.5 text-[11px] font-semibold bg-emerald-100 text-emerald-800 rounded-full flex items-center gap-1 shrink-0">
                      <CheckCircle2 className="w-3 h-3 text-emerald-700" />
                      {isUrdu ? 'تصدیق شدہ' : 'Verified'}
                    </span>
                  )}
                </div>

                <div className="mt-4 pt-3 border-t border-slate-100 space-y-1.5 text-xs text-slate-600">
                  <div className="flex justify-between">
                    <span className="text-slate-500">{isUrdu ? 'بورڈ:' : 'Board:'}</span>
                    <span className="font-medium text-slate-800">{school.board_display || school.board}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">{isUrdu ? 'شہر / صوبہ:' : 'City / Province:'}</span>
                    <span className="font-medium text-slate-800">
                      {[school.city, school.province_display || school.province].filter(Boolean).join(', ')}
                    </span>
                  </div>
                  {school.student_count !== undefined && (
                    <div className="flex justify-between items-center pt-1 text-emerald-800 font-bold">
                      <span className="flex items-center gap-1.5">
                        <Users className="w-3.5 h-3.5" />
                        {isUrdu ? 'رجسٹرڈ طلباء:' : 'Enrolled Cohort:'}
                      </span>
                      <span>{school.student_count} {isUrdu ? 'طلباء' : 'Students'}</span>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 px-4 border border-dashed border-slate-200 rounded-2xl bg-slate-50/50">
            <School className="w-10 h-10 text-slate-400 mx-auto mb-2" />
            <p className="text-sm font-bold text-slate-700">
              {isUrdu ? 'کوئی ادارہ منسلک نہیں ہے' : 'No institution directly assigned yet'}
            </p>
            <p className="text-xs text-slate-500 max-w-sm mx-auto mt-1">
              {isUrdu
                ? 'اپنے ادارے کے ایڈمن سے رابطہ کریں یا سپورٹ ٹیم کو اسکول کوڈ شامل کرنے کی درخواست کریں'
                : 'Please contact the system administrator to link your counselor account to your school code.'}
            </p>
          </div>
        )}
      </div>

      {/* Edit Personal & Contact Details */}
      <form onSubmit={handleSave} className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-xs space-y-6">
        <div className="flex items-center justify-between pb-4 border-b border-slate-100">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-slate-100 text-slate-700 flex items-center justify-center">
              <User className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-slate-900">
                {isUrdu ? 'کونسلر کی ذاتی معلومات' : 'Counselor Profile Details'}
              </h2>
              <p className="text-xs text-slate-500">
                {isUrdu ? 'اپنا نام اور رابطہ نمبر اپ ڈیٹ کریں' : 'Manage your advisor contact info and details'}
              </p>
            </div>
          </div>
        </div>

        {successMsg && (
          <div className="p-3.5 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-2xl text-xs flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
            <span>{successMsg}</span>
          </div>
        )}

        {errorMsg && (
          <div className="p-3.5 bg-rose-50 border border-rose-200 text-rose-800 rounded-2xl text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
            <span>{errorMsg}</span>
          </div>
        )}

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1.5">
              {isUrdu ? 'پہلا نام' : 'First Name'}
            </label>
            <input
              type="text"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-700/20 focus:border-emerald-700 text-sm"
              placeholder={isUrdu ? 'مثال: محمد' : 'e.g. Dr. Tariq'}
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1.5">
              {isUrdu ? 'آخری نام' : 'Last Name'}
            </label>
            <input
              type="text"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-700/20 focus:border-emerald-700 text-sm"
              placeholder={isUrdu ? 'مثال: علوی' : 'e.g. Alvi'}
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1.5">
              {isUrdu ? 'سرکاری ای میل ایڈریس' : 'Official Email Address'}
            </label>
            <div className="relative">
              <input
                type="email"
                value={user?.email || ''}
                disabled
                className="w-full px-4 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-slate-500 cursor-not-allowed text-sm"
              />
              <span className="absolute right-3 top-3 text-[10px] uppercase font-bold text-slate-400">
                {isUrdu ? 'تبدیل نہیں ہو سکتا' : 'Locked'}
              </span>
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1.5">
              {isUrdu ? 'رابطہ فون نمبر' : 'Phone / Mobile Number'}
            </label>
            <input
              type="tel"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-700/20 focus:border-emerald-700 text-sm"
              placeholder={isUrdu ? '0300-1234567' : '+92 300 1234567'}
            />
          </div>
        </div>

        <div className="pt-2 flex justify-end">
          <button
            type="submit"
            disabled={saving}
            className="inline-flex items-center gap-2 px-6 py-2.5 bg-emerald-800 hover:bg-emerald-900 text-white rounded-xl text-sm font-bold transition-all shadow-sm disabled:opacity-60"
          >
            {saving ? (
              <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <Save className="w-4 h-4" />
            )}
            <span>{isUrdu ? 'تبدیلیاں محفوظ کریں' : 'Save Changes'}</span>
          </button>
        </div>
      </form>

      {/* Security & PDPA Compliance Note */}
      <div className="p-4 bg-slate-100 rounded-2xl border border-slate-200 text-xs text-slate-600 flex items-start gap-3">
        <ShieldCheck className="w-5 h-5 text-emerald-700 shrink-0 mt-0.5" />
        <div>
          <span className="font-bold text-slate-800">
            {isUrdu ? 'پاکستان پرسنل ڈیٹا پروٹیکشن ایکٹ (PDPA 2023) کے عین مطابق:' : 'PDPA 2023 Compliance & Data Isolation:'}
          </span>{' '}
          {isUrdu
            ? 'کونسلر کا اکاؤنٹ صرف اپنے منسلک تعلیمی ادارے کے رجسٹرڈ طلباء کے رجحانات اور رپورٹس دیکھ سکتا ہے۔ طلباء کے ذاتی ٹیسٹ کے نتائج رازداری کے ساتھ محفوظ رہتے ہیں۔'
            : 'All psychometric analysis data is strictly siloed per educational institution. As a verified counselor, your access is confined exclusively to students enrolled under your campus code.'}
        </div>
      </div>

    </div>
  );
};
