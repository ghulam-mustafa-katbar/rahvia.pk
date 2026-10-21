import React, { useState, useEffect } from 'react';
import { api } from '../../api/client';
import { useAuth } from '../../context/AuthContext';
import { 
  Search, BookOpen, Filter, GraduationCap, MapPin, 
  ExternalLink, ChevronRight, CheckCircle, ShieldCheck, AlertCircle, Calendar, DollarSign, Building 
} from 'lucide-react';

export const CareerLibraryView = ({ initialCareerId, onClearInitialCareer }) => {
  const { language } = useAuth();
  const [careers, setCareers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedStream, setSelectedStream] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [loading, setLoading] = useState(true);
  const [selectedCareer, setSelectedCareer] = useState(null);

  const isUrdu = language === 'ur';

  useEffect(() => {
    const fetchCareers = async () => {
      try {
        setLoading(true);
        const data = await api.getCareers(selectedCategory, selectedStream);
        let list = [];
        if (data && Array.isArray(data)) {
          list = data;
        } else if (data && data.results) {
          list = data.results;
        }
        setCareers(list);

        // If an initialCareerId was passed from ReportView, auto-open that career
        if (initialCareerId && list.length > 0) {
          const match = list.find(c => String(c.field_id) === String(initialCareerId));
          if (match) {
            setSelectedCareer(match);
          }
        }
      } catch (err) {
        console.error('Error fetching careers:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCareers();
  }, [selectedStream, selectedCategory, initialCareerId]);

  const handleCloseModal = () => {
    setSelectedCareer(null);
    if (onClearInitialCareer) {
      onClearInitialCareer();
    }
  };

  const filteredCareers = careers.filter((c) => {
    if (!searchTerm) return true;
    const term = searchTerm.toLowerCase();
    return (
      c.name.toLowerCase().includes(term) ||
      (c.description && c.description.toLowerCase().includes(term)) ||
      (c.typical_degrees && c.typical_degrees.some((d) => d.toLowerCase().includes(term))) ||
      (c.required_exams && c.required_exams.some((e) => e.toLowerCase().includes(term)))
    );
  });

  const getVerificationBadge = (career) => {
    const status = career.verification_status;
    switch (status) {
      case 'VERIFIED_OFFICIAL':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
            <span>Officially Verified</span>
          </span>
        );
      case 'INSTITUTION_SPECIFIC':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-amber-100 text-amber-800 border border-amber-300">
            <Building className="w-3.5 h-3.5 text-amber-600" />
            <span>Institution-Specific Rules</span>
          </span>
        );
      case 'PARTIALLY_VERIFIED':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-blue-100 text-blue-800 border border-blue-300">
            <CheckCircle className="w-3.5 h-3.5 text-blue-600" />
            <span>Partially Verified</span>
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-slate-100 text-slate-700 border border-slate-300">
            <span>Standard Listing</span>
          </span>
        );
    }
  };

  return (
    <div className="max-w-6xl mx-auto py-8 px-4 sm:px-6 space-y-6">
      
      {/* Title & Search bar */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-xs space-y-4">
        <div className="max-w-2xl">
          <span className="text-xs font-bold uppercase tracking-wider text-emerald-800 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
            {isUrdu ? 'قومی کیریئر انسائیکلوپیڈیا' : 'Pakistan National Career Encyclopedia'}
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-2">
            {isUrdu ? 'پاکستانی تعلیمی و پیشہ ورانہ شعبہ جات' : 'Explore Pakistani Degree Pathways & Entry Tests'}
          </h1>
          <p className="text-sm text-slate-600 mt-1">
            {isUrdu 
              ? 'میٹرک اور انٹر کے بعد کے تمام مستند شعبہ جات، مطلوبہ داخلہ امتحانات (ECAT, MDCAT, NET) اور اہم جامعات کی معلومات۔' 
              : 'Verified statutory criteria, HEC-recognized degree pathways, institutional entrance tests, and industry salary data.'}
          </p>
        </div>

        {/* Search input */}
        <div className="relative">
          <Search className="w-5 h-5 text-slate-400 absolute left-4 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder={isUrdu ? 'شعبہ، ڈگری، یا داخلہ ٹیسٹ تلاش کریں (مثلاً: Software, MDCAT, NUST)...' : 'Search by field name, degree, or entry test (e.g. ECAT, AI, MBBS, Architecture)...'}
            className="w-full pl-12 pr-4 py-3.5 rounded-2xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-600/20 focus:border-emerald-600 transition-all bg-slate-50/50"
          />
        </div>

        {/* Stream Filter Pills */}
        <div className="flex flex-wrap gap-2 pt-2">
          {[
            { id: '', label: isUrdu ? 'تمام شعبے' : 'All Streams' },
            { id: 'ICS', label: 'ICS (Computer Science)' },
            { id: 'PRE_ENGINEERING', label: 'FSc Pre-Engineering' },
            { id: 'PRE_MEDICAL', label: 'FSc Pre-Medical' },
            { id: 'COMMERCE', label: 'I.Com / Commerce' },
            { id: 'HUMANITIES', label: 'FA Humanities / Law' },
            { id: 'OPEN_ALL', label: 'Open to All Streams' },
          ].map((stream) => (
            <button
              key={stream.id}
              onClick={() => setSelectedStream(stream.id)}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all ${
                selectedStream === stream.id
                  ? 'bg-emerald-800 text-white shadow-xs'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {stream.label}
            </button>
          ))}
        </div>
      </div>

      {/* Career Grid */}
      {loading ? (
        <div className="py-12 text-center">
          <div className="w-10 h-10 border-4 border-emerald-200 border-t-emerald-700 rounded-full animate-spin mx-auto mb-2" />
          <p className="text-slate-500 text-sm">Loading career catalog...</p>
        </div>
      ) : filteredCareers.length === 0 ? (
        <div className="bg-white rounded-3xl p-12 text-center border border-slate-200">
          <BookOpen className="w-12 h-12 text-slate-300 mx-auto mb-3" />
          <h3 className="text-lg font-bold text-slate-800">No career fields found</h3>
          <p className="text-slate-500 text-sm mt-1">Try adjusting your search criteria or stream filters.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredCareers.map((c) => (
            <div
              key={c.field_id}
              onClick={() => setSelectedCareer(c)}
              className="bg-white rounded-2xl p-5 border border-slate-200 shadow-xs hover:border-emerald-500 hover:shadow-md transition-all cursor-pointer flex flex-col justify-between group"
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-2">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">
                    {c.stream_display || 'Open Stream'}
                  </span>
                  {getVerificationBadge(c)}
                </div>

                <h3 className="text-base font-bold text-slate-900 group-hover:text-emerald-800 transition-colors">
                  {c.name}
                </h3>

                <p className="text-xs text-slate-600 mt-2 line-clamp-3 leading-relaxed">
                  {c.description}
                </p>

                {c.description_urdu && (
                  <p className="font-urdu text-xs text-slate-600 mt-2 line-clamp-1 bg-slate-50 p-1.5 rounded">
                    {c.description_urdu}
                  </p>
                )}

                <div className="mt-4 pt-3 border-t border-slate-100 space-y-1.5 text-[11px] text-slate-600">
                  <p>
                    <strong className="text-slate-800">Entrance Tests: </strong>
                    {(c.required_exams || []).join(', ') || 'Board Merit'}
                  </p>
                  <p>
                    <strong className="text-slate-800">Top Institutes: </strong>
                    {(c.top_universities_pakistan || []).slice(0, 3).join(', ')}
                  </p>
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs font-bold text-emerald-800 group-hover:translate-x-0.5 transition-transform">
                <span>View Verified Criteria</span>
                <ChevronRight className="w-4 h-4" />
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Detailed Modal with Structured Eligibility & Official Sources */}
      {selectedCareer && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-3xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 sm:p-8 shadow-2xl border border-slate-200 space-y-6">
            
            <div className="flex items-start justify-between gap-4">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-bold uppercase tracking-wider text-emerald-800 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
                    {selectedCareer.stream_display}
                  </span>
                  {getVerificationBadge(selectedCareer)}
                </div>
                <h2 className="text-2xl font-extrabold text-slate-900 mt-1">
                  {selectedCareer.name}
                </h2>
                <p className="text-xs text-slate-500 font-medium mt-0.5">
                  Category: {selectedCareer.category_display}
                </p>
              </div>
              <button
                onClick={handleCloseModal}
                className="w-8 h-8 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-600 flex items-center justify-center font-bold"
              >
                ✕
              </button>
            </div>

            {/* Description */}
            <div>
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-1">
                Overview & Professional Scope
              </h4>
              <p className="text-sm text-slate-700 leading-relaxed">
                {selectedCareer.description}
              </p>
              {selectedCareer.description_urdu && (
                <p className="font-urdu text-base text-emerald-950 bg-emerald-50/60 p-4 rounded-xl border border-emerald-100 mt-3 leading-loose">
                  {selectedCareer.description_urdu}
                </p>
              )}
            </div>

            {/* Structured Eligibility Card */}
            {selectedCareer.structured_eligibility && (
              <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200 space-y-3">
                <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-900 flex items-center gap-1.5">
                  <ShieldCheck className="w-4 h-4 text-emerald-600" />
                  <span>Verified Statutory & Institutional Admission Criteria</span>
                </h4>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                  <div>
                    <strong className="text-slate-800 block">Accepted Intermediate Streams:</strong>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {(selectedCareer.structured_eligibility.accepted_streams || []).map((st, i) => (
                        <span key={i} className="px-2 py-0.5 bg-white text-slate-700 rounded border border-slate-200 text-[11px] font-medium">
                          {st}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div>
                    <strong className="text-slate-800 block">Minimum Marks Requirement:</strong>
                    <p className="text-slate-600 mt-1 font-semibold">
                      {selectedCareer.structured_eligibility.minimum_intermediate_percentage || 'Per University Regulations'}
                    </p>
                  </div>
                </div>

                {selectedCareer.structured_eligibility.institutional_nuances && (
                  <div className="pt-2 border-t border-slate-200 text-xs">
                    <strong className="text-amber-900 block mb-1">Institutional Differences & Exceptions:</strong>
                    <p className="text-slate-700 bg-amber-50/60 p-2.5 rounded-xl border border-amber-200/60 leading-relaxed font-medium">
                      {selectedCareer.structured_eligibility.institutional_nuances}
                    </p>
                  </div>
                )}
              </div>
            )}

            {/* Degrees & Entry Exams */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">
                  Recognized Degree Programs
                </h4>
                <ul className="text-xs text-slate-800 space-y-1.5 font-semibold">
                  {(selectedCareer.typical_degrees || []).map((deg, i) => (
                    <li key={i} className="flex items-center gap-1.5">
                      <GraduationCap className="w-3.5 h-3.5 text-emerald-700 shrink-0" />
                      <span>{deg}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">
                  Required Pakistani Entry Exams
                </h4>
                <div className="flex flex-wrap gap-1.5">
                  {(selectedCareer.required_exams || []).map((exam, i) => (
                    <span key={i} className="px-2.5 py-1 bg-white border border-slate-300 rounded-lg text-xs font-bold text-slate-800">
                      {exam}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Industry Outlook & Verified Salary */}
            <div className="bg-emerald-50/50 p-4 rounded-2xl border border-emerald-200/80 space-y-2">
              <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-900">
                Industry Outlook & Employment Landscape
              </h4>
              <p className="text-xs text-slate-700 leading-relaxed font-medium">
                {selectedCareer.career_outlook}
              </p>

              {selectedCareer.salary_data && (
                <div className="pt-2 border-t border-emerald-200/60 grid grid-cols-3 gap-2 text-center text-xs">
                  <div className="bg-white p-2 rounded-xl border border-emerald-200">
                    <span className="text-[10px] text-slate-500 block uppercase font-bold">Entry Level</span>
                    <strong className="text-emerald-800 text-xs">{selectedCareer.salary_data.entry_level}</strong>
                  </div>
                  <div className="bg-white p-2 rounded-xl border border-emerald-200">
                    <span className="text-[10px] text-slate-500 block uppercase font-bold">Mid Career</span>
                    <strong className="text-emerald-800 text-xs">{selectedCareer.salary_data.mid_level}</strong>
                  </div>
                  <div className="bg-white p-2 rounded-xl border border-emerald-200">
                    <span className="text-[10px] text-slate-500 block uppercase font-bold">Senior / Lead</span>
                    <strong className="text-emerald-800 text-xs">{selectedCareer.salary_data.experienced}</strong>
                  </div>
                </div>
              )}
            </div>

            {/* Top Universities */}
            <div>
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">
                Premier Universities in Pakistan
              </h4>
              <div className="flex flex-wrap gap-2">
                {(selectedCareer.top_universities_pakistan || []).map((uni, i) => (
                  <span key={i} className="px-3 py-1.5 bg-slate-100 rounded-xl text-xs font-bold text-slate-700">
                    {uni}
                  </span>
                ))}
              </div>
            </div>

            {/* Verification Footer & Official Source Link */}
            <div className="pt-4 border-t border-slate-200 flex flex-wrap items-center justify-between gap-3 text-xs">
              <div className="flex items-center gap-2 text-slate-500 font-medium">
                {selectedCareer.last_verified_date && (
                  <span className="flex items-center gap-1">
                    <Calendar className="w-3.5 h-3.5 text-slate-400" />
                    Last verified: {selectedCareer.last_verified_date}
                  </span>
                )}
                {selectedCareer.official_source_url && (
                  <a
                    href={selectedCareer.official_source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-emerald-700 hover:text-emerald-900 font-bold underline flex items-center gap-1 ml-2"
                  >
                    <span>Regulatory Source</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                )}
              </div>

              <button
                onClick={handleCloseModal}
                className="px-6 py-2.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold rounded-xl transition-colors"
              >
                Close Details
              </button>
            </div>

          </div>
        </div>
      )}

    </div>
  );
};
