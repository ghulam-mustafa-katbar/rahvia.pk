import React, { useState } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { HomeView } from './components/HomeView';
import { AssessmentRunner } from './components/StudentPortal/AssessmentRunner';
import { ReportView } from './components/StudentPortal/ReportView';
import { CareerLibraryView } from './components/CareerLibrary/CareerLibraryView';
import { SchoolDashboardView } from './components/SchoolDashboard/SchoolDashboardView';
import { CounselorProfileView } from './components/SchoolDashboard/CounselorProfileView';
import { StudentProfileView } from './components/StudentPortal/StudentProfileView';
import { AdminConsoleView } from './components/AdminConsole/AdminConsoleView';
import { AuthView } from './components/AuthView';
import { Compass, Heart } from 'lucide-react';

function MainApp() {
  const [currentView, setCurrentView] = useState('home');
  const [activeReportId, setActiveReportId] = useState(null);
  const [selectedCareerId, setSelectedCareerId] = useState(null);
  const { user, isAuthenticated, language } = useAuth();

  const isUrdu = language === 'ur';

  const handleAssessmentComplete = (reportId) => {
    setActiveReportId(reportId);
    setCurrentView('report');
  };

  const handleViewStudentReport = (reportId) => {
    setActiveReportId(reportId);
    setCurrentView('report');
  };

  const handleExploreCareer = (fieldId) => {
    setSelectedCareerId(fieldId);
    setCurrentView('careers');
  };

  const renderContent = () => {
    switch (currentView) {
      case 'home':
        return (
          <HomeView
            onStartAssessment={() => {
              if (!isAuthenticated) {
                setCurrentView('auth');
              } else {
                setCurrentView('assessment');
              }
            }}
            onExploreCareers={() => {
              setSelectedCareerId(null);
              setCurrentView('careers');
            }}
            onOpenDashboard={() => setCurrentView('school')}
          />
        );

      case 'assessment':
        if (!isAuthenticated) {
          return (
            <AuthView
              defaultTab="login"
              onSuccess={() => setCurrentView('assessment')}
            />
          );
        }
        return (
          <AssessmentRunner
            onComplete={handleAssessmentComplete}
            onCancel={() => {
              if (!isAuthenticated) {
                setCurrentView('auth');
              } else {
                setCurrentView('home');
              }
            }}
          />
        );

      case 'report':
        return (
          <ReportView
            reportId={activeReportId}
            onRetake={() => setCurrentView('assessment')}
            onExploreCareer={handleExploreCareer}
          />
        );

      case 'careers':
        return (
          <CareerLibraryView
            initialCareerId={selectedCareerId}
            onClearInitialCareer={() => setSelectedCareerId(null)}
          />
        );

      case 'school':
        return <SchoolDashboardView onViewStudentReport={handleViewStudentReport} />;

      case 'profile':
        if (!isAuthenticated) {
          return <AuthView onSuccess={() => setCurrentView('profile')} />;
        }
        if (user?.role === 'COUNSELOR') {
          return <CounselorProfileView onOpenDashboard={() => setCurrentView('school')} />;
        }
        if (user?.role === 'ADMIN' || user?.is_staff) {
          return <AdminConsoleView />;
        }
        return <StudentProfileView />;

      case 'admin':
        if (!isAuthenticated || (!user?.is_staff && user?.role !== 'ADMIN')) {
          return (
            <div className="max-w-md mx-auto my-16 p-8 bg-white border border-slate-200 rounded-3xl text-center shadow-xs">
              <h3 className="text-lg font-bold text-slate-800">Super Admin Access Only</h3>
              <p className="text-xs text-slate-500 mt-2">Please sign in with administrator credentials.</p>
              <button
                onClick={() => setCurrentView('auth')}
                className="mt-4 px-5 py-2 bg-emerald-800 text-white rounded-xl text-xs font-bold"
              >
                Sign In
              </button>
            </div>
          );
        }
        return <AdminConsoleView />;

      case 'auth':
        return (
          <AuthView
            defaultTab="login"
            onSuccess={() => setCurrentView('home')}
          />
        );

      case 'auth_register':
        return (
          <AuthView
            defaultTab="register"
            onSuccess={() => setCurrentView('home')}
          />
        );

      default:
        return <HomeView onStartAssessment={() => setCurrentView('assessment')} />;
    }
  };

  return (
    <div className={`min-h-screen flex flex-col bg-slate-50 ${isUrdu ? 'font-urdu' : 'font-sans'}`}>
      <Navbar currentView={currentView} setCurrentView={setCurrentView} />

      <main className="flex-1">
        {renderContent()}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 py-10 px-4 sm:px-6 lg:px-8 mt-auto">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
          <div className="flex items-center gap-2">
            <Compass className="w-4 h-4 text-emerald-800" />
            <span className="font-extrabold text-slate-800">RAHVIA</span>
            <span>— Pakistan Student Career-Guidance Platform (Matric/Intermediate Boards)</span>
          </div>

          <p className="text-center sm:text-right">
            Aligned with Pakistani PDPA Draft Standards • Built with Django REST & React PWA
          </p>
        </div>
      </footer>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <MainApp />
    </AuthProvider>
  );
}
