// Global variables
let currentUser = null;
let authToken = null;

// API Base URL - HARDCODED
const API_BASE_URL = 'http://127.0.0.1:8000';

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is logged in - check all token keys
    const token = localStorage.getItem('access_token') || localStorage.getItem('authToken') || localStorage.getItem('token');
    const user = localStorage.getItem('currentUser');
    
    if (token && user) {
        authToken = token;
        currentUser = JSON.parse(user);
        updateUIForLoggedInUser();
    }
    
    console.log('🔍 DEBUG: App initialized');
    console.log('🔍 DEBUG: Token found:', !!token);
    console.log('🔍 DEBUG: User found:', !!user);
    console.log('🔍 DEBUG: Token keys in localStorage:', Object.keys(localStorage).filter(k => k.includes('token')));

    // Set up event listeners
    setupEventListeners();
    
    // Show home page by default
    showPage('home');
});

// Setup event listeners
function setupEventListeners() {
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
}

// Page navigation
function showPage(pageId) {
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
    
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/users/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });
        
        if (response.ok) {
            const data = await response.json();
            authToken = data.access_token;
            
            // Save token to localStorage with consistent key - use 'access_token' as primary
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('authToken', data.access_token);
            
            console.log('🔍 DEBUG: Login successful - token saved');
            console.log('🔍 DEBUG: Token value:', data.access_token.substring(0, 50) + '...');
            console.log('🔍 DEBUG: Token keys in localStorage:', Object.keys(localStorage).filter(k => k.includes('token')));
            
            // Get user info
            const userResponse = await fetch(`${API_BASE_URL}/users/me`, {
                headers: {
                    'Authorization': `Bearer ${authToken}`,
                },
            });
            
            if (userResponse.ok) {
                currentUser = await userResponse.json();
                localStorage.setItem('currentUser', JSON.stringify(currentUser));
                
                updateUIForLoggedInUser();
                showMessage('Login successful!', 'success');
                showPage('home');
            }
        } else {
            const error = await response.json();
            showMessage(error.detail || 'Login failed', 'error');
        }
    } catch (error) {
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
    authToken = null;
    currentUser = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('authToken');
    localStorage.removeItem('token');
    localStorage.removeItem('currentUser');
    
    updateUIForLoggedOutUser();
    showMessage('Logged out successfully', 'info');
    showPage('home');
}

function updateUIForLoggedInUser() {
    document.getElementById('login-btn').style.display = 'none';
    document.getElementById('register-btn').style.display = 'none';
    document.getElementById('logout-btn').style.display = 'block';
}

function updateUIForLoggedOutUser() {
    document.getElementById('login-btn').style.display = 'block';
    document.getElementById('register-btn').style.display = 'block';
    document.getElementById('logout-btn').style.display = 'none';
}

// Skill functions
async function loadSkills() {
    console.log('🔍 DEBUG: loadSkills() called');
    
    const category = document.getElementById('category-filter').value;
    let url = `${API_BASE_URL}/skills/`;
    
    if (category) {
        url += `?category=${category}`;
    }
    
    console.log('🔍 DEBUG: URL to fetch:', url);
    console.log('🔍 DEBUG: API_BASE_URL:', API_BASE_URL);
    
    // Check for token (optional for skills endpoint)
    const token = localStorage.getItem('access_token') || localStorage.getItem('authToken') || localStorage.getItem('token');
    console.log('🔍 DEBUG: Token available for skills request:', !!token);
    console.log('🔍 DEBUG: Token keys in localStorage:', Object.keys(localStorage).filter(k => k.includes('token')));
    
    try {
        // Skills endpoint doesn't require authentication - use simple fetch
        console.log('🔍 DEBUG: Making public request to skills endpoint...');
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                // Only add auth header if token exists (optional)
                ...(token ? {
                    'Authorization': 'Bearer ' + token
                } : {})
            }
        });
        
        console.log('🔍 DEBUG: Response status:', response.status);
        console.log('🔍 DEBUG: Response ok:', response.ok);
        
        if (response.ok) {
            const skills = await response.json();
            console.log('🔍 DEBUG: Raw skills data received:', skills);
            console.log('🔍 DEBUG: Skills array length:', skills.length);
            console.log('🔍 DEBUG: Skills array type:', Array.isArray(skills) ? 'array' : typeof skills);
            
            // ALERT for empty data
            if (skills.length === 0) {
                alert('Backend returned empty skills array! Check database.');
                console.error('🚨 BACKEND RETURNED EMPTY ARRAY!');
            }
            
            if (skills.length > 0) {
                console.log('🔍 DEBUG: First skill structure:', JSON.stringify(skills[0], null, 2));
            }
            
            displaySkills(skills, 'skills-list');
            console.log('🔍 DEBUG: Skills displayed successfully');
        } else {
            console.error('🔍 DEBUG: Response not ok:', response.status, response.statusText);
            const errorText = await response.text();
            console.error('🔍 DEBUG: Error response body:', errorText);
            showMessage(`Failed to load skills: ${response.status} ${response.statusText}`, 'error');
        }
    } catch (error) {
        console.error('🔍 DEBUG: Network error:', error);
        console.error('🔍 DEBUG: Error stack:', error.stack);
        showMessage(`Network error: ${error.message}`, 'error');
        
        // Show error on screen
        document.getElementById('skills-list').innerHTML = `
            <div style="background: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <h3>🚨 Network Error Detected</h3>
                <p><strong>Error:</strong> ${error.message}</p>
                <p><strong>URL:</strong> ${url}</p>
                <p><strong>API Base:</strong> ${API_BASE_URL}</p>
                <p><strong>Token Available:</strong> ${token ? 'Yes' : 'No'}</p>
                <p><strong>CORS Check:</strong> Ensure backend allows ${window.location.origin}</p>
                <p><strong>Backend Status:</strong> Check if backend is running on ${API_BASE_URL}</p>
                <p>Check browser console for more details.</p>
            </div>
        `;
    }
}

