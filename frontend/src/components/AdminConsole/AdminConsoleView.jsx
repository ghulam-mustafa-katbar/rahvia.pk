import React, { useState, useEffect } from 'react';
import { api } from '../../api/client';
import { useAuth } from '../../context/AuthContext';
import { 
  ShieldCheck, Plus, BookOpen, HelpCircle, Save, 
  CheckCircle, Database, Layers, Check 
} from 'lucide-react';

export const AdminConsoleView = () => {
  const [activeTab, setActiveTab] = useState('questions'); // 'questions' | 'careers'
  const [questions, setQuestions] = useState([]);
  const [careers, setCareers] = useState([]);
  const [loading, setLoading] = useState(true);

  // New Question Form
  const [newQText, setNewQText] = useState('');
  const [newQTextUrdu, setNewQTextUrdu] = useState('');
  const [newQCategory, setNewQCategory] = useState('APTITUDE');
  const [newQDimension, setNewQDimension] = useState('NumericalAptitude');
  const [newQType, setNewQType] = useState('MCQ');
  const [newQOptions, setNewQOptions] = useState(
    'A: Option 1\nB: Option 2\nC: Option 3\nD: Option 4'
  );
  const [newQCorrect, setNewQCorrect] = useState('A');
  const [qCreating, setQCreating] = useState(false);
  const [qSuccess, setQSuccess] = useState('');

  // New Career Form
  const [newCName, setNewCName] = useState('');
  const [newCCategory, setNewCCategory] = useState('COMPUTING_AI');
  const [newCStream, setNewCStream] = useState('ICS');
  const [newCDesc, setNewCDesc] = useState('');
  const [newCDegrees, setNewCDegrees] = useState('');
  const [newCExams, setNewCExams] = useState('ECAT, NET');
  const [newCUnis, setNewCUnis] = useState('NUST, FAST, LUMS');
  const [cCreating, setCCreating] = useState(false);
  const [cSuccess, setCSuccess] = useState('');

  const loadData = async () => {
    try {
      setLoading(true);
      const [qData, cData] = await Promise.all([
        api.getAdminQuestions(),
        api.getCareers(),
      ]);
      setQuestions(Array.isArray(qData) ? qData : (qData?.results || []));
      setCareers(Array.isArray(cData) ? cData : (cData?.results || []));
    } catch (err) {
      console.error('Error fetching admin data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateQuestion = async (e) => {
    e.preventDefault();
    try {
      setQCreating(true);
      setQSuccess('');

      // Parse options
      const parsedOptions = newQOptions.split('\n').filter(Boolean).map((line) => {
        const [id, ...rest] = line.split(':');
        return {
          id: id.trim(),
          text: rest.join(':').trim(),
          score: 1.0,
        };
      });

      const payload = {
        text: newQText,
        text_urdu: newQTextUrdu,
        category: newQCategory,
        dimension: newQDimension,
        type: newQType,
        options: parsedOptions,
        correct_answer: newQCorrect,
        correct_answer_weight: 1.0,
        target_audience: 'ALL',
      };

      await api.createQuestion(payload);
      setQSuccess('New question added to psychometric bank!');
      setNewQText('');
      setNewQTextUrdu('');
      loadData();
    } catch (err) {
      alert('Error creating question');
    } finally {
      setQCreating(false);
    }
  };

  const handleCreateCareer = async (e) => {
    e.preventDefault();
    try {
      setCCreating(true);
      setCSuccess('');

      const payload = {
        name: newCName,
        category: newCCategory,
        stream_requirement: newCStream,
        description: newCDesc,
        typical_degrees: newCDegrees.split(',').map((s) => s.trim()).filter(Boolean),
        required_exams: newCExams.split(',').map((s) => s.trim()).filter(Boolean),
        top_universities_pakistan: newCUnis.split(',').map((s) => s.trim()).filter(Boolean),
        career_outlook: 'Strong employment prospect across domestic and international markets.',
      };

      await api.createCareerField(payload);
      setCSuccess('Career field added to encyclopedia catalog!');
      setNewCName('');
      setNewCDesc('');
      loadData();
    } catch (err) {
      alert('Error creating career field');
    } finally {
      setCCreating(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-8">
      
      {/* Header */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-xs flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-emerald-800 text-xs font-bold uppercase tracking-wider bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200 w-fit">
            <ShieldCheck className="w-4 h-4" />
            <span>Super Administrator Control</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-2">
            Assessment & Career Catalog Console
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Manage standardized psychometric question items, dimension keys, and career-stream mappings
          </p>
        </div>

        {/* Tab switch */}
        <div className="flex gap-2 p-1 bg-slate-100 rounded-2xl border border-slate-200 text-xs font-bold">
          <button
            onClick={() => setActiveTab('questions')}
            className={`px-4 py-2 rounded-xl transition-all ${
              activeTab === 'questions' ? 'bg-white text-emerald-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Question Bank ({questions.length})
          </button>
          <button
            onClick={() => setActiveTab('careers')}
            className={`px-4 py-2 rounded-xl transition-all ${
              activeTab === 'careers' ? 'bg-white text-emerald-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Career Catalog ({careers.length})
          </button>
        </div>
      </div>

      {activeTab === 'questions' ? (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Add Question Form */}
          <div className="lg:col-span-1 bg-white p-6 rounded-3xl border border-slate-200 shadow-xs space-y-4 h-fit">
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Plus className="w-4 h-4 text-emerald-700" />
              <span>Add New Psychometric Question</span>
            </h3>

            {qSuccess && (
              <div className="p-3 bg-emerald-50 text-emerald-800 rounded-xl text-xs font-bold">
                {qSuccess}
              </div>
            )}

            <form onSubmit={handleCreateQuestion} className="space-y-3 text-xs">
              <div>
                <label className="block font-bold text-slate-700 mb-1">Question Text (English)</label>
                <textarea
                  rows={2}
                  value={newQText}
                  onChange={(e) => setNewQText(e.target.value)}
                  className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-600/20"
                  required
                />
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Urdu Translation (اردو ترجمہ)</label>
                <textarea
                  rows={2}
                  value={newQTextUrdu}
                  onChange={(e) => setNewQTextUrdu(e.target.value)}
                  className="font-urdu w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-600/20"
                />
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="block font-bold text-slate-700 mb-1">Category</label>
                  <select
                    value={newQCategory}
                    onChange={(e) => setNewQCategory(e.target.value)}
                    className="w-full p-2 rounded-xl border border-slate-200 bg-slate-50"
                  >
                    <option value="APTITUDE">Cognitive Aptitude</option>
                    <option value="INTEREST">RIASEC Interest</option>
                    <option value="ACADEMIC">Subject Knowledge</option>
                  </select>
                </div>

                <div>
                  <label className="block font-bold text-slate-700 mb-1">Dimension</label>
                  <input
                    type="text"
                    value={newQDimension}
                    onChange={(e) => setNewQDimension(e.target.value)}
                    className="w-full p-2 rounded-xl border border-slate-200"
                    placeholder="NumericalAptitude"
                  />
                </div>
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Options (ID: Text per line)</label>
                <textarea
                  rows={4}
                  value={newQOptions}
                  onChange={(e) => setNewQOptions(e.target.value)}
                  className="w-full p-2.5 font-mono text-xs rounded-xl border border-slate-200 bg-slate-50"
                />
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Correct Answer ID</label>
                <input
                  type="text"
                  value={newQCorrect}
                  onChange={(e) => setNewQCorrect(e.target.value)}
                  className="w-full p-2 rounded-xl border border-slate-200"
                />
              </div>

              <button
                type="submit"
                disabled={qCreating}
                className="w-full py-2.5 bg-emerald-800 hover:bg-emerald-900 text-white font-bold rounded-xl transition-colors disabled:opacity-50"
              >
                {qCreating ? 'Saving...' : 'Add to Question Bank'}
              </button>
            </form>
          </div>

          {/* Question List Table */}
          <div className="lg:col-span-2 bg-white rounded-3xl border border-slate-200 shadow-xs overflow-hidden">
            <div className="p-5 border-b border-slate-200">
              <h3 className="text-base font-bold text-slate-900">Current Question Bank ({questions.length})</h3>
              <p className="text-xs text-slate-500">Standardized aptitude and Holland RIASEC interest inventory items</p>
            </div>

            <div className="divide-y divide-slate-100 max-h-[600px] overflow-y-auto">
              {questions.map((q) => (
                <div key={q.question_id} className="p-4 hover:bg-slate-50 text-xs space-y-1.5">
                  <div className="flex items-center justify-between gap-2">
                    <div className="flex items-center gap-2">
                      <span className="px-2 py-0.5 rounded-md font-bold uppercase text-[10px] bg-slate-100 text-slate-700">
                        {q.category}
                      </span>
                      <span className="font-bold text-emerald-800 text-[11px]">
                        {q.dimension}
                      </span>
                    </div>
                    <span className="text-[10px] text-slate-400 font-mono">
                      Key: {q.correct_answer || 'Likert'}
                    </span>
                  </div>
                  <p className="font-semibold text-slate-800 text-sm">{q.text}</p>
                  {q.text_urdu && (
                    <p className="font-urdu text-xs text-emerald-900">{q.text_urdu}</p>
                  )}
                </div>
              ))}
            </div>
          </div>

        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Add Career Form */}
          <div className="lg:col-span-1 bg-white p-6 rounded-3xl border border-slate-200 shadow-xs space-y-4 h-fit">
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Plus className="w-4 h-4 text-emerald-700" />
              <span>Add New Career Field</span>
            </h3>

            {cSuccess && (
              <div className="p-3 bg-emerald-50 text-emerald-800 rounded-xl text-xs font-bold">
                {cSuccess}
              </div>
            )}

            <form onSubmit={handleCreateCareer} className="space-y-3 text-xs">
              <div>
                <label className="block font-bold text-slate-700 mb-1">Career Field Name</label>
                <input
                  type="text"
                  value={newCName}
                  onChange={(e) => setNewCName(e.target.value)}
                  className="w-full p-2.5 rounded-xl border border-slate-200"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="block font-bold text-slate-700 mb-1">Category</label>
                  <select
                    value={newCCategory}
                    onChange={(e) => setNewCCategory(e.target.value)}
                    className="w-full p-2 rounded-xl border border-slate-200 bg-slate-50"
                  >
                    <option value="COMPUTING_AI">Computing & AI</option>
                    <option value="ENGINEERING">Engineering</option>
                    <option value="MEDICAL_HEALTH">Medical & Health</option>
                    <option value="BUSINESS_FINANCE">Business & Finance</option>
                    <option value="SOCIAL_SCIENCES_LAW">Law & Social Sciences</option>
                  </select>
                </div>

                <div>
                  <label className="block font-bold text-slate-700 mb-1">Stream Req</label>
                  <select
                    value={newCStream}
                    onChange={(e) => setNewCStream(e.target.value)}
                    className="w-full p-2 rounded-xl border border-slate-200 bg-slate-50"
                  >
                    <option value="ICS">ICS</option>
                    <option value="PRE_ENGINEERING">Pre-Engineering</option>
                    <option value="PRE_MEDICAL">Pre-Medical</option>
                    <option value="COMMERCE">Commerce</option>
                    <option value="OPEN_ALL">Open to All</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Description</label>
                <textarea
                  rows={3}
                  value={newCDesc}
                  onChange={(e) => setNewCDesc(e.target.value)}
                  className="w-full p-2.5 rounded-xl border border-slate-200"
                />
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Degrees (comma separated)</label>
                <input
                  type="text"
                  value={newCDegrees}
                  onChange={(e) => setNewCDegrees(e.target.value)}
                  placeholder="BS CS, BS Software Engineering"
                  className="w-full p-2 rounded-xl border border-slate-200"
                />
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Required Exams (comma separated)</label>
                <input
                  type="text"
                  value={newCExams}
                  onChange={(e) => setNewCExams(e.target.value)}
                  placeholder="ECAT, FAST, NET"
                  className="w-full p-2 rounded-xl border border-slate-200"
                />
              </div>

              <button
                type="submit"
                disabled={cCreating}
                className="w-full py-2.5 bg-emerald-800 hover:bg-emerald-900 text-white font-bold rounded-xl transition-colors disabled:opacity-50"
              >
                {cCreating ? 'Saving...' : 'Save Career Field'}
              </button>
            </form>
          </div>

          {/* Career List Table */}
          <div className="lg:col-span-2 bg-white rounded-3xl border border-slate-200 shadow-xs overflow-hidden">
            <div className="p-5 border-b border-slate-200">
              <h3 className="text-base font-bold text-slate-900">Registered Career Pathways ({careers.length})</h3>
              <p className="text-xs text-slate-500">Degree mappings and entrance exams configured for Pakistani students</p>
            </div>

            <div className="divide-y divide-slate-100 max-h-[600px] overflow-y-auto">
              {careers.map((c) => (
                <div key={c.field_id} className="p-4 hover:bg-slate-50 text-xs space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-slate-900 text-sm">{c.name}</span>
                    <span className="px-2 py-0.5 rounded bg-emerald-50 text-emerald-800 font-bold text-[10px]">
                      {c.stream_display}
                    </span>
                  </div>
                  <p className="text-slate-500 line-clamp-2">{c.description}</p>
                  <p className="text-[11px] text-slate-700">
                    <strong>Exams:</strong> {(c.required_exams || []).join(', ') || 'Merit'}
                  </p>
                </div>
              ))}
            </div>
          </div>

        </div>
      )}

    </div>
  );
};
