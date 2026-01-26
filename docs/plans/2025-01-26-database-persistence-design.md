# Phase 1: Database Persistence Design

**Date**: 2025-01-26
**Author**: Brainstorming Session
**Status**: Design Approved - Ready for Implementation

## Overview

Add database persistence to autosar-pdf2txt using SQLAlchemy, enabling users to parse PDFs once, store the data in a database, and query/export it multiple times without re-parsing.

## Goals

- Parse AUTOSAR PDFs and store in SQLite database (with PostgreSQL support via SQLAlchemy)
- Merge new PDF data with existing database data
- Query and export from database to multiple formats (markdown, JSON, future formats)
- Maintain backward compatibility with existing in-memory parsing
- Support incremental updates as new PDFs are released

## Architecture

### Components

1. **Database Layer** (`src/autosar_pdf2txt/db/`)
   - SQLAlchemy models mirroring existing dataclass models
   - `AutosarPackageDB`, `AutosarClassDB`, `AutosarEnumerationDB`, `AutosarPrimitiveDB`
   - Relationship mappings (foreign keys for packages, base classes, subclasses)
   - Source tracking table for PDF metadata

2. **Parser Integration**
   - Modify `PdfParser` to support both modes: in-memory (current) and database (new)
   - New method: `parse_and_store(pdf_path, session)` - parses PDF and stores directly to DB
   - Existing `parse_pdf()` unchanged for backward compatibility

3. **Database Manager** (`src/autosar_pdf2txt/db/manager.py`)
   - `DatabaseManager` class for DB operations
   - `init_database()` - create schema
   - `store_packages()` - store parsed packages with merge logic
   - `query_packages()`, `query_classes()` - retrieve data
   - Handle SQLAlchemy sessions and connections

4. **CLI Enhancement**
   - New option: `--database PATH` to specify database file
   - When `--database` provided, store to DB instead of/alongside markdown output
   - Additional commands: `autosar-db query`, `autosar-db export`, `autosar-db init`

### Technology Stack

- SQLAlchemy 2.0+ (async support, improved ORM)
- SQLite (default) with PostgreSQL support via connection string
- Alembic for database migrations (future-proofing)

## Database Schema

### Core Tables

**packages** - Hierarchical package structure
```sql
CREATE TABLE packages (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    parent_id INTEGER REFERENCES packages(id),
    path VARCHAR UNIQUE NOT NULL,
    level INTEGER NOT NULL
);
CREATE INDEX idx_packages_path ON packages(path);
```

**document_sources** - PDF source tracking
```sql
CREATE TABLE document_sources (
    id INTEGER PRIMARY KEY,
    pdf_file VARCHAR NOT NULL,
    page_number INTEGER NOT NULL,
    autosar_standard VARCHAR,
    release VARCHAR,
    parsed_at TIMESTAMP NOT NULL
);
CREATE INDEX idx_sources_pdf ON document_sources(pdf_file);
```

**classes** - AUTOSAR class definitions
```sql
CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    package_id INTEGER REFERENCES packages(id),
    is_abstract BOOLEAN NOT NULL,
    atp_type VARCHAR,
    source_id INTEGER REFERENCES document_sources(id),
    UNIQUE(package_id, name)
);
CREATE INDEX idx_classes_name ON classes(name);
```

**class_relationships** - Inheritance and aggregation
```sql
CREATE TABLE class_relationships (
    id INTEGER PRIMARY KEY,
    class_id INTEGER REFERENCES classes(id),
    related_class_id INTEGER REFERENCES classes(id),
    relationship_type VARCHAR NOT NULL, -- 'base', 'subclass', 'aggregated_by'
    CHECK (relationship_type IN ('base', 'subclass', 'aggregated_by'))
);
CREATE INDEX idx_relationships_class ON class_relationships(class_id);
```

**attributes** - Class attributes
```sql
CREATE TABLE attributes (
    id INTEGER PRIMARY KEY,
    class_id INTEGER REFERENCES classes(id),
    name VARCHAR NOT NULL,
    type VARCHAR NOT NULL,
    mult VARCHAR NOT NULL,
    kind VARCHAR NOT NULL,
    note VARCHAR
);
CREATE INDEX idx_attributes_class ON attributes(class_id);
```

**enumerations** and **enumeration_literals**
```sql
CREATE TABLE enumerations (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    package_id INTEGER REFERENCES packages(id),
    source_id INTEGER REFERENCES document_sources(id),
    UNIQUE(package_id, name)
);

CREATE TABLE enumeration_literals (
    id INTEGER PRIMARY KEY,
    enumeration_id INTEGER REFERENCES enumerations(id),
    name VARCHAR NOT NULL,
    index INTEGER,
    description VARCHAR
);
```

