import { Routes, Route } from 'react-router-dom';
import { useUserStore } from './store/userStore';
import './App.css';

import Login from './pages/Login/login';
import NavBar from './components/NavBar';
import Dashboard from './pages/Dashboard/Dashboard';
import UserManagement from './pages/UserManagement/UserManagement';
import ProjectManagement from './pages/ProjectManagement/ProjectManagement';

function App() {
  const { user } = useUserStore();

  return (
    <div className="app-root">
      {!user && <Login />}
      {user && (
        <>
          <NavBar />
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/user-management" element={<UserManagement />} />
            <Route path="/project-management" element={<ProjectManagement />} />
            <Route path="*" element={<h1>404 - Not Found</h1>} />
          </Routes>
        </>
      )}
    </div>
  );
}

export default App;
