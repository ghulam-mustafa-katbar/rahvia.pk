import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { 
  Lock, Mail, User, ShieldCheck, CheckCircle2, 
  ArrowRight, AlertCircle, Compass, School 
} from 'lucide-react';

export const AuthView = ({ defaultTab = 'login', onSuccess }) => {
  const { login, register, language } = useAuth();
  const [isRegister, setIsRegister] = useState(defaultTab === 'register');
  const [role, setRole] = useState('STUDENT');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [grade, setGrade] = useState('MATRIC_10TH');
  const [board, setBoard] = useState('FBISE Islamabad');
  const [electiveGroup, setElectiveGroup] = useState('SCIENCE_CS');
  const [schoolCode, setSchoolCode] = useState('IMC-G-F72');

  // Guardian consent fields (PDPA compliance)
  const [guardianName, setGuardianName] = useState('');
  const [guardianEmail, setGuardianEmail] = useState('');
  const [parentConsent, setParentConsent] = useState(true);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const isUrdu = language === 'ur';

  const handleDemoFill = (type) => {
    setIsRegister(false);
    setError(null);
    if (type === 'student') {
      setEmail('student@rahvia.pk');
      setPassword('Password123!');
    } else if (type === 'counselor') {
      setEmail('counselor@rahvia.pk');
      setPassword('Password123!');
    } else if (type === 'admin') {
      setEmail('admin@rahvia.pk');
      setPassword('Password123!');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      if (isRegister) {
        if (password.length < 6) {
          setError(isUrdu ? 'پاس ورڈ کم از کم 6 حروف پر مشتمل ہونا چاہیے۔' : 'Password must be at least 6 characters long.');
          setLoading(false);
          return;
        }

        const payload = {
          email,
          password,
          role,
          name,
          first_name: name.split(' ')[0] || '',
          last_name: name.split(' ').slice(1).join(' ') || '',
          grade,
          board,
          elective_group: electiveGroup,
          school_code: schoolCode,
          parent_guardian_name: guardianName,
          parent_guardian_email: guardianEmail,
          parent_consent_granted: parentConsent,
        };

        const res = await register(payload);
        if (res.success) {
          onSuccess();
        } else {
          setError(typeof res.error === 'string' ? res.error : JSON.stringify(res.error));
        }
      } else {
        const res = await login(email, password);
        if (res.success) {
          onSuccess();
        } else {
          setError(res.error || 'Invalid credentials');
        }
      }
    } catch (err) {
      setError(err.message || 'Authentication error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-lg mx-auto py-10 px-4 sm:px-6">
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-xl space-y-6">
        
        {/* Top Header */}
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-2xl bg-emerald-800 text-white flex items-center justify-center mx-auto shadow-md shadow-emerald-900/20">
            <Compass className="w-6 h-6 text-emerald-300" />
          </div>
          <h2 className="text-2xl font-extrabold text-slate-900">
            {isRegister 
              ? (isUrdu ? 'نیا طالب علم اکاؤنٹ بنائیں' : 'Create Student Portal Account')
              : (isUrdu ? 'رہویا پورٹل پر لاگ ان کریں' : 'Welcome to Rahvia')}
          </h2>
          <p className="text-xs text-slate-500">
            {isUrdu ? 'ڈیٹا پرائیویسی اور پاکستانی تعلیمی معیار کے مطابق محفوظ پورٹل' : 'Pakistan Career Guidance & Psychometric Assessment Platform'}
          </p>
        </div>

        {/* Tab Switcher */}
        <div className="grid grid-cols-2 p-1 bg-slate-100 rounded-2xl text-xs font-bold">
          <button
            type="button"
            onClick={() => { setIsRegister(false); setError(null); }}
            className={`py-2.5 rounded-xl transition-all ${
              !isRegister ? 'bg-white text-emerald-900 shadow-xs' : 'text-slate-500 hover:text-slate-900'
            }`}
          >
            {isUrdu ? 'لاگ ان' : 'Sign In'}
          </button>
          <button
            type="button"
            onClick={() => { setIsRegister(true); setError(null); }}
            className={`py-2.5 rounded-xl transition-all ${
              isRegister ? 'bg-white text-emerald-900 shadow-xs' : 'text-slate-500 hover:text-slate-900'
            }`}
          >
            {isUrdu ? 'رجسٹریشن' : 'Register'}
          </button>
        </div>

        {/* Quick Demo Pre-fill Pills */}
        <div className="bg-emerald-50/70 p-3 rounded-2xl border border-emerald-200/80">
          <p className="text-[11px] font-bold text-emerald-900 mb-2">
            🚀 Quick Demo Login Accounts:
          </p>
          <div className="flex flex-wrap gap-1.5">
            <button
              type="button"
              onClick={() => handleDemoFill('student')}
              className="px-2.5 py-1 bg-white hover:bg-emerald-100 text-emerald-800 text-[11px] font-bold rounded-lg border border-emerald-300 shadow-2xs"
            >
              Student (Aisha Khan)
            </button>
            <button
              type="button"
              onClick={() => handleDemoFill('counselor')}
              className="px-2.5 py-1 bg-white hover:bg-emerald-100 text-emerald-800 text-[11px] font-bold rounded-lg border border-emerald-300 shadow-2xs"
            >
              School Counselor (Dr. Tariq)
            </button>
            <button
              type="button"
              onClick={() => handleDemoFill('admin')}
              className="px-2.5 py-1 bg-white hover:bg-emerald-100 text-emerald-800 text-[11px] font-bold rounded-lg border border-emerald-300 shadow-2xs"
            >
              Super Admin
            </button>
          </div>
        </div>

        {error && (
          <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-rose-800 text-xs font-semibold flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0 text-rose-600" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          
          {isRegister && (
            <>
              {/* Role Picker */}
              <div>
                <label className="block font-bold text-slate-700 mb-1">Account Role</label>
                <div className="grid grid-cols-2 gap-2">
                  <button
                    type="button"
                    onClick={() => setRole('STUDENT')}
                    className={`py-2 rounded-xl font-bold border transition-all ${
                      role === 'STUDENT' ? 'border-emerald-600 bg-emerald-50 text-emerald-900' : 'border-slate-200 text-slate-600'
                    }`}
                  >
                    Student
                  </button>
                  <button
                    type="button"
                    onClick={() => setRole('COUNSELOR')}
                    className={`py-2 rounded-xl font-bold border transition-all ${
                      role === 'COUNSELOR' ? 'border-emerald-600 bg-emerald-50 text-emerald-900' : 'border-slate-200 text-slate-600'
                    }`}
                  >
                    School Counselor
                  </button>
                </div>
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Full Name</label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="e.g. Fatima Ali"
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-xs focus:outline-none focus:ring-2 focus:ring-emerald-600/20"
                  required
                />
              </div>

              {role === 'STUDENT' && (
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <label className="block font-bold text-slate-700 mb-1">Grade</label>
                    <select
                      value={grade}
                      onChange={(e) => setGrade(e.target.value)}
                      className="w-full p-2 rounded-xl border border-slate-200 bg-slate-50"
                    >
                      <option value="MATRIC_9TH">Matric 9th</option>
                      <option value="MATRIC_10TH">Matric 10th</option>
                      <option value="INTER_11TH">Inter 1st Year (11th)</option>
                      <option value="INTER_12TH">Inter 2nd Year (12th)</option>
                      <option value="O_LEVELS">O-Levels</option>
                      <option value="A_LEVELS">A-Levels</option>
                    </select>
                  </div>

                  <div>
                    <label className="block font-bold text-slate-700 mb-1">Board</label>
                    <input
                      type="text"
                      value={board}
                      onChange={(e) => setBoard(e.target.value)}
                      className="w-full p-2 rounded-xl border border-slate-200"
                    />
                  </div>
                </div>
              )}
            </>
          )}

          <div>
            <label className="block font-bold text-slate-700 mb-1">Email Address</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="student@example.com"
                className="w-full pl-9 pr-3.5 py-2.5 rounded-xl border border-slate-200 text-xs focus:outline-none focus:ring-2 focus:ring-emerald-600/20"
                required
              />
            </div>
          </div>

          <div>
            <div className="flex justify-between items-center mb-1">
              <label className="block font-bold text-slate-700">Password</label>
              {isRegister && <span className="text-[10px] text-slate-400 font-medium">Minimum 6 characters</span>}
            </div>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder={isRegister ? "Minimum 6 characters" : "Enter password"}
                minLength={isRegister ? 6 : undefined}
                className="w-full pl-9 pr-3.5 py-2.5 rounded-xl border border-slate-200 text-xs focus:outline-none focus:ring-2 focus:ring-emerald-600/20"
                required
              />
            </div>
          </div>

          {/* Parental Consent (Pakistani PDPA Rule Compliance) */}
          {isRegister && role === 'STUDENT' && (
            <div className="p-3 bg-slate-50 rounded-2xl border border-slate-200 space-y-2">
              <div className="flex items-center gap-1.5 font-bold text-slate-800">
                <ShieldCheck className="w-4 h-4 text-emerald-700" />
                <span>Parental / Guardian Consent (PDPA Compliance)</span>
              </div>
              <div className="grid grid-cols-2 gap-2">
                <input
                  type="text"
                  placeholder="Guardian Name"
                  value={guardianName}
                  onChange={(e) => setGuardianName(e.target.value)}
                  className="w-full p-2 rounded-lg border border-slate-200 bg-white"
                />
                <input
                  type="email"
                  placeholder="Guardian Email"
                  value={guardianEmail}
                  onChange={(e) => setGuardianEmail(e.target.value)}
                  className="w-full p-2 rounded-lg border border-slate-200 bg-white"
                />
              </div>
              <label className="flex items-start gap-2 pt-1 cursor-pointer">
                <input
                  type="checkbox"
                  checked={parentConsent}
                  onChange={(e) => setParentConsent(e.target.checked)}
                  className="mt-0.5 rounded text-emerald-700"
                />
                <span className="text-[11px] text-slate-600 leading-tight">
                  I confirm parental consent has been granted for minor's psychometric evaluation.
                </span>
              </label>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-emerald-800 hover:bg-emerald-900 text-white font-bold rounded-xl text-sm transition-all shadow-md shadow-emerald-900/20 disabled:opacity-50"
          >
            {loading ? 'Processing...' : (isRegister ? 'Complete Registration' : 'Sign In to Portal')}
          </button>
        </form>

      </div>
    </div>
  );
};
