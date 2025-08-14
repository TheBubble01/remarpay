import axios from "axios";

const token = localStorage.getItem("token");
const api = axios.create({
  baseURL: "http://localhost:8000/api", // adjust if needed
  withCredentials: true, // if you need to send cookies with requests

  // baseURL: "https://51mqhwmd-8000.uks1.devtunnels.ms/" // tunneling my django server

  headers: {
    "Content-Type": "application/json",
    Authorization: token ? `Bearer ${token}` : "", // Include token if available
  },
});

export default api;
