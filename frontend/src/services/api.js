const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

const getToken = () => localStorage.getItem('token');

const createInstance = () => {
  const instance = {
    async request(method, url, data = null, params = null) {
      const options = {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
      };

      const token = getToken();
      if (token) {
        options.headers['Authorization'] = `Bearer ${token}`;
      }

      if (data) {
        options.body = JSON.stringify(data);
      }

      let queryString = '';
      if (params) {
        const searchParams = new URLSearchParams();
        Object.entries(params).forEach(([key, value]) => {
          if (value !== undefined && value !== null && value !== '') {
            searchParams.append(key, value);
          }
        });
        queryString = searchParams.toString();
      }

      const finalUrl = `${API_BASE_URL}${url}${queryString ? `?${queryString}` : ''}`;
      const response = await fetch(finalUrl, options);

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
        throw new Error(error.detail || `HTTP error! status: ${response.status}`);
      }

      if (response.status === 204) {
        return null;
      }

      return response.json();
    },

    get(url, params) {
      return this.request('GET', url, null, params);
    },

    post(url, data) {
      return this.request('POST', url, data);
    },

    put(url, data) {
      return this.request('PUT', url, data);
    },

    patch(url, data) {
      return this.request('PATCH', url, data);
    },

    delete(url) {
      return this.request('DELETE', url);
    },
  };

  return instance;
};

const api = createInstance();

export const userService = {
  getUsers({ page = 1, limit = 10, search = '' } = {}) {
    const params = { page, limit };
    if (search) {
      params.search = search;
    }
    return api.get('/users', params);
  },

  searchUsers({ search = '' } = {}) {
    const params = {};
    if (search) {
      params.name = search;
      params.email = search;
    }
    return api.get('/users/search', params);
  },

  createUser(userData) {
    return api.post('/users', userData);
  },

  updateUser(id, userData) {
    return api.put(`/users/${id}`, userData);
  },

  deleteUser(id) {
    return api.delete(`/users/${id}`);
  },

  getUser(id) {
    return api.get(`/users/${id}`);
  },

  login(credentials) {
    return api.post('/auth/login', credentials);
  },

  register(userData) {
    return api.post('/auth/register', userData);
  },

  logout() {
    return api.post('/auth/logout');
  },

  getMe() {
    return api.get('/auth/me');
  },
};

export default api;