async function loadMySkills() {
    if (!authToken) {
        showMessage('Please login to view your skills', 'error');
        showPage('login');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/skills/my-skills`, {
            headers: {
                'Authorization': `Bearer ${authToken}`,
            },
        });
        
        if (response.ok) {
            const skills = await response.json();
            displaySkills(skills, 'my-skills-list', true);
        } else {
            showMessage('Failed to load your skills', 'error');
        }
    } catch (error) {
        showMessage('Network error. Please try again.', 'error');
    }
}

function displaySkills(skills, containerId, showActions = false) {
    const container = document.getElementById(containerId);
    console.log('🔍 DEBUG: displaySkills called with', skills.length, 'skills for container', containerId);
    container.innerHTML = '';
    
    if (skills.length === 0) {
        container.innerHTML = '<p>No skills found.</p>';
        console.log('🔍 DEBUG: No skills to display');
        return;
    }
    
    console.log('🔍 DEBUG: Starting to render', skills.length, 'skills');
    skills.forEach((skill, index) => {
        console.log('🔍 DEBUG: Rendering skill', index + 1, skill.title);
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
        } else if (authToken && skill.owner.id !== currentUser.id) {
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
        console.log('🔍 DEBUG: Skill card appended for', skill.title);
    });
    
    console.log('🔍 DEBUG: Total skills rendered:', skills.length);
}

async function handleAddSkill(event) {
    event.preventDefault();
    
    if (!authToken) {
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
                'Authorization': `Bearer ${authToken}`,
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
    if (!authToken) {
        showMessage('Please login to add a skill', 'error');
        showPage('login');
        return;
    }
    
    document.getElementById('add-skill-modal').style.display = 'block';
}

async function deleteSkill(skillId) {
    if (!confirm('Are you sure you want to delete this skill?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/skills/${skillId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${authToken}`,
            },
        });
        
        if (response.ok) {
            showMessage('Skill deleted successfully!', 'success');
            loadMySkills();
        } else {
            const error = await response.json();
            showMessage(error.detail || 'Failed to delete skill', 'error');
        }
    } catch (error) {
        showMessage('Network error. Please try again.', 'error');
    }
}

