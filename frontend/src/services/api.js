import axios from 'axios';
import authService from './authService';

const apiClient = axios.create({
    baseURL: process.env.REACT_APP_API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

apiClient.interceptors.request.use(
    (config) => {
        const user = authService.getCurrentUser();
        if (user?.access_token) {
            config.headers.Authorization = `Bearer ${user.access_token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export default apiClient;
