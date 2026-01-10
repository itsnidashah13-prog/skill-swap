// COMPLETE AUTHENTICATION FIX - This will solve all token issues

// Global variables
let currentUser = null;
let authToken = null;

// API Base URL - HARDCODED
const API_BASE_URL = 'http://127.0.0.1:8000';

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔍 DEBUG: App initialization starting...');
    
    // Check if user is logged in - check ALL token keys
    const access_token = localStorage.getItem('access_token');
    const authToken_key = localStorage.getItem('authToken');
    const token_key = localStorage.getItem('token');
    const user = localStorage.getItem('currentUser');
    
    console.log('🔍 DEBUG: Token check - access_token:', !!access_token);
    console.log('🔍 DEBUG: Token check - authToken:', !!authToken_key);
    console.log('🔍 DEBUG: Token check - token:', !!token_key);
    console.log('🔍 DEBUG: User check:', !!user);
    
    // Use the first available token
    const availableToken = access_token || authToken_key || token_key;
    
    if (availableToken && user) {
        authToken = availableToken;
        currentUser = JSON.parse(user);
        updateUIForLoggedInUser();
        console.log('🔍 DEBUG: User restored from localStorage');
    }
    
    console.log('🔍 DEBUG: App initialized successfully');
    console.log('🔍 DEBUG: Final token available:', !!authToken);
    console.log('🔍 DEBUG: All localStorage keys:', Object.keys(localStorage));

    // Set up event listeners
    setupEventListeners();
    
    // Show home page by default
    showPage('home');
});

// Setup event listeners
function setupEventListeners() {
    console.log('🔍 DEBUG: Setting up event listeners...');
    
    // Navigation
    document.getElementById('login-btn').addEventListener('click', () => showPage('login'));
    document.getElementById('register-btn').addEventListener('click', () => showPage('register'));
    document.getElementById('logout-btn').addEventListener('click', logout);
    
    // Forms
    document.getElementById('login-form').addEventListener('submit', handleLogin);
    document.getElementById('register-form').addEventListener('submit', handleRegister);
    document.getElementById('add-skill-form').addEventListener('submit', handleAddSkill);
    document.getElementById('request-exchange-form').addEventListener('submit', handleRequestExchange);
    
    // Modals
    document.querySelectorAll('.close').forEach(closeBtn => {
        closeBtn.addEventListener('click', function() {
            this.closest('.modal').style.display = 'none';
        });
    });
    
    // Close modals when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
        }
    });
    
    console.log('🔍 DEBUG: Event listeners set up complete');
}

