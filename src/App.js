import axios from 'axios';
import { getToken } from './auth';

const API_URL = 'https://your-api-gateway-url.com'; // Replace with your actual API Gateway URL

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to every request
api.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const getSummary = () =>
  api.get('/summary').then((res) => res.data);

export const getTransactions = () =>
  api.get('/transactions').then((res) => res.data);

export const getBudgetSuggestions = () =>
  api.get('/budget-suggestions').then((res) => res.data);

export const getCategories = () =>
  api.get('/categories').then((res) => res.data);

export const updateTransaction = (id, transaction) =>
  api.put(`/transactions/${id}`, transaction);

export const getLinkToken = () =>
  api.get('/plaid/link-token').then((res) => res.data.link_token);

export const exchangePublicToken = (publicToken) =>
  api.post('/plaid/exchange-token', { publicToken });
