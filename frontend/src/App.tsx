import { useState } from 'react';
import { Routes, Route } from 'react-router-dom';

import Login from './pages/Login/login';
import Dashboard from './pages/Dashboard/Dashboard';

function App() {
  const [user, setUser] = useState<boolean>(false);
  return (
    <>
      {!user && <Login user={user} setUser={setUser} />}
      {user && (
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="*" element={<h1>404 - Not Found</h1>} />
        </Routes>
      )}
    </>
  );
}

export default App;
