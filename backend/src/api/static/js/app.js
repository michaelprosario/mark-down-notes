// Main application JavaScript

class App {
    constructor() {
        this.apiBaseUrl = '/api';
        this.currentNotebook = null;
        this.currentSection = null;
        this.currentPage = null;
        this.init();
    }

    init() {
        console.log('Notebook Management App initialized');
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Global event listeners
        document.addEventListener('DOMContentLoaded', () => {
            console.log('DOM loaded');
        });
    }

    async apiCall(endpoint, options = {}) {
        try {
            const response = await fetch(`${this.apiBaseUrl}${endpoint}`, {
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
            this.showError(error.message);
            throw error;
        }
    }

    showError(message) {
        // TODO: Implement toast notifications
        console.error('Error:', message);
        alert(`Error: ${message}`);
    }

    showSuccess(message) {
        // TODO: Implement toast notifications
        console.log('Success:', message);
    }

    showSaveIndicator(status = 'saved') {
        const indicator = document.getElementById('saveIndicator');
        if (!indicator) {
            const div = document.createElement('div');
            div.id = 'saveIndicator';
            div.className = 'save-indicator';
            document.body.appendChild(div);
        }

        const elem = document.getElementById('saveIndicator');
        elem.className = `save-indicator ${status}`;
        
        switch(status) {
            case 'saving':
                elem.textContent = 'Saving...';
                break;
            case 'saved':
                elem.textContent = 'Saved ✓';
                break;
            case 'error':
                elem.textContent = 'Save failed ✗';
                break;
        }

        elem.classList.add('show');
        
        if (status !== 'saving') {
            setTimeout(() => {
                elem.classList.remove('show');
            }, 2000);
        }
    }

    confirmDelete(itemType, itemName) {
        return confirm(`Are you sure you want to delete ${itemType} "${itemName}"? This action cannot be undone.`);
    }
}

// Initialize app
const app = new App();
