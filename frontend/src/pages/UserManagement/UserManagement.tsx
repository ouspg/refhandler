import ItemManagement from '../../components/ItemManagement';
import { useState } from 'react';
import Modal from '../../components/Modal';

type UserForm = {
  firstName: string;
  middleName: string;
  lastName: string;
  email: string;
  phone: string;
  role: string;
  status: string;
  password: string;
};

function UserManagement() {
  const [showAddUserModal, setShowAddUserModal] = useState(false);

  const [form, setForm] = useState<UserForm>({
    firstName: '',
    middleName: '',
    lastName: '',
    email: '',
    phone: '',
    role: '',
    status: 'active',
    password: '',
  });

  const [errors, setErrors] = useState<Partial<UserForm>>({});

  const handleChange = (field: keyof UserForm, value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }));
    setErrors((prev) => ({ ...prev, [field]: '' })); // clear error on change
  };

  const validate = (): boolean => {
    const newErrors: Partial<UserForm> = {};
    if (!form.firstName.trim()) newErrors.firstName = 'First name is required';
    if (!form.lastName.trim()) newErrors.lastName = 'Last name is required';
    if (!form.email.trim()) newErrors.email = 'Email is required';
    else if (!/^[\w.-]+@[a-zA-Z\d.-]+\.[a-zA-Z]{2,}$/.test(form.email))
      newErrors.email = 'Invalid email';
    if (!form.phone.trim()) newErrors.phone = 'Phone number is required';
    if (!form.role) newErrors.role = 'Role is required';
    if (!form.password.trim()) newErrors.password = 'Password is required';

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const saveUser = () => {
    if (!validate()) return;
    console.log('User form submitted', form);
    setForm({
      firstName: '',
      middleName: '',
      lastName: '',
      email: '',
      phone: '',
      role: '',
      status: 'active',
      password: '',
    });
    setShowAddUserModal(false);
  };

  return (
    <div>
      <h1>User management page</h1>
      <ItemManagement pageName="User" onAdd={() => setShowAddUserModal(true)} />

      {showAddUserModal && (
        <Modal title="Add New User" onClose={() => setShowAddUserModal(false)}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>

            <div style={{ display: 'flex', gap: '10px' }}>
              <div style={{ flex: 1 }}>
                <label>First Name</label>
                <input
                  style={inputStyle}
                  type="text"
                  value={form.firstName}
                  onChange={(e) => handleChange('firstName', e.target.value)}
                  placeholder="Enter first name"
                />
                {errors.firstName && <small style={errorStyle}>{errors.firstName}</small>}
              </div>
              <div style={{ flex: 1 }}>
                <label>Middle Name</label>
                <input
                  style={inputStyle}
                  type="text"
                  value={form.middleName}
                  onChange={(e) => handleChange('middleName', e.target.value)}
                  placeholder="Enter middle name"
                />
              </div>
            </div>

            <div>
              <label>Last Name</label>
              <input
                style={inputStyle}
                type="text"
                value={form.lastName}
                onChange={(e) => handleChange('lastName', e.target.value)}
                placeholder="Enter last name"
              />
              {errors.lastName && <small style={errorStyle}>{errors.lastName}</small>}
            </div>

            <div>
              <label>Email</label>
              <input
                style={inputStyle}
                type="email"
                value={form.email}
                onChange={(e) => handleChange('email', e.target.value)}
                placeholder="Enter email"
              />
              {errors.email && <small style={errorStyle}>{errors.email}</small>}
            </div>

            <div>
              <label>Phone Number</label>
              <input
                style={inputStyle}
                type="text"
                value={form.phone}
                onChange={(e) => handleChange('phone', e.target.value)}
                placeholder="Enter phone number"
              />
              {errors.phone && <small style={errorStyle}>{errors.phone}</small>}
            </div>

            <div>
              <label>Role</label>
              <select
                style={inputStyle}
                value={form.role}
                onChange={(e) => handleChange('role', e.target.value)}
              >
                <option value="">Select role</option>
                <option value="admin">Admin</option>
                <option value="manager">Manager</option>
                <option value="user">User</option>
              </select>
              {errors.role && <small style={errorStyle}>{errors.role}</small>}
            </div>

            <div>
              <label>Status</label>
              <select
                style={inputStyle}
                value={form.status}
                onChange={(e) => handleChange('status', e.target.value)}
              >
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
              </select>
            </div>

            <div>
              <label>Password</label>
              <input
                style={inputStyle}
                type="password"
                value={form.password}
                onChange={(e) => handleChange('password', e.target.value)}
                placeholder="Enter password"
              />
              {errors.password && <small style={errorStyle}>{errors.password}</small>}
            </div>

            <button style={buttonStyle} onClick={saveUser}>
              Save User
            </button>
          </div>
        </Modal>
      )}
    </div>
  );
}

export default UserManagement;

const inputStyle: React.CSSProperties = {
  width: '100%',
  padding: '8px 10px',
  marginTop: '5px',
  borderRadius: '6px',
  border: '1px solid #d1d5db',
  fontSize: '14px',
};

const errorStyle: React.CSSProperties = {
  color: 'red',
  fontSize: '12px',
  marginTop: '2px',
  display: 'block',
};

const buttonStyle: React.CSSProperties = {
  marginTop: '10px',
  background: '#0ea5a4',
  padding: '10px 14px',
  color: '#fff',
  border: 'none',
  borderRadius: '6px',
  cursor: 'pointer',
  fontWeight: 600,
};
