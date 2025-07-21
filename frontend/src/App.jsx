import { useEffect, useState } from 'react';
import axios from 'axios';

const API = '{LOAD_BALANCER_URL}';

function App() {
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState({ name: '', email: '' });

  // Fetch users
  const fetchUsers = async () => {
    const res = await axios.get(`${API}/users`);

    setUsers(res.data);
  };

  useEffect(() => { fetchUsers() }, []);

  // Handle form input
  const handleChange = e =>
    setForm({ ...form, [e.target.name]: e.target.value });

  // Create or update
  const handleSubmit = async e => {
    e.preventDefault();
    if (form.id) {
      await axios.put(`${API}/users/${form.id}`, form);
    } else {
      await axios.post(`${API}/users`, form);
    }
    setForm({ name: '', email: '' });
    fetchUsers();
  };

  // Edit button
  const editUser = user => setForm(user);

  // Delete button
  const deleteUser = async id => {
    await axios.delete(`${API}/users/${id}`);
    fetchUsers();
  };

  return (
    <div style={{ maxWidth: 600, margin: '2rem auto' }}>
      <h1>User Management</h1>
      <form onSubmit={handleSubmit}>
        <input name="name" value={form.name} onChange={handleChange} placeholder="Name" required />
        <input name="email" value={form.email} onChange={handleChange} placeholder="Email" required />
        <button type="submit">{form.id ? 'Update' : 'Create'}</button>
        {form.id && <button onClick={() => setForm({ name: '', email: '' })}>Cancel</button>}
      </form>

      <table border="1" cellPadding="5" style={{ marginTop: 20, width: '100%' }}>
        <thead><tr><th>ID</th><th>Name</th><th>Email</th><th>Actions</th></tr></thead>
        <tbody>
          {users.map(u =>
            <tr key={u.id}>
              <td>{u.id}</td>
              <td>{u.name}</td>
              <td>{u.email}</td>
              <td>
                <button onClick={() => editUser(u)}>✎</button>
                <button onClick={() => deleteUser(u.id)}>🗑</button>
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default App;
