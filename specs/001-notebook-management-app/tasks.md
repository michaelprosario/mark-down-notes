# Tasks: Notebook Management App

**Feature Branch**: `001-notebook-management-app`  
**Generated**: November 19, 2025  
**Input**: Design documents from `/specs/001-notebook-management-app/`

**Prerequisites Met**: ✅ plan.md, ✅ spec.md, ✅ research.md, ✅ data-model.md, ✅ contracts/

**Tests**: Not explicitly requested in spec - focusing on implementation tasks. Tests can be added incrementally.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

---

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **Checkbox**: `- [ ]` - Track completion
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1, US2, US3, US4, US5) - omitted for Setup/Foundational/Polish phases
- **File paths**: Exact locations based on project structure

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Initialize project structure and development environment

- [X] T001 Create backend directory structure: backend/src/{core,infrastructure,api}, backend/tests/{unit,integration,fixtures}
- [X] T002 Initialize Python project with pyproject.toml and requirements.txt per quickstart.md
- [X] T003 [P] Create .env.example file with all required environment variables
- [X] T004 [P] Create backend/src/main.py FastAPI application entry point with basic app initialization
- [X] T005 [P] Setup Alembic for database migrations in backend/migrations/
- [X] T006 [P] Create pytest.ini and configure pytest-asyncio
- [X] T007 [P] Create .gitignore for Python, virtual environments, and database files
- [X] T008 [P] Setup static file directories: backend/src/api/static/{css,js,images}
- [X] T009 [P] Create base Jinja2 template structure: backend/src/api/templates/base.html

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story implementation

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Core Architecture

- [X] T010 [P] Create Result wrapper class in backend/src/core/results/result.py for success/failure handling
- [X] T011 [P] Create base Command class in backend/src/core/commands/base.py
- [X] T012 [P] Create base Query class in backend/src/core/queries/base.py
- [X] T013 [P] Create TimestampMixin and SoftDeleteMixin in backend/src/infrastructure/data/models/base.py

### Database Setup

- [X] T014 Create database configuration in backend/src/infrastructure/config/database.py with async SQLAlchemy engine
- [X] T015 Create initial Alembic migration with all tables (notebooks, sections, pages, tags, page_tags) per data-model.md
- [X] T016 Add database indexes, constraints, and triggers (full-text search, foreign keys, unique constraints)
- [X] T017 [P] Create dependency injection providers in backend/src/api/dependencies.py (get_db, repository factories)

### API Infrastructure

- [X] T018 [P] Setup FastAPI routers structure in backend/src/api/routes/ (notebooks.py, sections.py, pages.py, tags.py, search.py)
- [X] T019 [P] Create error handling middleware in backend/src/api/middleware/error_handler.py
- [X] T020 [P] Setup CORS middleware configuration in backend/src/main.py
- [X] T021 [P] Create Pydantic settings configuration in backend/src/infrastructure/config/settings.py with validation

### Frontend Foundation

- [X] T022 [P] Add Bootstrap 5 CDN links and custom CSS setup in backend/src/api/templates/base.html
- [X] T023 [P] Create responsive three-pane layout structure in backend/src/api/templates/index.html
- [X] T024 [P] Create custom CSS file backend/src/api/static/css/custom.css with notebook/section/page styling

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and Organize Notes (Priority: P1) 🎯 MVP

**Goal**: Enable users to create notebooks, add sections within them, and create pages within sections - establishing the three-level hierarchy

**Independent Test**: Open app, create notebook "Work", add section "Projects", create page "Q1 Planning", verify all three levels display correctly

### Domain Models (Core Layer)

- [ ] T025 [P] [US1] Create Notebook entity in backend/src/core/domain/notebook.py with validation methods
- [ ] T026 [P] [US1] Create Section entity in backend/src/core/domain/section.py with validation methods
- [ ] T027 [P] [US1] Create Page entity in backend/src/core/domain/page.py with validation methods

### Repository Interfaces (Core Layer)

- [ ] T028 [P] [US1] Define INotebookRepository interface in backend/src/core/interfaces/repositories.py
- [ ] T029 [P] [US1] Define ISectionRepository interface in backend/src/core/interfaces/repositories.py
- [ ] T030 [P] [US1] Define IPageRepository interface in backend/src/core/interfaces/repositories.py

### ORM Models (Infrastructure Layer)

