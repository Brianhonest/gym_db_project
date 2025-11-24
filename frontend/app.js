const API_BASE_URL = 'http://localhost:8000';

// Tab switching
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.add('active');
    event.target.classList.add('active');
    
    // Hide all operation forms
    document.querySelectorAll('.operation-form').forEach(form => {
        form.style.display = 'none';
    });
}

// Show specific operation form
function showOperation(operation) {
    // Hide all operation forms
    document.querySelectorAll('.operation-form').forEach(form => {
        form.style.display = 'none';
    });
    
    // Show selected form
    const formId = `${operation}-form`;
    const form = document.getElementById(formId);
    if (form) {
        form.style.display = 'block';
    }
}

// Display response messages
function showResponse(tabName, message, isSuccess) {
    const responseDiv = document.getElementById(`${tabName}-response`);
    responseDiv.textContent = message;
    responseDiv.className = `response ${isSuccess ? 'success' : 'error'}`;
    responseDiv.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        responseDiv.style.display = 'none';
    }, 5000);
}

// Member Registration
async function registerMember(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    
    try {
        const response = await fetch(`${API_BASE_URL}/members/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showResponse('member', `Success! Member registered with ID: ${result.user_id}`, true);
            event.target.reset();
        } else {
            showResponse('member', `Error: ${result.detail}`, false);
        }
    } catch (error) {
        showResponse('member', `Error: ${error.message}`, false);
    }
}