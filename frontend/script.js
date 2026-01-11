// COMPLETE AUTHENTICATION FIX - This will solve all token issues

// Global variables
let currentUser = null;
let authToken = null;

// API Base URL - HARDCODED with full absolute URLs
const API_BASE_URL = 'http://127.0.0.1:8001';

// CRITICAL FIX: Ensure all API calls use absolute URLs with correct prefix
function getApiUrl(endpoint) {
    // Remove leading slash if present
    const cleanEndpoint = endpoint.startsWith('/') ? endpoint.substring(1) : endpoint;
    
    // Special handling for users endpoints (they don't have /api prefix)
    if (cleanEndpoint.startsWith('users/')) {
        return `${API_BASE_URL}/${cleanEndpoint}`;
    }
    
    // Add /api prefix for other endpoints if not already present
    if (!cleanEndpoint.startsWith('api/')) {
        return `${API_BASE_URL}/api/${cleanEndpoint}`;
    }
    
    return `${API_BASE_URL}/${cleanEndpoint}`;
}

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔍 DEBUG: App initialization starting...');
    
    // Check if user is logged in - check ALL token keys with 'accessToken' priority
    const accessToken = localStorage.getItem('accessToken');
    const access_token = localStorage.getItem('access_token');
    const authToken_key = localStorage.getItem('authToken');
    const token_key = localStorage.getItem('token');
    const user = localStorage.getItem('currentUser');
    
    console.log('🔍 DEBUG: Token check - accessToken:', !!accessToken);
    console.log('🔍 DEBUG: Token check - access_token:', !!access_token);
    console.log('🔍 DEBUG: Token check - authToken:', !!authToken_key);
    console.log('🔍 DEBUG: Token check - token:', !!token_key);
    console.log('🔍 DEBUG: User check:', !!user);
    
    // Use the first available token with 'accessToken' priority
    const availableToken = accessToken || access_token || authToken_key || token_key;
    
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
    
    if (!username || !password) {
        showMessage('Please enter username and password', 'error');
        return;
    }
    
    try {
        // CRITICAL FIX: Use getApiUrl function with correct port
        const response = await fetch(getApiUrl('users/login'), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });
        
        console.log('🔍 DEBUG: Login response status:', response.status);
        console.log('🔍 DEBUG: Login URL:', getApiUrl('users/login'));
        
        if (response.ok) {
            const data = await response.json();
            authToken = data.access_token;
            
            console.log('🔍 DEBUG: Login successful - received token');
            console.log('🔍 DEBUG: Token length:', authToken.length);
            console.log('🔍 DEBUG: Token type:', data.token_type);
            
            // CRITICAL FIX: Save token with consistent key 'accessToken' as requested
            localStorage.setItem('accessToken', data.access_token);
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('authToken', data.access_token);
            
            console.log('🔍 DEBUG: Token saved to localStorage with all keys');
            console.log('🔍 DEBUG: localStorage keys after save:', Object.keys(localStorage));
            
            // Verify token was saved
            const verifyToken = localStorage.getItem('accessToken');
            console.log('🔍 DEBUG: Token verification - accessToken exists:', !!verifyToken);
            
            // Get user info
            console.log('🔍 DEBUG: Fetching user info...');
            const userResponse = await fetch('http://127.0.0.1:8000/users/me', {
                headers: {
                    'Authorization': `Bearer ${authToken}`,
                },
            });
            
            console.log('🔍 DEBUG: User info response status:', userResponse.status);
            console.log('🔍 DEBUG: User info URL: http://127.0.0.1:8000/users/me');
            
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
        showMessage('Network error. Please check if backend is running.', 'error');
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
        // CRITICAL FIX: Use getApiUrl function with correct port
        const response = await fetch(getApiUrl('users/register'), {
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
    
    // Clear ALL token keys including 'accessToken'
    localStorage.removeItem('accessToken');
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

// CRITICAL FIX: Skills loading with proper token handling and absolute URLs
async function loadSkills() {
    console.log('🔍 DEBUG: loadSkills() called');
    
    const category = document.getElementById('category-filter').value;
    let endpoint = 'skills/';
    
    if (category) {
        endpoint += `?category=${category}`;
    }
    
    const url = getApiUrl(endpoint);
    console.log('🔍 DEBUG: Skills URL:', url);
    
    // CRITICAL FIX: Check ALL token keys and log detailed info with 'accessToken' priority
    const accessToken = localStorage.getItem('accessToken');
    const access_token = localStorage.getItem('access_token');
    const authToken_key = localStorage.getItem('authToken');
    const token_key = localStorage.getItem('token');
    
    console.log('🔍 DEBUG: Token availability check:');
    console.log('  - accessToken:', !!accessToken);
    console.log('  - access_token:', !!access_token);
    console.log('  - authToken:', !!authToken_key);
    console.log('  - token:', !!token_key);
    
    // Use the first available token with 'accessToken' priority
    const availableToken = accessToken || access_token || authToken_key || token_key;
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

async function loadRequests() {
    console.log('🔍 DEBUG: loadRequests() called');
    
    // CRITICAL FIX: Check ALL token keys with 'accessToken' priority
    const token = localStorage.getItem('accessToken') || 
                  localStorage.getItem('access_token') || 
                  localStorage.getItem('authToken') || 
                  localStorage.getItem('token');
    
    if (!token) {
        console.error('🔍 DEBUG: No token found for requests');
        showMessage('Please login to view your requests', 'error');
        // CRITICAL FIX: Redirect to login instead of just showing error
        showPage('login');
        return;
    }
    
    console.log('🔍 DEBUG: Token found for requests:', token.substring(0, 30) + '...');
    
    try {
        // CRITICAL FIX: Use correct API URL with /api prefix
        const response = await fetch(getApiUrl('exchanges/'), {
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });
        
        console.log('🔍 DEBUG: Requests response status:', response.status);
        
        if (response.ok) {
            const requests = await response.json();
            displayRequests(requests);
            console.log('🔍 DEBUG: Requests loaded successfully');
        } else {
            showMessage('Failed to load requests', 'error');
        }
    } catch (error) {
        console.error('🔍 DEBUG: Requests error:', error);
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
        requestCard.setAttribute('data-request-id', request.id);
        
        const statusClass = `status-${request.status}`;
        const isSkillOwner = request.skill_owner.id === currentUser.id;
        
        let actionsHtml = '';
        if (isSkillOwner && request.status === 'pending') {
            actionsHtml = `
                <div class="request-actions">
                    <button class="btn success" onclick="updateRequestStatus(${request.id}, 'Accepted')">Accept</button>
                    <button class="btn danger" onclick="updateRequestStatus(${request.id}, 'Rejected')">Reject</button>
                </div>
            `;
        } else if (isSkillOwner && request.status === 'accepted') {
            actionsHtml = `
                <div class="request-actions">
                    <button class="btn secondary" onclick="updateRequestStatus(${request.id}, 'completed')">Mark Complete</button>
                </div>
            `;
        } else if (request.status === 'accepted' || request.status === 'rejected' || request.status === 'completed') {
            // For accepted, rejected, or completed requests - no action buttons
            actionsHtml = `
                <div class="request-actions">
                    <span class="status-indicator">Request ${request.status.toUpperCase()}</span>
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

async function updateRequestStatus(requestId, status) {
    // CRITICAL FIX: Check ALL token keys with 'accessToken' priority
    const token = localStorage.getItem('accessToken') || 
                  localStorage.getItem('access_token') || 
                  localStorage.getItem('authToken') || 
                  localStorage.getItem('token');
    
    if (!token) {
        showMessage('Please login to update request', 'error');
        showPage('login');
        return;
    }
    
    try {
        // Use correct API endpoint for updating request status
        const response = await fetch(getApiUrl(`exchanges/requests/${requestId}`), {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token,
            },
            body: JSON.stringify({ status }),
        });
        
        if (response.ok) {
            const result = await response.json();
            showMessage(`Request ${status} successfully!`, 'success');
            
            // Update UI without page refresh
            updateRequestUI(requestId, status);
        } else {
            const error = await response.json();
            showMessage(error.detail || 'Failed to update request', 'error');
        }
    } catch (error) {
        console.error('🔍 DEBUG: Update request error:', error);
        showMessage('Network error. Please try again.', 'error');
    }
}

// Update UI without page refresh
function updateRequestUI(requestId, status) {
    console.log(`🔍 DEBUG: Updating UI for request ${requestId} to status ${status}`);
    
    // Find the request card
    const requestCard = document.querySelector(`[data-request-id="${requestId}"]`);
    if (!requestCard) {
        console.error(`🔍 DEBUG: Request card not found for ID ${requestId}`);
        return;
    }
    
    // Find the status element
    const statusElement = requestCard.querySelector('.request-status');
    if (statusElement) {
        statusElement.textContent = status;
        statusElement.className = `request-status status-${status.toLowerCase()}`;
    }
    
    // Find the actions container
    const actionsContainer = requestCard.querySelector('.request-actions');
    if (actionsContainer) {
        if (status === 'Accepted' || status === 'Rejected') {
            // Hide the accept/reject buttons
            actionsContainer.style.display = 'none';
        }
    }
    
    console.log(`🔍 DEBUG: UI updated for request ${requestId}`);
}

async function loadMySkills() {
    console.log('🔍 DEBUG: loadMySkills() called');
    
    // Get authentication token - check ALL possible keys
    const token = localStorage.getItem('accessToken') || 
                  localStorage.getItem('access_token') || 
                  localStorage.getItem('authToken') || 
                  localStorage.getItem('token');
    
    console.log('🔍 DEBUG: Token found:', !!token);
    if (token) {
        console.log('🔍 DEBUG: Token preview:', token.substring(0, 20) + '...');
    }
    
    if (!token) {
        console.log('🔍 DEBUG: No token found, showing login required');
        const container = document.getElementById('my-skills-list');
        container.innerHTML = '<p>Please login to view your skills</p>';
        return;
    }
    
    try {
        // Build the correct API URL
        const apiUrl = getApiUrl('skills/my-skills');
        console.log('🔍 DEBUG: API URL:', apiUrl);
        console.log('🔍 DEBUG: Loading skills from backend...');
        
        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
        });
        
        console.log('🔍 DEBUG: My-skills response status:', response.status);
        console.log('🔍 DEBUG: Response headers:', response.headers);
        
        if (response.ok) {
            const skills = await response.json();
            console.log('🔍 DEBUG: Skills loaded from backend:', skills);
            console.log('🔍 DEBUG: Skills count:', skills.length);
            
            if (Array.isArray(skills)) {
                displaySkills(skills, 'my-skills-list', true);
            } else {
                console.error('🔍 DEBUG: Expected array but got:', typeof skills);
                const container = document.getElementById('my-skills-list');
                container.innerHTML = '<p>Invalid data format received from server.</p>';
            }
        } else if (response.status === 401) {
            console.error('🔍 DEBUG: Unauthorized - token expired or invalid');
            const container = document.getElementById('my-skills-list');
            container.innerHTML = '<p>Your session has expired. Please login again.</p>';
            // Clear invalid tokens and redirect to login
            localStorage.removeItem('accessToken');
            localStorage.removeItem('access_token');
            localStorage.removeItem('authToken');
            localStorage.removeItem('token');
            localStorage.removeItem('currentUser');
            showPage('login');
        } else if (response.status === 403) {
            console.error('🔍 DEBUG: Forbidden - insufficient permissions');
            const container = document.getElementById('my-skills-list');
            container.innerHTML = '<p>You do not have permission to view skills.</p>';
        } else {
            console.error('🔍 DEBUG: Failed to load skills:', response.status);
            let errorMessage = 'Failed to load skills. Please try again.';
            
            try {
                const errorData = await response.json();
                console.error('🔍 DEBUG: Error details:', errorData);
                if (errorData.detail) {
                    errorMessage = errorData.detail;
                }
            } catch (e) {
                console.error('🔍 DEBUG: Could not parse error response:', e);
            }
            
            const container = document.getElementById('my-skills-list');
            container.innerHTML = `<p>${errorMessage}</p>`;
        }
    } catch (error) {
        console.error('🔍 DEBUG: Network error loading skills:', error);
        console.error('🔍 DEBUG: Error details:', {
            message: error.message,
            stack: error.stack
        });
        
        const container = document.getElementById('my-skills-list');
        container.innerHTML = '<p>Network error. Please check your connection and try again.</p>';
    }
}

function displaySkills(skills, containerId, showActions = false) {
    const container = document.getElementById(containerId);
    console.log('🔍 DEBUG: displaySkills called for', containerId, 'with', skills.length, 'skills');
    
    // Validate container exists
    if (!container) {
        console.error('🔍 DEBUG: Container not found:', containerId);
        return;
    }
    
    // Clear container
    container.innerHTML = '';
    
    // Handle empty or invalid data
    if (!skills || !Array.isArray(skills)) {
        console.error('🔍 DEBUG: Invalid skills data:', skills);
        container.innerHTML = '<p>No skills data available.</p>';
        return;
    }
    
    if (skills.length === 0) {
        console.log('🔍 DEBUG: No skills to display');
        container.innerHTML = '<p>No skills found.</p>';
        return;
    }
    
    console.log('🔍 DEBUG: Rendering skills:', skills);
    
    skills.forEach((skill, index) => {
        console.log(`🔍 DEBUG: Rendering skill ${index}:`, skill);
        
        // Validate skill data
        if (!skill || typeof skill !== 'object') {
            console.error('🔍 DEBUG: Invalid skill data at index', index, skill);
            return;
        }
        
        const skillCard = document.createElement('div');
        skillCard.className = 'skill-card';
        
        let actionsHtml = '';
        if (showActions) {
            // For My Skills page - always show Edit/Delete buttons
            actionsHtml = `
                <div class="skill-actions">
                    <button class="btn secondary" onclick="editSkill(${skill.id || 0})">Edit</button>
                    <button class="btn danger" onclick="deleteSkill(${skill.id || 0})">Delete</button>
                </div>
            `;
        } else if (authToken && skill.owner && skill.owner.id !== currentUser.id) {
            actionsHtml = `
                <div class="skill-actions">
                    <button class="btn primary" onclick="requestSkillExchange(${skill.id || 0})">Request Exchange</button>
                </div>
            `;
        }
        
        skillCard.innerHTML = `
            <div class="skill-header">
                <h3 class="skill-title">${skill.title || 'Untitled Skill'}</h3>
                <span class="skill-category">${skill.category || 'Uncategorized'}</span>
            </div>
            <p class="skill-description">${skill.description || 'No description available'}</p>
            <span class="skill-proficiency">${skill.proficiency_level || 'Not specified'}</span>
            <div class="skill-owner">
                <p class="skill-owner-name">Offered by: ${skill.owner ? (skill.owner.full_name || skill.owner.username || 'Unknown') : 'Unknown'}</p>
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
    
    // CRITICAL FIX: Check ALL token keys with detailed logging and 'accessToken' priority
    const accessToken = localStorage.getItem('accessToken');
    const access_token = localStorage.getItem('access_token');
    const authToken_key = localStorage.getItem('authToken');
    const token_key = localStorage.getItem('token');
    
    console.log('🔍 DEBUG: Exchange request - Token availability:');
    console.log('  - accessToken:', !!accessToken);
    console.log('  - access_token:', !!access_token);
    console.log('  - authToken:', !!authToken_key);
    console.log('  - token:', !!token_key);
    console.log('  - All localStorage keys:', Object.keys(localStorage));
    
    // Use the first available token with 'accessToken' priority
    const token = accessToken || access_token || authToken_key || token_key;
    
    if (!token) {
        console.error('🔍 DEBUG: No token available for exchange request');
        showMessage('Please login to send exchange request', 'error');
        // CRITICAL FIX: Redirect to login instead of just showing error
        showPage('login');
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
        // CRITICAL FIX: Use direct endpoint /request-skill (not /api/exchanges/request-skill)
        const url = 'http://127.0.0.1:8000/request-skill';
        console.log('🔍 DEBUG: Exchange request URL:', url);
        
        const response = await fetch(url, {
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
            const result = await response.json();
            console.log('🔍 DEBUG: Exchange response data:', result);
            
            // SUCCESS: Show success message and close modal
            alert('✅ Exchange request sent successfully!');
            console.log('✅ SUCCESS: Exchange request sent successfully!');
            
            // Reset form and close modal
            document.getElementById('request-exchange-form').reset();
            document.getElementById('request-exchange-modal').style.display = 'none';
            
            // Refresh skills list to show updated status
            await loadSkills();
            
        } else {
            const error = await response.json();
            console.error('🔍 DEBUG: Exchange request failed:', error);
            
            // Show error message
            alert('❌ Failed to send request: ' + (error.detail || error.message || 'Unknown error'));
            showMessage(error.detail || error.message || 'Failed to send request', 'error');
        }
    } catch (error) {
        console.error('🔍 DEBUG: Exchange request network error:', error);
        console.error('🔍 DEBUG: Error details:', error.message);
        
        // Show network error
        alert('❌ Network error: ' + error.message);
        showMessage(`Network error: ${error.message}`, 'error');
    }
}

// NEW FUNCTION: Send Skill Request - Direct implementation as requested
async function sendSkillRequest() {
    console.log('🔍 DEBUG: sendSkillRequest() called');
    
    // Get token from localStorage (accessToken priority)
    const accessToken = localStorage.getItem('accessToken');
    const access_token = localStorage.getItem('access_token');
    const authToken_key = localStorage.getItem('authToken');
    const token_key = localStorage.getItem('token');
    
    // Use the first available token with 'accessToken' priority
    const token = accessToken || access_token || authToken_key || token_key;
    
    if (!token) {
        console.error('🔍 DEBUG: No token available for skill request');
        alert('❌ Please login to send skill request');
        return;
    }
    
    // Get message from textarea (try both textareas)
    let message = '';
    const messageTextarea = document.getElementById('request-message');
    const directMessageTextarea = document.getElementById('direct-message');
    
    if (messageTextarea && messageTextarea.value.trim()) {
        message = messageTextarea.value.trim();
    } else if (directMessageTextarea && directMessageTextarea.value.trim()) {
        message = directMessageTextarea.value.trim();
    }
    
    if (!message) {
        console.error('🔍 DEBUG: No message provided');
        alert('❌ Please enter a message');
        return;
    }
    
    // Get skill ID (if available)
    const skillIdElement = document.getElementById('request-skill-id');
    const skill_id = skillIdElement ? parseInt(skillIdElement.value) : 1; // Default to 1 if not found
    
    console.log('🔍 DEBUG: Skill request data:', { skill_id, message });
    console.log('🔍 DEBUG: Token found:', token.substring(0, 30) + '...');
    
    try {
        // Call backend endpoint as requested: http://127.0.0.1:8000/request-skill
        const url = 'http://127.0.0.1:8000/request-skill';
        console.log('🔍 DEBUG: Skill request URL:', url);
        
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token,
            },
            body: JSON.stringify({
                message: message,
                skill_id: skill_id
            }),
        });
        
        console.log('🔍 DEBUG: Skill response status:', response.status);
        console.log('🔍 DEBUG: Skill response ok:', response.ok);
        
        if (response.ok) {
            const result = await response.json();
            console.log('🔍 DEBUG: Skill request response:', result);
            
            // SUCCESS: Show success message
            alert('✅ Skill request sent successfully!\n\n' + 
                  'Request ID: ' + result.request_id + '\n' +
                  'Skill: ' + result.skill_title + '\n' +
                  'Message: ' + message);
            console.log('✅ SUCCESS: Skill request sent successfully!');
            
            // Clear both textareas
            if (messageTextarea) {
                messageTextarea.value = '';
            }
            if (directMessageTextarea) {
                directMessageTextarea.value = '';
            }
            
            // Close modal if it's open
            const modal = document.getElementById('request-exchange-modal');
            if (modal) {
                modal.style.display = 'none';
            }
            
        } else {
            const error = await response.json();
            console.error('🔍 DEBUG: Skill request failed:', error);
            
            // Show error message
            alert('❌ Failed to send skill request: ' + (error.detail || error.message || 'Unknown error'));
        }
    } catch (error) {
        console.error('🔍 DEBUG: Skill request network error:', error);
        
        // Show network error
        alert('❌ Network error: ' + error.message);
    }
}

// LocalStorage functions for skill management
function saveSkillToLocalStorage(skill) {
    try {
        console.log('🔍 DEBUG: Saving skill to LocalStorage:', skill.title);
        let skills = getSkillsFromLocalStorage();
        skills.push(skill);
        localStorage.setItem('mySkills', JSON.stringify(skills));
        console.log('🔍 DEBUG: Skill saved successfully. Total skills:', skills.length);
        console.log('🔍 DEBUG: LocalStorage data:', JSON.stringify(localStorage.getItem('mySkills')));
    } catch (error) {
        console.error('🔍 DEBUG: Error saving to LocalStorage:', error);
    }
}

function getSkillsFromLocalStorage() {
    try {
        const skills = localStorage.getItem('mySkills');
        console.log('🔍 DEBUG: Raw LocalStorage data:', skills);
        const parsed = skills ? JSON.parse(skills) : [];
        console.log('🔍 DEBUG: Parsed LocalStorage skills:', parsed.length);
        return parsed;
    } catch (error) {
        console.error('🔍 DEBUG: Error loading from LocalStorage:', error);
        return [];
    }
}

function removeSkillFromLocalStorage(skillId) {
    try {
        console.log('🔍 DEBUG: Removing skill from LocalStorage:', skillId);
        let skills = getSkillsFromLocalStorage();
        skills = skills.filter(skill => skill.id !== skillId);
        localStorage.setItem('mySkills', JSON.stringify(skills));
        console.log('🔍 DEBUG: Skill removed. Remaining skills:', skills.length);
    } catch (error) {
        console.error('🔍 DEBUG: Error removing from LocalStorage:', error);
    }
}

async function handleAddSkill(event) {
    event.preventDefault();
    console.log('🔍 DEBUG: handleAddSkill() called - FORM SUBMISSION DETECTED!');
    
    // Get form values with validation
    const title = document.getElementById('skill-title').value.trim();
    const description = document.getElementById('skill-description').value.trim();
    const category = document.getElementById('skill-category').value;
    const proficiency_level = document.getElementById('skill-proficiency').value;
    
    console.log('🔍 DEBUG: Form values:', { title, description, category, proficiency_level });
    
    // Form validation
    if (!title) {
        showMessage('Please enter a skill title', 'error');
        return;
    }
    if (!description) {
        showMessage('Please enter a skill description', 'error');
        return;
    }
    if (!category) {
        showMessage('Please select a category', 'error');
        return;
    }
    if (!proficiency_level) {
        showMessage('Please select a proficiency level', 'error');
        return;
    }
    
    // Get authentication token
    const token = localStorage.getItem('accessToken') || 
                  localStorage.getItem('access_token') || 
                  localStorage.getItem('authToken') || 
                  localStorage.getItem('token');
    
    if (!token) {
        showMessage('Please login to add a skill', 'error');
        showPage('login');
        return;
    }
    
    // Create skill object for backend
    const skillData = {
        title: title,
        description: description,
        category: category,
        proficiency_level: proficiency_level,
    };
    
    console.log('🔍 DEBUG: Skill data to send to backend:', skillData);
    
    try {
        // Send to backend
        const response = await fetch(getApiUrl('skills/'), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify(skillData),
        });
        
        console.log('🔍 DEBUG: Backend response status:', response.status);
        
        if (response.ok) {
            const newSkill = await response.json();
            console.log('🔍 DEBUG: Skill saved to backend:', newSkill);
            
            // Clear form and close modal
            document.getElementById('add-skill-form').reset();
            document.getElementById('add-skill-modal').style.display = 'none';
            
            // Refresh skills display from backend
            await loadMySkills();
            
            // Show success message
            showMessage(`"${newSkill.title}" has been added to your skills!`, 'success');
            
        } else {
            const error = await response.json();
            console.error('🔍 DEBUG: Backend error:', error);
            showMessage(error.detail || 'Failed to add skill', 'error');
        }
    } catch (error) {
        console.error('🔍 DEBUG: Network error:', error);
        showMessage('Network error. Please try again.', 'error');
    }
}

function showAddSkillForm() {
    console.log('🔍 DEBUG: showAddSkillForm() called');
    document.getElementById('add-skill-modal').style.display = 'block';
}

function testLocalStorage() {
    console.log('🔍 DEBUG: Testing LocalStorage...');
    
    const testSkill = {
        id: Date.now(),
        title: 'Test Skill - ' + new Date().toLocaleTimeString(),
        description: 'This is a test skill added via Test LocalStorage button',
        category: 'Programming',
        proficiency_level: 'Advanced',
        created_at: new Date().toISOString(),
        is_active: true,
        user_id: 1,
        owner: {
            id: 1,
            username: 'testuser',
            full_name: 'Test User',
            email: 'test@example.com'
        }
    };
    
    saveSkillToLocalStorage(testSkill);
    loadMySkills();
    showMessage('Test skill added successfully!', 'success');
}

function clearLocalStorage() {
    console.log('🔍 DEBUG: Clearing LocalStorage...');
    if (confirm('Are you sure you want to clear all locally saved skills?')) {
        localStorage.removeItem('mySkills');
        loadMySkills();
        showMessage('LocalStorage cleared!', 'info');
    }
}

function deleteSkill(skillId) {
    console.log('🔍 DEBUG: deleteSkill() called for skill:', skillId);
    
    if (!confirm('Are you sure you want to delete this skill?')) {
        return;
    }
    
    // Remove from LocalStorage
    removeSkillFromLocalStorage(skillId);
    
    // Try to remove from backend if token is available
    const token = localStorage.getItem('accessToken') || 
                  localStorage.getItem('access_token') || 
                  localStorage.getItem('authToken') || 
                  localStorage.getItem('token');
    
    if (token) {
        fetch(getApiUrl(`skills/${skillId}`), {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        }).then(response => {
            if (response.ok) {
                console.log('🔍 DEBUG: Skill deleted from backend');
                showMessage('Skill deleted from backend', 'success');
            } else {
                console.log('🔍 DEBUG: Backend delete failed, but LocalStorage updated');
                showMessage('Skill deleted locally', 'info');
            }
        }).catch(error => {
            console.log('🔍 DEBUG: Backend delete error, but LocalStorage updated:', error);
            showMessage('Skill deleted locally', 'info');
        });
    } else {
        showMessage('Skill deleted locally', 'info');
    }
    
    // Refresh display
    loadMySkills();
}

function editSkill(skillId) {
    console.log('🔍 DEBUG: editSkill() called for skill:', skillId);
    // For now, just show a message
    showMessage('Edit functionality coming soon!', 'info');
}

function requestSkillExchange(skillId) {
    // CRITICAL FIX: Check ALL token keys with 'accessToken' priority
    const token = localStorage.getItem('accessToken') || 
                  localStorage.getItem('access_token') || 
                  localStorage.getItem('authToken') || 
                  localStorage.getItem('token');
    
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

// Modal close functionality
document.addEventListener('DOMContentLoaded', function() {
    // Get all modal close buttons
    const closeButtons = document.querySelectorAll('.close');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const modal = this.closest('.modal');
            if (modal) {
                modal.style.display = 'none';
                // Clear form if it's add-skill-modal
                if (modal.id === 'add-skill-modal') {
                    document.getElementById('add-skill-form').reset();
                }
            }
        });
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
            // Clear form if it's add-skill-modal
            if (event.target.id === 'add-skill-modal') {
                document.getElementById('add-skill-form').reset();
            }
        }
    });
});