## CLI Integration

### Enhanced `autosar-extract` Command

```bash
# Store to database
autosar-extract examples/pdf/ --database autosar.db

# Both markdown and database
autosar-extract examples/pdf/ -o output.md --database autosar.db

# Merge new PDFs into existing database
autosar-extract new_specs/ --database autosar.db --merge
```

### New `autosar-db` Command Group

```bash
# Initialize empty database
autosar-db init --database autosar.db

# Query database
autosar-db query --database autosar.db --class "SwComponentPrototype"
autosar-db query --database autosar.db --package "AUTOSAR::Components"

# Export from database to markdown
autosar-db export --database autosar.db -o output.md --format markdown
autosar-db export --database autosar.db -o output.json --format json

# Database statistics
autosar-db stats --database autosar.db
```

## Merge Logic

### Parsing to Database Flow

```
PDF File → PdfParser.parse_and_store()
           ↓
       Extract packages/classes/enums (existing logic)
           ↓
       DatabaseManager.store_packages()
           ↓
       For each package:
         1. Check if exists (by full path)
         2. If not exists: create with all children
         3. If exists: apply merge strategy
           ↓
       For each type in package:
         1. Check if exists (package_id + name)
         2. Store/merge based on strategy
         3. Store relationships (bases, subclasses, attributes)
           ↓
       Store document_source with parse timestamp
```

### Merge Strategies

```python
class MergeStrategy(Enum):
    SKIP = "skip"       # Don't overwrite existing types (default)
    UPDATE = "update"   # Update existing types with new data
    KEEP_ALL = "all"    # Store all versions with source tracking
```

### Duplicate Detection

- Primary key: `(package_id, name)` for all types
- Document source tracking prevents complete data loss
- Warning logs when duplicates detected (with merge strategy used)

## DatabaseManager API

```python
class DatabaseManager:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def init_database(self):
        """Create all tables"""
        Base.metadata.create_all(self.engine)

    def store_packages(self,
                      packages: List[AutosarPackage],
                      merge_strategy: MergeStrategy = MergeStrategy.SKIP)

    def get_class(self, name: str, package: str) -> Optional[AutosarClassDB]

    def find_classes_by_pattern(self, pattern: str) -> List[AutosarClassDB]

    def get_package_hierarchy(self) -> List[PackageDB]

    def get_session(self) -> Session:
        """Handle database connection failures gracefully"""
```

## Testing Strategy

### Test Database Setup

```python
# tests/conftest.py
@pytest.fixture
def test_db():
    """Create in-memory SQLite database for testing"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
```

### New Test Files

1. **tests/db/test_models.py** - Test SQLAlchemy models
   - Test model creation and relationships
   - Test foreign key constraints
   - Test cascade deletes

2. **tests/db/test_manager.py** - Test DatabaseManager
   - Test `store_packages()` with all merge strategies
   - Test duplicate detection and handling
   - Test query methods (`get_class`, `find_classes_by_pattern`)

3. **tests/db/test_integration.py** - Integration tests
   - Test full PDF → Database flow
   - Test parsing real AUTOSAR PDFs to database
   - Test multi-PDF merging scenarios

### Test Coverage Goals

- Maintain overall ≥95% coverage
- Database models: 100% (critical data integrity)
- DatabaseManager: 95%+ (complex business logic)
- CLI database commands: 85%+ (similar to current CLI coverage)

## File Structure

```
src/autosar_pdf2txt/
  db/
    __init__.py              # Database exports
    models.py                # SQLAlchemy models (AutosarClassDB, etc.)
    manager.py               # DatabaseManager class
    merge.py                 # MergeStrategy enum and logic
    base.py                  # Base database setup (Base, engine)
  cli/
    db_cmd.py                # New 'autosar-db' command group
  parser/
    pdf_parser.py            # Add parse_and_store() method

tests/
  db/
    __init__.py
    test_models.py           # SQLAlchemy model tests
    test_manager.py          # DatabaseManager tests
    test_integration.py      # Full PDF→DB flow tests

scripts/
  init_db.py                 # Script to initialize database
  migrate_to_db.py           # Migrate existing markdown data to DB

alembic/
  versions/                  # Database migration scripts
  env.py
  script.py.mako
```

## Implementation Order

1. **Step 1: Database Models** (`src/autosar_pdf2txt/db/models.py`)
   - Create SQLAlchemy models mirroring dataclasses
   - Define relationships and foreign keys
   - Add `from_autosar_class()` class methods for conversion