- [ ] T031 [P] [US1] Create NotebookModel SQLAlchemy model in backend/src/infrastructure/data/models/notebook_model.py
- [ ] T032 [P] [US1] Create SectionModel SQLAlchemy model in backend/src/infrastructure/data/models/section_model.py
- [ ] T033 [P] [US1] Create PageModel SQLAlchemy model in backend/src/infrastructure/data/models/page_model.py

### Repository Implementations (Infrastructure Layer)

- [ ] T034 [US1] Implement NotebookRepository in backend/src/infrastructure/data/repositories/notebook_repository.py
- [ ] T035 [US1] Implement SectionRepository in backend/src/infrastructure/data/repositories/section_repository.py
- [ ] T036 [US1] Implement PageRepository in backend/src/infrastructure/data/repositories/page_repository.py

### Commands & Queries (Core Layer)

- [ ] T037 [P] [US1] Create CreateNotebookCommand in backend/src/core/commands/create_notebook_command.py
- [ ] T038 [P] [US1] Create UpdateNotebookCommand in backend/src/core/commands/update_notebook_command.py
- [ ] T039 [P] [US1] Create DeleteNotebookCommand in backend/src/core/commands/delete_notebook_command.py
- [ ] T040 [P] [US1] Create CreateSectionCommand in backend/src/core/commands/create_section_command.py
- [ ] T041 [P] [US1] Create UpdateSectionCommand in backend/src/core/commands/update_section_command.py
- [ ] T042 [P] [US1] Create DeleteSectionCommand in backend/src/core/commands/delete_section_command.py
- [ ] T043 [P] [US1] Create CreatePageCommand in backend/src/core/commands/create_page_command.py
- [ ] T044 [P] [US1] Create UpdatePageCommand in backend/src/core/commands/update_page_command.py
- [ ] T045 [P] [US1] Create DeletePageCommand in backend/src/core/commands/delete_page_command.py
- [ ] T046 [P] [US1] Create GetNotebooksQuery in backend/src/core/queries/get_notebooks_query.py
- [ ] T047 [P] [US1] Create GetSectionsQuery in backend/src/core/queries/get_sections_query.py
- [ ] T048 [P] [US1] Create GetPagesQuery in backend/src/core/queries/get_pages_query.py

### Services (Core Layer)

- [ ] T049 [US1] Implement CreateNotebookService in backend/src/core/services/create_notebook_service.py
- [ ] T050 [US1] Implement UpdateNotebookService in backend/src/core/services/update_notebook_service.py
- [ ] T051 [US1] Implement DeleteNotebookService in backend/src/core/services/delete_notebook_service.py (with cascade validation)
- [ ] T052 [US1] Implement GetNotebooksService in backend/src/core/services/get_notebooks_service.py
- [ ] T053 [US1] Implement CreateSectionService in backend/src/core/services/create_section_service.py
- [ ] T054 [US1] Implement UpdateSectionService in backend/src/core/services/update_section_service.py
- [ ] T055 [US1] Implement DeleteSectionService in backend/src/core/services/delete_section_service.py (with cascade validation)
- [ ] T056 [US1] Implement GetSectionsService in backend/src/core/services/get_sections_service.py
- [ ] T057 [US1] Implement ReorderSectionsService in backend/src/core/services/reorder_sections_service.py
- [ ] T058 [US1] Implement CreatePageService in backend/src/core/services/create_page_service.py
- [ ] T059 [US1] Implement UpdatePageService in backend/src/core/services/update_page_service.py
- [ ] T060 [US1] Implement DeletePageService in backend/src/core/services/delete_page_service.py
- [ ] T061 [US1] Implement GetPagesService in backend/src/core/services/get_pages_service.py

### API Endpoints (Presentation Layer)

