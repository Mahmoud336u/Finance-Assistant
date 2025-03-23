import axios from 'axios';

const API_URL = 'https://your-api-gateway-url.com'; // Replace with your actual API Gateway URL

export const login = async (email, password) => {
  const response = await axios.post(`${API_URL}/login`, { email, password });
  localStorage.setItem('token', response.data.token);
};

export const signup = async (email, password) => {
  await axios.post(`${API_URL}/signup`, { email, password });
};

export const getToken = () => localStorage.getItem('token');
