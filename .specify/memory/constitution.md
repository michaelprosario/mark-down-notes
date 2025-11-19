<!--
Sync Impact Report:
Version: 0.0.0 → 1.0.0 (initial constitution)
Modified principles: N/A (initial creation)
Added sections: All sections (Core Principles, Project Structure, Development Standards, Governance)
Removed sections: None
Templates requiring updates:
  ✅ plan-template.md - Constitution Check section references this file
  ✅ spec-template.md - No changes needed (technology-agnostic requirements)
  ✅ tasks-template.md - No changes needed (task breakdown format)
  ✅ commands/*.md - No changes needed (agent-agnostic execution)
Follow-up TODOs: None - all placeholders filled
-->

# Markdown Notes Constitution

## Core Principles

### I. Dependency Inversion (NON-NEGOTIABLE)

**Dependencies MUST point inward towards the core business logic.**

- Core business logic MUST reside in the `core/` folder and have minimal external framework dependencies
- Core MUST NOT depend on infrastructure or presentation layers
- Core MUST define interfaces (abstractions) for all external concerns
- Infrastructure and presentation layers MUST implement interfaces defined by core
- All cross-layer communication MUST occur through abstractions, never concrete implementations

**Rationale**: This ensures business logic remains independent of technology choices, frameworks, and delivery mechanisms. It maximizes testability, flexibility, and long-term maintainability by allowing infrastructure to change without affecting core business rules.

### II. Clear Layer Separation

**Code MUST be organized into distinct architectural layers with explicit responsibilities.**

- **Core Layer**: Contains domain models, business logic, use cases, and interface definitions. Zero infrastructure dependencies allowed.
- **Infrastructure Layer**: Contains all implementation details including data access, external services, file I/O, and third-party integrations. Implements interfaces defined in core.
- **Presentation Layer**: Contains UI, API endpoints, controllers, and serialization logic. Orchestrates core services but contains no business logic.

**Rationale**: Clear separation of concerns makes the codebase easier to understand, test, and maintain. Each layer has a single responsibility and can evolve independently within its boundaries.

### III. Interface-Based Design

**Core services MUST depend only on interfaces, never concrete implementations.**

- Core business logic services MUST depend upon interfaces for repositories, providers, and external services
- Interfaces MUST be defined in the core layer where they are consumed
- Infrastructure implementations MUST be injected through dependency injection
- Test implementations MUST be easily substitutable through interface contracts

**Rationale**: Programming to interfaces rather than implementations enables testing with mocks, allows runtime configuration of implementations, and prevents tight coupling between layers.

### IV. Command/Query Segregation

**Core services MUST use command or query objects as method inputs and return result objects as outputs.**

- Commands represent state-changing operations (create, update, delete)
- Queries represent data retrieval operations (get, list, search)
- Service methods MUST accept a single command or query object parameter
- Service methods MUST return a result object (success/failure with messages and validation errors)
- Exceptions MUST be reserved for unexpected errors, not business rule violations

**Rationale**: CQRS pattern improves clarity by separating reads from writes. Result objects provide consistent error handling and eliminate exception-based flow control for expected business failures. Single-parameter methods are easier to evolve and test.

### V. Test-First Development

**Core business logic MUST have comprehensive unit test coverage.**

- Unit tests MUST be written before or alongside implementation
- Core services MUST be testable without external dependencies (databases, file systems, networks)
- Test coverage MUST include happy paths, edge cases, and business rule violations
- Infrastructure integration tests MUST verify contracts between layers
- Tests MUST run fast (unit tests < 100ms each, integration tests < 5s total)

**Rationale**: Testing validates business logic correctness and serves as living documentation. Core independence from infrastructure makes unit testing fast and reliable. Test-first development ensures code is designed for testability from the start.

### VI. Minimal Core Dependencies

**The core layer MUST remain framework-independent and lightweight.**

- Core MUST NOT reference web frameworks, ORMs, UI libraries, or infrastructure SDKs
- Core MAY depend on standard library utilities and pure domain-focused packages
- Any core dependency MUST be justified as essential to business logic, not convenience
- Framework-specific code MUST reside in infrastructure or presentation layers

**Rationale**: Keeping core free from framework dependencies ensures business logic longevity. Frameworks change frequently; business rules do not. This principle protects the most valuable code from technology churn.

### VII. Explicit Over Implicit

**Code structure and dependencies MUST be explicit and discoverable.**

- Folder structure MUST clearly reflect architectural layers
- Interface locations MUST be obvious (in core, near consuming services)
- Dependency injection registrations MUST be centralized and readable
- Magic strings, reflection-based conventions, and implicit behaviors MUST be avoided
- Configuration MUST be explicit and validated at startup

**Rationale**: Explicit code is maintainable code. Future developers (including yourself) should understand dependencies and structure without archaeological investigation. Compile-time safety beats runtime surprises.

## Project Structure Requirements

### Folder Organization

**Projects MUST follow this structure:**

```
project-root/
├── core/                    # Core business logic layer
│   ├── domain/              # Domain models (entities, value objects)
│   ├── services/            # Application services (use cases)
│   ├── interfaces/          # Abstractions for external concerns
│   ├── commands/            # Command objects (state changes)
│   ├── queries/             # Query objects (data retrieval)
│   └── results/             # Result objects (success/failure)
│
├── infrastructure/          # Infrastructure implementation layer
│   ├── data/                # Data access implementations
│   ├── services/            # External service implementations
│   ├── providers/           # Provider implementations
│   └── config/              # Infrastructure configuration
│
├── presentation/            # Presentation/UI layer (web, api, cli)
│   ├── api/                 # API endpoints/controllers
│   ├── templates/           # UI templates
│   ├── static/              # Static assets
│   └── middleware/          # Request/response processing
│
└── tests/                   # Test suite
    ├── unit/                # Core business logic unit tests
    ├── integration/         # Cross-layer integration tests
    └── fixtures/            # Test data and mocks
```

### Dependency Flow

**Allowed dependencies:**
- Presentation → Core (via interfaces)
- Presentation → Infrastructure (for DI registration only)
- Infrastructure → Core (implements interfaces)
- Tests → All layers

**Prohibited dependencies:**
- Core → Infrastructure (NEVER)
- Core → Presentation (NEVER)
- Infrastructure → Presentation (NEVER)

## Development Standards

### Code Quality Gates

**All code MUST pass these gates before merge:**

1. **Core Unit Tests**: 100% of core services have unit tests with > 80% coverage
2. **Integration Tests**: Infrastructure implementations have contract tests
3. **Interface Compliance**: All core service dependencies are interface-based
4. **Layer Separation**: No prohibited cross-layer dependencies exist
5. **Result Pattern**: All service methods return result objects, not exceptions for business failures

### Service Design Standards

**Core services MUST follow these patterns:**

```python
# ✅ CORRECT: Interface-based, command input, result output
class CreateNotebookService:
    def __init__(self, repository: INotebookRepository):
        self._repository = repository
    
    def execute(self, command: CreateNotebookCommand) -> Result[Notebook]:
        # Business logic here
        if not command.name:
            return Result.failure("Name is required")
        
        notebook = Notebook(command.name, command.color)
        self._repository.save(notebook)
        return Result.success(notebook, "Notebook created")

# ❌ INCORRECT: Concrete dependency, multiple parameters, exception-based
class CreateNotebookService:
    def __init__(self, repository: SqlNotebookRepository):  # Concrete!
        self._repository = repository
    
    def create(self, name: str, color: str) -> Notebook:  # Multiple params, no result!
        if not name:
            raise ValueError("Name required")  # Exception for business rule!
        return self._repository.save(Notebook(name, color))
```

### Testing Standards

**Core unit tests MUST:**
- Use mock implementations of interfaces (no real database, file system, network)
- Test one service or domain object per test class
- Cover happy path, edge cases, and validation failures
- Run in < 100ms each
- Have descriptive names following `test_method_scenario_expectedOutcome` pattern

**Integration tests MUST:**
- Verify infrastructure implementations honor core interface contracts
- Test cross-layer data flow (API → Service → Repository → Storage)
- Use test databases or isolated storage (never production)
- Clean up resources after execution

## Governance

### Constitution Authority

This constitution supersedes all other coding guidelines, conventions, or preferences. When conflicts arise, constitutional principles take precedence.

### Amendment Process

**Constitution changes require:**
1. Documented justification for the change
2. Impact analysis on existing codebase
3. Version increment following semantic versioning:
   - **MAJOR**: Principle removal or backward-incompatible changes
   - **MINOR**: New principle added or material expansion
   - **PATCH**: Clarifications, wording improvements, typo fixes
4. Update to sync impact report (HTML comment at top of this file)
5. Propagation of changes to affected templates and documentation

### Compliance Review

**All pull requests MUST:**
- Verify adherence to Core Principles (I-VII)
- Check folder structure matches requirements
- Confirm no prohibited dependencies exist
- Validate test coverage meets standards
- Ensure service design follows patterns

### Complexity Justification

**Violations of principles MUST be justified in planning documents:**
- Document the specific principle violated
- Explain why violation is necessary for current need
- Describe simpler alternatives considered and rejected
- Include plan for future remediation if applicable

### Runtime Guidance

For day-to-day development guidance and practical implementation patterns, refer to supplementary documentation. This constitution defines the non-negotiable rules; runtime guidance provides implementation recipes and examples.

**Version**: 1.0.0 | **Ratified**: 2025-11-19 | **Last Amended**: 2025-11-19
