import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// JWT Token Interceptor - Add auth header to all requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// Response Interceptor - Handle token refresh on 401
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // If 401 and we have a refresh token, try to refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/token/refresh/`, {
            refresh: refreshToken,
          });
          
          localStorage.setItem('access_token', response.data.access);
          apiClient.defaults.headers.Authorization = `Bearer ${response.data.access}`;
          originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
          
          return apiClient(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, clear tokens and redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/auth';
      }
    }
    
    return Promise.reject(error);
  }
);

// Helper to extract results from paginated response
const handlePaginatedResponse = async (promise) => {
  try {
    const response = await promise;
    return {
      data: response.data.results || response.data,
      count: response.data.count || 0,
      full: response.data,
    };
  } catch (error) {
    throw error;
  }
};

// Games
export const getGames = (params = {}) => handlePaginatedResponse(apiClient.get('/games/', { params }));
export const getGame = (id) => apiClient.get(`/games/${id}/`);
export const createGame = (data) => apiClient.post('/games/', data);

// Competitors
export const getCompetitors = (params = {}) => handlePaginatedResponse(apiClient.get('/competitors/', { params }));
export const getCompetitor = (id) => apiClient.get(`/competitors/${id}/`);
export const getTrendingCompetitors = () => handlePaginatedResponse(apiClient.get('/competitors/trending/'));

// Trends
export const getTrends = (params = {}) => handlePaginatedResponse(apiClient.get('/trends/', { params }));
export const getTrend = (id) => apiClient.get(`/trends/${id}/`);

// Market Analysis
export const getAnalysis = (params = {}) => handlePaginatedResponse(apiClient.get('/analysis/', { params }));
export const getAnalysisDetail = (id) => apiClient.get(`/analysis/${id}/`);

// Player Sentiment
export const getSentiment = (params = {}) => handlePaginatedResponse(apiClient.get('/sentiment/', { params }));
export const getSentimentDetail = (id) => apiClient.get(`/sentiment/${id}/`);

// Launch Strategies
export const getStrategies = (params = {}) => handlePaginatedResponse(apiClient.get('/strategies/', { params }));
export const getStrategy = (id) => apiClient.get(`/strategies/${id}/`);
export const generateStrategy = (data) => apiClient.post('/strategies/generate/', data);

// Scraped Games (Live Bright Data)
export const getScrapedGames = (params = {}) => handlePaginatedResponse(apiClient.get('/scraped-games/', { params }));
export const getScrapedGamesTrending = () => handlePaginatedResponse(apiClient.get('/scraped-games/trending/'));
export const getScrapedGamesByPlatform = () => apiClient.get('/scraped-games/by_platform/');

// Scraping Jobs (Collection Status)
export const getScrapingJobs = (params = {}) => handlePaginatedResponse(apiClient.get('/scraping-jobs/', { params }));
export const getScrapingJobResults = (jobId) => apiClient.get(`/scraping-jobs/${jobId}/results/`);

// AI Analysis Endpoints
export const analyzeTrends = (data) => apiClient.post('/ai/analyze-trends/', data);
export const analyzeCompetitors = (data) => apiClient.post('/ai/analyze-competitors/', data);
export const getMarketGaps = () => apiClient.get('/ai/market-gaps/');
export const generateLaunchStrategy = (data) => apiClient.post('/ai/generate-strategy/', data);
export const predictTrends = (data) => apiClient.post('/ai/predict-trends/', data);
export const queryAIAgent = (data) => apiClient.post('/ai/query/', data);

// Authentication Endpoints
export const register = (userData) => apiClient.post('/auth/register/', userData);
export const login = (username, password) => apiClient.post('/auth/login/', { username, password });
export const getCurrentUser = () => apiClient.get('/auth/me/');
export const updateUser = (data) => apiClient.put('/auth/me/', data);
export const changePassword = (data) => apiClient.post('/auth/change-password/', data);
export const refreshToken = (refreshToken) => apiClient.post('/token/refresh/', { refresh: refreshToken });

