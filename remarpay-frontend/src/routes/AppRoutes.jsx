import React from 'react';
import { Routes, Route } from 'react-router-dom';
import AuthRoutes from './AuthRoutes';
import NotFound from '../pages/shared/NotFound';

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/*" element={<AuthRoutes />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

export default AppRoutes;