- [ ] T062 [US1] Implement POST /api/notebooks endpoint in backend/src/api/routes/notebooks.py
- [ ] T063 [US1] Implement GET /api/notebooks endpoint in backend/src/api/routes/notebooks.py
- [ ] T064 [US1] Implement GET /api/notebooks/{id} endpoint in backend/src/api/routes/notebooks.py
- [ ] T065 [US1] Implement PUT /api/notebooks/{id} endpoint in backend/src/api/routes/notebooks.py
- [ ] T066 [US1] Implement DELETE /api/notebooks/{id} endpoint in backend/src/api/routes/notebooks.py
- [ ] T067 [US1] Implement POST /api/notebooks/{id}/sections endpoint in backend/src/api/routes/sections.py
- [ ] T068 [US1] Implement GET /api/notebooks/{id}/sections endpoint in backend/src/api/routes/sections.py
- [ ] T069 [US1] Implement PUT /api/sections/{id} endpoint in backend/src/api/routes/sections.py
- [ ] T070 [US1] Implement DELETE /api/sections/{id} endpoint in backend/src/api/routes/sections.py
- [ ] T071 [US1] Implement POST /api/sections/{id}/reorder endpoint in backend/src/api/routes/sections.py
- [ ] T072 [US1] Implement POST /api/sections/{id}/pages endpoint in backend/src/api/routes/pages.py
- [ ] T073 [US1] Implement GET /api/sections/{id}/pages endpoint in backend/src/api/routes/pages.py
- [ ] T074 [US1] Implement GET /api/pages/{id} endpoint in backend/src/api/routes/pages.py
- [ ] T075 [US1] Implement PUT /api/pages/{id} endpoint in backend/src/api/routes/pages.py
- [ ] T076 [US1] Implement DELETE /api/pages/{id} endpoint in backend/src/api/routes/pages.py

### UI Templates (Presentation Layer)

- [ ] T077 [US1] Create notebooks sidebar component in backend/src/api/templates/components/notebooks_sidebar.html
- [ ] T078 [US1] Create sections tabs component in backend/src/api/templates/components/sections_tabs.html
- [ ] T079 [US1] Create pages list component in backend/src/api/templates/components/pages_list.html
- [ ] T080 [US1] Create notebook/section/page creation modals in backend/src/api/templates/components/modals.html
- [ ] T081 [US1] Implement main page route GET / in backend/src/api/routes/pages.py serving index.html with initial data

### JavaScript Interactivity

- [ ] T082 [US1] Create notebook management JavaScript in backend/src/api/static/js/notebooks.js (CRUD operations)
- [ ] T083 [US1] Create section management JavaScript in backend/src/api/static/js/sections.js (CRUD + reordering)
- [ ] T084 [US1] Create page management JavaScript in backend/src/api/static/js/pages.js (CRUD operations)
- [ ] T085 [US1] Implement confirmation dialogs for delete operations in backend/src/api/static/js/app.js

**Checkpoint**: User Story 1 complete - Users can create/organize notebooks, sections, and pages with full hierarchy navigation

---

## Phase 4: User Story 2 - Write and Format Content (Priority: P2)

**Goal**: Enable users to write rich formatted content using Markdown with preview, supporting headings, lists, bold/italic, links, and images

**Independent Test**: Create a page, add formatted text (headings, bold, italic), lists, links, images, verify formatting displays correctly and persists

### Markdown Infrastructure (Infrastructure Layer)

- [ ] T086 [P] [US2] Create markdown rendering service in backend/src/infrastructure/services/markdown_service.py with markdown-it-py
- [ ] T087 [P] [US2] Create HTML sanitization service in backend/src/infrastructure/services/sanitizer_service.py with bleach
- [ ] T088 [P] [US2] Define IMarkdownService interface in backend/src/core/interfaces/services.py

### Image Storage (Infrastructure Layer)

- [ ] T089 [P] [US2] Create IStorageProvider interface in backend/src/core/interfaces/providers.py
- [ ] T090 [US2] Implement FileStorageProvider in backend/src/infrastructure/storage/file_storage_provider.py
- [ ] T091 [US2] Create image upload endpoint POST /api/images in backend/src/api/routes/images.py with validation

### Content Services (Core Layer)

- [ ] T092 [US2] Create UpdatePageContentCommand in backend/src/core/commands/update_page_content_command.py
- [ ] T093 [US2] Implement UpdatePageContentService in backend/src/core/services/update_page_content_service.py (auto-save optimized)
- [ ] T094 [US2] Implement RenderPageService in backend/src/core/services/render_page_service.py (converts markdown to HTML)

### API Endpoints (Presentation Layer)

- [ ] T095 [US2] Implement PUT /api/pages/{id}/content endpoint in backend/src/api/routes/pages.py for auto-save
- [ ] T096 [US2] Update GET /api/pages/{id} to include rendered HTML (content_html field)

### Editor UI (Presentation Layer)

- [ ] T097 [US2] Integrate EasyMDE markdown editor in backend/src/api/templates/components/page_editor.html
- [ ] T098 [US2] Create auto-save JavaScript in backend/src/api/static/js/auto-save.js with debouncing
- [ ] T099 [US2] Create editor toolbar customization in backend/src/api/static/js/editor.js
- [ ] T100 [US2] Add image upload handler in backend/src/api/static/js/editor.js
- [ ] T101 [US2] Implement preview mode toggle in backend/src/api/static/js/editor.js
- [ ] T102 [US2] Add save status indicator in UI (saving/saved/error)

