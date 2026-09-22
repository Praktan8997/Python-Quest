import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || '';

const api = axios.create({
  baseURL: `${API_BASE}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('pq_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const authService = {
  register: (data) => api.post('/auth/register', data),
  login: async (username, password) => {
    const res = await api.post('/auth/login', { username, password });
    if (res.data.access_token) {
      localStorage.setItem('pq_token', res.data.access_token);
    }
    return res.data;
  },
  getMe: () => api.get('/auth/me'),
  logout: () => {
    localStorage.removeItem('pq_token');
  }
};

export const topicService = {
  getTopics: () => api.get('/topics'),
  getTopicById: (id) => api.get(`/topics/${id}`),
  getLessons: (topicId) => api.get(`/topics/${topicId}/lessons`),
  getChallenges: (topicId) => api.get(`/topics/${topicId}/challenges`),
  getQuizzes: (topicId) => api.get(`/topics/${topicId}/quizzes`),
};

export const challengeService = {
  runCode: (challengeId, code) => api.post(`/challenges/${challengeId}/run`, { code }),
  submitChallenge: (challengeId, code) => api.post(`/challenges/${challengeId}/submit`, { code }),
  submitSolution: (challengeId, code) => api.post(`/challenges/${challengeId}/submit`, { code }),
  getSubmissions: () => api.get('/users/me/submissions'),
};

export const quizService = {
  submitQuiz: (quizId, answers) => api.post(`/quizzes/${quizId}/submit`, { answers }),
  getAttempts: (quizId) => api.get(`/quizzes/${quizId}/attempts`),
  getQuizHistory: () => api.get('/users/me/quiz-history'),
  getDailyPuzzle: () => api.get('/quizzes/daily-puzzle'),
  submitDailyPuzzle: (answers) => api.post('/quizzes/daily-puzzle/submit', { answers }),
};

export const leaderboardService = {
  getLeaderboard: () => api.get('/leaderboard'),
  getProgressSummary: () => api.get('/progress'),
  getBadges: () => api.get('/badges'),
};

export default api;