// API Key Management
export const getAPIKeys = () => apiClient.get('/api-keys/');
export const createAPIKey = (name) => apiClient.post('/api-keys/', { name });
export const deleteAPIKey = (id) => apiClient.delete(`/api-keys/${id}/`);

// Payment & Billing Endpoints
export const createPaymentIntent = (tierId, billingPeriod = 'monthly') => 
  apiClient.post('/payments/intent/', { tier_id: tierId, billing_period: billingPeriod });

export const confirmPayment = (paymentIntentId, tierId, billingPeriod = 'monthly') => 
  apiClient.post('/payments/confirm/', { 
    payment_intent_id: paymentIntentId, 
    tier_id: tierId, 
    billing_period: billingPeriod 
  });

export const getPaymentHistory = () => apiClient.get('/payments/history/');

export const getInvoices = () => apiClient.get('/invoices/');

export const getInvoice = (invoiceId) => apiClient.get(`/invoices/${invoiceId}/`);

// Analytics Endpoints
export const logAnalyticsEvent = (eventType, eventName, metadata = {}, page = '') => 
  apiClient.post('/analytics/events/', { 
    event_type: eventType, 
    event_name: eventName, 
    metadata, 
    page 
  });

export const getAnalyticsEvents = (eventType = null, days = 30) => {
  let url = `/analytics/events/?days=${days}`;
  if (eventType) {
    url += `&event_type=${eventType}`;
  }
  return apiClient.get(url);
};

export const getAnalyticsDashboard = (days = 30) => 
  apiClient.get(`/analytics/dashboard/?days=${days}`);
export const revokeAPIKey = (id) => apiClient.post(`/api-keys/${id}/revoke/`);
export const validateAPIKey = (key) => apiClient.post('/api-keys/validate/', { key });

// Subscription & Tier Management
export const getTiers = () => apiClient.get('/tiers/');
export const getCompareTiers = () => apiClient.get('/tiers/compare/');
export const getUserSubscription = () => apiClient.get('/subscription/');
export const getTokenUsage = () => apiClient.get('/tokens/');
export const recordTokenUsage = (actionType, tokensSpent, description = '') => 
  apiClient.post('/tokens/', { action_type: actionType, tokens_spent: tokensSpent, description });

// Tier Upgrade/Downgrade Endpoints
export const getAvailableTiers = () => apiClient.get('/tiers/available/');
export const getCurrentTier = () => apiClient.get('/tiers/current/');
export const upgradeTier = (data) => apiClient.post('/tiers/upgrade/', data);

// PDF Invoice Endpoints
export const generateInvoicePDF = (invoiceId) => 
  apiClient.post(`/invoices/${invoiceId}/pdf/generate/`);

export const downloadInvoicePDF = (invoiceId) => 
  apiClient.get(`/invoices/${invoiceId}/pdf/download/`, { responseType: 'blob' });

// Data Export Endpoints
export const exportPayments = (format = 'csv', days = 30) => 
  apiClient.get(`/export/payments/?format=${format}&days=${days}`, { responseType: 'blob' });

export const exportInvoices = (format = 'csv', days = 30) => 
  apiClient.get(`/export/invoices/?format=${format}&days=${days}`, { responseType: 'blob' });

export const exportAnalytics = (format = 'csv', days = 30, eventType = null) => {
  let url = `/export/analytics/?format=${format}&days=${days}`;
  if (eventType) url += `&event_type=${eventType}`;
  return apiClient.get(url, { responseType: 'blob' });
};

export const exportUserData = (format = 'csv') => 
  apiClient.get(`/export/user-data/?format=${format}`, { responseType: 'blob' });

// Logout helper
export const logout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  delete apiClient.defaults.headers.Authorization;
  window.location.href = '/';
};
