// Community Skill Swap - Main JavaScript File

// API Configuration - Updated to port 8000
const API_BASE_URL = 'http://127.0.0.1:8000';

// DOM Elements
let currentUser = null;
let authToken = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    checkAuthStatus();
    setupEventListeners();
});

// Check if user is authenticated
function checkAuthStatus() {
    authToken = localStorage.getItem('authToken');
    const userData = localStorage.getItem('currentUser');
    
    if (authToken && userData) {
        currentUser = JSON.parse(userData);
        updateUIForAuthenticatedUser();
    } else {
        updateUIForUnauthenticatedUser();
    }
}

// Update UI for authenticated users
function updateUIForAuthenticatedUser() {
    // Update user name in dashboard
    const userNameElement = document.getElementById('user-name');
    if (userNameElement && currentUser) {
        userNameElement.textContent = currentUser.full_name || currentUser.username;
    }
    
    // Load dashboard data if on dashboard page
    if (window.location.pathname.includes('dashboard.html')) {
        loadDashboardData();
    }
    
    // Load skills if on skills page
    if (window.location.pathname.includes('skills.html')) {
        loadSkills();
    }
}

// Update UI for unauthenticated users
function updateUIForUnauthenticatedUser() {
    // Redirect to login if trying to access protected pages
    if (window.location.pathname !== '/login.html' && 
        window.location.pathname !== '/register.html' && 
        !window.location.pathname.endsWith('/')) {
        window.location.href = 'login.html';
    }
}

// Setup event listeners
function setupEventListeners() {
    // Login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    // Register form
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
    
    // Add skill form
    const addSkillForm = document.getElementById('addSkillForm');
    if (addSkillForm) {
        addSkillForm.addEventListener('submit', handleAddSkill);
    }
}

// Handle user login
async function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorElement = document.getElementById('error-message');
    
    try {
        const response = await fetch(`${API_BASE_URL}/users/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Store authentication data
            localStorage.setItem('authToken', data.access_token);
            localStorage.setItem('currentUser', JSON.stringify({
                username: username,
                full_name: username // Will be updated from user profile
            }));
            
            // Redirect to dashboard
            window.location.href = 'dashboard.html';
        } else {
            showError(errorElement, data.detail || 'Login failed');
        }
    } catch (error) {
        showError(errorElement, 'Network error. Please try again.');
    }
}

// Handle user registration
async function handleRegister(event) {
    event.preventDefault();
    
    const formData = {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        full_name: document.getElementById('full_name').value,
        password: document.getElementById('password').value,
        bio: document.getElementById('bio').value
    };
    
    const errorElement = document.getElementById('error-message');
    
    try {
        const response = await fetch(`${API_BASE_URL}/users/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showSuccess(errorElement, 'Registration successful! Please login.');
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
        } else {
            showError(errorElement, data.detail || 'Registration failed');
        }
    } catch (error) {
        showError(errorElement, 'Network error. Please try again.');
    }
}

// Handle adding a new skill
async function handleAddSkill(event) {
    event.preventDefault();
    
    const formData = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        category: document.getElementById('category').value,
        proficiency_level: document.getElementById('proficiency_level').value,
        value: parseInt(document.getElementById('value').value) || 0
    };
    
    const errorElement = document.getElementById('error-message');
    
    try {
        const response = await makeAuthenticatedRequest(`${API_BASE_URL}/skills/`, {
            method: 'POST',
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showSuccess(errorElement, 'Skill added successfully!');
            setTimeout(() => {
                window.location.href = 'skills.html';
            }, 2000);
        } else {
            showError(errorElement, data.detail || 'Failed to add skill');
        }
    } catch (error) {
        showError(errorElement, 'Network error. Please try again.');
    }
}

