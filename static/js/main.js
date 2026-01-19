// Main JavaScript for Quiz Platform

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Quiz timer functionality
    const timerElement = document.getElementById('quiz-timer');
    if (timerElement) {
        const timeLimit = parseInt(timerElement.dataset.timeLimit);
        const startTime = new Date(timerElement.dataset.startTime);
        
        function updateTimer() {
            const now = new Date();
            const elapsed = Math.floor((now - startTime) / 1000);
            const remaining = (timeLimit * 60) - elapsed;
            
            if (remaining <= 0) {
                // Time's up - auto-submit form
                document.getElementById('quiz-form').submit();
                return;
            }
            
            const minutes = Math.floor(remaining / 60);
            const seconds = remaining % 60;
            
            timerElement.textContent = `Time: ${minutes}:${seconds.toString().padStart(2, '0')}`;
            
            // Warning colors
            if (remaining <= 60) {
                timerElement.className = 'timer danger';
            } else if (remaining <= 300) {
                timerElement.className = 'timer warning';
            }
        }
        
        updateTimer();
        setInterval(updateTimer, 1000);
    }
    
    // Confirm before deleting
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
    
    // Auto-save quiz progress
    const quizForm = document.getElementById('quiz-form');
    if (quizForm && quizForm.dataset.autosave === 'true') {
        let saveTimeout;
        const inputs = quizForm.querySelectorAll('input, textarea');
        
        inputs.forEach(function(input) {
            input.addEventListener('change', function() {
                clearTimeout(saveTimeout);
                saveTimeout = setTimeout(function() {
                    saveProgress();
                }, 2000);
            });
        });
        
        function saveProgress() {
            const formData = new FormData(quizForm);
            const data = {};
            formData.forEach((value, key) => {
                if (data[key]) {
                    if (!Array.isArray(data[key])) {
                        data[key] = [data[key]];
                    }
                    data[key].push(value);
                } else {
                    data[key] = value;
                }
            });
            
            localStorage.setItem('quiz_progress_' + quizForm.dataset.quizId, JSON.stringify(data));
            
            // Show saved indicator
            const indicator = document.createElement('div');
            indicator.className = 'alert alert-success position-fixed top-0 end-0 m-3';
            indicator.textContent = 'Progress saved';
            document.body.appendChild(indicator);
            
            setTimeout(function() {
                indicator.remove();
            }, 2000);
        }
    }
    
    // Live search functionality
    const searchInput = document.getElementById('live-search');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const items = document.querySelectorAll('[data-searchable]');
            
            items.forEach(function(item) {
                const text = item.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
    
    // Form validation enhancement
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // Character counter for textareas
    const textareas = document.querySelectorAll('textarea[data-max-length]');
    textareas.forEach(function(textarea) {
        const maxLength = parseInt(textarea.dataset.maxLength);
        const counter = document.createElement('div');
        counter.className = 'text-muted small mt-1';
        textarea.parentNode.appendChild(counter);
        
        function updateCounter() {
            const remaining = maxLength - textarea.value.length;
            counter.textContent = `${remaining} characters remaining`;
            if (remaining < 0) {
                counter.className = 'text-danger small mt-1';
            } else {
                counter.className = 'text-muted small mt-1';
            }
        }
        
        textarea.addEventListener('input', updateCounter);
        updateCounter();
    });
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // Quiz confirmation before submit
    const quizSubmitBtn = document.getElementById('quiz-submit-btn');
    if (quizSubmitBtn) {
        quizSubmitBtn.addEventListener('click', function(e) {
            const unanswered = document.querySelectorAll('.question-container').length;
            const answered = document.querySelectorAll('input:checked').length;
            
            if (answered < unanswered) {
                if (!confirm(`You have answered ${answered} out of ${unanswered} questions. Submit anyway?`)) {
                    e.preventDefault();
                }
            }
        });
    }
    
    // Initialize tooltips
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(function(tooltip) {
        new bootstrap.Tooltip(tooltip);
    });
    
    // Initialize popovers
    const popovers = document.querySelectorAll('[data-bs-toggle="popover"]');
    popovers.forEach(function(popover) {
        new bootstrap.Popover(popover);
    });
});

// Utility function for AJAX requests
function fetchJSON(url, options = {}) {
    return fetch(url, {
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            ...options.headers
        },
        ...options
    }).then(response => response.json());
}
