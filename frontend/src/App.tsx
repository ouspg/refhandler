import { useState } from 'react';
import { Routes, Route } from 'react-router-dom';

import Login from './pages/Login/login';
import NavBar from './components/NavBar';
import Dashboard from './pages/Dashboard/Dashboard';
import UserManagement from './pages/UserManagement/UserManagement';
import ProjectManagement from './pages/ProjectManagement/ProjectManagement';

function App() {
  const [user, setUser] = useState<boolean>(false);
  return (
    <>
      {!user && <Login user={user} setUser={setUser} />}
      {user && (
        <>
          <NavBar setUser={setUser} />
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/user-management" element={<UserManagement />} />
            <Route path="/project-management" element={<ProjectManagement />} />
            <Route path="*" element={<h1>404 - Not Found</h1>} />
          </Routes>
        </>
      )}
    </>
  );
}

export default App;
