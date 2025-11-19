/**
 * Tree View Application
 * Main application logic for the tree-view based note-taking app
 */

// Global state
const AppState = {
    notebooks: [],
    sections: [],
    pages: [],
    currentNotebookId: null,
    currentSectionId: null,
    currentPageId: null,
    markdownEditor: null,
    isDirty: false
};

// Utility functions
const Utils = {
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },
    
    formatDate(dateString) {
        if (!dateString) return 'Never';
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        
        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
        
        const diffHours = Math.floor(diffMins / 60);
        if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
        
        const diffDays = Math.floor(diffHours / 24);
        if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
        
        return date.toLocaleDateString();
    },
    
    showModal(modalId) {
        document.getElementById(modalId).style.display = 'flex';
    },
    
    hideModal(modalId) {
        document.getElementById(modalId).style.display = 'none';
    },
    
    showError(message) {
        alert('Error: ' + message);
    },
    
    showSuccess(message) {
        console.log('Success:', message);
    }
};

// Notebook Management
const NotebookManager = {
    async loadNotebooks() {
        try {
            const response = await fetch('/api/notebooks/');
            if (!response.ok) throw new Error('Failed to load notebooks');
            
            AppState.notebooks = await response.json();
            this.renderNotebooks();
        } catch (error) {
            console.error('Error loading notebooks:', error);
            Utils.showError('Failed to load notebooks');
        }
    },
    
    renderNotebooks() {
        const container = document.getElementById('notebooksList');
        
        if (AppState.notebooks.length === 0) {
            container.innerHTML = '<div class="empty-state">No notebooks yet. Create one to get started.</div>';
            return;
        }
        
        container.innerHTML = AppState.notebooks.map(notebook => `
            <div class="notebook-item ${notebook.id === AppState.currentNotebookId ? 'active' : ''}"
                 data-notebook-id="${notebook.id}"
                 onclick="NotebookManager.selectNotebook('${notebook.id}')">
                <i class="bi bi-journal-text"></i>
                <span style="flex: 1;">${Utils.escapeHtml(notebook.name)}</span>
                <div class="tree-actions">
                    <button class="tree-action-btn" onclick="NotebookManager.editNotebook('${notebook.id}'); event.stopPropagation();" title="Edit">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="tree-action-btn delete" onclick="NotebookManager.deleteNotebook('${notebook.id}'); event.stopPropagation();" title="Delete">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </div>
        `).join('');
    },
    
    async selectNotebook(notebookId) {
        AppState.currentNotebookId = notebookId;
        AppState.currentSectionId = null;
        AppState.currentPageId = null;
        
        const notebook = AppState.notebooks.find(n => n.id === notebookId);
        if (notebook) {
            document.getElementById('currentNotebookTitle').textContent = notebook.name;
        }
        
        this.renderNotebooks();
        document.getElementById('btnNewSection').removeAttribute('disabled');
        
        await TreeViewManager.loadTreeView(notebookId);
    },
    
    showCreateModal() {
        document.getElementById('notebookModalTitle').textContent = 'Create Notebook';
        document.getElementById('notebookForm').reset();
        document.getElementById('notebookId').value = '';
        Utils.showModal('notebookModal');
    },
    
    async editNotebook(notebookId) {
        const notebook = AppState.notebooks.find(n => n.id === notebookId);
        if (!notebook) return;
        
        document.getElementById('notebookModalTitle').textContent = 'Edit Notebook';
        document.getElementById('notebookId').value = notebook.id;
        document.getElementById('notebookName').value = notebook.name;
        document.getElementById('notebookDescription').value = notebook.description || '';
        Utils.showModal('notebookModal');
    },
    
    async saveNotebook(event) {
        event.preventDefault();
        
        const id = document.getElementById('notebookId').value;
        const name = document.getElementById('notebookName').value;
        const description = document.getElementById('notebookDescription').value;
        
        const data = { name, description };
        
        try {
            let response;
            if (id) {
                response = await fetch(`/api/notebooks/${id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
            } else {
                response = await fetch('/api/notebooks/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
            }
            
            if (!response.ok) throw new Error('Failed to save notebook');
            
            Utils.hideModal('notebookModal');
            await this.loadNotebooks();
            Utils.showSuccess('Notebook saved successfully');
        } catch (error) {
            console.error('Error saving notebook:', error);
            Utils.showError('Failed to save notebook');
        }
    },
    
    async deleteNotebook(notebookId) {
        const notebook = AppState.notebooks.find(n => n.id === notebookId);
        if (!notebook) return;
        
        document.getElementById('deleteMessage').textContent = 
            `Are you sure you want to delete "${notebook.name}"? This will also delete all sections and pages within it.`;
        
        AppState.deleteCallback = async () => {
            try {
                const response = await fetch(`/api/notebooks/${notebookId}`, {
                    method: 'DELETE'
                });
                
                if (!response.ok) throw new Error('Failed to delete notebook');
                
                if (AppState.currentNotebookId === notebookId) {
                    AppState.currentNotebookId = null;
                    AppState.currentSectionId = null;
                    AppState.currentPageId = null;
                    TreeViewManager.clearTreeView();
                    EditorManager.hideEditor();
                }
                
                await this.loadNotebooks();
                Utils.showSuccess('Notebook deleted successfully');
            } catch (error) {
                console.error('Error deleting notebook:', error);
                Utils.showError('Failed to delete notebook');
            }
        };
        
        Utils.showModal('deleteModal');
    }
};

// Tree View Management
const TreeViewManager = {
    async loadTreeView(notebookId) {
        try {
            // Load sections
            const sectionsResponse = await fetch(`/api/sections/?notebook_id=${notebookId}`);
            if (!sectionsResponse.ok) throw new Error('Failed to load sections');
            AppState.sections = await sectionsResponse.json();
            
            // Load all pages for this notebook
            const pagesPromises = AppState.sections.map(section =>
                fetch(`/api/pages/?section_id=${section.id}`).then(r => r.json())
            );
            
            const pagesArrays = await Promise.all(pagesPromises);
            AppState.pages = pagesArrays.flat();
            
            this.renderTreeView();
        } catch (error) {
            console.error('Error loading tree view:', error);
            Utils.showError('Failed to load tree view');
        }
    },
    
    renderTreeView() {
        const container = document.getElementById('treeViewContainer');
        const emptyState = document.getElementById('treeEmptyState');
        
        if (AppState.sections.length === 0) {
            emptyState.style.display = 'block';
            emptyState.textContent = 'No sections yet. Create a section to get started.';
            container.querySelectorAll('.tree-node').forEach(n => n.remove());
            return;
        }
        
        emptyState.style.display = 'none';
        
        const treeHTML = AppState.sections.map(section => {
            const sectionPages = AppState.pages.filter(p => p.section_id === section.id);
            const hasPages = sectionPages.length > 0;
            
            return `
                <div class="tree-node tree-section" data-section-id="${section.id}">
                    <div class="tree-node-header" onclick="TreeViewManager.toggleSection('${section.id}')">
                        <i class="bi bi-chevron-right tree-toggle ${hasPages ? '' : 'hidden'}" id="toggle-${section.id}"></i>
                        <i class="bi bi-folder tree-icon"></i>
                        <span class="tree-label">${Utils.escapeHtml(section.name)}</span>
                        <div class="tree-actions">
                            <button class="tree-action-btn" onclick="SectionManager.showCreatePageModal('${section.id}'); event.stopPropagation();" title="New Page">
                                <i class="bi bi-file-earmark-plus"></i>
                            </button>
                            <button class="tree-action-btn" onclick="SectionManager.editSection('${section.id}'); event.stopPropagation();" title="Edit">
                                <i class="bi bi-pencil"></i>
                            </button>
                            <button class="tree-action-btn delete" onclick="SectionManager.deleteSection('${section.id}'); event.stopPropagation();" title="Delete">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </div>
                    <div class="tree-children" id="children-${section.id}">
                        ${sectionPages.map(page => `
                            <div class="tree-node tree-page" data-page-id="${page.id}">
                                <div class="tree-node-header ${page.id === AppState.currentPageId ? 'selected' : ''}"
                                     onclick="PageManager.selectPage('${page.id}')">
                                    <i class="bi bi-chevron-right tree-toggle hidden"></i>
                                    <i class="bi bi-file-earmark-text tree-icon"></i>
                                    <span class="tree-label">${Utils.escapeHtml(page.title)}</span>
                                    <div class="tree-actions">
                                        <button class="tree-action-btn delete" onclick="PageManager.deletePage('${page.id}'); event.stopPropagation();" title="Delete">
                                            <i class="bi bi-trash"></i>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }).join('');
        
        const existingNodes = container.querySelectorAll('.tree-node');
        existingNodes.forEach(n => n.remove());
        container.insertAdjacentHTML('beforeend', treeHTML);
    },
    
    toggleSection(sectionId) {
        const toggle = document.getElementById(`toggle-${sectionId}`);
        const children = document.getElementById(`children-${sectionId}`);
        
        if (toggle && children && !toggle.classList.contains('hidden')) {
            toggle.classList.toggle('expanded');
            children.classList.toggle('expanded');
        }
    },
    
    collapseAll() {
        document.querySelectorAll('.tree-toggle.expanded').forEach(toggle => {
            toggle.classList.remove('expanded');
        });
        document.querySelectorAll('.tree-children.expanded').forEach(children => {
            children.classList.remove('expanded');
        });
    },
    
    clearTreeView() {
        const container = document.getElementById('treeViewContainer');
        const emptyState = document.getElementById('treeEmptyState');
        
        container.querySelectorAll('.tree-node').forEach(n => n.remove());
        emptyState.style.display = 'block';
        emptyState.textContent = 'Select a notebook to view its contents';
        
        document.getElementById('currentNotebookTitle').textContent = 'Work Projects';
        document.getElementById('btnNewSection').setAttribute('disabled', 'disabled');
    }
};

// Section Management
const SectionManager = {
    showCreateModal() {
        if (!AppState.currentNotebookId) {
            Utils.showError('Please select a notebook first');
            return;
        }
        
        document.getElementById('sectionModalTitle').textContent = 'Create Section';
        document.getElementById('sectionForm').reset();
        document.getElementById('sectionId').value = '';
        document.getElementById('sectionNotebookId').value = AppState.currentNotebookId;
        Utils.showModal('sectionModal');
    },
    
    async editSection(sectionId) {
        const section = AppState.sections.find(s => s.id === sectionId);
        if (!section) return;
        
        document.getElementById('sectionModalTitle').textContent = 'Edit Section';
        document.getElementById('sectionId').value = section.id;
        document.getElementById('sectionNotebookId').value = section.notebook_id;
        document.getElementById('sectionName').value = section.name;
        document.getElementById('sectionDescription').value = section.description || '';
        Utils.showModal('sectionModal');
    },
    
    async saveSection(event) {
        event.preventDefault();
        
        const id = document.getElementById('sectionId').value;
        const notebookId = document.getElementById('sectionNotebookId').value;
        const name = document.getElementById('sectionName').value;
        const description = document.getElementById('sectionDescription').value;
        
        const data = { 
            notebook_id: notebookId,
            name, 
            description,
            order_index: AppState.sections.length
        };
        
        try {
            let response;
            if (id) {
                response = await fetch(`/api/sections/${id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
            } else {
                response = await fetch('/api/sections/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
            }
            
            if (!response.ok) throw new Error('Failed to save section');
            
            Utils.hideModal('sectionModal');
            await TreeViewManager.loadTreeView(AppState.currentNotebookId);
            Utils.showSuccess('Section saved successfully');
        } catch (error) {
            console.error('Error saving section:', error);
            Utils.showError('Failed to save section');
        }
    },
    
    async deleteSection(sectionId) {
        const section = AppState.sections.find(s => s.id === sectionId);
        if (!section) return;
        
        document.getElementById('deleteMessage').textContent = 
            `Are you sure you want to delete "${section.name}"? This will also delete all pages within it.`;
        
        AppState.deleteCallback = async () => {
            try {
                const response = await fetch(`/api/sections/${sectionId}`, {
                    method: 'DELETE'
                });
                
                if (!response.ok) throw new Error('Failed to delete section');
                
                if (AppState.currentSectionId === sectionId) {
                    AppState.currentSectionId = null;
                    AppState.currentPageId = null;
                    EditorManager.hideEditor();
                }
                
                await TreeViewManager.loadTreeView(AppState.currentNotebookId);
                Utils.showSuccess('Section deleted successfully');
            } catch (error) {
                console.error('Error deleting section:', error);
                Utils.showError('Failed to delete section');
            }
        };
        
        Utils.showModal('deleteModal');
    },
    
    showCreatePageModal(sectionId) {
        AppState.currentSectionId = sectionId;
        
        document.getElementById('pageModalTitle').textContent = 'Create Page';
        document.getElementById('pageForm').reset();
        document.getElementById('pageId').value = '';
        document.getElementById('pageSectionId').value = sectionId;
        Utils.showModal('pageModal');
    }
};

// Page Management
const PageManager = {
    async selectPage(pageId) {
        // Check if there are unsaved changes
        if (AppState.isDirty) {
            if (!confirm('You have unsaved changes. Do you want to continue without saving?')) {
                return;
            }
        }
        
        try {
            const response = await fetch(`/api/pages/${pageId}`);
            if (!response.ok) throw new Error('Failed to load page');
            
            const page = await response.json();
            AppState.currentPageId = pageId;
            AppState.currentSectionId = page.section_id;
            
            // Update tree view selection
            document.querySelectorAll('.tree-page .tree-node-header').forEach(header => {
                header.classList.toggle('selected', header.closest('.tree-page').dataset.pageId === pageId);
            });
            
            // Expand the parent section
            const sectionNode = document.querySelector(`[data-section-id="${page.section_id}"]`);
            if (sectionNode) {
                const toggle = sectionNode.querySelector('.tree-toggle');
                const children = sectionNode.querySelector('.tree-children');
                if (toggle && children && !toggle.classList.contains('hidden')) {
                    toggle.classList.add('expanded');
                    children.classList.add('expanded');
                }
            }
            
            EditorManager.showEditor(page);
        } catch (error) {
            console.error('Error loading page:', error);
            Utils.showError('Failed to load page');
        }
    },
    
    async savePage() {
        if (!AppState.currentPageId || !AppState.markdownEditor) return;
        
        const content = AppState.markdownEditor.value();
        const title = document.getElementById('pageTitle').textContent;
        
        try {
            const response = await fetch(`/api/pages/${AppState.currentPageId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    title,
                    content,
                    section_id: AppState.currentSectionId
                })
            });
            
            if (!response.ok) throw new Error('Failed to save page');
            
            AppState.isDirty = false;
            Utils.showSuccess('Page saved successfully');
            
            // Update the tree view
            await TreeViewManager.loadTreeView(AppState.currentNotebookId);
            
            // Update metadata
            const page = await response.json();
            document.getElementById('pageMeta').textContent = 
                `Last updated: ${Utils.formatDate(page.updated_at)}`;
        } catch (error) {
            console.error('Error saving page:', error);
            Utils.showError('Failed to save page');
        }
    },
    
    async createPage(event) {
        event.preventDefault();
        
        const sectionId = document.getElementById('pageSectionId').value;
        const title = document.getElementById('pageFormTitle').value;
        
        const data = {
            section_id: sectionId,
            title,
            content: '',
            order_index: AppState.pages.filter(p => p.section_id === sectionId).length
        };
        
        try {
            const response = await fetch('/api/pages/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) throw new Error('Failed to create page');
            
            const newPage = await response.json();
            
            Utils.hideModal('pageModal');
            await TreeViewManager.loadTreeView(AppState.currentNotebookId);
            await this.selectPage(newPage.id);
            Utils.showSuccess('Page created successfully');
        } catch (error) {
            console.error('Error creating page:', error);
            Utils.showError('Failed to create page');
        }
    },
    
    async deletePage(pageId) {
        const page = AppState.pages.find(p => p.id === pageId);
        if (!page) return;
        
        document.getElementById('deleteMessage').textContent = 
            `Are you sure you want to delete "${page.title}"?`;
        
        AppState.deleteCallback = async () => {
            try {
                const response = await fetch(`/api/pages/${pageId}`, {
                    method: 'DELETE'
                });
                
                if (!response.ok) throw new Error('Failed to delete page');
                
                if (AppState.currentPageId === pageId) {
                    AppState.currentPageId = null;
                    EditorManager.hideEditor();
                }
                
                await TreeViewManager.loadTreeView(AppState.currentNotebookId);
                Utils.showSuccess('Page deleted successfully');
            } catch (error) {
                console.error('Error deleting page:', error);
                Utils.showError('Failed to delete page');
            }
        };
        
        Utils.showModal('deleteModal');
    }
};

// Editor Management
const EditorManager = {
    initEditor() {
        const textarea = document.getElementById('markdownEditor');
        
        AppState.markdownEditor = new EasyMDE({
            element: textarea,
            spellChecker: false,
            autosave: {
                enabled: false
            },
            toolbar: [
                "bold", "italic", "heading", "|",
                "quote", "unordered-list", "ordered-list", "|",
                "link", "image", "|",
                "preview", "side-by-side", "fullscreen", "|",
                "guide"
            ],
            status: false,
            minHeight: "calc(100vh - 200px)"
        });
        
        AppState.markdownEditor.codemirror.on('change', () => {
            AppState.isDirty = true;
        });
    },
    
    showEditor(page) {
        document.getElementById('welcomeScreen').style.display = 'none';
        document.getElementById('editorContainer').style.display = 'flex';
        
        document.getElementById('pageTitle').textContent = page.title;
        document.getElementById('pageMeta').textContent = 
            `Last updated: ${Utils.formatDate(page.updated_at)}`;
        
        if (AppState.markdownEditor) {
            AppState.markdownEditor.value(page.content || '');
            AppState.isDirty = false;
        }
    },
    
    hideEditor() {
        document.getElementById('welcomeScreen').style.display = 'flex';
        document.getElementById('editorContainer').style.display = 'none';
        
        if (AppState.markdownEditor) {
            AppState.markdownEditor.value('');
            AppState.isDirty = false;
        }
    }
};

// Search functionality
const SearchManager = {
    async search(query) {
        if (!query.trim()) {
            NotebookManager.renderNotebooks();
            return;
        }
        
        // Simple client-side search
        const filtered = AppState.notebooks.filter(nb => 
            nb.name.toLowerCase().includes(query.toLowerCase()) ||
            (nb.description && nb.description.toLowerCase().includes(query.toLowerCase()))
        );
        
        const container = document.getElementById('notebooksList');
        
        if (filtered.length === 0) {
            container.innerHTML = '<div class="empty-state">No notebooks found</div>';
            return;
        }
        
        container.innerHTML = filtered.map(notebook => `
            <div class="notebook-item ${notebook.id === AppState.currentNotebookId ? 'active' : ''}"
                 data-notebook-id="${notebook.id}"
                 onclick="NotebookManager.selectNotebook('${notebook.id}')">
                <i class="bi bi-journal-text"></i>
                <span style="flex: 1;">${Utils.escapeHtml(notebook.name)}</span>
            </div>
        `).join('');
    }
};

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize markdown editor
    EditorManager.initEditor();
    
    // Load notebooks
    NotebookManager.loadNotebooks();
    
    // Event listeners
    document.getElementById('btnNewNotebook').addEventListener('click', () => {
        NotebookManager.showCreateModal();
    });
    
    document.getElementById('btnNewSection').addEventListener('click', () => {
        SectionManager.showCreateModal();
    });
    
    document.getElementById('btnCollapseAll').addEventListener('click', () => {
        TreeViewManager.collapseAll();
    });
    
    document.getElementById('btnSavePage').addEventListener('click', () => {
        PageManager.savePage();
    });
    
    document.getElementById('btnDeletePage').addEventListener('click', () => {
        if (AppState.currentPageId) {
            PageManager.deletePage(AppState.currentPageId);
        }
    });
    
    // Modal forms
    document.getElementById('notebookForm').addEventListener('submit', (e) => {
        NotebookManager.saveNotebook(e);
    });
    
    document.getElementById('sectionForm').addEventListener('submit', (e) => {
        SectionManager.saveSection(e);
    });
    
    document.getElementById('pageForm').addEventListener('submit', (e) => {
        PageManager.createPage(e);
    });
    
    // Modal cancel buttons
    document.getElementById('btnCancelNotebook').addEventListener('click', () => {
        Utils.hideModal('notebookModal');
    });
    
    document.getElementById('btnCancelSection').addEventListener('click', () => {
        Utils.hideModal('sectionModal');
    });
    
    document.getElementById('btnCancelPage').addEventListener('click', () => {
        Utils.hideModal('pageModal');
    });
    
    document.getElementById('btnCancelDelete').addEventListener('click', () => {
        Utils.hideModal('deleteModal');
    });
    
    document.getElementById('btnConfirmDelete').addEventListener('click', () => {
        if (AppState.deleteCallback) {
            AppState.deleteCallback();
            AppState.deleteCallback = null;
        }
        Utils.hideModal('deleteModal');
    });
    
    // Search
    let searchTimeout;
    document.getElementById('notebookSearch').addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            SearchManager.search(e.target.value);
        }, 300);
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + S to save
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            if (AppState.currentPageId) {
                PageManager.savePage();
            }
        }
    });
});
