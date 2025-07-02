import React from "react";
import { Routes, Route } from "react-router-dom";

function AuthRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<div>Login Page</div>} />
      <Route path="/register" element={<div>Register Page</div>} />
    </Routes>
  );
}

export default AuthRoutes;
