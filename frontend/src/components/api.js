import axios from 'axios';
import authService from '../services/authService';

// ✅ Use environment variable for backend URL
const api = axios.create({
    baseURL: `${process.env.REACT_APP_API_BASE_URL}/api/v1/auth`, // ✅ Updated to match backend prefix
    headers: {
        'Content-Type': 'application/json',
    },
});

/**
 * Interceptor to add the JWT token to every outgoing request if the user is logged in.
 */
api.interceptors.request.use(
    (config) => {
        const user = authService.getCurrentUser();
        if (user && user.access_token) {
            // FastAPI expects "Bearer <token>"
            config.headers['Authorization'] = `Bearer ${user.access_token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default api;
