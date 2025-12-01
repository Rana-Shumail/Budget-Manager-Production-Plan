/**
 * BudBuddy Logic Controller
 * Handles Auth, Data Storage, Goals, Budgets, and Expenses
 */

// CONFIGURATION
const API_URL = 'https://budbuddy-api.onrender.com'; 
const KEY_CURRENT_USER = 'budbuddy_current_user';

// --- AUTHENTICATION ---

async function registerUser(username, email, password) {
    try {
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }) 
        });
        const result = await response.json();
        if (response.ok) return true;
        else { alert(result.message); return false; }
    } catch (error) { console.error(error); return false; }
}

async function loginUser(username, password, rememberMe) {
    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const result = await response.json();
        if (response.ok && result.success) {
            localStorage.setItem(KEY_CURRENT_USER, username);
            if (rememberMe) localStorage.setItem('budbuddy_remembered', username);
            else localStorage.removeItem('budbuddy_remembered');
            return true;
        }
        return false;
    } catch (error) { console.error(error); return false; }
}

function logout() {
    localStorage.removeItem(KEY_CURRENT_USER);
    window.location.href = 'index.html';
}

// --- DATA LOADING FUNCTIONS ---

async function loadGoalsFromCloud() {
    const currentUser = localStorage.getItem(KEY_CURRENT_USER);
    const container = document.getElementById('goalsContainer');
    if (!container) return;

    // Load Stats as well
    loadStats();

    try {
        const response = await fetch(`${API_URL}/goals?username=${currentUser}`);
        const goals = await response.json();
        container.innerHTML = '';

        if (goals.length === 0) container.innerHTML = '<p style="color:#666; text-align:center;">No goals yet.</p>';

        goals.forEach(goal => {
            const percent = goal.target > 0 ? Math.min(100, Math.round((goal.current / goal.target) * 100)) : 0;
            const html = `
                <div class="item-card">
                    <div style="flex-grow:1; margin-right:20px;">
                        <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                            <span style="font-weight:600;">${goal.title}</span>
                            <span style="color:var(--primary);">${percent}%</span>
                        </div>
                        <div class="progress-bg"><div class="progress-fill" style="width: ${percent}%"></div></div>
                        <div style="display:flex; justify-content:space-between; font-size:0.8rem; color:#888; margin-top:5px;">
                            <span>$${goal.current} / $${goal.target}</span><span>Due: ${goal.date}</span>
                        </div>
                    </div>
                    <button onclick='openEditModal(${JSON.stringify(goal)})' style="background:none; border:none; color:#666; cursor:pointer; font-size:1.2rem;"><i class='bx bxs-pencil'></i></button>
                </div>`;
            container.insertAdjacentHTML('beforeend', html);
        });
    } catch (error) { console.error(error); }
}

async function loadStats() {
    const currentUser = localStorage.getItem(KEY_CURRENT_USER);
    try {
        const response = await fetch(`${API_URL}/stats?username=${currentUser}`);
        const stats = await response.json();
        
        // 1. Total Balance Card (Now shows Remaining Budget)
        if(document.getElementById('totalBalance')) {
            document.getElementById('totalBalance').textContent = stats.remaining_balance.toFixed(2);
            
            // Optional: Turn red if balance is negative
            const card = document.getElementById('totalBalance').parentElement.parentElement;
            if (stats.remaining_balance < 0) {
                document.getElementById('totalBalance').style.color = '#ff4d4d';
            } else {
                document.getElementById('totalBalance').style.color = 'var(--text)';
            }
        }

        // 2. Monthly Budget Card
        if(document.getElementById('monthlyBudget')) {
            document.getElementById('monthlyBudget').textContent = stats.total_budget.toFixed(2);
        }

        // 3. Total Expenses Card (Now actually works!)
        if(document.getElementById('totalExpenses')) {
            document.getElementById('totalExpenses').textContent = stats.total_expenses.toFixed(2);
        }

    } catch (e) { console.error("Error loading stats:", e); }
}

