import React, { useState } from 'react';

type LoginProps = {
  user: boolean;
  setUser: React.Dispatch<React.SetStateAction<boolean>>;
};

const Login: React.FC<LoginProps> = ({ user, setUser }) => {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (username === 'admin' && password === 'admin') {
      setUser(true);
    } else {
      alert('Wrong username or password');
      setUser(false);
    }
  };

  return (
    <div>
      <h1>Login page</h1>

      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Username:
            <input
              value={username}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setUsername(e.target.value)
              }
              name="username"
              autoComplete="username"
            />
          </label>
        </div>

        <div>
          <label>
            Password:
            <input
              type="password"
              value={password}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setPassword(e.target.value)
              }
              name="password"
              autoComplete="current-password"
            />
          </label>
        </div>

        <button type="submit">Login</button>
      </form>

      {user ? <p>Logged in</p> : <p>Not logged in</p>}
    </div>
  );
};

export default Login;