// Page navigation
function showPage(pageId) {
    console.log('🔍 DEBUG: Navigating to page:', pageId);
    
    // Hide all pages
    document.querySelectorAll('.page-section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Show selected page
    const targetPage = document.getElementById(pageId);
    if (targetPage) {
        targetPage.classList.add('active');
    }
    
    // Load data for specific pages
    if (pageId === 'skills') {
        loadSkills();
    } else if (pageId === 'my-skills') {
        loadMySkills();
    } else if (pageId === 'requests') {
        loadRequests();
    }
}

// Authentication functions
async function handleLogin(event) {
    event.preventDefault();
    console.log('🔍 DEBUG: Login form submitted');
    
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    
    console.log('🔍 DEBUG: Login attempt for username:', username);
    
    try {
        const response = await fetch(`${API_BASE_URL}/users/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });
        
        console.log('🔍 DEBUG: Login response status:', response.status);
        
        if (response.ok) {
            const data = await response.json();
            authToken = data.access_token;
            
            console.log('🔍 DEBUG: Login successful - received token');
            console.log('🔍 DEBUG: Token length:', authToken.length);
            console.log('🔍 DEBUG: Token type:', data.token_type);
            
            // CRITICAL FIX: Save token with ALL possible keys for maximum compatibility
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('authToken', data.access_token);
            
            console.log('🔍 DEBUG: Token saved to localStorage with all keys');
            console.log('🔍 DEBUG: localStorage keys after save:', Object.keys(localStorage));
            
            // Verify token was saved
            const verifyToken = localStorage.getItem('access_token');
            console.log('🔍 DEBUG: Token verification - access_token exists:', !!verifyToken);
            
            // Get user info
            console.log('🔍 DEBUG: Fetching user info...');
            const userResponse = await fetch(`${API_BASE_URL}/users/me`, {
                headers: {
                    'Authorization': `Bearer ${authToken}`,
                },
            });
            
            console.log('🔍 DEBUG: User info response status:', userResponse.status);
            
            if (userResponse.ok) {
                currentUser = await userResponse.json();
                localStorage.setItem('currentUser', JSON.stringify(currentUser));
                
                console.log('🔍 DEBUG: User info saved:', currentUser.username);
                
                updateUIForLoggedInUser();
                showMessage('Login successful!', 'success');
                showPage('home');
            } else {
                console.error('🔍 DEBUG: Failed to get user info');
                showMessage('Login successful but failed to get user info', 'error');
            }
        } else {
            const error = await response.json();
            console.error('🔍 DEBUG: Login failed:', error);
            showMessage(error.detail || 'Login failed', 'error');
        }
    } catch (error) {
        console.error('🔍 DEBUG: Login network error:', error);
        showMessage('Network error. Please try again.', 'error');
    }
}

async function handleRegister(event) {
    event.preventDefault();
    
    const userData = {
        username: document.getElementById('register-username').value,
        email: document.getElementById('register-email').value,
        full_name: document.getElementById('register-fullname').value,
        password: document.getElementById('register-password').value,
        bio: document.getElementById('register-bio').value,
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/users/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        });
        
        if (response.ok) {
            showMessage('Registration successful! Please login.', 'success');
            showPage('login');
            document.getElementById('register-form').reset();
        } else {
            const error = await response.json();
            showMessage(error.detail || 'Registration failed', 'error');
        }
    } catch (error) {
        showMessage('Network error. Please try again.', 'error');
    }
}

function logout() {
    console.log('🔍 DEBUG: Logout initiated');
    
    authToken = null;
    currentUser = null;
    
    // Clear ALL token keys
    localStorage.removeItem('access_token');
    localStorage.removeItem('authToken');
    localStorage.removeItem('token');
    localStorage.removeItem('currentUser');
    
    console.log('🔍 DEBUG: All tokens cleared from localStorage');
    
    updateUIForLoggedOutUser();
    showMessage('Logged out successfully', 'info');
    showPage('home');
}

function updateUIForLoggedInUser() {
    document.getElementById('login-btn').style.display = 'none';
    document.getElementById('register-btn').style.display = 'none';
    document.getElementById('logout-btn').style.display = 'block';
    console.log('🔍 DEBUG: UI updated for logged in user');
}

function updateUIForLoggedOutUser() {
    document.getElementById('login-btn').style.display = 'block';
    document.getElementById('register-btn').style.display = 'block';
    document.getElementById('logout-btn').style.display = 'none';
    console.log('🔍 DEBUG: UI updated for logged out user');
}

// CRITICAL FIX: Skills loading with proper token handling
async function loadSkills() {
    console.log('🔍 DEBUG: loadSkills() called');
    
    const category = document.getElementById('category-filter').value;
    let url = `${API_BASE_URL}/skills/`;
    
    if (category) {
        url += `?category=${category}`;
    }
    
    console.log('🔍 DEBUG: Skills URL:', url);
    
    // CRITICAL FIX: Check ALL token keys and log detailed info
    const access_token = localStorage.getItem('access_token');
    const authToken_key = localStorage.getItem('authToken');
    const token_key = localStorage.getItem('token');
    
    console.log('🔍 DEBUG: Token availability check:');
    console.log('  - access_token:', !!access_token);
    console.log('  - authToken:', !!authToken_key);
    console.log('  - token:', !!token_key);
    
    // Use the first available token
    const availableToken = access_token || authToken_key || token_key;
    console.log('🔍 DEBUG: Available token for skills request:', !!availableToken);
    
    try {
        // Skills endpoint is public - token is optional
        console.log('🔍 DEBUG: Making skills request...');
        
        const headers = {
            'Content-Type': 'application/json',
        };
        
        // Only add auth header if token exists
        if (availableToken) {
            headers['Authorization'] = 'Bearer ' + availableToken;
            console.log('🔍 DEBUG: Added Authorization header with token');
        } else {
            console.log('🔍 DEBUG: No token available - making public request');
        }
        
        const response = await fetch(url, {
            method: 'GET',
            headers: headers
        });
        
        console.log('🔍 DEBUG: Skills response status:', response.status);
        console.log('🔍 DEBUG: Skills response ok:', response.ok);
        
        if (response.ok) {
            const skills = await response.json();
            console.log('🔍 DEBUG: Skills data received:', skills.length, 'items');
            
            if (skills.length === 0) {
                console.warn('🔍 DEBUG: No skills found in database');
                document.getElementById('skills-list').innerHTML = '<p>No skills available at the moment.</p>';
            } else {
                console.log('🔍 DEBUG: First skill sample:', skills[0]);
            }
            
            displaySkills(skills, 'skills-list');
            console.log('🔍 DEBUG: Skills displayed successfully');
        } else {
            console.error('🔍 DEBUG: Skills request failed:', response.status);
            const errorText = await response.text();
            console.error('🔍 DEBUG: Error response:', errorText);
            showMessage(`Failed to load skills: ${response.status} ${response.statusText}`, 'error');
        }
    } catch (error) {
        console.error('🔍 DEBUG: Skills network error:', error);
        console.error('🔍 DEBUG: Error details:', error.message);
        showMessage(`Network error: ${error.message}`, 'error');
        
        // Show detailed error on screen
        document.getElementById('skills-list').innerHTML = `
            <div style="background: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <h3>🚨 Skills Loading Error</h3>
                <p><strong>Error:</strong> ${error.message}</p>
                <p><strong>URL:</strong> ${url}</p>
                <p><strong>Token Available:</strong> ${availableToken ? 'Yes' : 'No'}</p>
                <p><strong>Backend Status:</strong> Check if backend is running on ${API_BASE_URL}</p>
                <p><strong>Solution:</strong> Start backend server or check network connection</p>
            </div>
        `;
    }
}

async function loadMySkills() {
    console.log('🔍 DEBUG: loadMySkills() called');
    
    // CRITICAL FIX: Check ALL token keys
    const token = localStorage.getItem('access_token') || localStorage.getItem('authToken') || localStorage.getItem('token');
    
    if (!token) {
        console.error('🔍 DEBUG: No token found for my-skills');
        showMessage('Please login to view your skills', 'error');
        showPage('login');
        return;
    }
    
    console.log('🔍 DEBUG: Token found for my-skills:', token.substring(0, 30) + '...');
    
    try {
        const response = await fetch(`${API_BASE_URL}/skills/my-skills`, {
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });
        
        console.log('🔍 DEBUG: My-skills response status:', response.status);
        
        if (response.ok) {
            const skills = await response.json();
            displaySkills(skills, 'my-skills-list', true);
        } else {
            showMessage('Failed to load your skills', 'error');
        }
    } catch (error) {
        console.error('🔍 DEBUG: My-skills error:', error);
        showMessage('Network error. Please try again.', 'error');
    }
}

function displaySkills(skills, containerId, showActions = false) {
    const container = document.getElementById(containerId);
    console.log('🔍 DEBUG: displaySkills called for', containerId, 'with', skills.length, 'skills');
    
    container.innerHTML = '';
    
    if (skills.length === 0) {
        container.innerHTML = '<p>No skills found.</p>';
        return;
    }
    
    skills.forEach((skill, index) => {
        const skillCard = document.createElement('div');
        skillCard.className = 'skill-card';
        
        let actionsHtml = '';
        if (showActions) {
            actionsHtml = `
                <div class="skill-actions">
                    <button class="btn secondary" onclick="editSkill(${skill.id})">Edit</button>
                    <button class="btn danger" onclick="deleteSkill(${skill.id})">Delete</button>
                </div>
            `;
        } else if (authToken && skill.owner && skill.owner.id !== currentUser.id) {
            actionsHtml = `
                <div class="skill-actions">
                    <button class="btn primary" onclick="requestSkillExchange(${skill.id})">Request Exchange</button>
                </div>
            `;
        }
        
        skillCard.innerHTML = `
            <div class="skill-header">
                <h3 class="skill-title">${skill.title}</h3>
                <span class="skill-category">${skill.category}</span>
            </div>
            <p class="skill-description">${skill.description}</p>
            <span class="skill-proficiency">${skill.proficiency_level}</span>
            <div class="skill-owner">
                <p class="skill-owner-name">Offered by: ${skill.owner ? (skill.owner.full_name || skill.owner.username) : 'Unknown'}</p>
                <p>${skill.owner ? (skill.owner.bio || 'No bio available') : 'No bio available'}</p>
            </div>
            ${actionsHtml}
        `;
        
        container.appendChild(skillCard);
    });
    
    console.log('🔍 DEBUG: Skills rendered successfully');
}

// CRITICAL FIX: Exchange request with comprehensive token handling
async function handleRequestExchange(event) {
    event.preventDefault();
    console.log('🔍 DEBUG: handleRequestExchange() called');
    
    // CRITICAL FIX: Check ALL token keys with detailed logging
    const access_token = localStorage.getItem('access_token');
    const authToken_key = localStorage.getItem('authToken');
    const token_key = localStorage.getItem('token');
    
    console.log('🔍 DEBUG: Exchange request - Token availability:');
    console.log('  - access_token:', !!access_token);
    console.log('  - authToken:', !!authToken_key);
    console.log('  - token:', !!token_key);
    console.log('  - All localStorage keys:', Object.keys(localStorage));
    
    // Use the first available token
    const token = access_token || authToken_key || token_key;
    
    if (!token) {
        console.error('🔍 DEBUG: No token available for exchange request');
        showMessage('Please login to send exchange request', 'error');
        return;
    }
    
    console.log('🔍 DEBUG: Token found for exchange request:', token.substring(0, 30) + '...');
    console.log('🔍 DEBUG: Token length:', token.length);
    
    const requestData = {
        skill_id: parseInt(document.getElementById('request-skill-id').value),
        message: document.getElementById('request-message').value,
    };
    
    console.log('🔍 DEBUG: Exchange request data:', requestData);
    console.log('🔍 DEBUG: Authorization header will be:', 'Bearer ' + token.substring(0, 30) + '...');
    
    try {
        const response = await fetch(`${API_BASE_URL}/exchanges/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token,
            },
            body: JSON.stringify(requestData),
        });
        
        console.log('🔍 DEBUG: Exchange response status:', response.status);
        console.log('🔍 DEBUG: Exchange response ok:', response.ok);
        
        if (response.ok) {
            showMessage('Exchange request sent successfully!', 'success');
            document.getElementById('request-exchange-form').reset();
            document.getElementById('request-exchange-modal').style.display = 'none';
            console.log('🔍 DEBUG: Exchange request successful');
        } else {
            const error = await response.json();
            console.error('🔍 DEBUG: Exchange request failed:', error);
            showMessage(error.detail || 'Failed to send request', 'error');
        }
    } catch (error) {
        console.error('🔍 DEBUG: Exchange request network error:', error);
        console.error('🔍 DEBUG: Error details:', error.message);
        showMessage(`Network error: ${error.message}`, 'error');
    }
}