// Skill Exchange Request functions
async function loadRequests() {
    if (!authToken) {
        showMessage('Please login to view requests', 'error');
        showPage('login');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/exchanges/`, {
            headers: {
                'Authorization': `Bearer ${authToken}`,
            },
        });
        
        if (response.ok) {
            const requests = await response.json();
            displayRequests(requests);
        } else {
            showMessage('Failed to load requests', 'error');
        }
    } catch (error) {
        showMessage('Network error. Please try again.', 'error');
    }
}

function displayRequests(requests) {
    const container = document.getElementById('requests-list');
    container.innerHTML = '';
    
    if (requests.length === 0) {
        container.innerHTML = '<p>No requests found.</p>';
        return;
    }
    
    requests.forEach(request => {
        const requestCard = document.createElement('div');
        requestCard.className = 'request-card';
        
        const statusClass = `status-${request.status}`;
        const isSkillOwner = request.skill_owner.id === currentUser.id;
        
        let actionsHtml = '';
        if (isSkillOwner && request.status === 'pending') {
            actionsHtml = `
                <div class="request-actions">
                    <button class="btn success" onclick="updateRequestStatus(${request.id}, 'accepted')">Accept</button>
                    <button class="btn danger" onclick="updateRequestStatus(${request.id}, 'rejected')">Reject</button>
                </div>
            `;
        } else if (isSkillOwner && request.status === 'accepted') {
            actionsHtml = `
                <div class="request-actions">
                    <button class="btn secondary" onclick="updateRequestStatus(${request.id}, 'completed')">Mark Complete</button>
                </div>
            `;
        }
        
        requestCard.innerHTML = `
            <div class="request-header">
                <h3>Request for: ${request.skill.title}</h3>
                <span class="request-status ${statusClass}">${request.status.toUpperCase()}</span>
            </div>
            <p><strong>From:</strong> ${request.requester.full_name}</p>
            <p><strong>To:</strong> ${request.skill_owner.full_name}</p>
            <div class="request-message">
                <strong>Message:</strong> ${request.message}
            </div>
            <p><small>Created: ${new Date(request.created_at).toLocaleDateString()}</small></p>
            ${actionsHtml}
        `;
        
        container.appendChild(requestCard);
    });
}

function requestSkillExchange(skillId) {
    if (!authToken) {
        showMessage('Please login to request a skill exchange', 'error');
        showPage('login');
        return;
    }
    
    document.getElementById('request-skill-id').value = skillId;
    document.getElementById('request-exchange-modal').style.display = 'block';
}

async function handleRequestExchange(event) {
    event.preventDefault();
    
    // Get token from localStorage - check all token keys
    const token = localStorage.getItem('access_token') || localStorage.getItem('authToken') || localStorage.getItem('token');
    
    console.log('🔍 DEBUG: Exchange request - Token check');
    console.log('🔍 DEBUG: Token exists:', !!token);
    console.log('🔍 DEBUG: Token length:', token ? token.length : 0);
    console.log('🔍 DEBUG: Token format:', token ? token.substring(0, 20) + '...' : 'null');
    console.log('🔍 DEBUG: Token keys available:', Object.keys(localStorage).filter(k => k.includes('token')));
    
    if (!token) {
        showMessage('Please login to send exchange request', 'error');
        return;
    }
    
    const requestData = {
        skill_id: parseInt(document.getElementById('request-skill-id').value),
        message: document.getElementById('request-message').value,
    };
    
    console.log('🔍 DEBUG: Request data:', requestData);
    console.log('🔍 DEBUG: Authorization header:', 'Bearer ' + token.substring(0, 20) + '...');
    
    try {
        const response = await fetch(`${API_BASE_URL}/exchanges/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token,  // Ensure space after Bearer
            },
            body: JSON.stringify(requestData),
        });
        
        console.log('🔍 DEBUG: Response status:', response.status);
        console.log('🔍 DEBUG: Response ok:', response.ok);
        
        if (response.ok) {
            showMessage('Exchange request sent successfully!', 'success');
            document.getElementById('request-exchange-form').reset();
            document.getElementById('request-exchange-modal').style.display = 'none';
        } else {
            const error = await response.json();
            console.error('🔍 DEBUG: Backend error:', error);
            showMessage(error.detail || 'Failed to send request', 'error');
        }
    } catch (error) {
        console.error('🔍 DEBUG: Exchange request error:', error);
        showMessage(`Network error: ${error.message}`, 'error');
    }
}

async function updateRequestStatus(requestId, status) {
    // Get token from localStorage - check all token keys
    const token = localStorage.getItem('access_token') || localStorage.getItem('authToken') || localStorage.getItem('token');
    
    if (!token) {
        showMessage('Please login to update request', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/exchanges/${requestId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token,
            },
            body: JSON.stringify({ status }),
        });
        
        if (response.ok) {
            showMessage(`Request ${status} successfully!`, 'success');
            loadRequests();
        } else {
            const error = await response.json();
            showMessage(error.detail || 'Failed to update request', 'error');
        }
    } catch (error) {
        console.error('🔍 DEBUG: Update request error:', error);
        showMessage(`Network error: ${error.message}`, 'error');
    }
}

// Utility functions
function showMessage(message, type) {
    const messageEl = document.getElementById('message');
    messageEl.textContent = message;
    messageEl.className = `message ${type}`;
    messageEl.style.display = 'block';
    
    setTimeout(() => {
        messageEl.style.display = 'none';
    }, 5000);
}

// Helper function for authenticated requests
async function makeAuthenticatedRequest(url, options = {}) {
    console.log('🔍 DEBUG: makeAuthenticatedRequest called');
    console.log('🔍 DEBUG: URL:', url);
    console.log('🔍 DEBUG: authToken global:', authToken ? 'present' : 'missing');
    
    // Get token from localStorage as backup - check all token keys
    const token = authToken || localStorage.getItem('access_token') || localStorage.getItem('authToken') || localStorage.getItem('token');
    console.log('🔍 DEBUG: Token from storage:', token ? token.substring(0, 50) + '...' : 'null');
    
    if (!token) {
        console.error('🔍 DEBUG: No authentication token available');
        throw new Error('No authentication token found');
    }
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
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
    
    console.log('🔍 DEBUG: Request headers:', mergedOptions.headers);
    console.log('🔍 DEBUG: Making fetch request...');
    
    try {
        const response = await fetch(url, mergedOptions);
        console.log('🔍 DEBUG: Fetch response received');
        console.log('🔍 DEBUG: Response status:', response.status);
        console.log('🔍 DEBUG: Response headers:', [...response.headers.entries()]);
        return response;
    } catch (error) {
        console.error('🔍 DEBUG: Fetch error:', error);
        throw error;
    }
}