async function loadBudgets() {
    const currentUser = localStorage.getItem(KEY_CURRENT_USER);
    const container = document.getElementById('budgetsContainer');
    if (!container) return;

    try {
        const response = await fetch(`${API_URL}/budgets?username=${currentUser}`);
        const budgets = await response.json();
        container.innerHTML = '';
        let totalLimit = 0;

        if (budgets.length === 0) container.innerHTML = '<p style="color:#666;">No budgets found.</p>';

        budgets.forEach(b => {
            totalLimit += b.limit;
            const percent = b.limit > 0 ? Math.min(100, Math.round((b.spent / b.limit) * 100)) : 0;
            const barColor = b.remaining < 0 ? '#ff4d4d' : 'var(--primary)';

            const html = `
                <div class="card" style="display:flex; flex-direction:column; gap:15px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h2 style="color:white;">${b.category}</h2>
                        <button onclick="deleteBudget(${b.id})" style="color:#444; background:none; border:none; cursor:pointer;"><i class='bx bxs-trash'></i></button>
                    </div>
                    <div style="display:flex; justify-content:space-between; font-size:1.1rem;">
                        <span style="color:#888;">Limit: $${b.limit}</span>
                        <span style="color:#ff4d4d;">Spent: $${b.spent}</span>
                        <span style="color:${barColor}; font-weight:bold;">Left: $${b.remaining}</span>
                    </div>
                    <div class="progress-bg"><div class="progress-fill" style="width: ${percent}%; background-color:${barColor};"></div></div>
                    <div style="border-top:1px solid #333; padding-top:15px; margin-top:5px;">
                        <button onclick="openExpenseModal(${b.id})" style="width:100%; padding:10px; background:#333; color:white; border:none; border-radius:8px; cursor:pointer;">+ Add Expense</button>
                    </div>
                </div>`;
            container.insertAdjacentHTML('beforeend', html);
        });
        const totalDisplay = document.getElementById('totalBudgetDisplay');
        if (totalDisplay) totalDisplay.textContent = totalLimit.toFixed(2);
    } catch (error) { console.error(error); }
}

// --- HELPER FUNCTIONS ---

async function deleteBudget(id) {
    if(!confirm('Delete this budget?')) return;
    await fetch(`${API_URL}/delete_budget?id=${id}`, { method: 'DELETE' });
    loadBudgets();
}

window.openEditModal = function(goal) {
    const modal = document.getElementById('newGoalModal');
    const form = document.getElementById('addGoalForm');
    document.getElementById('goalTitle').value = goal.title;
    document.getElementById('goalTarget').value = goal.target;
    document.getElementById('goalCurrent').value = goal.current;
    document.getElementById('goalDate').value = goal.date;
    form.dataset.id = goal.id; 
    form.querySelector('button[type="submit"]').textContent = "Update Goal";
    modal.style.display = 'flex';
}

window.openExpenseModal = function(budgetID) {
    document.getElementById('expenseBudgetID').value = budgetID;
    document.getElementById('newExpenseModal').style.display = 'flex';
}

// --- NEW FUNCTION: LOAD FULL GOALS PAGE ---
async function loadFullGoalsPage() {
    const currentUser = localStorage.getItem(KEY_CURRENT_USER);
    const container = document.getElementById('fullGoalsContainer');
    if (!container) return; // Only runs on goals.html

    try {
        const response = await fetch(`${API_URL}/goals?username=${currentUser}`);
        const goals = await response.json();
        container.innerHTML = '';

        if (goals.length === 0) {
            container.innerHTML = '<p style="color:#666; grid-column: 1/-1; text-align:center;">No goals found. Click + to add one!</p>';
            return;
        }

        goals.forEach(goal => {
            const percent = goal.target > 0 ? Math.min(100, Math.round((goal.current / goal.target) * 100)) : 0;
            
            // Calculate Days Left
            const today = new Date();
            const due = new Date(goal.date);
            const diffTime = Math.ceil((due - today) / (1000 * 60 * 60 * 24)); 
            const daysLeft = diffTime > 0 ? diffTime : 0;
            const daysText = diffTime > 0 ? `${diffTime} days left` : "Due today or passed";

            // Calculate Amount Needed
            const remaining = goal.target - goal.current;
            
            const html = `
                <div class="goal-card-large">
                    <div style="display:flex; justify-content:space-between; align-items:start;">
                        <div class="goal-icon"><i class='bx bxs-trophy'></i></div>
                        <button onclick='openEditModal(${JSON.stringify(goal)})' style="background:none; border:none; color:#666; cursor:pointer; font-size:1.2rem;"><i class='bx bxs-pencil'></i></button>
                    </div>
                    
                    <h3 style="font-size:1.2rem; margin-bottom:5px;">${goal.title}</h3>
                    <p style="color:#888; font-size:0.9rem;">Target: $${goal.target}</p>

                    <div class="progress-container">
                        <div class="progress-bar" style="width: ${percent}%"></div>
                    </div>

                    <div class="goal-stat-row">
                        <span>Saved</span>
                        <span class="goal-stat-val" style="color:var(--primary);">$${goal.current} (${percent}%)</span>
                    </div>
                    <div class="goal-stat-row">
                        <span>Remaining</span>
                        <span class="goal-stat-val">$${remaining.toFixed(2)}</span>
                    </div>
                    <div style="margin-top:15px; padding-top:15px; border-top:1px solid rgba(255,255,255,0.1); font-size:0.85rem; color:#888; display:flex; align-items:center;">
                        <i class='bx bxs-time-five' style="margin-right:5px;"></i> ${daysText}
                    </div>
                </div>
            `;
            container.insertAdjacentHTML('beforeend', html);
        });

    } catch (error) { console.error(error); }
}