// Load dashboard data
async function loadDashboardData() {
    try {
        // Load user stats
        await Promise.all([
            loadUserStats(),
            loadNotifications()
        ]);
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

// Load user statistics
async function loadUserStats() {
    try {
        const [skillsResponse, requestsResponse] = await Promise.all([
            makeAuthenticatedRequest(`${API_BASE_URL}/skills/my-skills`),
            makeAuthenticatedRequest(`${API_BASE_URL}/exchanges/`)
        ]);
        
        const skills = await skillsResponse.json();
        const requests = await requestsResponse.json();
        
        document.getElementById('skills-count').textContent = skills.length;
        document.getElementById('requests-count').textContent = requests.length;
    } catch (error) {
        console.error('Error loading user stats:', error);
    }
}

// Load notifications
async function loadNotifications() {
    try {
        const response = await makeAuthenticatedRequest(`${API_BASE_URL}/notifications/`);
        const notifications = await response.json();
        
        const notificationsList = document.getElementById('notifications-list');
        
        if (notifications.length === 0) {
            notificationsList.innerHTML = '<p class="no-data">No notifications yet</p>';
            return;
        }
        
        notificationsList.innerHTML = notifications.map(notification => `
            <div class="notification-item ${!notification.is_read ? 'unread' : ''}">
                <div class="notification-title">${notification.title}</div>
                <div class="notification-message">${notification.message}</div>
                <div class="notification-time">${formatDate(notification.created_at)}</div>
            </div>
        `).join('');
        
        // Update unread count
        const unreadCount = notifications.filter(n => !n.is_read).length;
        document.getElementById('notifications-count').textContent = unreadCount;
        
    } catch (error) {
        console.error('Error loading notifications:', error);
    }
}

// Load skills
async function loadSkills() {
    const skillsGrid = document.getElementById('skills-grid');
    skillsGrid.innerHTML = '<div class="loading">Loading skills...</div>';
    
    try {
        const response = await makeAuthenticatedRequest(`${API_BASE_URL}/skills/`);
        const skills = await response.json();
        
        if (skills.length === 0) {
            skillsGrid.innerHTML = '<p class="no-data">No skills available yet</p>';
            return;
        }
        
        skillsGrid.innerHTML = skills.map(skill => `
            <div class="skill-card">
                <h3 class="skill-title">${skill.title}</h3>
                <p class="skill-description">${skill.description}</p>
                <div class="skill-meta">
                    <span class="skill-category">${skill.category}</span>
                    <span class="skill-proficiency">${skill.proficiency_level}</span>
                    ${skill.value ? `<span class="skill-value">Value: ${skill.value}</span>` : ''}
                </div>
                <div class="skill-owner">
                    Offered by: ${skill.owner ? (skill.owner.full_name || skill.owner.username) : 'Unknown'}
                </div>
                <div class="skill-actions">
                    <button onclick="requestSkillExchange(${skill.id})" class="btn btn-primary btn-small">
                        Request Exchange
                    </button>
                </div>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Error loading skills:', error);
        skillsGrid.innerHTML = '<p class="error-message">Error loading skills. Please check your login status.</p>';
    }
}

// Request skill exchange
async function requestSkillExchange(skillId) {
    if (!authToken) {
        window.location.href = 'login.html';
        return;
    }
    
    const message = prompt('What would you like to learn from this skill?');
    if (!message) return;
    
    try {
        const response = await makeAuthenticatedRequest(`${API_BASE_URL}/exchanges/`, {
            method: 'POST',
            body: JSON.stringify({
                skill_id: skillId,
                message: message
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('Exchange request sent successfully!');
        } else {
            alert(data.detail || 'Failed to send exchange request');
        }
    } catch (error) {
        alert('Network error. Please try again.');
    }
}

// Make authenticated API request
async function makeAuthenticatedRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`
        }
    };
    
    const mergedOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers
        }
    };
    
    return fetch(url, mergedOptions);
}

// Show error message
function showError(element, message) {
    if (element) {
        element.textContent = message;
        element.className = 'error-message';
        element.style.display = 'block';
    }
}

// Show success message
function showSuccess(element, message) {
    if (element) {
        element.textContent = message;
        element.className = 'success-message';
        element.style.display = 'block';
    }
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// Logout function
function logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    window.location.href = 'login.html';
}
