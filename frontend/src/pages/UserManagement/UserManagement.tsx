import ItemManagement from '../../components/ItemManagement';
import { useState } from 'react';
import Modal from '../../components/Modal';

function UserManagement() {
  const [showAddUserModal, setShowAddUserModal] = useState(false);

  const saveUser = () => {
    console.log('save user clicked');
  }

  return (
    <div>
      <h1>User management page</h1>
      <ItemManagement
        pageName="User"
        onAdd={() => setShowAddUserModal(true)}
      />
    {showAddUserModal && (
      <Modal title="Add New User" onClose={() => setShowAddUserModal(false)}>
        <div className="d-flex flex-column gap-4">
          <div className="d-flex gap-2">
            <div>
            <label>First Name</label>
            <input type="text" placeholder="Enter first name" style={inputStyle} />
            </div>
            <div>
            <label>Middle Name</label>
            <input type="text" placeholder="Enter middle name" style={inputStyle} />
            </div>
          </div>

          <div>
            <label>Last Name</label>
            <input type="text" placeholder="Enter last name" style={inputStyle} />
          </div>

          <div>
            <label>Email</label>
            <input type="email" placeholder="Enter email" style={inputStyle} />
          </div>

          <div>
            <label>Phone Number</label>
            <input type="text" placeholder="Enter phone number" style={inputStyle} />
          </div>

          <div>
            <label>Role</label>
            <select style={inputStyle}>
              <option value="">Select role</option>
              <option value="admin">Admin</option>
              <option value="manager">Manager</option>
              <option value="user">User</option>
            </select>
          </div>

          <div>
            <label>Status</label>
            <select style={inputStyle}>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
            </select>
          </div>

          <div>
            <label>Password</label>
            <input type="password" placeholder="Enter password" style={inputStyle} />
          </div>

          <button
            style={{
              marginTop: "10px",
              background: "#0ea5a4",
              padding: "10px 14px",
              color: "#fff",
              border: "none",
              borderRadius: "6px",
              cursor: "pointer",
              fontWeight: 600,
            }}
            onClick={() => {saveUser()}}
          >

            Save User
          </button>
        </div>
      </Modal>
      )}
    </div>
  );
}

const inputStyle: React.CSSProperties = {
  width: "100%",
  padding: "8px 10px",
  marginTop: "5px",
  borderRadius: "6px",
  border: "1px solid #d1d5db",
  fontSize: "14px",
};


export default UserManagement;