// --- REPORTS PAGE LOGIC ---
// We use an array to track chart instances so we can destroy them on reload
let chartInstances = []; 

async function loadReports() {
    const currentUser = localStorage.getItem(KEY_CURRENT_USER);
    const container = document.getElementById('reportsGrid');
    if (!container) return;

    try {
        const response = await fetch(`${API_URL}/budgets?username=${currentUser}`);
        const budgets = await response.json();

        container.innerHTML = ''; // Clear "Loading..." message
        
        // Clean up old charts to prevent memory leaks/glitches
        chartInstances.forEach(chart => chart.destroy());
        chartInstances = [];

        if (budgets.length === 0) {
            container.innerHTML = '<p style="grid-column: 1/-1; text-align:center; color:#666;">No budgets found. Create one to see analytics.</p>';
            return;
        }

        budgets.forEach((b, index) => {
            // Calculate math
            const spent = b.spent;
            // If over budget, remaining is 0 (visually), otherwise it's the difference
            const remaining = Math.max(0, b.limit - b.spent);
            
            // Determine colors
            // If over budget: Full Red. If safe: Neon Green + Dark Gray
            const isOver = b.spent > b.limit;
            const spentColor = isOver ? '#ff0000' : '#ff4d4d'; // Bright red if over, soft red if normal
            const remainingColor = '#aeff00'; // Neon Green
            
            // Create Card HTML
            const cardId = `chartCanvas_${index}`;
            const html = `
                <div class="chart-card">
                    <div class="chart-title">${b.category}</div>
                    <div class="chart-subtitle">
                        Spent $${spent} / $${b.limit}
                    </div>
                    <div class="canvas-wrapper">
                        <canvas id="${cardId}"></canvas>
                    </div>
                </div>
            `;
            container.insertAdjacentHTML('beforeend', html);

            // Generate Chart immediately after injecting HTML
            const ctx = document.getElementById(cardId).getContext('2d');
            const newChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Spent', 'Remaining'],
                    datasets: [{
                        data: [spent, remaining],
                        backgroundColor: [spentColor, remainingColor],
                        borderWidth: 0,
                        hoverOffset: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '70%', // Thinner ring for futuristic look
                    plugins: {
                        legend: { display: false }, // Hide legend for cleaner look
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return ` $${context.raw}`;
                                }
                            }
                        }
                    }
                }
            });
            chartInstances.push(newChart);
        });

    } catch (error) {
        console.error('Error loading reports:', error);
        container.innerHTML = '<p style="color:red;">Error loading data.</p>';
    }
}

// --- EVENT LISTENERS ---

