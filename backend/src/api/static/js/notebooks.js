/**
 * Notebook Management JavaScript
 * Handles CRUD operations for notebooks
 */

const NotebookManager = {
    currentNotebookId: null,
    
    /**
     * Initialize notebook management
     */
    init() {
        this.attachEventListeners();
        this.loadNotebooks();
    },
    
    /**
     * Attach event listeners
     */
    attachEventListeners() {
        document.getElementById('btnSaveNotebook')?.addEventListener('click', () => {
            this.saveNotebook();
        });
    },
    
    /**
     * Load all notebooks
     */
    async loadNotebooks() {
        try {
            const response = await fetch('/api/notebooks/');
            if (!response.ok) throw new Error('Failed to load notebooks');
            
            const notebooks = await response.json();
            this.renderNotebooks(notebooks);
        } catch (error) {
            console.error('Error loading notebooks:', error);
        }
    },
    
    /**
     * Render notebooks list
     */
    renderNotebooks(notebooks) {
        const list = document.getElementById('notebooksList');
        if (!list) return;
        
        list.innerHTML = notebooks.map(notebook => `
            <a href="#" class="list-group-item list-group-item-action ${notebook.id === this.currentNotebookId ? 'active' : ''}"
               data-notebook-id="${notebook.id}"
               onclick="NotebookManager.selectNotebook('${notebook.id}'); return false;">
                <div class="d-flex justify-content-between align-items-center">
                    <span>
                        <i class="bi bi-journal-text me-2" style="color: ${this.escapeHtml(notebook.color)}"></i>
                        ${this.escapeHtml(notebook.name)}
                    </span>
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-link text-primary p-0 me-2" 
                                onclick="NotebookManager.editNotebook('${notebook.id}'); event.stopPropagation(); return false;"
                                title="Edit">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-link text-danger p-0" 
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
    async selectNotebook(notebookId) {
        this.currentNotebookId = notebookId;
        
        // Update active state
        document.querySelectorAll('#notebooksList .list-group-item').forEach(item => {
            item.classList.toggle('active', item.dataset.notebookId === notebookId);
        });
        
        // Load sections for this notebook
        if (window.SectionManager) {
            await SectionManager.loadSections(notebookId);
        }
    },
    
    /**
     * Show notebook modal for creating new notebook
     */
    showNotebookModal() {
        const modal = document.getElementById('notebookModal');
        const form = document.getElementById('notebookForm');
        
        form.reset();
        document.getElementById('notebookId').value = '';
        document.getElementById('notebookModalLabel').textContent = 'Create Notebook';
        
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    },
    
    /**
     * Edit a notebook
     */
    async editNotebook(notebookId) {
        try {
            const response = await fetch(`/api/notebooks/${notebookId}`);
            if (!response.ok) throw new Error('Failed to load notebook');
            
            const notebook = await response.json();
            
            document.getElementById('notebookId').value = notebook.id;
            document.getElementById('notebookName').value = notebook.name;
            document.getElementById('notebookColor').value = notebook.color;
            document.getElementById('notebookModalLabel').textContent = 'Edit Notebook';
            
            const modal = new bootstrap.Modal(document.getElementById('notebookModal'));
            modal.show();
        } catch (error) {
            console.error('Error loading notebook for edit:', error);
            alert('Error: ' + error.message);
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
            
            // Close modal properly
            const modalEl = document.getElementById('notebookModal');
            const modalInstance = bootstrap.Modal.getInstance(modalEl);
            if (modalInstance) {
                modalInstance.hide();
            }
            
            // Remove any lingering backdrops
            document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
            document.body.classList.remove('modal-open');
            document.body.style.removeProperty('overflow');
            document.body.style.removeProperty('padding-right');
            
            // Reload notebooks
            await this.loadNotebooks();
            
            // Show success message
            if (window.AppManager) {
                AppManager.showSuccess(notebookId ? 'Notebook updated successfully' : 'Notebook created successfully');
            }
        } catch (error) {
            console.error('Error saving notebook:', error);
            
            // Close modal and cleanup even on error
            const modalEl = document.getElementById('notebookModal');
            const modalInstance = bootstrap.Modal.getInstance(modalEl);
            if (modalInstance) {
                modalInstance.hide();
            }
            document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
            document.body.classList.remove('modal-open');
            document.body.style.removeProperty('overflow');
            document.body.style.removeProperty('padding-right');
            
            // Show error message
            if (window.AppManager) {
                AppManager.showError('Error: ' + error.message);
            } else {
                alert('Error: ' + error.message);
            }
        }
    },
    
    /**
     * Delete a notebook
     */
    deleteNotebook(notebookId) {
        AppManager.showDeleteConfirmation(
            'Delete this notebook and all its sections and pages?',
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
                        if (window.SectionManager) {
                            SectionManager.clearSections();
                        }
                    }
                    
                    await this.loadNotebooks();
                } catch (error) {
                    console.error('Error deleting notebook:', error);
                    alert('Error: ' + error.message);
                }
            }
        );
    },
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    NotebookManager.init();
    window.NotebookManager = NotebookManager;
    
    // Attach to new notebook button
    document.getElementById('btnNewNotebook')?.addEventListener('click', () => {
        NotebookManager.showNotebookModal();
    });
});

