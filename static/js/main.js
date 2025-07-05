// Main JavaScript file for AI Pitch Generator

// Global variables
window.currentPitchId = null;
window.isGenerating = false;

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Initialize the application
function initializeApp() {
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize alerts auto-dismiss
    initializeAlerts();
    
    // Initialize smooth scrolling
    initializeSmoothScrolling();
    
    // Add loading states to forms
    addLoadingStates();
    
    console.log('AI Pitch Generator initialized successfully');
}

// Form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Auto-dismiss alerts
function initializeAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert && alert.parentNode) {
                alert.classList.add('fade');
                setTimeout(() => {
                    alert.remove();
                }, 150);
            }
        }, 5000);
    });
}

// Smooth scrolling for anchor links
function initializeSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Add loading states to forms
function addLoadingStates() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            form.addEventListener('submit', function() {
                addLoadingState(submitBtn);
            });
        }
    });
}

// Utility Functions
function addLoadingState(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Loading...';
    button.disabled = true;
    
    // Remove loading state after 5 seconds (fallback)
    setTimeout(() => {
        removeLoadingState(button, originalText);
    }, 5000);
}

function removeLoadingState(button, originalText) {
    button.innerHTML = originalText;
    button.disabled = false;
}

// Show success message
function showSuccessMessage(message) {
    showAlert(message, 'success');
}

// Show error message
function showErrorMessage(message) {
    showAlert(message, 'danger');
}

// Show info message
function showInfoMessage(message) {
    showAlert(message, 'info');
}

// Generic alert function
function showAlert(message, type) {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
    alertContainer.innerHTML = `
        <i class="fas fa-${getAlertIcon(type)} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at the top of the main content area
    const mainContent = document.querySelector('main') || document.body;
    mainContent.insertBefore(alertContainer, mainContent.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertContainer && alertContainer.parentNode) {
            alertContainer.remove();
        }
    }, 5000);
}

// Get appropriate icon for alert type
function getAlertIcon(type) {
    const icons = {
        success: 'check-circle',
        danger: 'exclamation-triangle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// Copy text to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showSuccessMessage('Text copied to clipboard!');
    }, function(err) {
        showErrorMessage('Failed to copy text to clipboard');
        console.error('Could not copy text: ', err);
    });
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Validate email format
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Validate password strength
function validatePassword(password) {
    const minLength = 6;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);
    
    const errors = [];
    
    if (password.length < minLength) {
        errors.push(`Password must be at least ${minLength} characters long`);
    }
    
    if (!hasUpperCase) {
        errors.push('Password must contain at least one uppercase letter');
    }
    
    if (!hasLowerCase) {
        errors.push('Password must contain at least one lowercase letter');
    }
    
    if (!hasNumbers) {
        errors.push('Password must contain at least one number');
    }
    
    return {
        isValid: errors.length === 0,
        errors: errors
    };
}

// Debounce function for search inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function for scroll events
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// API call wrapper with error handling
async function apiCall(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// Local storage helpers
function saveToLocalStorage(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
        console.error('Failed to save to localStorage:', error);
    }
}

function loadFromLocalStorage(key) {
    try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : null;
    } catch (error) {
        console.error('Failed to load from localStorage:', error);
        return null;
    }
}

function removeFromLocalStorage(key) {
    try {
        localStorage.removeItem(key);
    } catch (error) {
        console.error('Failed to remove from localStorage:', error);
    }
}

// Animation helpers
function fadeIn(element, duration = 300) {
    element.style.opacity = '0';
    element.style.display = 'block';
    
    const start = performance.now();
    
    function animate(currentTime) {
        const elapsed = currentTime - start;
        const progress = elapsed / duration;
        
        if (progress < 1) {
            element.style.opacity = progress;
            requestAnimationFrame(animate);
        } else {
            element.style.opacity = '1';
        }
    }
    
    requestAnimationFrame(animate);
}

function fadeOut(element, duration = 300) {
    element.style.opacity = '1';
    
    const start = performance.now();
    
    function animate(currentTime) {
        const elapsed = currentTime - start;
        const progress = elapsed / duration;
        
        if (progress < 1) {
            element.style.opacity = 1 - progress;
            requestAnimationFrame(animate);
        } else {
            element.style.opacity = '0';
            element.style.display = 'none';
        }
    }
    
    requestAnimationFrame(animate);
}

// Export functions for use in other scripts
window.PitchGenerator = {
    showSuccessMessage,
    showErrorMessage,
    showInfoMessage,
    copyToClipboard,
    formatDate,
    validateEmail,
    validatePassword,
    debounce,
    throttle,
    apiCall,
    saveToLocalStorage,
    loadFromLocalStorage,
    removeFromLocalStorage,
    fadeIn,
    fadeOut
};

// Handle page visibility changes
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        // Page is hidden
        console.log('Page is hidden');
    } else {
        // Page is visible
        console.log('Page is visible');
    }
});

// Handle online/offline status
window.addEventListener('online', function() {
    showSuccessMessage('You are back online!');
});

window.addEventListener('offline', function() {
    showErrorMessage('You are offline. Some features may not work.');
});

// Performance monitoring
window.addEventListener('load', function() {
    const loadTime = performance.now();
    console.log(`Page loaded in ${loadTime.toFixed(2)}ms`);
});