2. **Step 2: Database Manager** (`src/autosar_pdf2txt/db/manager.py`)
   - Implement `DatabaseManager` class
   - CRUD operations for packages, classes, enums
   - Merge strategy implementation

3. **Step 3: Parser Integration**
   - Add `parse_and_store()` to `PdfParser`
   - Integrate with `DatabaseManager`

4. **Step 4: CLI Commands**
   - Add `--database` option to `autosar-extract`
   - Create new `autosar-db` command group

5. **Step 5: Tests**
   - Write tests incrementally with each step

## Error Handling & Edge Cases

### Database Connection Errors
```python
def get_session(self) -> Session:
    try:
        return self.Session()
    except SQLAlchemyError as e:
        logger.error(f"Database connection failed: {e}")
        raise DatabaseConnectionError(f"Cannot connect to database: {e}")
```

### Edge Cases

1. **Large PDFs/Many Types:**
   - Batch insert operations (bulk_insert_mappings)
   - Commit in chunks (every 100 types) to avoid memory issues
   - Progress indicators for long operations

2. **Concurrent Access:**
   - SQLite: Single writer, multiple readers
   - File locking with `timeout` parameter
   - Retry logic for "database is locked" errors

3. **Corrupted Database:**
   - Integrity check on startup
   - Recovery mode: `--rebuild` flag to recreate from scratch
   - Backup before major operations

4. **Schema Migrations:**
   - Alembic version tracking
   - Auto-migrate on startup if schema version mismatch
   - User prompt: "Database schema outdated. Migrate? [y/N]"

### CLI Error Messages

```bash
$ autosar-extract file.pdf --database autosar.db
Error: Database file does not exist. Use 'autosar-db init' first.

$ autosar-extract file.pdf --database autosar.db
Warning: Class 'SwComponentPrototype' already exists. Skipping (use --merge update to overwrite)

$ autosar-extract file.pdf --database autosar.db
Parsed 234 classes, 15 packages in 2.3s
Stored to database: autosar.db
```

## Dependencies

```python
# setup.py / pyproject.toml
install_requires = [
    ...,
    "sqlalchemy>=2.0.0",      # Database ORM
    "alembic>=1.12.0",        # Database migrations
    "click>=8.0.0",           # CLI (already have for current CLI)
]
```

## Backward Compatibility

- Existing `parse_pdf()` API unchanged - returns in-memory objects
- Existing markdown generation continues to work
- Database is opt-in via `--database` flag
- No breaking changes to current functionality

## Performance Optimizations

1. **Bulk Operations:**
   ```python
   # Use bulk operations instead of individual inserts
   session.bulk_insert_mappings(AutosarClassDB, [
       cls.to_dict() for cls in classes
   ])
   ```

2. **Eager Loading:**
   ```python
   # Avoid N+1 queries
   classes = session.query(AutosarClassDB)\
       .options(joinedload(AutosarClassDB.attributes))\
       .all()
   ```

3. **Connection Pooling:**
   ```python
   engine = create_engine(
       db_url,
       pool_size=5,
       max_overflow=10,
       pool_pre_ping=True  # Verify connections before use
   )
   ```

## Migration Path for Existing Users

```bash
# Users with existing parsed markdown can import to DB
python scripts/migrate_markdown_to_db.py --input output.md --database autosar.db
```

## Future Phases

### Phase 2: REST API
- Flask/FastAPI web server
- Endpoints for querying packages, classes, attributes
- Search and filtering capabilities
- JSON responses

### Phase 3: Frontend
- React/Vue web interface
- Browse packages and classes
- Search functionality
- View hierarchies and relationships

## Requirements Traceability

New requirements to be added to `docs/requirements/requirements.md`:

- **SWR_DB_00001**: Database persistence with SQLAlchemy
- **SWR_DB_00002**: SQLite support with PostgreSQL compatibility
- **SWR_DB_00003**: Merge strategies for duplicate handling
- **SWR_DB_00004**: Database query CLI commands
- **SWR_DB_00005**: Export from database to markdown
- **SWR_DB_00006**: Export from database to JSON
- **SWR_DB_00007**: Database migration support with Alembic
- **SWR_CLI_00015**: `--database` option for autosar-extract
- **SWR_CLI_00016**: `autosar-db` command group
- **SWR_CLI_00017**: `autosar-db init` command
- **SWR_CLI_00018**: `autosar-db query` command
- **SWR_CLI_00019**: `autosar-db export` command
- **SWR_CLI_00020**: `autosar-db stats` command
