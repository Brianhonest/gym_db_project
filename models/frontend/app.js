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

async function logHealthMetrics(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    const memberId = data.member_id;
    delete data.member_id;
    
    try {
        const response = await fetch(`${API_BASE_URL}/members/${memberId}/health-metrics`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showResponse('member', 'Health metrics logged successfully!', true);
            event.target.reset();
        } else {
            showResponse('member', `Error: ${result.detail}`, false);
        }
    } catch (error) {
        showResponse('member', `Error: ${error.message}`, false);
    }
}


async function setAvailability(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    const trainerId = data.trainer_id;
    delete data.trainer_id;
    
    try {
        const response = await fetch(`${API_BASE_URL}/trainers/${trainerId}/availability`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showResponse('trainer', 'Availability set successfully!', true);
            event.target.reset();
        } else {
            showResponse('trainer', `Error: ${result.detail}`, false);
        }
    } catch (error) {
        showResponse('trainer', `Error: ${error.message}`, false);
    }
}

// Member: Update Profile
async function updateProfile(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    const memberId = data.member_id;
    delete data.member_id;
    
    try {
        const response = await fetch(`${API_BASE_URL}/members/${memberId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showResponse('member', 'Profile updated successfully!', true);
            event.target.reset();
        } else {
            showResponse('member', `Error: ${result.detail}`, false);
        }
    } catch (error) {
        showResponse('member', `Error: ${error.message}`, false);
    }
}

// Member: View Dashboard
async function viewDashboard(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const memberId = formData.get('member_id');
    
    try {
        const response = await fetch(`${API_BASE_URL}/members/${memberId}/dashboard`);
        const result = await response.json();
        
        if (response.ok) {
            // Format dashboard data nicely
            let message = `<h4>Dashboard for Member ${memberId}</h4>`;
            message += `<p><strong>Health Metrics:</strong> Weight: ${result.health_metrics?.weight || 'N/A'} lbs, Heart Rate: ${result.health_metrics?.heart_rate || 'N/A'} bpm</p>`;
            message += `<p><strong>Active Goals:</strong> ${result.active_goals?.length || 0}</p>`;
            message += `<p><strong>Classes Attended:</strong> ${result.past_classes_attended || 0}</p>`;
            message += `<p><strong>Upcoming PT Sessions:</strong> ${result.upcoming_pt_sessions?.length || 0}</p>`;
            
            document.getElementById('member-response').innerHTML = message;
            document.getElementById('member-response').className = 'response success';
            document.getElementById('member-response').style.display = 'block';
        } else {
            showResponse('member', `Error: ${result.detail}`, false);
        }
    } catch (error) {
        showResponse('member', `Error: ${error.message}`, false);
    }
}

// Member: Register for Class
async function registerForClass(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    const memberId = data.member_id;
    delete data.member_id;
    
    try {
        const response = await fetch(`${API_BASE_URL}/members/${memberId}/class-registrations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showResponse('member', `Successfully registered for class!`, true);
            event.target.reset();
        } else {
            showResponse('member', `Error: ${result.detail}`, false);
        }
    } catch (error) {
        showResponse('member', `Error: ${error.message}`, false);
    }
}

// Member: Schedule PT Session
async function schedulePTSession(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    const memberId = data.member_id;
    delete data.member_id;
    delete data.notes; // Backend doesn't use notes
    
    try {
        const response = await fetch(`${API_BASE_URL}/members/${memberId}/pt-sessions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showResponse('member', `PT Session scheduled successfully!`, true);
            event.target.reset();
        } else {
            showResponse('member', `Error: ${result.detail}`, false);
        }
    } catch (error) {
        showResponse('member', `Error: ${error.message}`, false);
    }
}

// Trainer: View Schedule
async function viewSchedule(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const trainerId = formData.get('trainer_id');
    
    try {
        const response = await fetch(`${API_BASE_URL}/trainers/${trainerId}/schedule`);
        const result = await response.json();
        
        if (response.ok) {
            let message = `<h4>Schedule for Trainer ${trainerId}</h4>`;
            message += `<p><strong>PT Sessions:</strong> ${result.personal_training_sessions?.length || 0}</p>`;
            message += `<p><strong>Group Classes:</strong> ${result.group_classes?.length || 0}</p>`;
            
            document.getElementById('trainer-response').innerHTML = message;
            document.getElementById('trainer-response').className = 'response success';
            document.getElementById('trainer-response').style.display = 'block';
        } else {
            showResponse('trainer', `Error: ${result.detail}`, false);
        }
    } catch (error) {
        showResponse('trainer', `Error: ${error.message}`, false);
    }
}

// Admin: Create Group Class
async function createGroupClass(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    const adminId = 5; // Using admin user_id 5 from sample data
    
    try {
        const response = await fetch(`${API_BASE_URL}/admin/${adminId}/classes`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showResponse('admin', `Class created successfully! Class ID: ${result.class_id}`, true);
            event.target.reset();
        } else {
            showResponse('admin', `Error: ${result.detail}`, false);
        }
    } catch (error) {
        showResponse('admin', `Error: ${error.message}`, false);
    }
}

// Admin: Update Room Booking
async function updateRoomBooking(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    const adminId = data.admin_id;
    delete data.admin_id;
    
    try {
        const response = await fetch(`${API_BASE_URL}/admin/${adminId}/room-booking`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showResponse('admin', `Room booking updated successfully!`, true);
            event.target.reset();
        } else {
            showResponse('admin', `Error: ${result.detail}`, false);
        }
    } catch (error) {
        showResponse('admin', `Error: ${error.message}`, false);
    }
}