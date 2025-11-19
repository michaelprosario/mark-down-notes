/**
 * Notebook Management JavaScript
 * Handles CRUD operations for notebooks using the services-based API
 */

const NotebookManager = {
    currentNotebookId: null,
    
    /**
     * Initialize notebook management
     */
    init() {
        this.loadNotebooks();
        this.attachEventListeners();
    },
    
    /**
     * Attach event listeners
     */
    attachEventListeners() {
        // Save notebook button
        document.getElementById('btnSaveNotebook')?.addEventListener('click', () => {
            this.saveNotebook();
        });
        
        // New notebook button
        document.getElementById('btnNewNotebook')?.addEventListener('click', () => {
            this.showNotebookModal();
        });
    },
    
    /**
     * Load all notebooks from API
     */
    async loadNotebooks() {
        try {
            const response = await fetch('/api/notebooks/');
            if (!response.ok) throw new Error('Failed to load notebooks');
            
            const notebooks = await response.json();
            this.renderNotebooks(notebooks);
        } catch (error) {
            console.error('Error loading notebooks:', error);
            this.showError('Failed to load notebooks');
        }
    },
    
    /**
     * Render notebooks in sidebar
     */
    renderNotebooks(notebooks) {
        const container = document.getElementById('notebooksList');
        if (!container) return;
        
        if (notebooks.length === 0) {
            container.innerHTML = `
                <div class="text-center text-muted p-4">
                    <i class="bi bi-journal-text" style="font-size: 3rem;"></i>
                    <p class="mt-2">No notebooks yet</p>
                    <button class="btn btn-sm btn-outline-primary" data-bs-toggle="modal" data-bs-target="#notebookModal">
                        Create First Notebook
                    </button>
                </div>
            `;
            return;
        }
        
        container.innerHTML = notebooks.map(notebook => `
            <a href="#" class="list-group-item list-group-item-action ${notebook.id === this.currentNotebookId ? 'active' : ''}"
               data-notebook-id="${notebook.id}"
               onclick="NotebookManager.selectNotebook('${notebook.id}'); return false;">
                <div class="d-flex justify-content-between align-items-center">
                    <div class="d-flex align-items-center">
                        <span class="badge rounded-circle me-2" style="width: 12px; height: 12px; background-color: ${notebook.color};"></span>
                        <span>${this.escapeHtml(notebook.name)}</span>
                    </div>
                    <div class="btn-group btn-group-sm" role="group">
                        <button class="btn btn-link btn-sm text-secondary p-0 me-2" 
                                onclick="NotebookManager.editNotebook('${notebook.id}'); event.stopPropagation(); return false;"
                                title="Edit">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-link btn-sm text-danger p-0" 
                                onclick="NotebookManager.deleteNotebook('${notebook.id}'); event.stopPropagation(); return false;"
                                title="Delete">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </div>
            </a>
        `).join('');
    },
    
    /**
     * Select a notebook
     */
    selectNotebook(notebookId) {
        this.currentNotebookId = notebookId;
        
        // Update UI
        document.querySelectorAll('#notebooksList .list-group-item').forEach(item => {
            item.classList.toggle('active', item.dataset.notebookId === notebookId);
        });
        
        // Enable section button
        document.getElementById('btnNewSection')?.removeAttribute('disabled');
        
        // Load sections for this notebook
        if (window.SectionManager) {
            window.SectionManager.loadSections(notebookId);
        }
    },
    
    /**
     * Show notebook modal for create/edit
     */
    showNotebookModal(notebookId = null) {
        const modal = document.getElementById('notebookModal');
        const modalTitle = document.getElementById('notebookModalLabel');
        const form = document.getElementById('notebookForm');
        
        if (notebookId) {
            // Edit mode
            modalTitle.textContent = 'Edit Notebook';
            this.loadNotebookForEdit(notebookId);
        } else {
            // Create mode
            modalTitle.textContent = 'Create Notebook';
            form.reset();
            document.getElementById('notebookId').value = '';
            document.getElementById('notebookColor').value = '#0078D4';
        }
        
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    },
    
    /**
     * Load notebook data for editing
     */
    async loadNotebookForEdit(notebookId) {
        try {
            const response = await fetch(`/api/notebooks/${notebookId}`);
            if (!response.ok) throw new Error('Failed to load notebook');
            
            const notebook = await response.json();
            document.getElementById('notebookId').value = notebook.id;
            document.getElementById('notebookName').value = notebook.name;
            document.getElementById('notebookColor').value = notebook.color;
        } catch (error) {
            console.error('Error loading notebook:', error);
            this.showError('Failed to load notebook');
        }
    },
    
    /**
     * Save notebook (create or update)
     */
    async saveNotebook() {
        const form = document.getElementById('notebookForm');
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }
        
        const notebookId = document.getElementById('notebookId').value;
        const data = {
            name: document.getElementById('notebookName').value,
            color: document.getElementById('notebookColor').value
        };
        
        try {
            let response;
            if (notebookId) {
                // Update
                response = await fetch(`/api/notebooks/${notebookId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
            } else {
                // Create
                response = await fetch('/api/notebooks/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
            }
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to save notebook');
            }
            
            // Close modal and reload
            bootstrap.Modal.getInstance(document.getElementById('notebookModal')).hide();
            await this.loadNotebooks();
            
            if (!notebookId && response.ok) {
                const newNotebook = await response.json();
                this.selectNotebook(newNotebook.id);
            }
        } catch (error) {
            console.error('Error saving notebook:', error);
            this.showError(error.message);
        }
    },
    
    /**
     * Edit notebook
     */
    editNotebook(notebookId) {
        this.showNotebookModal(notebookId);
    },
    
    /**
     * Delete notebook
     */
    deleteNotebook(notebookId) {
        AppManager.showDeleteConfirmation(
            'Are you sure you want to delete this notebook? All sections and pages will also be deleted.',
            async () => {
                try {
                    const response = await fetch(`/api/notebooks/${notebookId}`, {
                        method: 'DELETE'
                    });
                    
                    if (!response.ok) {
                        const error = await response.json();
                        throw new Error(error.detail || 'Failed to delete notebook');
                    }
                    
                    if (this.currentNotebookId === notebookId) {
                        this.currentNotebookId = null;
                        if (window.SectionManager) window.SectionManager.clearSections();
                        if (window.PageManager) window.PageManager.clearPages();
                    }
                    
                    await this.loadNotebooks();
                } catch (error) {
                    console.error('Error deleting notebook:', error);
                    this.showError(error.message);
                }
            }
        );
    },
    
    /**
     * Show error message
     */
    showError(message) {
        // Simple alert for now - could be replaced with toast notifications
        alert('Error: ' + message);
    },
    
    /**
     * Escape HTML to prevent XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    NotebookManager.init();
});
