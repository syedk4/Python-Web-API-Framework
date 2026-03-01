// HTTPie-Python-Web Main JavaScript

// Utility Functions
const utils = {
    // Format file size
    formatSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    },

    // Format date
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    },

    // Show toast notification
    showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toastContainer') || createToastContainer();
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} alert-dismissible fade show`;
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 5000);
    },

    // Create toast container if it doesn't exist
    createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toastContainer';
        container.style.position = 'fixed';
        container.style.top = '20px';
        container.style.right = '20px';
        container.style.zIndex = '9999';
        container.style.maxWidth = '400px';
        document.body.appendChild(container);
        return container;
    }
};

// API Helper Functions
const api = {
    // Get configuration
    async getConfig() {
        try {
            const response = await fetch('/api/config');
            return await response.json();
        } catch (error) {
            console.error('Error fetching config:', error);
            return null;
        }
    },

    // Save configuration
    async saveConfig(configData) {
        try {
            const response = await fetch('/api/config', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(configData)
            });
            return await response.json();
        } catch (error) {
            console.error('Error saving config:', error);
            return { success: false, error: error.message };
        }
    },

    // Get test files
    async getTestFiles() {
        try {
            const response = await fetch('/api/test-files');
            return await response.json();
        } catch (error) {
            console.error('Error fetching test files:', error);
            return [];
        }
    },

    // Upload test file
    async uploadTestFile(file) {
        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch('/api/upload-test-file', {
                method: 'POST',
                body: formData
            });
            return await response.json();
        } catch (error) {
            console.error('Error uploading file:', error);
            return { success: false, error: error.message };
        }
    }
};

// Form Validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;

    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        }
    });

    return isValid;
}

// Auto-remove validation classes on input
document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            input.classList.remove('is-invalid', 'is-valid');
        });
    });
});

// File Upload Handler
function handleFileUpload(inputId, callback) {
    const input = document.getElementById(inputId);
    if (!input) return;

    input.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        // Validate file type
        const allowedTypes = ['text/csv', 'application/json'];
        if (!allowedTypes.includes(file.type) && !file.name.match(/\.(csv|json)$/i)) {
            utils.showToast('Invalid file type. Please upload CSV or JSON files only.', 'danger');
            input.value = '';
            return;
        }

        // Validate file size (max 16MB)
        if (file.size > 16 * 1024 * 1024) {
            utils.showToast('File too large. Maximum size is 16MB.', 'danger');
            input.value = '';
            return;
        }

        if (callback) {
            callback(file);
        }
    });
}

// Export utilities
window.utils = utils;
window.api = api;
window.validateForm = validateForm;
window.handleFileUpload = handleFileUpload;

console.log('HTTPie-Python-Web JavaScript loaded successfully');
