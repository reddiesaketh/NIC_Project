from django.http import HttpResponse

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NIC Employee Portal</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg: #f4f5f7;
    --surface: #ffffff;
    --sidebar-bg: #1a1f2e;
    --sidebar-text: #8b95a8;
    --sidebar-active: #ffffff;
    --sidebar-active-bg: #2d3548;
    --sidebar-accent: #4f6ef7;
    --primary: #4f6ef7;
    --primary-hover: #3a58e0;
    --text: #1a1f2e;
    --text-muted: #6b7280;
    --border: #e5e7eb;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --info: #3b82f6;
    --radius: 10px;
    --shadow: 0 1px 3px rgba(0,0,0,0.08);
  }

  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }

  /* AUTH */
  #auth-screen { display: flex; align-items: center; justify-content: center; min-height: 100vh; background: var(--sidebar-bg); }
  .auth-card { background: var(--surface); border-radius: 16px; padding: 2.5rem; width: 100%; max-width: 400px; }
  .auth-logo { text-align: center; margin-bottom: 2rem; }
  .auth-logo h1 { font-size: 1.5rem; font-weight: 700; color: var(--text); }
  .auth-logo p { color: var(--text-muted); font-size: 0.875rem; margin-top: 4px; }
  .auth-logo .badge { display: inline-block; background: #eef1fe; color: var(--primary); font-size: 0.7rem; font-weight: 600; padding: 3px 10px; border-radius: 20px; margin-bottom: 12px; letter-spacing: 0.05em; text-transform: uppercase; }
  label { display: block; font-size: 0.8rem; font-weight: 600; color: var(--text-muted); margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.04em; }
  input { width: 100%; padding: 10px 14px; border: 1.5px solid var(--border); border-radius: 8px; font-size: 0.9rem; color: var(--text); background: var(--surface); outline: none; transition: border-color 0.15s; margin-bottom: 1rem; }
  input:focus { border-color: var(--primary); }
  .btn { display: inline-flex; align-items: center; gap: 6px; padding: 10px 18px; border-radius: 8px; font-size: 0.875rem; font-weight: 600; cursor: pointer; border: none; transition: all 0.15s; }
  .btn-primary { background: var(--primary); color: #fff; width: 100%; justify-content: center; }
  .btn-primary:hover { background: var(--primary-hover); }
  .btn-sm { padding: 6px 12px; font-size: 0.8rem; }
  .btn-outline { background: transparent; border: 1.5px solid var(--border); color: var(--text-muted); }
  .btn-outline:hover { border-color: var(--primary); color: var(--primary); }
  .btn-danger { background: #fee2e2; color: var(--danger); border: none; }
  .btn-success { background: #d1fae5; color: var(--success); border: none; }
  #auth-error { color: var(--danger); font-size: 0.8rem; margin-bottom: 1rem; display: none; background: #fee2e2; padding: 8px 12px; border-radius: 6px; }

  /* LAYOUT */
  #app { display: none; height: 100vh; overflow: hidden; }
  .layout { display: flex; height: 100vh; }

  /* SIDEBAR */
  .sidebar { width: 220px; background: var(--sidebar-bg); display: flex; flex-direction: column; flex-shrink: 0; }
  .sidebar-header { padding: 1.5rem 1.25rem 1rem; border-bottom: 1px solid rgba(255,255,255,0.06); }
  .sidebar-header h2 { color: #fff; font-size: 1rem; font-weight: 700; }
  .sidebar-header p { color: var(--sidebar-text); font-size: 0.72rem; margin-top: 2px; }
  .nav { flex: 1; padding: 1rem 0.75rem; display: flex; flex-direction: column; gap: 2px; }
  .nav-group-label { font-size: 0.65rem; font-weight: 700; color: #4a5568; text-transform: uppercase; letter-spacing: 0.08em; padding: 0.75rem 0.5rem 0.25rem; }
  .nav-item { display: flex; align-items: center; gap: 10px; padding: 8px 10px; border-radius: 7px; color: var(--sidebar-text); font-size: 0.85rem; cursor: pointer; transition: all 0.15s; }
  .nav-item:hover { background: rgba(255,255,255,0.06); color: #d1d5db; }
  .nav-item.active { background: var(--sidebar-active-bg); color: var(--sidebar-active); }
  .nav-item .nav-icon { width: 16px; text-align: center; font-size: 0.9rem; }
  .sidebar-footer { padding: 1rem 0.75rem; border-top: 1px solid rgba(255,255,255,0.06); }
  .user-chip { display: flex; align-items: center; gap: 8px; }
  .user-avatar { width: 30px; height: 30px; border-radius: 50%; background: var(--sidebar-accent); display: flex; align-items: center; justify-content: center; color: #fff; font-size: 0.7rem; font-weight: 700; }
  .user-info { flex: 1; }
  .user-info .name { color: #d1d5db; font-size: 0.8rem; font-weight: 600; }
  .user-info .role { color: var(--sidebar-text); font-size: 0.7rem; }
  .logout-btn { background: none; border: none; color: var(--sidebar-text); cursor: pointer; padding: 4px; border-radius: 4px; font-size: 0.8rem; }
  .logout-btn:hover { color: var(--danger); }

  /* MAIN */
  .main { flex: 1; overflow-y: auto; display: flex; flex-direction: column; }
  .topbar { background: var(--surface); border-bottom: 1px solid var(--border); padding: 1rem 1.75rem; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 10; }
  .topbar h1 { font-size: 1.1rem; font-weight: 700; }
  .topbar-actions { display: flex; gap: 8px; }
  .content { padding: 1.75rem; flex: 1; }

  /* CARDS */
  .card { background: var(--surface); border-radius: var(--radius); border: 1px solid var(--border); }
  .card-header { padding: 1rem 1.25rem; border-bottom: 1px solid var(--border); display: flex; align-items: center; justify-content: space-between; }
  .card-header h3 { font-size: 0.9rem; font-weight: 700; }
  .card-body { padding: 1.25rem; }

  /* STATS GRID */
  .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
  .stat-card { background: var(--surface); border-radius: var(--radius); border: 1px solid var(--border); padding: 1.25rem; }
  .stat-label { font-size: 0.72rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 8px; }
  .stat-value { font-size: 2rem; font-weight: 700; color: var(--text); line-height: 1; }
  .stat-sub { font-size: 0.75rem; color: var(--text-muted); margin-top: 4px; }
  .stat-icon { float: right; width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; }

  /* TABLE */
  .table-wrap { overflow-x: auto; }
  table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
  th { text-align: left; padding: 10px 14px; font-size: 0.7rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; background: #f9fafb; border-bottom: 1px solid var(--border); }
  td { padding: 12px 14px; border-bottom: 1px solid #f3f4f6; vertical-align: middle; }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: #fafbfc; }

  /* BADGE */
  .badge { display: inline-block; padding: 3px 8px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; }
  .badge-active, .badge-approved, .badge-completed { background: #d1fae5; color: #065f46; }
  .badge-inactive, .badge-rejected, .badge-cancelled { background: #fee2e2; color: #991b1b; }
  .badge-pending { background: #fef3c7; color: #92400e; }
  .badge-suspended { background: #ede9fe; color: #5b21b6; }
  .badge-contract { background: #dbeafe; color: #1e40af; }
  .badge-permanent { background: #d1fae5; color: #065f46; }
  .badge-probation { background: #fef3c7; color: #92400e; }

  /* FORM */
  .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
  .form-group { margin-bottom: 0; }
  .form-group label { margin-bottom: 4px; }
  select { width: 100%; padding: 10px 14px; border: 1.5px solid var(--border); border-radius: 8px; font-size: 0.9rem; color: var(--text); background: var(--surface); outline: none; cursor: pointer; }
  select:focus { border-color: var(--primary); }
  textarea { width: 100%; padding: 10px 14px; border: 1.5px solid var(--border); border-radius: 8px; font-size: 0.9rem; color: var(--text); background: var(--surface); outline: none; resize: vertical; min-height: 80px; }

  /* MODAL */
  .modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.45); z-index: 100; display: none; align-items: center; justify-content: center; }
  .modal-overlay.open { display: flex; }
  .modal { background: var(--surface); border-radius: 14px; width: 100%; max-width: 560px; max-height: 90vh; overflow-y: auto; }
  .modal-header { padding: 1.25rem 1.5rem; border-bottom: 1px solid var(--border); display: flex; align-items: center; justify-content: space-between; }
  .modal-header h3 { font-size: 1rem; font-weight: 700; }
  .modal-body { padding: 1.5rem; }
  .modal-footer { padding: 1rem 1.5rem; border-top: 1px solid var(--border); display: flex; justify-content: flex-end; gap: 8px; }
  .close-btn { background: none; border: none; font-size: 1.2rem; cursor: pointer; color: var(--text-muted); }

  /* TOAST */
  #toast { position: fixed; bottom: 1.5rem; right: 1.5rem; z-index: 9999; display: flex; flex-direction: column; gap: 8px; }
  .toast-item { padding: 12px 18px; border-radius: 10px; font-size: 0.85rem; font-weight: 600; color: #fff; animation: slideIn 0.2s ease; min-width: 220px; }
  .toast-success { background: var(--success); }
  .toast-error { background: var(--danger); }
  .toast-info { background: var(--info); }
  @keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }

  /* EMPTY */
  .empty { text-align: center; padding: 3rem; color: var(--text-muted); }
  .empty-icon { font-size: 2.5rem; margin-bottom: 12px; opacity: 0.3; }
  .empty p { font-size: 0.875rem; }

  /* LOADER */
  .loader { text-align: center; padding: 2rem; color: var(--text-muted); font-size: 0.85rem; }

  /* DETAIL PANEL */
  .detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
  .detail-item { }
  .detail-item .dl { font-size: 0.72rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 3px; }
  .detail-item .dv { font-size: 0.875rem; color: var(--text); }

  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
  @media (max-width: 900px) { .stats-grid { grid-template-columns: 1fr 1fr; } .two-col { grid-template-columns: 1fr; } .form-grid { grid-template-columns: 1fr; } }
</style>
</head>
<body>

<!-- AUTH -->
<div id="auth-screen">
  <div class="auth-card">
    <div class="auth-logo">
      <div class="badge">NIC Project</div>
      <h1>Employee Portal</h1>
      <p>Sign in to access the dashboard</p>
    </div>
    <div id="auth-error"></div>
    <div class="form-group">
      <label>Username or Email</label>
      <input type="text" id="login-username" placeholder="admin" />
    </div>
    <div class="form-group">
      <label>Password</label>
      <input type="password" id="login-password" placeholder="••••••••" />
    </div>
    <button class="btn btn-primary" onclick="login()">Sign in</button>
  </div>
</div>

<!-- APP -->
<div id="app">
  <div class="layout">
    <!-- SIDEBAR -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2>NIC Portal</h2>
        <p>Employee Management</p>
      </div>
      <nav class="nav">
        <div class="nav-group-label">Overview</div>
        <div class="nav-item active" onclick="showPage('dashboard')">
          <span class="nav-icon">⬛</span> Dashboard
        </div>
        <div class="nav-group-label">Records</div>
        <div class="nav-item" onclick="showPage('employees')">
          <span class="nav-icon">👤</span> Employees
        </div>
        <div class="nav-item" onclick="showPage('offices')">
          <span class="nav-icon">🏢</span> Offices
        </div>
        <div class="nav-item" onclick="showPage('departments')">
          <span class="nav-icon">📁</span> Departments
        </div>
        <div class="nav-item" onclick="showPage('designations')">
          <span class="nav-icon">🏷️</span> Designations
        </div>
        <div class="nav-group-label">Operations</div>
        <div class="nav-item" onclick="showPage('transfers')">
          <span class="nav-icon">🔄</span> Transfers
        </div>
        <div class="nav-item" onclick="showPage('systems')">
          <span class="nav-icon">💻</span> System Details
        </div>
      </nav>
      <div class="sidebar-footer">
        <div class="user-chip">
          <div class="user-avatar" id="user-avatar">?</div>
          <div class="user-info">
            <div class="name" id="user-name">—</div>
            <div class="role" id="user-role">—</div>
          </div>
          <button class="logout-btn" onclick="logout()" title="Sign out">✕</button>
        </div>
      </div>
    </aside>

    <!-- MAIN -->
    <main class="main">
      <div class="topbar">
        <h1 id="page-title">Dashboard</h1>
        <div class="topbar-actions" id="topbar-actions"></div>
      </div>
      <div class="content" id="page-content"></div>
    </main>
  </div>
</div>

<!-- MODAL -->
<div class="modal-overlay" id="modal">
  <div class="modal">
    <div class="modal-header">
      <h3 id="modal-title">Modal</h3>
      <button class="close-btn" onclick="closeModal()">✕</button>
    </div>
    <div class="modal-body" id="modal-body"></div>
    <div class="modal-footer" id="modal-footer"></div>
  </div>
</div>

<!-- TOAST -->
<div id="toast"></div>

<script>
const API = '/api/records';
const API_USERS = '/api/users';
let TOKEN = localStorage.getItem('nic_token') || '';
let currentUser = JSON.parse(localStorage.getItem('nic_user') || 'null');

// ── AUTH ──────────────────────────────────────────────────────────────────
async function login() {
  const username = document.getElementById('login-username').value.trim();
  const password = document.getElementById('login-password').value;
  const errEl = document.getElementById('auth-error');
  errEl.style.display = 'none';
  if (!username || !password) { showError(errEl, 'Please enter credentials.'); return; }
  try {
    const res = await fetch(`${API_USERS}/token/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    if (!res.ok) { showError(errEl, data.detail || 'Invalid credentials.'); return; }
    TOKEN = data.access;
    localStorage.setItem('nic_token', TOKEN);
    await fetchCurrentUser();
    document.getElementById('auth-screen').style.display = 'none';
    document.getElementById('app').style.display = 'flex';
    showPage('dashboard');
  } catch (e) { showError(errEl, 'Could not connect to server.'); }
}

function showError(el, msg) { el.textContent = msg; el.style.display = 'block'; }

async function fetchCurrentUser() {
  try {
    const res = await api(`${API_USERS}/me/`);
    currentUser = await res.json();
    localStorage.setItem('nic_user', JSON.stringify(currentUser));
    const name = (currentUser.first_name || '') + ' ' + (currentUser.last_name || '');
    document.getElementById('user-name').textContent = name.trim() || currentUser.username;
    document.getElementById('user-role').textContent = currentUser.role || 'User';
    document.getElementById('user-avatar').textContent = (name.trim()[0] || currentUser.username[0] || '?').toUpperCase();
  } catch(e) {}
}

function logout() {
  TOKEN = ''; localStorage.removeItem('nic_token'); localStorage.removeItem('nic_user');
  document.getElementById('app').style.display = 'none';
  document.getElementById('auth-screen').style.display = 'flex';
}

// ── API HELPER ────────────────────────────────────────────────────────────
function api(url, options = {}) {
  return fetch(url, {
    ...options,
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${TOKEN}`, ...(options.headers || {}) }
  });
}

// ── NAVIGATION ────────────────────────────────────────────────────────────
function showPage(page) {
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  const pages = { dashboard: 'Dashboard', employees: 'Employees', offices: 'Offices', departments: 'Departments', designations: 'Designations', transfers: 'Transfers', systems: 'System Details' };
  document.getElementById('page-title').textContent = pages[page] || page;
  document.getElementById('topbar-actions').innerHTML = '';
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(el => { if (el.textContent.toLowerCase().includes(page.replace('-','').toLowerCase())) el.classList.add('active'); });
  const content = document.getElementById('page-content');
  content.innerHTML = '<div class="loader">Loading...</div>';
  const fns = { dashboard: loadDashboard, employees: loadEmployees, offices: loadOffices, departments: loadDepartments, designations: loadDesignations, transfers: loadTransfers, systems: loadSystems };
  if (fns[page]) fns[page]();
}

// ── DASHBOARD ─────────────────────────────────────────────────────────────
async function loadDashboard() {
  const res = await api(`${API}/dashboard/`);
  const data = (await res.json()).data;
  const colors = { total_employees: '#eef1fe', total_offices: '#d1fae5', total_departments: '#fef3c7', total_designations: '#dbeafe' };
  const icons = { total_employees: '👤', total_offices: '🏢', total_departments: '📁', total_designations: '🏷️' };
  const labels = { total_employees: 'Total Employees', total_offices: 'Active Offices', total_departments: 'Departments', total_designations: 'Designations' };

  let statsHTML = '<div class="stats-grid">';
  ['total_employees','total_offices','total_departments','total_designations'].forEach(k => {
    statsHTML += `<div class="stat-card"><div class="stat-label">${labels[k]}<span class="stat-icon" style="background:${colors[k]}">${icons[k]}</span></div><div class="stat-value">${data[k]}</div></div>`;
  });
  statsHTML += '</div>';

  const transferRows = `
    <div class="two-col">
      <div class="card">
        <div class="card-header"><h3>Transfer Stats</h3></div>
        <div class="card-body">
          <div style="display:flex;gap:1rem">
            <div class="stat-card" style="flex:1;background:#fef3c7"><div class="stat-label">Pending</div><div class="stat-value" style="font-size:1.5rem">${data.pending_transfers}</div></div>
            <div class="stat-card" style="flex:1;background:#d1fae5"><div class="stat-label">Completed</div><div class="stat-value" style="font-size:1.5rem">${data.completed_transfers}</div></div>
          </div>
        </div>
      </div>
      <div class="card">
        <div class="card-header"><h3>Employment Types</h3></div>
        <div class="card-body">
          ${Object.entries(data.employment_type_breakdown || {}).map(([k,v]) => `
            <div style="display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid #f3f4f6">
              <span style="font-size:0.82rem">${k}</span>
              <span class="badge badge-${k.toLowerCase()}">${v}</span>
            </div>`).join('')}
        </div>
      </div>
    </div>`;

  document.getElementById('page-content').innerHTML = statsHTML + transferRows;
}

// ── EMPLOYEES ─────────────────────────────────────────────────────────────
async function loadEmployees() {
  document.getElementById('topbar-actions').innerHTML = `<button class="btn btn-primary btn-sm" onclick="openCreateEmployee()">+ Add Employee</button>`;
  const res = await api(`${API}/employees/`);
  const data = await res.json();
  const employees = data.data || [];

  if (!employees.length) { document.getElementById('page-content').innerHTML = `<div class="empty"><div class="empty-icon">👤</div><p>No employees found.</p></div>`; return; }

  const rows = employees.map(e => `
    <tr>
      <td><strong>${e.employee_id}</strong></td>
      <td>${e.full_name || '—'}</td>
      <td>${e.office_name || '—'}</td>
      <td>${e.department_name || '—'}</td>
      <td>${e.designation_name || '—'}</td>
      <td><span class="badge badge-${(e.employment_status||'').toLowerCase()}">${e.employment_status || '—'}</span></td>
      <td><span class="badge badge-${(e.employment_type||'').toLowerCase()}">${e.employment_type || '—'}</span></td>
      <td><button class="btn btn-outline btn-sm" onclick="viewEmployee(${e.id})">View</button></td>
    </tr>`).join('');

  document.getElementById('page-content').innerHTML = `
    <div class="card">
      <div class="card-header"><h3>All Employees (${employees.length})</h3></div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>ID</th><th>Name</th><th>Office</th><th>Department</th><th>Designation</th><th>Status</th><th>Type</th><th></th></tr></thead>
          <tbody>${rows}</tbody>
        </table>
      </div>
    </div>`;
}

async function viewEmployee(id) {
  const res = await api(`${API}/employees/${id}/`);
  const e = (await res.json()).data;
  document.getElementById('modal-title').textContent = `Employee: ${e.employee_id}`;
  document.getElementById('modal-body').innerHTML = `
    <div class="detail-grid">
      <div class="detail-item"><div class="dl">Full Name</div><div class="dv">${e.full_name || '—'}</div></div>
      <div class="detail-item"><div class="dl">Email</div><div class="dv">${e.email || '—'}</div></div>
      <div class="detail-item"><div class="dl">Office</div><div class="dv">${e.office_detail?.name || '—'}</div></div>
      <div class="detail-item"><div class="dl">Department</div><div class="dv">${e.department_detail?.name || '—'}</div></div>
      <div class="detail-item"><div class="dl">Designation</div><div class="dv">${e.designation_detail?.name || '—'}</div></div>
      <div class="detail-item"><div class="dl">Gender</div><div class="dv">${e.gender || '—'}</div></div>
      <div class="detail-item"><div class="dl">Date of Birth</div><div class="dv">${e.date_of_birth || '—'}</div></div>
      <div class="detail-item"><div class="dl">Date of Joining</div><div class="dv">${e.date_of_joining || '—'}</div></div>
      <div class="detail-item"><div class="dl">Employment Type</div><div class="dv"><span class="badge badge-${(e.employment_type||'').toLowerCase()}">${e.employment_type || '—'}</span></div></div>
      <div class="detail-item"><div class="dl">Status</div><div class="dv"><span class="badge badge-${(e.employment_status||'').toLowerCase()}">${e.employment_status || '—'}</span></div></div>
      <div class="detail-item"><div class="dl">Phone</div><div class="dv">${e.phone || '—'}</div></div>
      <div class="detail-item"><div class="dl">Address</div><div class="dv">${e.address || '—'}</div></div>
    </div>`;
  document.getElementById('modal-footer').innerHTML = `<button class="btn btn-outline btn-sm" onclick="closeModal()">Close</button>`;
  openModal();
}

async function openCreateEmployee() {
  const [officesRes, deptRes, desigRes] = await Promise.all([
    api(`${API}/offices/`), api(`${API}/departments/`), api(`${API}/designations/`)
  ]);
  const offices = (await officesRes.json()).data || [];
  const departments = (await deptRes.json()).data || [];
  const designations = (await desigRes.json()).data || [];

  const officeOpts = offices.map(o => `<option value="${o.id}">${o.name}</option>`).join('');
  const deptOpts = departments.map(d => `<option value="${d.id}">${d.name}</option>`).join('');
  const desigOpts = designations.map(d => `<option value="${d.id}">${d.name}</option>`).join('');

  document.getElementById('modal-title').textContent = 'Add Employee';
  document.getElementById('modal-body').innerHTML = `
    <div class="form-grid">
      <div class="form-group"><label>User ID</label><input type="number" id="ef-user" placeholder="User ID" /></div>
      <div class="form-group"><label>Employee ID</label><input id="ef-empid" placeholder="EMP-001" /></div>
      <div class="form-group"><label>Office</label><select id="ef-office"><option value="">Select office</option>${officeOpts}</select></div>
      <div class="form-group"><label>Department</label><select id="ef-dept"><option value="">Select department</option>${deptOpts}</select></div>
      <div class="form-group"><label>Designation</label><select id="ef-desig"><option value="">Select designation</option>${desigOpts}</select></div>
      <div class="form-group"><label>Gender</label><select id="ef-gender"><option value="">Select</option><option value="M">Male</option><option value="F">Female</option><option value="O">Other</option></select></div>
      <div class="form-group"><label>Date of Joining</label><input type="date" id="ef-doj" /></div>
      <div class="form-group"><label>Employment Type</label><select id="ef-type"><option value="PERMANENT">Permanent</option><option value="CONTRACT">Contract</option><option value="PROBATION">Probation</option><option value="DEPUTATION">Deputation</option><option value="TEMPORARY">Temporary</option></select></div>
    </div>`;
  document.getElementById('modal-footer').innerHTML = `
    <button class="btn btn-outline btn-sm" onclick="closeModal()">Cancel</button>
    <button class="btn btn-primary btn-sm" onclick="createEmployee()">Create</button>`;
  openModal();
}

async function createEmployee() {
  const body = {
    user: document.getElementById('ef-user').value,
    employee_id: document.getElementById('ef-empid').value,
    office: document.getElementById('ef-office').value,
    department: document.getElementById('ef-dept').value,
    designation: document.getElementById('ef-desig').value,
    gender: document.getElementById('ef-gender').value,
    date_of_joining: document.getElementById('ef-doj').value,
    employment_type: document.getElementById('ef-type').value,
  };
  const res = await api(`${API}/employees/`, { method: 'POST', body: JSON.stringify(body) });
  const data = await res.json();
  if (res.ok) { toast('Employee created successfully.', 'success'); closeModal(); loadEmployees(); }
  else { toast(JSON.stringify(data.errors || data.message), 'error'); }
}

// ── OFFICES ───────────────────────────────────────────────────────────────
async function loadOffices() {
  document.getElementById('topbar-actions').innerHTML = `<button class="btn btn-primary btn-sm" onclick="openCreateOffice()">+ Add Office</button>`;
  const res = await api(`${API}/offices/`);
  const offices = (await res.json()).data || [];
  if (!offices.length) { document.getElementById('page-content').innerHTML = `<div class="empty"><div class="empty-icon">🏢</div><p>No offices found.</p></div>`; return; }
  const rows = offices.map(o => `
    <tr>
      <td><strong>${o.code}</strong></td>
      <td>${o.name}</td>
      <td>${o.office_type}</td>
      <td>${o.district_name || '—'}</td>
      <td>${o.state_name || '—'}</td>
      <td>${o.employee_count ?? '—'}</td>
      <td><span class="badge badge-${o.is_active ? 'active' : 'inactive'}">${o.is_active ? 'Active' : 'Inactive'}</span></td>
      <td>
        <button class="btn btn-outline btn-sm" onclick="editOffice(${o.id})">Edit</button>
        <button class="btn btn-danger btn-sm" onclick="deleteOffice(${o.id})">Deactivate</button>
      </td>
    </tr>`).join('');
  document.getElementById('page-content').innerHTML = `
    <div class="card">
      <div class="card-header"><h3>All Offices (${offices.length})</h3></div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Code</th><th>Name</th><th>Type</th><th>District</th><th>State</th><th>Employees</th><th>Status</th><th></th></tr></thead>
          <tbody>${rows}</tbody>
        </table>
      </div>
    </div>`;
}

function openCreateOffice() {
  document.getElementById('modal-title').textContent = 'Add Office';
  document.getElementById('modal-body').innerHTML = `
    <div class="form-grid">
      <div class="form-group"><label>Name</label><input id="of-name" placeholder="Head Office" /></div>
      <div class="form-group"><label>Code</label><input id="of-code" placeholder="HQ-01" /></div>
      <div class="form-group"><label>Office Type</label><select id="of-type"><option value="HEAD">Head Office</option><option value="REGIONAL">Regional</option><option value="DISTRICT">District</option><option value="SUB">Sub Office</option><option value="OTHER">Other</option></select></div>
      <div class="form-group"><label>District ID</label><input type="number" id="of-district" placeholder="District ID" /></div>
    </div>
    <div class="form-group" style="margin-top:1rem"><label>Address</label><textarea id="of-address" placeholder="Office address"></textarea></div>
    <div class="form-grid" style="margin-top:1rem">
      <div class="form-group"><label>Phone</label><input id="of-phone" placeholder="+91..." /></div>
      <div class="form-group"><label>Email</label><input id="of-email" type="email" placeholder="office@nic.in" /></div>
    </div>`;
  document.getElementById('modal-footer').innerHTML = `
    <button class="btn btn-outline btn-sm" onclick="closeModal()">Cancel</button>
    <button class="btn btn-primary btn-sm" onclick="createOffice()">Create</button>`;
  openModal();
}

async function createOffice() {
  const body = { name: document.getElementById('of-name').value, code: document.getElementById('of-code').value, office_type: document.getElementById('of-type').value, district: document.getElementById('of-district').value, address: document.getElementById('of-address').value, phone: document.getElementById('of-phone').value, email: document.getElementById('of-email').value };
  const res = await api(`${API}/offices/`, { method: 'POST', body: JSON.stringify(body) });
  const data = await res.json();
  if (res.ok) { toast('Office created.', 'success'); closeModal(); loadOffices(); }
  else { toast(JSON.stringify(data.errors || data.message), 'error'); }
}

async function editOffice(id) {
  const res = await api(`${API}/offices/${id}/`);
  const o = (await res.json()).data;
  document.getElementById('modal-title').textContent = `Edit Office: ${o.name}`;
  document.getElementById('modal-body').innerHTML = `
    <div class="form-grid">
      <div class="form-group"><label>Name</label><input id="of-name" value="${o.name}" /></div>
      <div class="form-group"><label>Code</label><input id="of-code" value="${o.code}" /></div>
      <div class="form-group"><label>Phone</label><input id="of-phone" value="${o.phone || ''}" /></div>
      <div class="form-group"><label>Email</label><input id="of-email" value="${o.email || ''}" /></div>
    </div>
    <div class="form-group" style="margin-top:1rem"><label>Address</label><textarea id="of-address">${o.address || ''}</textarea></div>`;
  document.getElementById('modal-footer').innerHTML = `
    <button class="btn btn-outline btn-sm" onclick="closeModal()">Cancel</button>
    <button class="btn btn-primary btn-sm" onclick="updateOffice(${id})">Save</button>`;
  openModal();
}

async function updateOffice(id) {
  const body = { name: document.getElementById('of-name').value, phone: document.getElementById('of-phone').value, email: document.getElementById('of-email').value, address: document.getElementById('of-address').value };
  const res = await api(`${API}/offices/${id}/`, { method: 'PATCH', body: JSON.stringify(body) });
  if (res.ok) { toast('Office updated.', 'success'); closeModal(); loadOffices(); }
  else { const d = await res.json(); toast(JSON.stringify(d.errors || d.message), 'error'); }
}

async function deleteOffice(id) {
  if (!confirm('Deactivate this office?')) return;
  const res = await api(`${API}/offices/${id}/`, { method: 'DELETE' });
  if (res.ok) { toast('Office deactivated.', 'success'); loadOffices(); }
  else { const d = await res.json(); toast(d.message || 'Error.', 'error'); }
}

// ── DEPARTMENTS ───────────────────────────────────────────────────────────
async function loadDepartments() {
  document.getElementById('topbar-actions').innerHTML = `<button class="btn btn-primary btn-sm" onclick="openCreateDept()">+ Add Department</button>`;
  const res = await api(`${API}/departments/`);
  const depts = (await res.json()).data || [];
  if (!depts.length) { document.getElementById('page-content').innerHTML = `<div class="empty"><div class="empty-icon">📁</div><p>No departments found.</p></div>`; return; }
  const rows = depts.map(d => `
    <tr>
      <td><strong>${d.name}</strong></td>
      <td>${d.code || '—'}</td>
      <td>${d.description || '—'}</td>
      <td><span class="badge badge-${d.is_active ? 'active' : 'inactive'}">${d.is_active ? 'Active' : 'Inactive'}</span></td>
      <td>
        <button class="btn btn-outline btn-sm" onclick="editDept(${d.id}, '${d.name}', '${d.code||''}', '${d.description||''}')">Edit</button>
        <button class="btn btn-danger btn-sm" onclick="deleteDept(${d.id})">Delete</button>
      </td>
    </tr>`).join('');
  document.getElementById('page-content').innerHTML = `
    <div class="card">
      <div class="card-header"><h3>Departments (${depts.length})</h3></div>
      <div class="table-wrap"><table><thead><tr><th>Name</th><th>Code</th><th>Description</th><th>Status</th><th></th></tr></thead><tbody>${rows}</tbody></table></div>
    </div>`;
}

function openCreateDept() {
  document.getElementById('modal-title').textContent = 'Add Department';
  document.getElementById('modal-body').innerHTML = `
    <div class="form-group"><label>Name</label><input id="df-name" placeholder="Finance" /></div>
    <div class="form-group" style="margin-top:1rem"><label>Code</label><input id="df-code" placeholder="FIN" /></div>
    <div class="form-group" style="margin-top:1rem"><label>Description</label><textarea id="df-desc" placeholder="Department description"></textarea></div>`;
  document.getElementById('modal-footer').innerHTML = `<button class="btn btn-outline btn-sm" onclick="closeModal()">Cancel</button><button class="btn btn-primary btn-sm" onclick="createDept()">Create</button>`;
  openModal();
}

async function createDept() {
  const body = { name: document.getElementById('df-name').value, code: document.getElementById('df-code').value, description: document.getElementById('df-desc').value };
  const res = await api(`${API}/departments/`, { method: 'POST', body: JSON.stringify(body) });
  const data = await res.json();
  if (res.ok) { toast('Department created.', 'success'); closeModal(); loadDepartments(); }
  else { toast(JSON.stringify(data.errors || data.message), 'error'); }
}

function editDept(id, name, code, desc) {
  document.getElementById('modal-title').textContent = 'Edit Department';
  document.getElementById('modal-body').innerHTML = `
    <div class="form-group"><label>Name</label><input id="df-name" value="${name}" /></div>
    <div class="form-group" style="margin-top:1rem"><label>Code</label><input id="df-code" value="${code}" /></div>
    <div class="form-group" style="margin-top:1rem"><label>Description</label><textarea id="df-desc">${desc}</textarea></div>`;
  document.getElementById('modal-footer').innerHTML = `<button class="btn btn-outline btn-sm" onclick="closeModal()">Cancel</button><button class="btn btn-primary btn-sm" onclick="updateDept(${id})">Save</button>`;
  openModal();
}

async function updateDept(id) {
  const body = { name: document.getElementById('df-name').value, code: document.getElementById('df-code').value, description: document.getElementById('df-desc').value };
  const res = await api(`${API}/departments/${id}/`, { method: 'PATCH', body: JSON.stringify(body) });
  if (res.ok) { toast('Department updated.', 'success'); closeModal(); loadDepartments(); }
  else { const d = await res.json(); toast(JSON.stringify(d.errors || d.message), 'error'); }
}

async function deleteDept(id) {
  if (!confirm('Delete this department?')) return;
  const res = await api(`${API}/departments/${id}/`, { method: 'DELETE' });
  if (res.ok) { toast('Department deleted.', 'success'); loadDepartments(); }
  else { const d = await res.json(); toast(d.message || 'Error.', 'error'); }
}

// ── DESIGNATIONS ──────────────────────────────────────────────────────────
async function loadDesignations() {
  document.getElementById('topbar-actions').innerHTML = `<button class="btn btn-primary btn-sm" onclick="openCreateDesig()">+ Add Designation</button>`;
  const res = await api(`${API}/designations/`);
  const desigs = (await res.json()).data || [];
  if (!desigs.length) { document.getElementById('page-content').innerHTML = `<div class="empty"><div class="empty-icon">🏷️</div><p>No designations found.</p></div>`; return; }
  const rows = desigs.map(d => `
    <tr>
      <td><strong>${d.name}</strong></td>
      <td>${d.code || '—'}</td>
      <td>${d.description || '—'}</td>
      <td><span class="badge badge-${d.is_active ? 'active' : 'inactive'}">${d.is_active ? 'Active' : 'Inactive'}</span></td>
      <td>
        <button class="btn btn-outline btn-sm" onclick="editDesig(${d.id}, '${d.name}', '${d.code||''}', '${d.description||''}')">Edit</button>
        <button class="btn btn-danger btn-sm" onclick="deleteDesig(${d.id})">Delete</button>
      </td>
    </tr>`).join('');
  document.getElementById('page-content').innerHTML = `
    <div class="card">
      <div class="card-header"><h3>Designations (${desigs.length})</h3></div>
      <div class="table-wrap"><table><thead><tr><th>Name</th><th>Code</th><th>Description</th><th>Status</th><th></th></tr></thead><tbody>${rows}</tbody></table></div>
    </div>`;
}

function openCreateDesig() {
  document.getElementById('modal-title').textContent = 'Add Designation';
  document.getElementById('modal-body').innerHTML = `
    <div class="form-group"><label>Name</label><input id="dg-name" placeholder="Senior Engineer" /></div>
    <div class="form-group" style="margin-top:1rem"><label>Code</label><input id="dg-code" placeholder="SE" /></div>
    <div class="form-group" style="margin-top:1rem"><label>Description</label><textarea id="dg-desc" placeholder="Description"></textarea></div>`;
  document.getElementById('modal-footer').innerHTML = `<button class="btn btn-outline btn-sm" onclick="closeModal()">Cancel</button><button class="btn btn-primary btn-sm" onclick="createDesig()">Create</button>`;
  openModal();
}

async function createDesig() {
  const body = { name: document.getElementById('dg-name').value, code: document.getElementById('dg-code').value, description: document.getElementById('dg-desc').value };
  const res = await api(`${API}/designations/`, { method: 'POST', body: JSON.stringify(body) });
  const data = await res.json();
  if (res.ok) { toast('Designation created.', 'success'); closeModal(); loadDesignations(); }
  else { toast(JSON.stringify(data.errors || data.message), 'error'); }
}

function editDesig(id, name, code, desc) {
  document.getElementById('modal-title').textContent = 'Edit Designation';
  document.getElementById('modal-body').innerHTML = `
    <div class="form-group"><label>Name</label><input id="dg-name" value="${name}" /></div>
    <div class="form-group" style="margin-top:1rem"><label>Code</label><input id="dg-code" value="${code}" /></div>
    <div class="form-group" style="margin-top:1rem"><label>Description</label><textarea id="dg-desc">${desc}</textarea></div>`;
  document.getElementById('modal-footer').innerHTML = `<button class="btn btn-outline btn-sm" onclick="closeModal()">Cancel</button><button class="btn btn-primary btn-sm" onclick="updateDesig(${id})">Save</button>`;
  openModal();
}

async function updateDesig(id) {
  const body = { name: document.getElementById('dg-name').value, code: document.getElementById('dg-code').value, description: document.getElementById('dg-desc').value };
  const res = await api(`${API}/designations/${id}/`, { method: 'PATCH', body: JSON.stringify(body) });
  if (res.ok) { toast('Designation updated.', 'success'); closeModal(); loadDesignations(); }
  else { const d = await res.json(); toast(JSON.stringify(d.errors || d.message), 'error'); }
}

async function deleteDesig(id) {
  if (!confirm('Delete this designation?')) return;
  const res = await api(`${API}/designations/${id}/`, { method: 'DELETE' });
  if (res.ok) { toast('Designation deleted.', 'success'); loadDesignations(); }
  else { const d = await res.json(); toast(d.message || 'Error.', 'error'); }
}

// ── TRANSFERS ─────────────────────────────────────────────────────────────
async function loadTransfers() {
  document.getElementById('topbar-actions').innerHTML = `<button class="btn btn-primary btn-sm" onclick="openCreateTransfer()">+ Initiate Transfer</button>`;
  const res = await api(`${API}/employee-transfers/`);
  const transfers = (await res.json()).data || [];
  if (!transfers.length) { document.getElementById('page-content').innerHTML = `<div class="empty"><div class="empty-icon">🔄</div><p>No transfers found.</p></div>`; return; }
  const rows = transfers.map(t => `
    <tr>
      <td><strong>#${t.id}</strong></td>
      <td>${t.employee_name || '—'} <small style="color:var(--text-muted)">${t.employee_code || ''}</small></td>
      <td>${t.from_office_name || '—'}</td>
      <td>${t.to_office_name || '—'}</td>
      <td>${t.transfer_date || '—'}</td>
      <td><span class="badge badge-${(t.status||'').toLowerCase()}">${t.status || '—'}</span></td>
      <td>
        ${t.status === 'PENDING' ? `<button class="btn btn-success btn-sm" onclick="updateTransferStatus(${t.id}, 'APPROVED')">Approve</button> <button class="btn btn-danger btn-sm" onclick="updateTransferStatus(${t.id}, 'REJECTED')">Reject</button>` : ''}
        ${t.status === 'APPROVED' ? `<button class="btn btn-primary btn-sm" onclick="updateTransferStatus(${t.id}, 'COMPLETED')">Complete</button>` : ''}
      </td>
    </tr>`).join('');
  document.getElementById('page-content').innerHTML = `
    <div class="card">
      <div class="card-header"><h3>Employee Transfers (${transfers.length})</h3></div>
      <div class="table-wrap"><table><thead><tr><th>#</th><th>Employee</th><th>From</th><th>To</th><th>Date</th><th>Status</th><th>Actions</th></tr></thead><tbody>${rows}</tbody></table></div>
    </div>`;
}

async function openCreateTransfer() {
  const [empRes, offRes] = await Promise.all([api(`${API}/employees/`), api(`${API}/offices/`)]);
  const employees = (await empRes.json()).data || [];
  const offices = (await offRes.json()).data || [];
  const empOpts = employees.map(e => `<option value="${e.id}">${e.full_name} (${e.employee_id})</option>`).join('');
  const offOpts = offices.map(o => `<option value="${o.id}">${o.name}</option>`).join('');
  document.getElementById('modal-title').textContent = 'Initiate Transfer';
  document.getElementById('modal-body').innerHTML = `
    <div class="form-grid">
      <div class="form-group"><label>Employee</label><select id="tf-emp"><option value="">Select employee</option>${empOpts}</select></div>
      <div class="form-group"><label>To Office</label><select id="tf-tooff"><option value="">Select office</option>${offOpts}</select></div>
      <div class="form-group"><label>Transfer Date</label><input type="date" id="tf-date" /></div>
      <div class="form-group"><label>Order Number</label><input id="tf-order" placeholder="ORD-2025-001" /></div>
    </div>
    <div class="form-group" style="margin-top:1rem"><label>Reason</label><textarea id="tf-reason" placeholder="Reason for transfer"></textarea></div>`;
  document.getElementById('modal-footer').innerHTML = `<button class="btn btn-outline btn-sm" onclick="closeModal()">Cancel</button><button class="btn btn-primary btn-sm" onclick="createTransfer()">Initiate</button>`;
  openModal();
}

async function createTransfer() {
  const body = { employee: document.getElementById('tf-emp').value, to_office: document.getElementById('tf-tooff').value, transfer_date: document.getElementById('tf-date').value, order_number: document.getElementById('tf-order').value, reason: document.getElementById('tf-reason').value };
  const res = await api(`${API}/employee-transfers/`, { method: 'POST', body: JSON.stringify(body) });
  const data = await res.json();
  if (res.ok) { toast('Transfer initiated.', 'success'); closeModal(); loadTransfers(); }
  else { toast(JSON.stringify(data.errors || data.message), 'error'); }
}

async function updateTransferStatus(id, status) {
  if (!confirm(`Set transfer #${id} to ${status}?`)) return;
  const res = await api(`${API}/employee-transfers/${id}/status/`, { method: 'PATCH', body: JSON.stringify({ status }) });
  const data = await res.json();
  if (res.ok) { toast(`Transfer ${status.toLowerCase()}.`, 'success'); loadTransfers(); }
  else { toast(data.message || 'Error.', 'error'); }
}

// ── SYSTEMS ───────────────────────────────────────────────────────────────
async function loadSystems() {
  document.getElementById('topbar-actions').innerHTML = `<button class="btn btn-primary btn-sm" onclick="openCreateSystem()">+ Add System</button>`;
  const res = await api(`${API}/employee-systems/`);
  const systems = (await res.json()).data || [];
  if (!systems.length) { document.getElementById('page-content').innerHTML = `<div class="empty"><div class="empty-icon">💻</div><p>No system records found.</p></div>`; return; }
  const rows = systems.map(s => `
    <tr>
      <td>${s.employee_name || '—'} <small style="color:var(--text-muted)">${s.employee_id || ''}</small></td>
      <td>${s.computer_name || '—'}</td>
      <td>${s.ip_address || '—'}</td>
      <td>${s.operating_system || '—'}</td>
      <td>${s.domain_username || '—'}</td>
      <td><span class="badge badge-${s.is_active ? 'active' : 'inactive'}">${s.is_active ? 'Active' : 'Inactive'}</span></td>
    </tr>`).join('');
  document.getElementById('page-content').innerHTML = `
    <div class="card">
      <div class="card-header"><h3>System Details (${systems.length})</h3></div>
      <div class="table-wrap"><table><thead><tr><th>Employee</th><th>Computer</th><th>IP Address</th><th>OS</th><th>Domain User</th><th>Status</th></tr></thead><tbody>${rows}</tbody></table></div>
    </div>`;
}

async function openCreateSystem() {
  const empRes = await api(`${API}/employees/`);
  const employees = (await empRes.json()).data || [];
  const empOpts = employees.map(e => `<option value="${e.id}">${e.full_name} (${e.employee_id})</option>`).join('');
  document.getElementById('modal-title').textContent = 'Add System Details';
  document.getElementById('modal-body').innerHTML = `
    <div class="form-grid">
      <div class="form-group"><label>Employee</label><select id="sf-emp"><option value="">Select</option>${empOpts}</select></div>
      <div class="form-group"><label>Computer Name</label><input id="sf-computer" placeholder="PC-001" /></div>
      <div class="form-group"><label>IP Address</label><input id="sf-ip" placeholder="192.168.1.1" /></div>
      <div class="form-group"><label>MAC Address</label><input id="sf-mac" placeholder="AA:BB:CC:DD:EE:FF" /></div>
      <div class="form-group"><label>OS</label><select id="sf-os"><option value="">Select</option><option value="WINDOWS">Windows</option><option value="LINUX">Linux</option><option value="MACOS">macOS</option><option value="OTHER">Other</option></select></div>
      <div class="form-group"><label>Domain Username</label><input id="sf-domain" placeholder="domain\\user" /></div>
    </div>`;
  document.getElementById('modal-footer').innerHTML = `<button class="btn btn-outline btn-sm" onclick="closeModal()">Cancel</button><button class="btn btn-primary btn-sm" onclick="createSystem()">Add</button>`;
  openModal();
}

async function createSystem() {
  const body = { employee: document.getElementById('sf-emp').value, computer_name: document.getElementById('sf-computer').value, ip_address: document.getElementById('sf-ip').value, mac_address: document.getElementById('sf-mac').value, operating_system: document.getElementById('sf-os').value, domain_username: document.getElementById('sf-domain').value };
  const res = await api(`${API}/employee-systems/`, { method: 'POST', body: JSON.stringify(body) });
  const data = await res.json();
  if (res.ok) { toast('System details added.', 'success'); closeModal(); loadSystems(); }
  else { toast(JSON.stringify(data.errors || data.message), 'error'); }
}

// ── MODAL ─────────────────────────────────────────────────────────────────
function openModal() { document.getElementById('modal').classList.add('open'); }
function closeModal() { document.getElementById('modal').classList.remove('open'); }
document.getElementById('modal').addEventListener('click', function(e) { if (e.target === this) closeModal(); });

// ── TOAST ─────────────────────────────────────────────────────────────────
function toast(msg, type = 'info') {
  const el = document.createElement('div');
  el.className = `toast-item toast-${type}`;
  el.textContent = msg;
  document.getElementById('toast').appendChild(el);
  setTimeout(() => el.remove(), 3500);
}

// ── INIT ──────────────────────────────────────────────────────────────────
document.getElementById('login-password').addEventListener('keydown', e => { if (e.key === 'Enter') login(); });
if (TOKEN && currentUser) {
  document.getElementById('auth-screen').style.display = 'none';
  document.getElementById('app').style.display = 'flex';
  const name = (currentUser.first_name || '') + ' ' + (currentUser.last_name || '');
  document.getElementById('user-name').textContent = name.trim() || currentUser.username;
  document.getElementById('user-role').textContent = currentUser.role || 'User';
  document.getElementById('user-avatar').textContent = (name.trim()[0] || currentUser.username[0] || '?').toUpperCase();
  showPage('dashboard');
}
</script>
</body>
</html>"""

def index(request):
    return HttpResponse(HTML, content_type='text/html')