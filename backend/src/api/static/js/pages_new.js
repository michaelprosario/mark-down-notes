/**
 * Page Management JavaScript
 * Handles CRUD operations for pages
 */

const PageManager = {
    currentSectionId: null,
    currentPageId: null,
    
    /**
     * Initialize page management
     */
    init() {
        this.attachEventListeners();
    },
    
    /**
     * Attach event listeners
     */
    attachEventListeners() {
        document.getElementById('btnSavePage')?.addEventListener('click', () => {
            this.savePage();
        });
        
        document.getElementById('btnEditPage')?.addEventListener('click', () => {
            this.editCurrentPage();
        });
        
        document.getElementById('btnDeletePageBtn')?.addEventListener('click', () => {
            if (this.currentPageId) {
                this.deletePage(this.currentPageId);
            }
        });
    },
    
    /**
     * Load pages for a section
     */
    async loadPages(sectionId) {
        this.currentSectionId = sectionId;
        
        try {
            const response = await fetch(`/api/pages/?section_id=${sectionId}`);
            if (!response.ok) throw new Error('Failed to load pages');
            
            const pages = await response.json();
            this.renderPagesList(pages);
        } catch (error) {
            console.error('Error loading pages:', error);
        }
    },
    
    /**
     * Render pages list
     */
    renderPagesList(pages) {
        const placeholder = document.getElementById('pagesPlaceholder');
        const list = document.getElementById('pagesList');
        
        if (pages.length === 0) {
            placeholder?.classList.remove('d-none');
            list?.classList.add('d-none');
            return;
        }
        
        placeholder?.classList.add('d-none');
        list?.classList.remove('d-none');
        
        if (list) {
            list.innerHTML = pages.map(page => `
                <a href="#" class="list-group-item list-group-item-action ${page.id === this.currentPageId ? 'active' : ''}"
                   data-page-id="${page.id}"
                   onclick="PageManager.selectPage('${page.id}'); return false;">
                    <div class="d-flex justify-content-between align-items-center">
                        <span><i class="bi bi-file-earmark-text me-2"></i>${this.escapeHtml(page.title)}</span>
                        <button class="btn btn-link btn-sm text-danger p-0" 
                                onclick="PageManager.deletePage('${page.id}'); event.stopPropagation(); return false;">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </a>
            `).join('');
        }
    },
    
    /**
     * Select and display a page
     */
    async selectPage(pageId) {
        try {
            const response = await fetch(`/api/pages/${pageId}`);
            if (!response.ok) throw new Error('Failed to load page');
            
            const page = await response.json();
            this.currentPageId = pageId;
            this.displayPage(page);
            
            // Update active state
            document.querySelectorAll('#pagesList .list-group-item').forEach(item => {
                item.classList.toggle('active', item.dataset.pageId === pageId);
            });
        } catch (error) {
            console.error('Error loading page:', error);
        }
    },
    
    /**
     * Display page content
     */
    displayPage(page) {
        const welcomeScreen = document.getElementById('welcomeScreen');
        const pageEditor = document.getElementById('pageEditor');
        
        welcomeScreen?.classList.add('d-none');
        pageEditor?.classList.remove('d-none');
        
        document.getElementById('currentPageTitle').textContent = page.title;
        document.getElementById('pageMetadata').textContent = 
            `Last updated: ${new Date(page.updated_at).toLocaleString()}`;
        
        // Render markdown content (simple conversion for now)
        const content = document.getElementById('pageContent');
        if (content) {
            content.innerHTML = this.renderMarkdown(page.content);
        }
    },
    
    /**
     * Simple markdown rendering
     */
    renderMarkdown(markdown) {
        if (!markdown) return '';
        
        let html = this.escapeHtml(markdown);
        
        // Headers
        html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
        html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
        html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');
        
        // Bold and italic
        html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
        
        // Code blocks
        html = html.replace(/```(.+?)```/gs, '<pre><code>$1</code></pre>');
        html = html.replace(/`(.+?)`/g, '<code>$1</code>');
        
        // Links
        html = html.replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2" target="_blank">$1</a>');
        
        // Line breaks
        html = html.replace(/\n/g, '<br>');
        
        return html;
    },
    
    /**
     * Show page modal
     */
    showPageModal() {
        const modal = document.getElementById('pageModal');
        const form = document.getElementById('pageForm');
        
        form.reset();
        document.getElementById('pageId').value = '';
        document.getElementById('pageSectionId').value = this.currentSectionId;
        document.getElementById('pageModalLabel').textContent = 'Create Page';
        
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    },
    
    /**
     * Edit current page
     */
    async editCurrentPage() {
        if (!this.currentPageId) return;
        
        try {
            const response = await fetch(`/api/pages/${this.currentPageId}`);
            if (!response.ok) throw new Error('Failed to load page');
            
            const page = await response.json();
            
            document.getElementById('pageId').value = page.id;
            document.getElementById('pageSectionId').value = page.section_id;
            document.getElementById('pageTitle').value = page.title;
            document.getElementById('pageContent').value = page.content;
            document.getElementById('pageOrder').value = page.display_order;
            document.getElementById('pageModalLabel').textContent = 'Edit Page';
            
            const modal = new bootstrap.Modal(document.getElementById('pageModal'));
            modal.show();
        } catch (error) {
            console.error('Error loading page for edit:', error);
            alert('Error: ' + error.message);
        }
    },
    
    /**
     * Save page
     */
    async savePage() {
        const form = document.getElementById('pageForm');
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }
        
        const pageId = document.getElementById('pageId').value;
        const data = {
            section_id: document.getElementById('pageSectionId').value,
            title: document.getElementById('pageTitle').value,
            content: document.getElementById('pageContent').value,
            display_order: parseInt(document.getElementById('pageOrder').value) || 0
        };
        
        try {
            let response;
            if (pageId) {
                // Update
                response = await fetch(`/api/pages/${pageId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
            } else {
                // Create
                response = await fetch('/api/pages/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
            }
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to save page');
            }
            
            bootstrap.Modal.getInstance(document.getElementById('pageModal')).hide();
            await this.loadPages(this.currentSectionId);
            
            if (!pageId) {
                const newPage = await response.json();
                this.selectPage(newPage.id);
            } else {
                this.selectPage(pageId);
            }
        } catch (error) {
            console.error('Error saving page:', error);
            alert('Error: ' + error.message);
        }
    },
    
    /**
     * Delete page
     */
    deletePage(pageId) {
        AppManager.showDeleteConfirmation(
            'Delete this page?',
            async () => {
                try {
                    const response = await fetch(`/api/pages/${pageId}`, {
                        method: 'DELETE'
                    });
                    
                    if (!response.ok) {
                        const error = await response.json();
                        throw new Error(error.detail || 'Failed to delete page');
                    }
                    
                    if (this.currentPageId === pageId) {
                        this.currentPageId = null;
                        document.getElementById('welcomeScreen')?.classList.remove('d-none');
                        document.getElementById('pageEditor')?.classList.add('d-none');
                    }
                    
                    await this.loadPages(this.currentSectionId);
                } catch (error) {
                    console.error('Error deleting page:', error);
                    alert('Error: ' + error.message);
                }
            }
        );
    },
    
    /**
     * Clear pages UI
     */
    clearPages() {
        const placeholder = document.getElementById('pagesPlaceholder');
        const list = document.getElementById('pagesList');
        
        placeholder?.classList.remove('d-none');
        list?.classList.add('d-none');
        
        document.getElementById('welcomeScreen')?.classList.remove('d-none');
        document.getElementById('pageEditor')?.classList.add('d-none');
        
        this.currentSectionId = null;
        this.currentPageId = null;
    },
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    PageManager.init();
    window.PageManager = PageManager;
    
    // Attach to new page button
    document.getElementById('btnNewPage')?.addEventListener('click', () => {
        PageManager.showPageModal();
    });
});