**Checkpoint**: User Story 2 complete - Users can write and format rich content with auto-save and preview

---

## Phase 5: User Story 3 - Search and Find Notes (Priority: P3)

**Goal**: Enable full-text search across all pages with filtering by notebook/section and search term highlighting

**Independent Test**: Create several pages with distinct content, search for a term, verify relevant pages appear with highlighted results

### Search Infrastructure (Infrastructure Layer)

- [ ] T103 [P] [US3] Define ISearchService interface in backend/src/core/interfaces/services.py
- [ ] T104 [US3] Implement PostgreSQLSearchService in backend/src/infrastructure/services/search_service.py using full-text search
- [ ] T105 [US3] Add content_plain field auto-update logic in PageRepository (strip markdown to plain text)

### Search Services (Core Layer)

- [ ] T106 [US3] Create SearchPagesQuery in backend/src/core/queries/search_pages_query.py
- [ ] T107 [US3] Implement SearchPagesService in backend/src/core/services/search_pages_service.py
- [ ] T108 [US3] Implement GetRecentPagesService in backend/src/core/services/get_recent_pages_service.py

### API Endpoints (Presentation Layer)

- [ ] T109 [US3] Implement GET /api/search endpoint in backend/src/api/routes/search.py with query, filters, pagination
- [ ] T110 [US3] Implement GET /api/pages/recent endpoint in backend/src/api/routes/pages.py

### Search UI (Presentation Layer)

- [ ] T111 [US3] Create search bar component in backend/src/api/templates/components/search_bar.html
- [ ] T112 [US3] Create search results display in backend/src/api/templates/components/search_results.html
- [ ] T113 [US3] Create search JavaScript in backend/src/api/static/js/search.js with debounced search
- [ ] T114 [US3] Implement search term highlighting in backend/src/api/static/js/search.js
- [ ] T115 [US3] Add search filters (notebook, section) in UI
- [ ] T116 [US3] Create recent pages widget in sidebar

**Checkpoint**: User Story 3 complete - Users can search all content and quickly find notes

---

## Phase 6: User Story 4 - Tag and Categorize Notes (Priority: P4)

**Goal**: Enable cross-cutting organization via tags, with tag suggestions and tag-based page filtering

**Independent Test**: Add tags to several pages across different sections/notebooks, click a tag, verify all tagged pages display correctly

### Domain & Models (Core/Infrastructure)

- [ ] T117 [P] [US4] Create Tag entity in backend/src/core/domain/tag.py
- [ ] T118 [P] [US4] Define ITagRepository interface in backend/src/core/interfaces/repositories.py
- [ ] T119 [US4] Create TagModel and PageTagModel in backend/src/infrastructure/data/models/tag_model.py
- [ ] T120 [US4] Implement TagRepository in backend/src/infrastructure/data/repositories/tag_repository.py

### Commands & Services (Core Layer)

- [ ] T121 [P] [US4] Create CreateTagCommand in backend/src/core/commands/create_tag_command.py
- [ ] T122 [P] [US4] Create UpdateTagCommand in backend/src/core/commands/update_tag_command.py
- [ ] T123 [P] [US4] Create DeleteTagCommand in backend/src/core/commands/delete_tag_command.py
- [ ] T124 [P] [US4] Create AddPageTagCommand in backend/src/core/commands/add_page_tag_command.py
- [ ] T125 [P] [US4] Create RemovePageTagCommand in backend/src/core/commands/remove_page_tag_command.py
- [ ] T126 [US4] Implement CreateTagService in backend/src/core/services/create_tag_service.py
- [ ] T127 [US4] Implement UpdateTagService in backend/src/core/services/update_tag_service.py
- [ ] T128 [US4] Implement DeleteTagService in backend/src/core/services/delete_tag_service.py
- [ ] T129 [US4] Implement AddPageTagService in backend/src/core/services/add_page_tag_service.py
- [ ] T130 [US4] Implement GetTagsService in backend/src/core/services/get_tags_service.py
- [ ] T131 [US4] Implement GetPagesByTagService in backend/src/core/services/get_pages_by_tag_service.py

### API Endpoints (Presentation Layer)

