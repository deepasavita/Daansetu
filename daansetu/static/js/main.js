// DaanSetu - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if Bootstrap 5 is loaded
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    if (typeof bootstrap !== 'undefined') {
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Toggle password visibility in forms
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            const passwordField = document.querySelector(this.dataset.target);
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);
            
            // Toggle icon
            this.querySelector('i').classList.toggle('bi-eye');
            this.querySelector('i').classList.toggle('bi-eye-slash');
        });
    });
    
    // Form validation enhancement
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Enhance dropdown menus to be more mobile-friendly
    const dropdownMenus = document.querySelectorAll('.dropdown-menu');
    if (window.innerWidth < 768) {
        dropdownMenus.forEach(menu => {
            menu.classList.add('dropdown-menu-end');
        });
    }
    
    // Handle status filter buttons on donation tables
    const filterButtons = document.querySelectorAll('.filter-btn');
    if (filterButtons.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Remove active class from all buttons
                filterButtons.forEach(btn => {
                    btn.classList.remove('active');
                });
                
                // Add active class to clicked button
                this.classList.add('active');
                
                // Filter the table rows
                const filter = this.dataset.filter;
                const tableRows = document.querySelectorAll('table tbody tr[data-status]');
                
                tableRows.forEach(row => {
                    if (filter === 'all' || row.dataset.status === filter) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                });
            });
        });
    }
    
    // Handle sorting on donation tables
    const sortSelects = document.querySelectorAll('.sort-select');
    sortSelects.forEach(select => {
        select.addEventListener('change', function() {
            const tableId = this.dataset.table;
            const table = document.getElementById(tableId);
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            
            // Sort rows based on selected option value
            const sortBy = this.value;
            rows.sort((a, b) => {
                const aValue = a.querySelector(`[data-sort="${sortBy}"]`).textContent;
                const bValue = b.querySelector(`[data-sort="${sortBy}"]`).textContent;
                
                if (this.dataset.type === 'number') {
                    return parseFloat(aValue) - parseFloat(bValue);
                } else if (this.dataset.type === 'date') {
                    return new Date(aValue) - new Date(bValue);
                } else {
                    return aValue.localeCompare(bValue);
                }
            });
            
            // Reverse if descending order
            if (this.dataset.order === 'desc') {
                rows.reverse();
            }
            
            // Clear and append sorted rows
            rows.forEach(row => tbody.appendChild(row));
        });
    });
    
    // Role selection in registration form
    const roleSelect = document.getElementById('id_role');
    if (roleSelect) {
        const updateFormFields = () => {
            const selectedRole = roleSelect.value;
            const phoneField = document.querySelector('.phone-field-container');
            
            // Show phone field for volunteers
            if (selectedRole === 'volunteer') {
                phoneField.style.display = 'block';
                document.getElementById('id_phone').required = true;
            } else {
                phoneField.style.display = 'none';
                document.getElementById('id_phone').required = false;
            }
        };
        
        // Initial update
        updateFormFields();
        
        // Update on change
        roleSelect.addEventListener('change', updateFormFields);
    }
    
    // Animate elements when they come into view
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.animate-on-scroll');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementPosition < windowHeight - 50) {
                element.classList.add('animated');
            }
        });
    };
    
    // Initial check and attach scroll listener
    animateOnScroll();
    window.addEventListener('scroll', animateOnScroll);
});

// Function to confirm actions like deletions
function confirmAction(message) {
    return confirm(message || 'Are you sure you want to perform this action?');
}

// Format currency values
function formatCurrency(amount, currency = '₹') {
    return currency + parseFloat(amount).toFixed(2);
}

// Dynamically update counters on dashboard
function updateStats(elementId, newValue) {
    const element = document.getElementById(elementId);
    if (element) {
        // Animate counting up
        const currentValue = parseInt(element.textContent);
        const increment = Math.ceil((newValue - currentValue) / 20);
        let current = currentValue;
        
        const timer = setInterval(() => {
            current += increment;
            element.textContent = current;
            
            if ((increment > 0 && current >= newValue) || 
                (increment < 0 && current <= newValue)) {
                clearInterval(timer);
                element.textContent = newValue;
            }
        }, 30);
    }
}
