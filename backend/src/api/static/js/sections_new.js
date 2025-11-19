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
    },
    
    /**
     * Load sections for a notebook
     */
    async loadSections(notebookId) {
        this.currentNotebookId = notebookId;
        
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
     * Render sections
     */
    renderSections(sections) {
        const placeholder = document.getElementById('sectionsPlaceholder');
        const list = document.getElementById('sectionsList');
        
        if (sections.length === 0) {
            placeholder?.classList.remove('d-none');
            list?.classList.add('d-none');
            if (placeholder) {
                placeholder.innerHTML = `
                    <i class="bi bi-collection" style="font-size: 3rem;"></i>
                    <p class="mt-2">No sections yet</p>
                    <button class="btn btn-sm btn-primary" data-bs-toggle="modal" data-bs-target="#sectionModal">
                        Create Section
                    </button>
                `;
            }
            return;
        }
        
        placeholder?.classList.add('d-none');
        list?.classList.remove('d-none');
        
        if (list) {
            list.innerHTML = sections.map(section => `
                <li class="nav-item mb-2">
                    <a class="nav-link ${section.id === this.currentSectionId ? 'active' : ''}" 
                       href="#" 
                       data-section-id="${section.id}"
                       onclick="SectionManager.selectSection('${section.id}'); return false;">
                        <div class="d-flex justify-content-between align-items-center">
                            <span>${this.escapeHtml(section.name)}</span>
                            <button class="btn btn-link btn-sm text-danger p-0" 
                                    onclick="SectionManager.deleteSection('${section.id}'); event.stopPropagation(); return false;">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </a>
                </li>
            `).join('');
        }
    },
    
    /**
     * Select a section
     */
    selectSection(sectionId) {
        this.currentSectionId = sectionId;
        
        // Update UI
        document.querySelectorAll('#sectionsList .nav-link').forEach(link => {
            link.classList.toggle('active', link.dataset.sectionId === sectionId);
        });
        
        // Enable page button
        document.getElementById('btnNewPage')?.removeAttribute('disabled');
        
        // Load pages
        if (window.PageManager) {
            window.PageManager.loadPages(sectionId);
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
        
        const data = {
            notebook_id: document.getElementById('sectionNotebookId').value,
            name: document.getElementById('sectionName').value,
            display_order: parseInt(document.getElementById('sectionOrder').value) || 0
        };
        
        try {
            const response = await fetch('/api/sections/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to save section');
            }
            
            bootstrap.Modal.getInstance(document.getElementById('sectionModal')).hide();
            await this.loadSections(this.currentNotebookId);
        } catch (error) {
            console.error('Error saving section:', error);
            alert('Error: ' + error.message);
        }
    },
    
    /**
     * Delete section
     */
    deleteSection(sectionId) {
        AppManager.showDeleteConfirmation(
            'Delete this section? All pages in this section will also be deleted.',
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
                        if (window.PageManager) window.PageManager.clearPages();
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