- [ ] T132 [US4] Implement POST /api/tags endpoint in backend/src/api/routes/tags.py
- [ ] T133 [US4] Implement GET /api/tags endpoint in backend/src/api/routes/tags.py
- [ ] T134 [US4] Implement PUT /api/tags/{id} endpoint in backend/src/api/routes/tags.py
- [ ] T135 [US4] Implement DELETE /api/tags/{id} endpoint in backend/src/api/routes/tags.py
- [ ] T136 [US4] Implement GET /api/tags/{id}/pages endpoint in backend/src/api/routes/tags.py
- [ ] T137 [US4] Update CreatePageService to handle tag names array (create tags if needed)
- [ ] T138 [US4] Update UpdatePageService to sync page tags

### Tagging UI (Presentation Layer)

- [ ] T139 [US4] Create tag input component with autocomplete in backend/src/api/templates/components/tag_input.html
- [ ] T140 [US4] Create tag display badges in page list/detail views
- [ ] T141 [US4] Create tag management JavaScript in backend/src/api/static/js/tags.js
- [ ] T142 [US4] Implement tag autocomplete in backend/src/api/static/js/tags.js
- [ ] T143 [US4] Add tag filter to search interface
- [ ] T144 [US4] Create tag cloud/list widget in sidebar

**Checkpoint**: User Story 4 complete - Users can tag pages and find content via tags

---

## Phase 7: User Story 5 - Export and Backup Notes (Priority: P5)

**Goal**: Enable exporting notebooks as JSON and pages as Markdown, with import capability for backups/migration

**Independent Test**: Create notebook with content, export to file, verify file contains all data, import back, verify recreation

### Export Services (Core Layer)

- [ ] T145 [P] [US5] Create ExportNotebookQuery in backend/src/core/queries/export_notebook_query.py
- [ ] T146 [P] [US5] Create ExportPageQuery in backend/src/core/queries/export_page_query.py
- [ ] T147 [P] [US5] Create ImportNotebookCommand in backend/src/core/commands/import_notebook_command.py
- [ ] T148 [US5] Implement ExportNotebookService in backend/src/core/services/export_notebook_service.py
- [ ] T149 [US5] Implement ExportPageService in backend/src/core/services/export_page_service.py
- [ ] T150 [US5] Implement ImportNotebookService in backend/src/core/services/import_notebook_service.py with validation

### API Endpoints (Presentation Layer)

- [ ] T151 [US5] Implement GET /api/notebooks/{id}/export endpoint in backend/src/api/routes/notebooks.py
- [ ] T152 [US5] Implement GET /api/pages/{id}/export endpoint in backend/src/api/routes/pages.py
- [ ] T153 [US5] Implement POST /api/import endpoint in backend/src/api/routes/notebooks.py

### Export UI (Presentation Layer)

- [ ] T154 [US5] Add export button to notebook context menu
- [ ] T155 [US5] Add export button to page context menu
- [ ] T156 [US5] Create import modal in backend/src/api/templates/components/import_modal.html
- [ ] T157 [US5] Implement export/import JavaScript in backend/src/api/static/js/export.js
- [ ] T158 [US5] Add import validation and error display

**Checkpoint**: User Story 5 complete - Users can export/import data for backup and portability

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements and refinements affecting multiple user stories

### User Experience Enhancements

- [ ] T159 [P] Add favorites functionality (implement GET /api/pages/favorites, POST/DELETE /api/pages/{id}/favorite)
- [ ] T160 [P] Add keyboard shortcuts handler in backend/src/api/static/js/shortcuts.js
- [ ] T161 [P] Implement drag-and-drop for section reordering in UI
- [ ] T162 [P] Add loading states and spinners throughout UI
- [ ] T163 [P] Implement breadcrumb navigation in backend/src/api/templates/components/breadcrumbs.html

### Error Handling & Validation

- [ ] T164 [P] Add client-side form validation for all creation/edit modals
- [ ] T165 [P] Implement user-friendly error messages for all API failures
- [ ] T166 [P] Add validation for special characters, empty names, duplicate names
- [ ] T167 [P] Handle edge cases: very long content, max depth subpages, storage quota

### Performance & Optimization

- [ ] T168 [P] Add database query optimization (select eager loading for relationships)
- [ ] T169 [P] Implement pagination for large page lists
- [ ] T170 [P] Add caching for frequently accessed notebooks/sections
- [ ] T171 [P] Optimize search query performance with query plan analysis

### Documentation & Developer Experience

