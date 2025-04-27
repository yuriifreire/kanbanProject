import api from './api';

export default {
  async login(email, password) {
    const response = await api.post('/token', { username: email, password });
    return response.data;
  },
  async logout() {
    await api.post('/token/revoke');
  }
};