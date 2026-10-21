import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { 
  Compass, BookOpen, Award, School, ShieldCheck, 
  Globe, LogOut, User, Menu, X, CheckCircle 
} from 'lucide-react';

export const Navbar = ({ currentView, setCurrentView }) => {
  const { user, isAuthenticated, logout, language, toggleLanguage, isStudent, isCounselor, isAdmin } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const isUrdu = language === 'ur';

  const navItems = [
    { id: 'assessment', label: isUrdu ? 'ٹیسٹ شروع کریں' : 'Take Assessment', icon: Compass, show: true },
    { id: 'report', label: isUrdu ? 'میری رہنمائی رپورٹ' : 'My Career Report', icon: Award, show: isAuthenticated && isStudent },
    { id: 'careers', label: isUrdu ? 'کیریئر لائبریری' : 'Career Library', icon: BookOpen, show: true },
    { id: 'school', label: isUrdu ? 'اسکول ڈیش بورڈ' : 'School Dashboard', icon: School, show: !isAuthenticated || isCounselor || isAdmin },
    { id: 'admin', label: isUrdu ? 'ایڈمن کنسول' : 'Admin Console', icon: ShieldCheck, show: isAdmin },
  ];

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          
          {/* Logo & Brand */}
          <div 
            className="flex items-center gap-3 cursor-pointer group"
            onClick={() => setCurrentView('home')}
          >
            <div className="w-10 h-10 rounded-xl bg-emerald-800 text-white flex items-center justify-center shadow-md shadow-emerald-900/10 group-hover:bg-emerald-900 transition-colors">
              <Compass className="w-6 h-6 text-emerald-300" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-xl tracking-tight text-slate-900">RAHVIA</span>
                <span className="bg-emerald-100 text-emerald-800 text-[10px] font-bold px-1.5 py-0.5 rounded-full border border-emerald-200">
                  PAKISTAN
                </span>
              </div>
              <p className="text-xs text-slate-500 font-medium">
                {isUrdu ? 'طلباء کے لیے کیریئر گائیڈنس پورٹل' : 'Student Career-Guidance Platform'}
              </p>
            </div>
          </div>

          {/* Desktop Nav Links */}
          <nav className="hidden md:flex items-center gap-1">
            {navItems.filter(i => i.show).map((item) => {
              const Icon = item.icon;
              const isActive = currentView === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setCurrentView(item.id)}
                  className={`flex items-center gap-2 px-3.5 py-2 rounded-lg text-sm font-semibold transition-all ${
                    isActive
                      ? 'bg-emerald-50 text-emerald-800 border border-emerald-200 shadow-xs'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-emerald-700' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>

          {/* Right Controls: Language toggle + User badge / Login */}
          <div className="hidden md:flex items-center gap-3">
            {/* Language Switcher */}
            <button
              onClick={toggleLanguage}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 text-xs font-semibold text-slate-700 hover:bg-slate-50 hover:border-slate-300 transition-colors"
              title="Toggle English / Urdu Language"
            >
              <Globe className="w-3.5 h-3.5 text-emerald-700" />
              <span>{isUrdu ? 'English' : 'اردو'}</span>
            </button>

            {isAuthenticated ? (
              <div className="flex items-center gap-3 pl-2 border-l border-slate-200">
                <div 
                  className="flex items-center gap-2 cursor-pointer py-1 px-2 rounded-lg hover:bg-slate-50"
                  onClick={() => setCurrentView('profile')}
                >
                  <div className="w-8 h-8 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center font-bold text-xs border border-emerald-300">
                    {user?.first_name ? user.first_name[0].toUpperCase() : 'U'}
                  </div>
                  <div className="text-left">
                    <p className="text-xs font-bold text-slate-900 leading-tight">
                      {user?.first_name || user?.email?.split('@')[0]}
                    </p>
                    <span className="text-[10px] text-slate-500 font-medium">
                      {user?.role === 'ADMIN' ? 'Super Admin' : user?.role === 'COUNSELOR' ? 'Counselor' : 'Student'}
                    </span>
                  </div>
                </div>

                <button
                  onClick={logout}
                  className="p-2 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                  title="Log out"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setCurrentView('auth')}
                  className="px-4 py-2 text-sm font-semibold text-emerald-800 bg-emerald-50 hover:bg-emerald-100 rounded-lg border border-emerald-200 transition-colors"
                >
                  {isUrdu ? 'لاگ ان' : 'Sign In'}
                </button>
                <button
                  onClick={() => setCurrentView('auth_register')}
                  className="px-4 py-2 text-sm font-semibold text-white bg-emerald-800 hover:bg-emerald-900 rounded-lg shadow-xs shadow-emerald-900/20 transition-colors"
                >
                  {isUrdu ? 'رجسٹریشن' : 'Get Started'}
                </button>
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="flex md:hidden items-center gap-2">
            <button
              onClick={toggleLanguage}
              className="px-2.5 py-1 text-xs font-bold rounded border border-slate-200 text-emerald-800"
            >
              {isUrdu ? 'EN' : 'اردو'}
            </button>
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg text-slate-600 hover:bg-slate-100"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>

        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-slate-200 bg-white px-4 pt-3 pb-6 space-y-3">
          <div className="space-y-1">
            {navItems.filter(i => i.show).map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    setCurrentView(item.id);
                    setMobileMenuOpen(false);
                  }}
                  className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-semibold ${
                    currentView === item.id ? 'bg-emerald-50 text-emerald-800' : 'text-slate-600 hover:bg-slate-50'
                  }`}
                >
                  <Icon className="w-5 h-5 text-emerald-700" />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </div>

          <div className="pt-3 border-t border-slate-200">
            {isAuthenticated ? (
              <div className="space-y-2">
                <div 
                  className="flex items-center gap-3 p-2 bg-slate-50 rounded-lg cursor-pointer"
                  onClick={() => {
                    setCurrentView('profile');
                    setMobileMenuOpen(false);
                  }}
                >
                  <User className="w-5 h-5 text-emerald-700" />
                  <div>
                    <p className="text-sm font-bold text-slate-900">{user?.first_name || user?.email}</p>
                    <p className="text-xs text-slate-500 capitalize">{user?.role?.toLowerCase()}</p>
                  </div>
                </div>
                <button
                  onClick={() => {
                    logout();
                    setMobileMenuOpen(false);
                  }}
                  className="w-full flex items-center justify-center gap-2 py-2 px-3 text-sm font-semibold text-rose-600 bg-rose-50 rounded-lg"
                >
                  <LogOut className="w-4 h-4" />
                  <span>Log Out</span>
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-2 gap-2">
                <button
                  onClick={() => {
                    setCurrentView('auth');
                    setMobileMenuOpen(false);
                  }}
                  className="w-full py-2.5 text-center text-sm font-semibold text-emerald-800 bg-emerald-50 rounded-lg border border-emerald-200"
                >
                  Sign In
                </button>
                <button
                  onClick={() => {
                    setCurrentView('auth_register');
                    setMobileMenuOpen(false);
                  }}
                  className="w-full py-2.5 text-center text-sm font-semibold text-white bg-emerald-800 rounded-lg"
                >
                  Register
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </header>
  );
};
