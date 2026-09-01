import api from './api';

interface LoginRequest {
  username: string;
  password: string;
}

interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  full_name?: string;
  role?: string;
  department?: string;
}

interface User {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  role: string;
  department?: string;
  is_active: boolean;
  created_at: string;
}

interface LoginResponse {
  message: string;
  access_token: string;
  user: User;
}

export const authService = {
  login: async (data: LoginRequest): Promise<LoginResponse> => {
    const response = await api.post('/auth/login', data);
    if (response.data.access_token) {
      localStorage.setItem('accessToken', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  register: async (data: RegisterRequest): Promise<LoginResponse> => {
    return (await api.post('/auth/register', data)).data;
  },

  logout: () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('user');
  },

  getProfile: async (): Promise<User> => {
    return (await api.get('/auth/profile')).data;
  },

  updateProfile: async (data: Partial<User>): Promise<User> => {
    return (await api.put('/auth/profile', data)).data;
  },

  changePassword: async (oldPassword: string, newPassword: string) => {
    return (await api.post('/auth/change-password', { old_password: oldPassword, new_password: newPassword })).data;
  },
};
