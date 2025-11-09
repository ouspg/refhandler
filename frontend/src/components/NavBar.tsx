import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useUserStore } from '../store/userStore';

const NavBar = () => {
  const navigate = useNavigate();
  const { user, setUser } = useUserStore();

  const handleLogout = () => {
    setUser(null);
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

      <div>Hello {user ? user.username : 'User'}</div>

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
    /* match login button accent */
    background: '#2563eb',
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
    color: 'rgba(255,255,255,0.95)',
    textDecoration: 'none',
    padding: '0.25rem 0',
  },
  activeLink: {
    color: '#fff',
    borderBottom: '2px solid rgba(255,255,255,0.18)',
  },
  actions: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
  },
  logout: {
    /* inverted button to stand out on the blue nav */
    background: '#ffffff',
    border: '1px solid rgba(255,255,255,0.12)',
    color: '#2563eb',
    padding: '0.35rem 0.6rem',
    cursor: 'pointer',
    borderRadius: '8px',
  },
};
