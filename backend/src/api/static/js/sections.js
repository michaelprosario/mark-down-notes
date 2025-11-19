/**
 * Section Management JavaScript
 * Handles CRUD operations for sections
 */

const SectionManager = {
    currentNotebookId: null,
    currentSectionId: null,
    
    /**
     * Initialize section management
     */
    init() {
        this.attachEventListeners();
    },
    
    /**
     * Attach event listeners
     */
    attachEventListeners() {
        document.getElementById('btnSaveSection')?.addEventListener('click', () => {
            this.saveSection();
        });
        
        document.getElementById('btnDeleteNotebook')?.addEventListener('click', () => {
            this.deleteCurrentNotebook();
        });
    },
    
    /**
     * Load sections for a notebook
     */
    async loadSections(notebookId) {
        this.currentNotebookId = notebookId;
        
        // Enable the "Add Section" and "Delete Notebook" buttons
        const btnNewSection = document.getElementById('btnNewSection');
        if (btnNewSection) {
            btnNewSection.removeAttribute('disabled');
        }
        
        const btnDeleteNotebook = document.getElementById('btnDeleteNotebook');
        if (btnDeleteNotebook) {
            btnDeleteNotebook.removeAttribute('disabled');
        }
        
        try {
            const response = await fetch(`/api/sections/?notebook_id=${notebookId}`);
            if (!response.ok) throw new Error('Failed to load sections');
            
            const sections = await response.json();
            this.renderSections(sections);
        } catch (error) {
            console.error('Error loading sections:', error);
        }
    },
    
    /**
     * Render sections list
     */
    renderSections(sections) {
        const placeholder = document.getElementById('sectionsPlaceholder');
        const list = document.getElementById('sectionsList');
        
        if (sections.length === 0) {
            placeholder?.classList.remove('d-none');
            list?.classList.add('d-none');
            if (window.PageManager) {
                PageManager.clearPages();
            }
            return;
        }
        
        placeholder?.classList.add('d-none');
        list?.classList.remove('d-none');
        
        if (list) {
            list.innerHTML = sections.map(section => `
                <li class="nav-item">
                    <button class="nav-link ${section.id === this.currentSectionId ? 'active' : ''}"
                            data-section-id="${section.id}"
                            onclick="SectionManager.selectSection('${section.id}')">
                        ${this.escapeHtml(section.name)}
                        <button class="btn btn-link btn-sm text-danger p-0 ms-2" 
                                onclick="SectionManager.deleteSection('${section.id}'); event.stopPropagation();"
                                title="Delete section">
                            <i class="bi bi-trash"></i>
                        </button>
                    </button>
                </li>
            `).join('');
        }
    },
    
    /**
     * Select a section
     */
    async selectSection(sectionId) {
        this.currentSectionId = sectionId;
        
        // Update active state
        document.querySelectorAll('#sectionsList .nav-link').forEach(item => {
            item.classList.toggle('active', item.dataset.sectionId === sectionId);
        });
        
        // Load pages for this section
        if (window.PageManager) {
            await PageManager.loadPages(sectionId);
        }
    },
    
    /**
     * Show section modal
     */
    showSectionModal() {
        const modal = document.getElementById('sectionModal');
        const form = document.getElementById('sectionForm');
        
        form.reset();
        document.getElementById('sectionId').value = '';
        document.getElementById('sectionNotebookId').value = this.currentNotebookId;
        document.getElementById('sectionModalLabel').textContent = 'Create Section';
        
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    },
    
    /**
     * Save section
     */
    async saveSection() {
        const form = document.getElementById('sectionForm');
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }
        
        const sectionId = document.getElementById('sectionId').value;
        const data = {
            notebook_id: document.getElementById('sectionNotebookId').value,
            name: document.getElementById('sectionName').value,
            display_order: parseInt(document.getElementById('sectionOrder').value) || 0
        };
        
        try {
            let response;
            if (sectionId) {
                // Update
                response = await fetch(`/api/sections/${sectionId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
            } else {
                // Create
                response = await fetch('/api/sections/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
            }
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to save section');
            }
            
            // Close modal properly
            const modalEl = document.getElementById('sectionModal');
            const modalInstance = bootstrap.Modal.getInstance(modalEl);
            if (modalInstance) {
                modalInstance.hide();
            }
            
            // Remove any lingering backdrops
            document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
            document.body.classList.remove('modal-open');
            document.body.style.removeProperty('overflow');
            document.body.style.removeProperty('padding-right');
            
            // Reload sections
            await this.loadSections(this.currentNotebookId);
            
            // Show success message
            if (window.AppManager) {
                AppManager.showSuccess(sectionId ? 'Section updated successfully' : 'Section created successfully');
            }
        } catch (error) {
            console.error('Error saving section:', error);
            
            // Close modal and cleanup even on error
            const modalEl = document.getElementById('sectionModal');
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
     * Delete the current notebook
     */
    deleteCurrentNotebook() {
        if (!this.currentNotebookId) return;
        
        if (window.NotebookManager) {
            NotebookManager.deleteNotebook(this.currentNotebookId);
        }
    },
    
    /**
     * Delete section
     */
    deleteSection(sectionId) {
        AppManager.showDeleteConfirmation(
            'Delete this section? (Note: Cannot delete if it contains pages)',
            async () => {
                try {
                    const response = await fetch(`/api/sections/${sectionId}`, {
                        method: 'DELETE'
                    });
                    
                    if (!response.ok) {
                        const error = await response.json();
                        throw new Error(error.detail || 'Failed to delete section');
                    }
                    
                    if (this.currentSectionId === sectionId) {
                        this.currentSectionId = null;
                        if (window.PageManager) {
                            PageManager.clearPages();
                        }
                    }
                    
                    await this.loadSections(this.currentNotebookId);
                } catch (error) {
                    console.error('Error deleting section:', error);
                    alert('Error: ' + error.message);
                }
            }
        );
    },
    
    /**
     * Clear sections UI
     */
    clearSections() {
        const placeholder = document.getElementById('sectionsPlaceholder');
        const list = document.getElementById('sectionsList');
        
        placeholder?.classList.remove('d-none');
        list?.classList.add('d-none');
        
        // Disable the "Add Section" and "Delete Notebook" buttons
        const btnNewSection = document.getElementById('btnNewSection');
        if (btnNewSection) {
            btnNewSection.setAttribute('disabled', 'disabled');
        }
        
        const btnDeleteNotebook = document.getElementById('btnDeleteNotebook');
        if (btnDeleteNotebook) {
            btnDeleteNotebook.setAttribute('disabled', 'disabled');
        }
        
        if (window.PageManager) {
            PageManager.clearPages();
        }
        
        this.currentNotebookId = null;
        this.currentSectionId = null;
    },
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    SectionManager.init();
    window.SectionManager = SectionManager;
    
    // Attach to new section button
    document.getElementById('btnNewSection')?.addEventListener('click', () => {
        SectionManager.showSectionModal();
    });
});

