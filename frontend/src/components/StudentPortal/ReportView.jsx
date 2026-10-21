import React, { useState, useEffect } from 'react';
import { api } from '../../api/client';
import { useAuth } from '../../context/AuthContext';
import { 
  Award, Download, Sparkles, CheckCircle2, TrendingUp, 
  BookOpen, ArrowRight, School, Compass, Share2, 
  ExternalLink, Check, AlertCircle, Layers, Cpu, HeartHandshake, ShieldCheck 
} from 'lucide-react';

export const ReportView = ({ reportId, onRetake, onExploreCareer }) => {
  const { studentId, language } = useAuth();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('pathways'); // 'pathways' | 'dimensions' | 'careers'

  const isUrdu = language === 'ur';

  useEffect(() => {
    const fetchReport = async () => {
      try {
        setLoading(true);
        setError(null);
        let data = null;

        if (reportId) {
          data = await api.getReportDetail(reportId);
        } else if (studentId) {
          data = await api.getStudentReport(studentId);
        }

        if (data && data.report_id) {
          setReport(data);
        } else {
          throw new Error('No career guidance report found yet. Complete an assessment first.');
        }
      } catch (err) {
        console.error('Report fetch error:', err);
        setError(err.message || 'Error loading guidance report');
      } finally {
        setLoading(false);
      }
    };

    fetchReport();
  }, [reportId, studentId]);

  const handleDownloadPdf = () => {
    if (!report?.report_id) return;
    try {
      setDownloading(true);
      const downloadUrl = typeof api.downloadReportPdfUrl === 'function' 
        ? api.downloadReportPdfUrl(report.report_id) 
        : `/api/report/${report.report_id}/pdf`;
      const a = document.createElement('a');
      a.href = downloadUrl;
      const safeName = (report.student_name || 'Student').replace(/\s+/g, '_');
      a.download = `Rahvia_Career_Report_${safeName}.pdf`;
      document.body.appendChild(a);
      a.click();
      setTimeout(() => {
        if (document.body.contains(a)) {
          document.body.removeChild(a);
        }
        setDownloading(false);
      }, 1000);
    } catch (err) {
      alert('Could not download PDF. Please try again.');
      setDownloading(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto py-16 px-4 text-center">
        <div className="w-16 h-16 border-4 border-emerald-200 border-t-emerald-700 rounded-full animate-spin mx-auto mb-4" />
        <h3 className="text-xl font-bold text-slate-800">
          {isUrdu ? 'آپ کی جامع کیریئر رپورٹ تیار کی جا رہی ہے...' : 'Synthesizing Your Career Guidance Report...'}
        </h3>
        <p className="text-slate-500 text-sm mt-1">
          {isUrdu ? 'تمام شعبہ جات اور پاکستانی داخلہ معیارات کا موازنہ جاری ہے۔' : 'Correlating psychometric percentiles with Pakistani admission criteria'}
        </p>
      </div>
    );
  }

  if (error || !report) {
    return (
      <div className="max-w-xl mx-auto my-12 p-8 bg-white border border-slate-200 rounded-3xl text-center shadow-xs">
        <div className="w-16 h-16 bg-emerald-50 rounded-2xl flex items-center justify-center mx-auto mb-4 text-emerald-700">
          <Compass className="w-8 h-8" />
        </div>
        <h3 className="text-xl font-bold text-slate-900 mb-2">
          {isUrdu ? 'کوئی رپورٹ دستیاب نہیں' : 'No Assessment Report Yet'}
        </h3>
        <p className="text-slate-600 text-sm mb-6">
          {isUrdu 
            ? 'آپ نے ابھی تک کیریئر ٹیسٹ مکمل نہیں کیا۔ اپنی صلاحیتوں اور موزوں شعبوں کے تعین کے لیے ٹیسٹ شروع کریں۔' 
            : 'You have not completed an assessment session yet. Take our diagnostic test to unlock your customized pathway.'}
        </p>
        <button
          onClick={onRetake}
          className="px-6 py-3 bg-emerald-800 hover:bg-emerald-900 text-white font-bold rounded-xl text-sm transition-all shadow-md shadow-emerald-900/20"
        >
          {isUrdu ? 'ابھی ٹیسٹ شروع کریں' : 'Take Diagnostic Assessment'}
        </button>
      </div>
    );
  }

  // Filter cognitive vs RIASEC from dimension_scores
  const allDimensionScores = report.dimension_scores || [];
  const cognitiveDimensions = allDimensionScores.filter(ds => 
    !ds.dimension_name.startsWith('RIASEC_') && !ds.dimension_name.startsWith('Academic_')
  );
  const riasecDimensions = allDimensionScores.filter(ds => 
    ds.dimension_name.startsWith('RIASEC_')
  );

  const getMatchStrengthBadge = (strength) => {
    switch (strength) {
      case 'HIGH_EVIDENCE':
        return (
          <span className="px-2.5 py-1 rounded-full text-xs font-extrabold bg-emerald-100 text-emerald-900 border border-emerald-300 flex items-center gap-1">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-700" />
            {isUrdu ? 'مضبوط شواہد (High Evidence)' : 'High Evidence'}
          </span>
        );
      case 'MODERATE_EVIDENCE':
        return (
          <span className="px-2.5 py-1 rounded-full text-xs font-extrabold bg-amber-100 text-amber-900 border border-amber-300 flex items-center gap-1">
            <TrendingUp className="w-3.5 h-3.5 text-amber-700" />
            {isUrdu ? 'مناسب شواہد (Moderate)' : 'Moderate Evidence'}
          </span>
        );
      default:
        return (
          <span className="px-2.5 py-1 rounded-full text-xs font-extrabold bg-slate-100 text-slate-700 border border-slate-300 flex items-center gap-1">
            <Compass className="w-3.5 h-3.5 text-slate-500" />
            {isUrdu ? 'قابل غور (Exploratory)' : 'Exploratory'}
          </span>
        );
    }
  };

  return (
    <div className="max-w-5xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      
      {/* Hero Banner / Actions */}
      <div className="bg-gradient-to-br from-emerald-900 via-emerald-800 to-slate-900 rounded-3xl p-6 sm:p-10 text-white shadow-xl">
        <div className="flex flex-wrap items-center justify-between gap-6">
          <div className="space-y-2 max-w-2xl">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-700/60 text-emerald-200 text-xs font-bold border border-emerald-500/30">
              <Sparkles className="w-3.5 h-3.5" />
              <span>
                {String(report.grade || '').includes('9')
                  ? (isUrdu ? 'نہم جماعت (SSC Part-I) تعلیمی رہنمائی رپورٹ' : 'Class 9 (SSC-I) Foundational Exploration Report')
                  : (isUrdu ? 'دہم جماعت (SSC Part-II) انٹرمیڈیٹ و داخلہ رہنمائی رپورٹ' : 'Class 10 (SSC-II) College Transition & SECCAP Report')}
              </span>
            </div>
            <h1 className="text-2xl sm:text-4xl font-extrabold tracking-tight">
              {report.student_name}
            </h1>
            <p className="text-emerald-100 text-sm font-medium">
              {report.school_name ? `${report.school_name} • ` : ''}{report.board} • {report.grade}
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <button
              onClick={handleDownloadPdf}
              disabled={downloading}
              className="flex items-center gap-2 px-5 py-3 rounded-xl bg-white text-emerald-900 font-extrabold text-sm hover:bg-emerald-50 transition-all shadow-lg shadow-black/20"
            >
              <Download className="w-4 h-4 text-emerald-700" />
              <span>{downloading ? 'Generating PDF...' : (isUrdu ? 'ڈاؤن لوڈ پی ڈی ایف رپورٹ' : 'Download PDF Dossier')}</span>
            </button>
            <button
              onClick={onRetake}
              className="px-4 py-3 rounded-xl bg-emerald-700/50 hover:bg-emerald-700 text-emerald-100 font-bold text-sm border border-emerald-500/40 transition-colors"
            >
              {isUrdu ? 'دوبارہ ٹیسٹ دیں' : 'Retake Test'}
            </button>
          </div>
        </div>

        {/* Top Stream Badges */}
        <div className="mt-8 pt-6 border-t border-emerald-700/60">
          <p className="text-xs font-bold uppercase tracking-wider text-emerald-300 mb-3">
            {isUrdu ? 'تجویز کردہ انٹرمیڈیٹ گروپس (سندھ بورڈز / SECCAP):' : 'Top Recommended Class 11 Educational Pathways (Sindh):'}
          </p>
          <div className="flex flex-wrap gap-2.5">
            {report.recommended_streams && report.recommended_streams.map((stream, idx) => (
              <span
                key={idx}
                className="px-4 py-2 rounded-xl bg-white/10 backdrop-blur-md text-white font-bold text-sm border border-white/20 flex items-center gap-2 shadow-xs"
              >
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                <span>{stream}</span>
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Executive Summary Card */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-xs border border-slate-200">
        <h2 className="text-xl font-bold text-slate-900 mb-3 flex items-center gap-2">
          <Award className="w-5 h-5 text-emerald-700" />
          <span>{isUrdu ? 'خلاصہ و رہنمائی' : 'Matric Pathway Guidance Summary'}</span>
        </h2>
        <p className="text-slate-700 leading-relaxed text-base">
          {report.summary_narrative}
        </p>

        {report.summary_narrative_urdu && (
          <p className="font-urdu text-lg text-emerald-950 bg-emerald-50/60 p-5 rounded-2xl border border-emerald-100 mt-4 leading-loose">
            {report.summary_narrative_urdu}
          </p>
        )}
      </div>

      {/* Sindh Class 11 Educational Pathways Section */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-xs border border-slate-200 space-y-6">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider bg-emerald-100 text-emerald-800 border border-emerald-200">
              Sindh Education Structure
            </span>
          </div>
          <h2 className="text-xl font-bold text-slate-900 mt-2 flex items-center gap-2">
            <Layers className="w-5 h-5 text-emerald-700" />
            <span>{isUrdu ? 'سندھ میں جماعت گیارہویں (انٹرمیڈیٹ) کے تعلیمی راستے' : 'Sindh Class 11 Educational Pathways (SECCAP / Boards)'}</span>
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            {isUrdu 
              ? 'کراچی سینٹرلائزڈ داخلہ پالیسی (SECCAP)، سندھ کے تمام تعلیمی بورڈز اور ٹیکنیکل ایجوکیشن (SBTE) کے مطابق تجزیہ' 
              : 'Detailed evaluation of all 8 Sindh secondary pathways based on cognitive evidence, subject interests, and SECCAP cutoff patterns.'}
          </p>
        </div>

        <div className="space-y-4">
          {(report.pathway_details && report.pathway_details.length > 0 ? report.pathway_details : []).map((pathway, idx) => (
            <div 
              key={idx}
              className={`p-5 rounded-2xl border transition-all ${
                pathway.match_strength === 'HIGH_EVIDENCE'
                  ? 'border-emerald-300 bg-emerald-50/20'
                  : pathway.match_strength === 'MODERATE_EVIDENCE'
                  ? 'border-amber-200 bg-amber-50/10'
                  : 'border-slate-200 bg-white'
              }`}
            >
              <div className="flex flex-wrap items-start justify-between gap-3 mb-3">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-extrabold text-slate-400">Option #{idx + 1}</span>
                    {getMatchStrengthBadge(pathway.match_strength)}
                  </div>
                  <h3 className="text-lg font-bold text-slate-900">
                    {pathway.stream_name}
                  </h3>
                  {pathway.stream_name_urdu && (
                    <p className="font-urdu text-sm text-emerald-900 font-semibold mt-0.5">
                      {pathway.stream_name_urdu}
                    </p>
                  )}
                </div>

                <div className="text-right">
                  <span className="text-2xl font-black text-emerald-800">
                    {pathway.fit_score}%
                  </span>
                  <p className="text-[10px] font-bold uppercase text-slate-400 tracking-wider">Fit Score</p>
                </div>
              </div>

              {/* Rationale */}
              <p className="text-xs text-slate-700 leading-relaxed mb-3">
                <strong>Guidance: </strong>{pathway.rationale_english}
              </p>
              {pathway.rationale_urdu && (
                <p className="font-urdu text-xs text-emerald-900 leading-relaxed bg-emerald-50/60 p-2.5 rounded-xl border border-emerald-100 mb-3">
                  {pathway.rationale_urdu}
                </p>
              )}

              {/* Core Subjects & SECCAP Details Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs bg-white p-3.5 rounded-xl border border-slate-200">
                <div>
                  <strong className="text-slate-800 block mb-1">Core Subjects (Sindh Boards):</strong>
                  <div className="flex flex-wrap gap-1.5">
                    {(pathway.core_subjects || []).map((subj, sIdx) => (
                      <span key={sIdx} className="px-2 py-0.5 bg-slate-100 text-slate-700 rounded text-[11px] font-medium">
                        {subj}
                      </span>
                    ))}
                  </div>
                  <p className="text-[11px] text-slate-500 mt-2 leading-relaxed">
                    {pathway.curriculum_summary}
                  </p>
                </div>

                <div className="border-t md:border-t-0 md:border-l md:pl-3 border-slate-200">
                  <strong className="text-slate-800 block mb-1">SECCAP / Admission Criteria:</strong>
                  <p className="text-[11px] text-slate-600 leading-relaxed mb-2">
                    {pathway.seccap_criteria}
                  </p>
                  {pathway.accessible_careers && (
                    <div>
                      <strong className="text-slate-800 block text-[11px] mb-1">Leading Degrees & Careers:</strong>
                      <div className="flex flex-wrap gap-1">
                        {pathway.accessible_careers.map((car, cIdx) => (
                          <span key={cIdx} className="px-2 py-0.5 bg-emerald-50 text-emerald-800 border border-emerald-200 rounded text-[10px] font-bold">
                            {car}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>

            </div>
          ))}
        </div>
      </div>

      {/* Dimension Scores & Psychometric Breakdown */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-xs border border-slate-200 space-y-6">
        <div>
          <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-700" />
            <span>{isUrdu ? 'ذہنی صلاحیتیں اور کیریئر رجحانات (RIASEC)' : 'Psychometric & Cognitive Aptitude Evaluation'}</span>
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            {isUrdu 
              ? 'طلباء کے موازنے کے لیے شماریاتی پرسنٹائل رینکس۔ یہ کسی طبی یا نفسیاتی تشخیص کا دعویٰ نہیں کرتے۔' 
              : 'Indicative comparative percentile rankings referenced to secondary student cohorts. Transparently separated into cognitive aptitude and vocational interest dimensions.'}
          </p>
        </div>

        {/* 1. Cognitive Aptitude Dimensions */}
        <div>
          <h3 className="text-sm font-extrabold uppercase tracking-wider text-slate-500 mb-3 flex items-center gap-1.5">
            <Cpu className="w-4 h-4 text-emerald-600" />
            <span>Cognitive Aptitude Factors (Verified Answer Keys)</span>
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {cognitiveDimensions.map((ds, idx) => (
              <div key={idx} className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2">
                <div className="flex justify-between items-center text-sm">
                  <span className="font-bold text-slate-800">{ds.dimension_name}</span>
                  <span className="font-extrabold text-emerald-800 bg-emerald-100 px-2.5 py-0.5 rounded-lg text-xs">
                    {ds.percentile}th %ile
                  </span>
                </div>
                <div className="w-full bg-slate-200 h-2.5 rounded-full overflow-hidden">
                  <div
                    className="bg-emerald-600 h-full rounded-full transition-all duration-500"
                    style={{ width: `${ds.percentage}%` }}
                  />
                </div>
                <div className="flex justify-between text-[11px] text-slate-500 font-medium">
                  <span>Score: {ds.raw_score} / {ds.max_possible}</span>
                  <span>Accuracy: {ds.percentage}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 2. RIASEC Interest Profile */}
        {riasecDimensions.length > 0 && (
          <div className="pt-4 border-t border-slate-200">
            <h3 className="text-sm font-extrabold uppercase tracking-wider text-slate-500 mb-3 flex items-center gap-1.5">
              <HeartHandshake className="w-4 h-4 text-emerald-600" />
              <span>Holland RIASEC Vocational Interests (1-5 Likert Scale)</span>
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
              {riasecDimensions.map((ds, idx) => (
                <div key={idx} className="p-3.5 rounded-xl bg-emerald-50/40 border border-emerald-100 space-y-1.5">
                  <div className="flex justify-between items-center text-xs">
                    <span className="font-bold text-emerald-950">{ds.dimension_name.replace('RIASEC_', '')}</span>
                    <span className="font-extrabold text-emerald-800 bg-white px-2 py-0.5 rounded text-[11px] border border-emerald-200">
                      {ds.raw_score} / 5.0
                    </span>
                  </div>
                  <div className="w-full bg-emerald-200/60 h-2 rounded-full overflow-hidden">
                    <div
                      className="bg-emerald-700 h-full rounded-full"
                      style={{ width: `${ds.percentage}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Strengths & Growth Areas Side-by-Side */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-3xl p-6 sm:p-7 shadow-xs border border-emerald-200 bg-emerald-50/20">
          <h3 className="text-lg font-bold text-emerald-900 mb-4 flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5 text-emerald-600" />
            <span>{isUrdu ? 'نمایاں صلاحیتیں اور طاقتیں' : 'Key Core Strengths'}</span>
          </h3>
          <ul className="space-y-3">
            {report.strengths && report.strengths.map((s, idx) => (
              <li key={idx} className="text-sm text-slate-700 flex items-start gap-2.5 leading-relaxed">
                <div className="w-1.5 h-1.5 rounded-full bg-emerald-600 mt-2 shrink-0" />
                <span>{s}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="bg-white rounded-3xl p-6 sm:p-7 shadow-xs border border-amber-200 bg-amber-50/20">
          <h3 className="text-lg font-bold text-amber-900 mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-amber-600" />
            <span>{isUrdu ? 'ترقی و بہتری کے شعبے' : 'Targeted Growth Areas'}</span>
          </h3>
          <ul className="space-y-3">
            {report.growth_areas && report.growth_areas.map((g, idx) => (
              <li key={idx} className="text-sm text-slate-700 flex items-start gap-2.5 leading-relaxed">
                <div className="w-1.5 h-1.5 rounded-full bg-amber-600 mt-2 shrink-0" />
                <span>{g}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Top Matched Career Fields Catalog (Pakistan National Career Encyclopedia Connection) */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-xs border border-slate-200 space-y-6">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider bg-emerald-100 text-emerald-800 border border-emerald-200">
              National Career Encyclopedia
            </span>
          </div>
          <h2 className="text-xl font-bold text-slate-900 mt-2 flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-emerald-700" />
            <span>{isUrdu ? 'موزوں ترین پیشہ ورانہ راستے (پاکستانی جامعات و ڈگریاں)' : 'Top Matched Pakistani Degree Pathways'}</span>
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            {isUrdu 
              ? 'قومی کیریئر انسائیکلوپیڈیا سے مربوط۔ ہر شعبے کی آفیشل تصدیق، جامعات اور اہلیت کے قواعد ملاحظہ کریں۔' 
              : 'Directly integrated with the Pakistan National Career Encyclopedia. Discover accredited degrees, entrance examinations, and verified institutional rules.'}
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {report.recommendations && report.recommendations.map((rec) => {
            const field = rec.field_details || {};
            const matchPct = Math.round((rec.match_score || 0) * 100);

            return (
              <div
                key={rec.id}
                className="p-5 rounded-2xl border border-slate-200 bg-white hover:border-emerald-500 hover:shadow-md transition-all flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-start justify-between gap-3 mb-2">
                    <div>
                      <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">
                        Rank #{rec.rank}
                      </span>
                      <h4 className="text-lg font-bold text-slate-900 mt-1">
                        {field.name}
                      </h4>
                    </div>
                    <div className="text-right shrink-0">
                      <span className="text-xl font-extrabold text-emerald-800">
                        {matchPct}%
                      </span>
                      <p className="text-[10px] font-bold text-slate-400 uppercase">Match</p>
                    </div>
                  </div>

                  <p className="text-xs text-slate-600 line-clamp-2 mb-3">
                    {field.description}
                  </p>

                  <div className="space-y-1.5 text-xs text-slate-700 bg-slate-50 p-3 rounded-xl border border-slate-200/60 mb-3">
                    <p>
                      <strong className="text-slate-900">Degrees: </strong> 
                      {(field.typical_degrees || []).slice(0, 2).join(', ')}
                    </p>
                    <p>
                      <strong className="text-slate-900">Required Tests: </strong> 
                      {(field.required_exams || []).join(', ') || 'Board Merit'}
                    </p>
                    <p>
                      <strong className="text-slate-900">Top Universities: </strong> 
                      {(field.top_universities_pakistan || []).slice(0, 3).join(', ')}
                    </p>
                  </div>

                  {rec.rationale_text && (
                    <p className="text-[11px] text-slate-600 italic bg-amber-50/40 p-2 rounded-lg border border-amber-100 mb-3 leading-relaxed">
                      <strong>Why matched: </strong>{rec.rationale_text}
                    </p>
                  )}
                </div>

                <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                  <span className="font-medium text-slate-500 italic">
                    {field.stream_display || 'Open Stream'}
                  </span>
                  
                  {onExploreCareer && field.field_id && (
                    <button
                      onClick={() => onExploreCareer(field.field_id)}
                      className="text-xs font-bold text-emerald-700 hover:text-emerald-900 bg-emerald-50 hover:bg-emerald-100 px-3 py-1 rounded-lg border border-emerald-200 transition-colors flex items-center gap-1"
                    >
                      <span>Explore in Encyclopedia</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Actionable Next Steps */}
      <div className="bg-slate-900 text-white rounded-3xl p-6 sm:p-8 shadow-lg space-y-4">
        <h3 className="text-lg font-bold flex items-center gap-2 text-emerald-300">
          <Compass className="w-5 h-5 text-emerald-400" />
          <span>{isUrdu ? 'اگلے عملی اقدامات اور لائحہ عمل' : 'Actionable Next Steps & Academic Roadmap'}</span>
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
          {report.next_steps && report.next_steps.map((step, idx) => (
            <div key={idx} className="bg-slate-800/80 border border-slate-700 p-4 rounded-2xl flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-emerald-600 text-white font-extrabold text-xs flex items-center justify-center shrink-0">
                {idx + 1}
              </div>
              <p className="text-xs text-slate-200 leading-relaxed font-medium">
                {step}
              </p>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
};
