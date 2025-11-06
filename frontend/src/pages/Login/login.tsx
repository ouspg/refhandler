import React, { useState } from 'react';
import { useUserStore } from '../../store/userStore';
import './login.css';

const Login = () => {
  const { user, setUser } = useUserStore();
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const login = () => {
      if (username === 'admin' && password === 'admin') {
        setUser(true);
      } else {
        alert('Wrong username or password');
        setUser(false);
      }
    };
    login();
  };

  return (
    <div className="login-page">
      <div className="login-card" role="region" aria-labelledby="login-title">
        <h1 id="login-title" className="login-title">
          Welcome back
        </h1>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              className="input"
              value={username}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setUsername(e.target.value)
              }
              name="username"
              autoComplete="username"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              className="input"
              type="password"
              value={password}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setPassword(e.target.value)
              }
              name="password"
              autoComplete="current-password"
            />
          </div>

          <button type="submit" className="btn btn-primary">
            Login
          </button>
        </form>

        <p className="login-status">{user ? 'Logged in' : 'Not logged in'}</p>
      </div>
    </div>
  );
};

export default Login;