document.addEventListener('DOMContentLoaded', () => {
    
    // 1. LOGIN
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        const remembered = localStorage.getItem('budbuddy_remembered');
        if (remembered) {
            document.getElementById('username').value = remembered;
            document.getElementById('rememberMe').checked = true;
        }
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const success = await loginUser(document.getElementById('username').value, document.getElementById('password').value, document.getElementById('rememberMe').checked);
            if (success) window.location.href = 'dashboard.html';
            else alert('Invalid Username or Password');
        });
    }

    // 2. SIGNUP
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const p = document.getElementById('newPassword').value;
            if (p !== document.getElementById('confirmPassword').value) { alert('Passwords do not match!'); return; }
            const success = await registerUser(document.getElementById('newUsername').value, document.getElementById('email').value, p);
            if (success) { alert('Account created!'); window.location.href = 'index.html'; }
        });
    }

    // 3. DASHBOARD (GOALS)
    if (window.location.pathname.includes('dashboard.html')) {
        const currentUser = localStorage.getItem(KEY_CURRENT_USER);
        if (!currentUser) window.location.href = 'index.html';
        else {
            if(document.getElementById('userDisplay')) document.getElementById('userDisplay').textContent = currentUser;
            loadGoalsFromCloud();
        }

        const addGoalForm = document.getElementById('addGoalForm');
        if (addGoalForm) {
            addGoalForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const goalId = e.target.dataset.id;
                const goalData = {
                    id: goalId,
                    username: currentUser,
                    title: document.getElementById('goalTitle').value,
                    target: document.getElementById('goalTarget').value,
                    current: document.getElementById('goalCurrent').value,
                    date: document.getElementById('goalDate').value
                };
                const endpoint = goalId ? '/edit_goal' : '/add_goal';
                const method = goalId ? 'PUT' : 'POST';
                await fetch(`${API_URL}${endpoint}`, { method: method, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(goalData) });
                loadGoalsFromCloud();
                document.getElementById('newGoalModal').style.display = 'none';
                addGoalForm.reset();
                delete addGoalForm.dataset.id;
                addGoalForm.querySelector('button[type="submit"]').textContent = "Save Goal";
            });
        }
    }

    // 4. BUDGETS PAGE
    if (document.getElementById('budgetsContainer')) {
        const currentUser = localStorage.getItem(KEY_CURRENT_USER);
        if (!currentUser) window.location.href = 'index.html';
        else {
            if(document.getElementById('userDisplay')) document.getElementById('userDisplay').textContent = currentUser;
            loadBudgets();
        }

        const addBudgetForm = document.getElementById('addBudgetForm');
        if (addBudgetForm) {
            addBudgetForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                await fetch(`${API_URL}/add_budget`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        username: currentUser,
                        category: document.getElementById('budgetCategory').value,
                        amount: document.getElementById('budgetAmount').value
                    })
                });
                loadBudgets();
                document.getElementById('newBudgetModal').style.display = 'none';
                addBudgetForm.reset();
            });
        }

        const addExpenseForm = document.getElementById('addExpenseForm');
        if (addExpenseForm) {
            addExpenseForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                await fetch(`${API_URL}/add_expense`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        budget_id: document.getElementById('expenseBudgetID').value,
                        description: document.getElementById('expenseDesc').value,
                        amount: document.getElementById('expenseAmount').value,
                        date: document.getElementById('expenseDate').value
                    })
                });
                loadBudgets();
                document.getElementById('newExpenseModal').style.display = 'none';
                addExpenseForm.reset();
            });
        }
    }

// 5. GOALS PAGE LOGIC
    if (document.getElementById('fullGoalsContainer')) {
        const currentUser = localStorage.getItem(KEY_CURRENT_USER);
        if (!currentUser) window.location.href = 'index.html';
        else {
            if(document.getElementById('userDisplay')) document.getElementById('userDisplay').textContent = currentUser;
            loadFullGoalsPage(); // Load the big cards
        }

        // Re-use the Goal Form logic for this page too
        const addGoalForm = document.getElementById('addGoalForm');
        if (addGoalForm) {
            addGoalForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const goalId = e.target.dataset.id;
                const goalData = {
                    id: goalId,
                    username: currentUser,
                    title: document.getElementById('goalTitle').value,
                    target: document.getElementById('goalTarget').value,
                    current: document.getElementById('goalCurrent').value,
                    date: document.getElementById('goalDate').value
                };
                const endpoint = goalId ? '/edit_goal' : '/add_goal';
                const method = goalId ? 'PUT' : 'POST';
                
                await fetch(`${API_URL}${endpoint}`, { method: method, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(goalData) });
                
                loadFullGoalsPage(); // Refresh the BIG cards
                document.getElementById('newGoalModal').style.display = 'none';
                addGoalForm.reset();
                delete addGoalForm.dataset.id;
                addGoalForm.querySelector('button[type="submit"]').textContent = "Save Goal";
            });
        }
    }

// 6. REPORTS PAGE
    if (window.location.pathname.includes('reports.html')) {
        const currentUser = localStorage.getItem(KEY_CURRENT_USER);
        if (!currentUser) window.location.href = 'index.html';
        else {
            if(document.getElementById('userDisplay')) document.getElementById('userDisplay').textContent = currentUser;
            loadReports(); // Draw the chart
        }
    }
});
