import React, { useState, useEffect } from 'react';
import { api } from '../../api/client';
import { useAuth } from '../../context/AuthContext';
import { 
  Users, Award, CheckCircle, Clock, Search, UserPlus, 
  Download, BarChart3, School as SchoolIcon, Filter, AlertTriangle 
} from 'lucide-react';

export const SchoolDashboardView = ({ onViewStudentReport }) => {
  const { user, language } = useAuth();
  const [schools, setSchools] = useState([]);
  const [selectedSchoolId, setSelectedSchoolId] = useState('');
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showBatchModal, setShowBatchModal] = useState(false);
  const [batchInput, setBatchInput] = useState('');
  const [batchLoading, setBatchLoading] = useState(false);
  const [batchResult, setBatchResult] = useState(null);

  const isUrdu = language === 'ur';

  // Fetch schools list
  useEffect(() => {
    const fetchSchools = async () => {
      try {
        const data = await api.getSchools();
        const list = Array.isArray(data) ? data : (data?.results || []);
        setSchools(list);
        if (list.length > 0) {
          setSelectedSchoolId(list[0].school_id);
        }
      } catch (err) {
        console.error('Error fetching schools:', err);
      }
    };
    fetchSchools();
  }, []);

  // Fetch school dashboard data
  useEffect(() => {
    if (!selectedSchoolId) return;

    const fetchDashboard = async () => {
      try {
        setLoading(true);
        const data = await api.getSchoolDashboard(selectedSchoolId);
        setDashboardData(data);
      } catch (err) {
        console.error('Error fetching school dashboard:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, [selectedSchoolId]);

  const handleBatchEnroll = async (e) => {
    e.preventDefault();
    if (!batchInput.trim()) return;

    try {
      setBatchLoading(true);
      setBatchResult(null);

      // Parse lines: Name, Email, Grade (e.g. Fatima Ali, fatima@school.edu, MATRIC_10TH)
      const lines = batchInput.trim().split('\n');
      const studentList = lines.map((line) => {
        const parts = line.split(',').map((p) => p.trim());
        return {
          name: parts[0] || 'Student',
          email: parts[1] || `student_${Math.floor(Math.random() * 10000)}@school.pk`,
          grade: parts[2] || 'MATRIC_10TH',
          elective_group: parts[3] || 'SCIENCE_CS',
          parent_consent: true,
        };
      });

      const res = await api.batchEnrollStudents(selectedSchoolId, studentList);
      setBatchResult(res);
      setBatchInput('');
      
      // Refresh dashboard
      const refreshed = await api.getSchoolDashboard(selectedSchoolId);
      setDashboardData(refreshed);
    } catch (err) {
      alert('Batch enrollment failed. Please check formatting.');
    } finally {
      setBatchLoading(false);
    }
  };

  const school = dashboardData?.school;
  const summary = dashboardData?.summary;
  const roster = dashboardData?.roster || [];

  const filteredRoster = roster.filter((s) => {
    if (!searchTerm) return true;
    const term = searchTerm.toLowerCase();
    return s.name.toLowerCase().includes(term) || s.email.toLowerCase().includes(term);
  });

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-8">
      
      {/* Top Controls & School Selector */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-xs flex flex-wrap items-center justify-between gap-6">
        <div>
          <div className="flex items-center gap-2 text-emerald-800 text-xs font-bold uppercase tracking-wider bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200 w-fit">
            <SchoolIcon className="w-4 h-4" />
            <span>{isUrdu ? 'اسکول اور کالج کونسلر پورٹل' : 'Institutional Counselor Portal'}</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-2">
            {school ? school.name : 'School Analytics & Student Management'}
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            {school ? `${school.board_display} • Institution Code: ${school.code} • ${school.city}` : 'Select an institution to inspect cohort data'}
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          {schools.length > 1 && (
            <select
              value={selectedSchoolId}
              onChange={(e) => setSelectedSchoolId(e.target.value)}
              className="px-4 py-2.5 rounded-xl border border-slate-200 text-xs font-bold text-slate-700 bg-slate-50 focus:outline-none focus:ring-2 focus:ring-emerald-600/20"
            >
              {schools.map((s) => (
                <option key={s.school_id} value={s.school_id}>
                  {s.name} ({s.city})
                </option>
              ))}
            </select>
          )}

          <button
            onClick={() => setShowBatchModal(true)}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-800 hover:bg-emerald-900 text-white text-xs font-bold shadow-xs transition-colors"
          >
            <UserPlus className="w-4 h-4" />
            <span>{isUrdu ? 'بیچ رجسٹریشن' : 'Batch Enroll Students'}</span>
          </button>
        </div>
      </div>

      {loading ? (
        <div className="py-16 text-center">
          <div className="w-10 h-10 border-4 border-emerald-200 border-t-emerald-700 rounded-full animate-spin mx-auto mb-2" />
          <p className="text-slate-500 text-sm">Aggregating cohort psychometrics...</p>
        </div>
      ) : schools.length === 0 ? (
        <div className="bg-white rounded-3xl p-12 text-center border border-slate-200 shadow-xs max-w-xl mx-auto space-y-4">
          <div className="w-16 h-16 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center mx-auto border border-amber-200">
            <SchoolIcon className="w-8 h-8" />
          </div>
          <h3 className="text-xl font-bold text-slate-800">
            {isUrdu ? 'کوئی ادارہ آپ کے پروفائل سے منسلک نہیں ہے' : 'No Institution Assigned Yet'}
          </h3>
          <p className="text-sm text-slate-500">
            {isUrdu 
              ? 'آپ کے کونسلر اکاؤنٹ کو ابھی تک کسی اسکول یا کالج سے منسلک نہیں کیا گیا۔ براہ کرم اپنے ایڈمن سے رابطہ کریں یا اپنا اسکول کوڈ تصدیق کرائیں۔' 
              : 'Your counselor account is not yet assigned to an institution. Please contact the platform admin at admin@rahvia.pk to link your school code.'}
          </p>
        </div>
      ) : (
        <>
          {/* Key Metrics Grid */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
              <div className="flex items-center justify-between text-slate-500 text-xs font-bold uppercase tracking-wider mb-2">
                <span>Total Enrolled</span>
                <Users className="w-4 h-4 text-emerald-700" />
              </div>
              <p className="text-3xl font-extrabold text-slate-900">{summary?.total_students || 0}</p>
              <p className="text-[11px] text-slate-400 mt-1">Secondary & intermediate roster</p>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
              <div className="flex items-center justify-between text-slate-500 text-xs font-bold uppercase tracking-wider mb-2">
                <span>Assessed Students</span>
                <CheckCircle className="w-4 h-4 text-emerald-600" />
              </div>
              <p className="text-3xl font-extrabold text-emerald-800">{summary?.assessed_students || 0}</p>
              <p className="text-[11px] text-emerald-600 font-semibold mt-1">
                {summary?.completion_rate || 0}% Completion Rate
              </p>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
              <div className="flex items-center justify-between text-slate-500 text-xs font-bold uppercase tracking-wider mb-2">
                <span>Pending Test</span>
                <Clock className="w-4 h-4 text-amber-600" />
              </div>
              <p className="text-3xl font-extrabold text-amber-700">{summary?.pending_assessment || 0}</p>
              <p className="text-[11px] text-slate-400 mt-1">Awaiting session completion</p>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
              <div className="flex items-center justify-between text-slate-500 text-xs font-bold uppercase tracking-wider mb-2">
                <span>Institutional Code</span>
                <SchoolIcon className="w-4 h-4 text-slate-400" />
              </div>
              <p className="text-2xl font-mono font-extrabold text-slate-800">{school?.code || 'N/A'}</p>
              <p className="text-[11px] text-slate-400 mt-1">Student self-join token</p>
            </div>
          </div>

          {/* Cohort Stream Distribution & Average Aptitudes */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            {/* Stream Distribution */}
            <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs space-y-4">
              <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <BarChart3 className="w-4 h-4 text-emerald-700" />
                <span>Cohort Recommended Stream Breakdown</span>
              </h3>
              <p className="text-xs text-slate-500">
                Distribution of guidance recommendations generated for this institution's students:
              </p>

              {summary?.stream_distribution && Object.keys(summary.stream_distribution).length > 0 ? (
                <div className="space-y-3 pt-2">
                  {Object.entries(summary.stream_distribution).map(([stream, count], i) => {
                    const total = summary.assessed_students || 1;
                    const pct = Math.round((count / total) * 100);
                    return (
                      <div key={i} className="space-y-1">
                        <div className="flex justify-between text-xs font-bold">
                          <span className="text-slate-800">{stream}</span>
                          <span className="text-emerald-800">{count} students ({pct}%)</span>
                        </div>
                        <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
                          <div
                            className="bg-emerald-600 h-full rounded-full"
                            style={{ width: `${pct}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <div className="py-8 text-center text-xs text-slate-400">
                  No assessment stream reports compiled yet.
                </div>
              )}
            </div>

            {/* Average Aptitudes by Dimension */}
            <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs space-y-4">
              <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <Award className="w-4 h-4 text-emerald-700" />
                <span>Cohort Psychometric Dimension Averages</span>
              </h3>
              <p className="text-xs text-slate-500">
                Average percentage and norm percentiles across students:
              </p>

              {summary?.dimension_averages && Object.keys(summary.dimension_averages).length > 0 ? (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                  {Object.entries(summary.dimension_averages).map(([dim, metrics], i) => (
                    <div key={i} className="bg-slate-50 p-3 rounded-xl border border-slate-200 text-xs space-y-1">
                      <div className="font-bold text-slate-800 truncate" title={dim}>
                        {dim}
                      </div>
                      <div className="flex justify-between items-center text-slate-600">
                        <span>Avg: {metrics.avg_percentage}%</span>
                        <span className="font-bold text-emerald-800 bg-emerald-100 px-1.5 py-0.5 rounded text-[10px]">
                          {metrics.avg_percentile}th %ile
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="py-8 text-center text-xs text-slate-400">
                  Dimension averages will appear once students complete tests.
                </div>
              )}
            </div>

          </div>

          {/* Student Roster Table */}
          <div className="bg-white rounded-3xl border border-slate-200 shadow-xs overflow-hidden">
            <div className="p-5 border-b border-slate-200 flex flex-wrap items-center justify-between gap-4">
              <div>
                <h3 className="text-base font-bold text-slate-900">Enrolled Student Roster</h3>
                <p className="text-xs text-slate-500">Individual assessment progress and downloadable reports</p>
              </div>

              <div className="relative">
                <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="Filter by student name or email..."
                  className="pl-9 pr-3 py-1.5 text-xs rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-600/20"
                />
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50 text-slate-500 uppercase tracking-wider font-bold border-b border-slate-200">
                  <tr>
                    <th className="px-5 py-3">Student Name</th>
                    <th className="px-5 py-3">Grade & Stream</th>
                    <th className="px-5 py-3">Parent Consent (PDPA)</th>
                    <th className="px-5 py-3">Assessment Status</th>
                    <th className="px-5 py-3">Primary Recommendation</th>
                    <th className="px-5 py-3 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 font-medium">
                  {filteredRoster.map((student) => (
                    <tr key={student.student_id} className="hover:bg-slate-50/70">
                      <td className="px-5 py-3.5">
                        <div className="font-bold text-slate-900">{student.name}</div>
                        <div className="text-[11px] text-slate-400">{student.email}</div>
                      </td>
                      <td className="px-5 py-3.5 text-slate-700">
                        {student.grade_display}
                      </td>
                      <td className="px-5 py-3.5">
                        {student.parent_consent ? (
                          <span className="inline-flex items-center gap-1 text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded text-[11px] font-bold border border-emerald-200">
                            <CheckCircle className="w-3 h-3" /> Granted
                          </span>
                        ) : (
                          <span className="text-slate-400 text-[11px]">Not recorded</span>
                        )}
                      </td>
                      <td className="px-5 py-3.5">
                        {student.has_completed_assessment ? (
                          <span className="inline-flex items-center gap-1 text-emerald-800 bg-emerald-100 font-bold px-2 py-0.5 rounded text-[11px]">
                            Completed
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 text-amber-700 bg-amber-50 font-bold px-2 py-0.5 rounded text-[11px]">
                            Pending
                          </span>
                        )}
                      </td>
                      <td className="px-5 py-3.5 font-bold text-slate-800">
                        {student.top_recommended_stream || '—'}
                      </td>
                      <td className="px-5 py-3.5 text-right">
                        {student.latest_report_id ? (
                          <div className="flex items-center justify-end gap-2">
                            <button
                              onClick={() => onViewStudentReport(student.latest_report_id)}
                              className="px-2.5 py-1 text-xs font-bold text-emerald-800 bg-emerald-50 hover:bg-emerald-100 rounded-lg transition-colors"
                            >
                              View Report
                            </button>
                            <a
                              href={`/api/report/${student.latest_report_id}/pdf`}
                              target="_blank"
                              rel="noreferrer"
                              className="p-1 text-slate-400 hover:text-emerald-700"
                              title="Download PDF"
                            >
                              <Download className="w-4 h-4" />
                            </a>
                          </div>
                        ) : (
                          <span className="text-slate-300 italic text-[11px]">No report</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}

      {/* Batch Enroll Modal */}
      {showBatchModal && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-8 shadow-2xl border border-slate-200 space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="text-lg font-extrabold text-slate-900">
                Batch Enroll Student Cohort
              </h3>
              <button
                onClick={() => setShowBatchModal(false)}
                className="w-7 h-7 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-600 flex items-center justify-center font-bold text-xs"
              >
                ✕
              </button>
            </div>

            <p className="text-xs text-slate-500 leading-relaxed">
              Paste student details, one student per line in comma-separated format:
              <br />
              <code>Name, Email, Grade, Elective Group</code>
            </p>

            <form onSubmit={handleBatchEnroll} className="space-y-4">
              <textarea
                rows={6}
                value={batchInput}
                onChange={(e) => setBatchInput(e.target.value)}
                placeholder="Hamza Ali, hamza@school.edu.pk, MATRIC_10TH, SCIENCE_CS&#10;Zainab Bibi, zainab@school.edu.pk, MATRIC_10TH, SCIENCE_BIO"
                className="w-full p-3 font-mono text-xs rounded-xl border border-slate-200 bg-slate-50 focus:outline-none focus:ring-2 focus:ring-emerald-600/20"
                required
              />

              {batchResult && (
                <div className="p-3 bg-emerald-50 text-emerald-800 rounded-xl text-xs font-semibold">
                  {batchResult.message}
                </div>
              )}

              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowBatchModal(false)}
                  className="px-4 py-2 text-xs font-bold text-slate-600 hover:bg-slate-100 rounded-xl"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={batchLoading}
                  className="px-5 py-2 text-xs font-bold text-white bg-emerald-800 hover:bg-emerald-900 rounded-xl disabled:opacity-50"
                >
                  {batchLoading ? 'Enrolling...' : 'Import & Register Students'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};
