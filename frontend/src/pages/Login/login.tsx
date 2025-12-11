import React, { useState, useEffect } from 'react';
import { useUserStore } from '../../store/userStore';
import './login.css';
import { StorageManager } from '../../utils/Storage/storageManager';

const Login = () => {
  const { user, setUser } = useUserStore();
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');

  useEffect(() => {
    // Initialize StorageManager
    try {
      StorageManager.init('local');
    } catch (e) {
      // ignore if storage is already initialized
    }

    // Check token in localStorage
    const token = StorageManager.getInstance().getItem('auth_token');

    // Check token validity
    if (token) {
      // Mock API call to validate token
      const mockValidateToken = (token: string): Promise<boolean> => {
        return new Promise((resolve) => {
          setTimeout(() => {
            // Mock valid token if it's 'mocked-jwt-token'
            resolve(token === 'mocked-jwt-token');
          }, 200);
        });
      };

      mockValidateToken(token).then((isValid) => {
        if (isValid) {
          setUser({ username: 'admin', token, role: 'admin' });
        } else {
          StorageManager.getInstance().removeItem('auth_token');
          setUser(null);
        }
      });
    }
  }, []);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const login = () => {
      if (username === 'admin' && password === 'admin') {
        // Mocked token
        const _token = 'mocked-jwt-token';
        // Save token in localStorage, (sessionStorage, or Cookie)
        StorageManager.getInstance().setItem('auth_token', _token);
        setUser({ username, token: _token });
      } else {
        alert('Wrong username or password');
        setUser(null);
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

        <p className="login-status">
          {user ? `Logged in as ${user.username}` : 'Not logged in'}
        </p>
      </div>
    </div>
  );
};

export default Login;
