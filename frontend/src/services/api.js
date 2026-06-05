import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

const api = axios.create({ baseURL: BASE_URL });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export const authService = {
  register: (data) => api.post("/users/register", data),
  login: (email, password) => {
    const form = new FormData();
    form.append("username", email);
    form.append("password", password);
    return api.post("/users/login", form);
  },
  getMe: () => api.get("/users/me"),
};

export const proposalService = {
  create: (data) => api.post("/proposals/", data),
  list: (skip = 0, limit = 20) => api.get(`/proposals/?skip=${skip}&limit=${limit}`),
  get: (id) => api.get(`/proposals/${id}`),
  getStatus: (id) => api.get(`/proposals/${id}/status`),
  sign: (id) => api.post(`/proposals/${id}/sign`),
  getComments: (id) => api.get(`/proposals/${id}/comments`),
  addComment: (data) => api.post("/proposals/comments/", data),
  addResource: (data) => api.post("/proposals/resources/", data),
};

export default api;