- [ ] T172 [P] Create seed_demo_data.py script in backend/src/scripts/ per quickstart.md sample data
- [ ] T173 [P] Validate all quickstart.md setup instructions work correctly
- [ ] T174 [P] Create API documentation using FastAPI's automatic OpenAPI docs
- [ ] T175 [P] Add inline code comments for complex business logic

### Security & Production Readiness

- [ ] T176 [P] Add rate limiting to API endpoints
- [ ] T177 [P] Implement CSRF protection for forms
- [ ] T178 [P] Add input sanitization for all user inputs
- [ ] T179 [P] Create Dockerfile per quickstart.md specifications
- [ ] T180 [P] Setup health check endpoint GET /health

---

## Dependencies & Execution Order

### Phase Dependencies

1. **Setup (Phase 1)**: No dependencies - start immediately
2. **Foundational (Phase 2)**: Depends on Setup - **BLOCKS all user stories**
3. **User Story 1 (Phase 3)**: Depends on Foundational - **No dependencies on other stories**
4. **User Story 2 (Phase 4)**: Depends on Foundational + US1 (needs Page model) - Can integrate with US1
5. **User Story 3 (Phase 5)**: Depends on Foundational + US1 (searches pages) - Independent of US2/US4
6. **User Story 4 (Phase 6)**: Depends on Foundational + US1 (tags pages) - Independent of US2/US3
7. **User Story 5 (Phase 7)**: Depends on Foundational + US1 (exports structure) - Can work with US2/US4 data if present
8. **Polish (Phase 8)**: Depends on desired user stories completion

### Story Completion Order for MVP

**Recommended MVP**: Complete User Story 1 only (P1) for initial release
- Provides core value: hierarchical note organization
- Independently testable and deployable
- Foundation for all other features

**Subsequent Releases**:
- **v1.1**: Add User Story 2 (P2) - Rich text editing
- **v1.2**: Add User Story 3 (P3) - Search
- **v2.0**: Add User Stories 4 & 5 (P4, P5) - Tags and Export

### Parallel Execution Opportunities

Within each phase, all tasks marked **[P]** can run in parallel:

**Phase 1 (Setup)**: T003-T009 can all run in parallel (8 parallel tasks)

**Phase 2 (Foundational)**: 
- T010-T013 (core architecture) can run in parallel
- T018-T024 (API/frontend foundation) can run in parallel after T014-T017

**Phase 3 (User Story 1)**:
- T025-T027 (domain models) in parallel
- T028-T030 (interfaces) in parallel
- T031-T033 (ORM models) in parallel
- T037-T048 (commands/queries) in parallel (12 tasks)
- T049-T061 (services) sequentially after repositories
- T062-T076 (API endpoints) can run in parallel after services
- T077-T081 (UI templates) can run in parallel
- T082-T085 (JavaScript) can run in parallel

**All User Stories**: Different stories can be implemented in parallel by different developers after Phase 2 completes

### Critical Path

1. Setup → Foundational (sequential, ~2-3 days)
2. User Story 1 (sequential within story, ~5-7 days)
3. User Stories 2-5 (can be parallel, ~3-5 days each)
4. Polish (parallel, ~2-3 days)

**Estimated Total**: 15-25 days for MVP (US1 only), 30-40 days for all features

---

## Parallel Example: User Story 1 Kickoff

After Foundational phase completes, User Story 1 can start with these parallel tracks:

```bash
# Track 1: Domain models (Developer A)
T025 Create Notebook entity
T026 Create Section entity  
T027 Create Page entity

# Track 2: Repository interfaces (Developer B)
T028 Define INotebookRepository
T029 Define ISectionRepository
T030 Define IPageRepository

# Track 3: ORM models (Developer C)
T031 Create NotebookModel
T032 Create SectionModel
T033 Create PageModel

# Then converge for repository implementations
# Then split again for commands/queries (12 parallel tasks possible)
```

---

## Summary

- **Total Tasks**: 180
- **User Stories**: 5 (P1-P5)
- **Parallelizable Tasks**: ~85 tasks marked [P]
- **Critical Dependencies**: Foundational phase blocks all user stories
- **MVP Scope**: Phase 1 + Phase 2 + Phase 3 (User Story 1) = ~60 tasks
- **Independent Test Criteria**: Each user story has clear, testable acceptance criteria
- **Incremental Delivery**: Each completed story adds measurable user value

**Next Step**: Start with Phase 1 (Setup) tasks T001-T009
