import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';

type Props = {
  setUser: React.Dispatch<React.SetStateAction<boolean>>;
};

const NavBar: React.FC<Props> = ({ setUser }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    setUser(false);
    navigate('/');
  };

  return (
    <nav style={styles.nav}>
      <div style={styles.brand}>RefHandler</div>

      <ul style={styles.links}>
        <li>
          <NavLink
            to="/"
            style={({ isActive }) =>
              isActive ? { ...styles.link, ...styles.activeLink } : styles.link
            }
          >
            Dashboard
          </NavLink>
        </li>
        <li>
          <NavLink
            to="/user-management"
            style={({ isActive }) =>
              isActive ? { ...styles.link, ...styles.activeLink } : styles.link
            }
          >
            Users
          </NavLink>
        </li>
        <li>
          <NavLink
            to="/project-management"
            style={({ isActive }) =>
              isActive ? { ...styles.link, ...styles.activeLink } : styles.link
            }
          >
            Projects
          </NavLink>
        </li>
      </ul>

      <div>Hello User</div>

      <div style={styles.actions}>
        <button style={styles.logout} onClick={handleLogout}>
          Logout
        </button>
      </div>
    </nav>
  );
};

export default NavBar;

const styles: Record<string, React.CSSProperties> = {
  nav: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '0.5rem 1rem',
    background: '#0f172a',
    color: '#fff',
  },
  brand: {
    fontWeight: 700,
    fontSize: '1.1rem',
  },
  links: {
    display: 'flex',
    gap: '1rem',
    listStyle: 'none',
    margin: 0,
    padding: 0,
    alignItems: 'center',
  },
  link: {
    color: '#cbd5e1',
    textDecoration: 'none',
    padding: '0.25rem 0',
  },
  activeLink: {
    color: '#fff',
    borderBottom: '2px solid #60a5fa',
  },
  actions: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
  },
  logout: {
    background: 'transparent',
    border: '1px solid #334155',
    color: '#fff',
    padding: '0.25rem 0.5rem',
    cursor: 'pointer',
  },
};
