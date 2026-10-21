// Resolve API Base URL from Vite environment (supports Vercel cloud deployments and local proxy fallbacks)
const API_BASE = (import.meta.env.VITE_API_BASE_URL || '/api').replace(/\/+$/, '');

export const getAuthToken = () => {
  return localStorage.getItem('rahvia_access_token');
};

export const setAuthTokens = (access, refresh) => {
  if (access) localStorage.setItem('rahvia_access_token', access);
  if (refresh) localStorage.setItem('rahvia_refresh_token', refresh);
};

export const clearAuthTokens = () => {
  localStorage.removeItem('rahvia_access_token');
  localStorage.removeItem('rahvia_refresh_token');
  localStorage.removeItem('rahvia_user');
  localStorage.removeItem('rahvia_student_id');
};

async function request(endpoint, options = {}) {
  const token = getAuthToken();
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  let response;
  try {
    response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers,
    });
  } catch (networkErr) {
    throw new Error('Unable to connect to the Rahvia server. Please check your network connection.');
  }

  if (response.status === 401 && !endpoint.includes('/auth/login')) {
    clearAuthTokens();
    window.dispatchEvent(new Event('auth:unauthorized'));
  }

  // Parse response safely based on Content-Type
  const contentType = response.headers.get('content-type') || '';
  let data;
  if (contentType.includes('application/json')) {
    try {
      data = await response.json();
    } catch (e) {
      data = null;
    }
  } else {
    // Non-JSON response (e.g. HTML error page or raw text)
    const text = await response.text();
    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Your session has expired. Please log in to start or continue your assessment.');
      }
      if (response.status === 404) {
        throw new Error(`The requested resource was not found on the server (${endpoint}).`);
      }
      if (response.status === 500) {
        throw new Error('Server encountered a temporary issue. Please try again in a moment.');
      }
      throw new Error(`Request error (${response.status}). Please try again.`);
    }
    return text;
  }

  if (!response.ok) {
    let errorMsg = data?.detail || data?.error || data?.message;
    if (!errorMsg && data && typeof data === 'object') {
      const messages = Object.entries(data)
        .map(([field, errs]) => {
          const fieldLabel = field.charAt(0).toUpperCase() + field.slice(1).replace(/_/g, ' ');
          const errText = Array.isArray(errs) ? errs.join(' ') : String(errs);
          return `${fieldLabel}: ${errText}`;
        })
        .filter(Boolean);
      if (messages.length > 0) {
        errorMsg = messages.join(' | ');
      }
    }
    if (!errorMsg) {
      errorMsg = response.status === 401 ? 'Please log in to continue.' : `Request failed with status ${response.status}`;
    }
    const err = new Error(errorMsg);
    err.status = response.status;
    err.data = data;
    throw err;
  }

  return data;
}

export const api = {
  // Auth
  register: async (userData) => {
    return request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  },
  login: async (credentials) => {
    return request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  },
  getCurrentUser: async () => {
    return request('/auth/me');
  },

  // Student Profile
  getProfile: async () => {
    return request('/student/profile');
  },
  updateProfile: async (profileData) => {
    return request('/student/profile', {
      method: 'PUT',
      body: JSON.stringify(profileData),
    });
  },

  // Assessment Engine
  startAssessment: async (params = {}) => {
    return request('/assessment/start', {
      method: 'POST',
      body: JSON.stringify(params),
    });
  },
  getAssessmentQuestions: async (assessmentId) => {
    return request(`/assessment/${assessmentId}/questions`);
  },
  submitAssessment: async (assessmentId, payload) => {
    return request(`/assessment/${assessmentId}/submit`, {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  // Report & Recommendations
  getStudentReport: async (studentId) => {
    return request(`/report/${studentId}`);
  },
  getReportDetail: async (reportId) => {
    return request(`/report/detail/${reportId}`);
  },
  downloadReportPdfUrl: (reportId) => {
    return `${API_BASE}/report/${reportId}/pdf`;
  },

  // School Counselor & Cohort Analytics
  getSchools: async (query = '') => {
    const qs = query ? (query.startsWith('?') ? query : `?${query}`) : '';
    return request(`/schools/${qs}`);
  },
  getSchoolDashboard: async (schoolId) => {
    return request(`/school/${schoolId}/dashboard`);
  },
  batchEnrollStudents: async (schoolId, studentList) => {
    return request(`/school/${schoolId}/batch-enroll`, {
      method: 'POST',
      body: JSON.stringify({ students: studentList }),
    });
  },

  // Career Fields Catalog
  getCareers: async (category = '', stream = '') => {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (stream) params.append('stream', stream);
    const qs = params.toString() ? `?${params.toString()}` : '';
    return request(`/careers/${qs}`);
  },
  getCareerDetail: async (fieldId) => {
    return request(`/careers/${fieldId}`);
  },

  // Admin Controls
  adminGetQuestions: async (category = '') => {
    const qs = category ? `?category=${category}` : '';
    return request(`/admin/questions${qs}`);
  },
  adminCreateQuestion: async (questionData) => {
    return request('/admin/questions', {
      method: 'POST',
      body: JSON.stringify(questionData),
    });
  },
  adminUpdateQuestion: async (questionId, questionData) => {
    return request(`/admin/questions/${questionId}`, {
      method: 'PUT',
      body: JSON.stringify(questionData),
    });
  },
  adminDeleteQuestion: async (questionId) => {
    return request(`/admin/questions/${questionId}`, {
      method: 'DELETE',
    });
  },
};