// Other functions (keeping them the same but with debug logging)
async function handleAddSkill(event) {
    event.preventDefault();
    
    const token = localStorage.getItem('access_token') || localStorage.getItem('authToken') || localStorage.getItem('token');
    
    if (!token) {
        showMessage('Please login to add a skill', 'error');
        return;
    }
    
    const skillData = {
        title: document.getElementById('skill-title').value,
        description: document.getElementById('skill-description').value,
        category: document.getElementById('skill-category').value,
        proficiency_level: document.getElementById('skill-proficiency').value,
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/skills/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify(skillData),
        });
        
        if (response.ok) {
            showMessage('Skill added successfully!', 'success');
            document.getElementById('add-skill-form').reset();
            document.getElementById('add-skill-modal').style.display = 'none';
            loadMySkills();
        } else {
            const error = await response.json();
            showMessage(error.detail || 'Failed to add skill', 'error');
        }
    } catch (error) {
        showMessage('Network error. Please try again.', 'error');
    }
}

function showAddSkillForm() {
    const token = localStorage.getItem('access_token') || localStorage.getItem('authToken') || localStorage.getItem('token');
    
    if (!token) {
        showMessage('Please login to add a skill', 'error');
        showPage('login');
        return;
    }
    
    document.getElementById('add-skill-modal').style.display = 'block';
}

function requestSkillExchange(skillId) {
    const token = localStorage.getItem('access_token') || localStorage.getItem('authToken') || localStorage.getItem('token');
    
    if (!token) {
        showMessage('Please login to request a skill exchange', 'error');
        showPage('login');
        return;
    }
    
    document.getElementById('request-skill-id').value = skillId;
    document.getElementById('request-exchange-modal').style.display = 'block';
}

// Utility functions
function showMessage(message, type) {
    const messageEl = document.getElementById('message');
    if (messageEl) {
        messageEl.textContent = message;
        messageEl.className = `message ${type}`;
        messageEl.style.display = 'block';
        
        setTimeout(() => {
            messageEl.style.display = 'none';
        }, 5000);
    }
}

console.log('🔍 DEBUG: auth_fixed.js loaded successfully');
