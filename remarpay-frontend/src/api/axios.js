import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api", // adjust if needed

  // baseURL: "https://51mqhwmd-8000.uks1.devtunnels.ms/" // tunneling my django server

  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
