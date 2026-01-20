# Version Control Policy

## Version Number Format

This project follows [Semantic Versioning 2.0.0](https://semver.org/): `MAJOR.MINOR.PATCH`

- **MAJOR**: Controlled by project lead only (user)
- **MINOR**: Increment for minor changes (backward-compatible features)
- **PATCH**: Increment for bug fixes (backward-compatible fixes)

## Version Increment Rules

### PATCH Version (Z in X.Y.Z)

**When to increment:**
- Bug fixes that resolve issues without changing functionality
- Small fixes to existing code
- Documentation updates that don't affect code behavior
- Typo corrections in code comments or docstrings
- Minor internal refactoring that doesn't affect public API
- Test improvements or test coverage increases
- Linting or code style fixes

**Examples:**
- Fix: "Corrected parent attribute type from object to string"
- Fix: "Fixed markdown output indentation for nested packages"
- Fix: "Resolved edge case in attribute parsing for multi-line tables"
- Docs: "Updated docstring for AutosarClass to clarify parent attribute"
- Tests: "Added test coverage for edge case in parent resolution"

**Process:**
1. Make the bug fix
2. Run full test suite to ensure no regressions
3. Update version in `src/autosar_pdf2txt/__init__.py`: `__version__ = "0.1.1"`
4. Commit with message format: `fix: description` or `docs: description`
5. Create git tag: `git tag v0.1.1`

---

### MINOR Version (Y in X.Y.Z)

**When to increment:**
- New backward-compatible features added
- New public API methods or classes added
- New functionality that doesn't break existing code
- Deprecation of old features (but features still work)
- New command-line options added
- New data model fields with default values
- Enhancements to existing features

**Examples:**
- Feature: "Added AutosarDoc class to represent parsed document structure"
- Feature: "Added --write-class-files CLI option for per-class markdown output"
- Feature: "Added support for ATP marker extraction from PDFs"
- Feature: "Added enumeration literal extraction with index support"
- Enhancement: "Improved error messages in parser for better debugging"

**Process:**
1. Implement the new feature
2. Add tests for the new functionality
3. Update documentation (requirements, docstrings)
4. Update version in `src/autosar_pdf2txt/__init__.py`: `__version__ = "0.2.0"`
5. Commit with message format: `feat: description`
6. Create git tag: `git tag v0.2.0`

---

### MAJOR Version (X in X.Y.Z)

**Controlled by project lead only.**

**When to increment:**
- Breaking changes to public API
- Removal of deprecated features
- Changes that require user code updates
- Incompatible changes to data models
- Changes to CLI interface that break existing usage
- Major redesigns or rewrites

**Examples:**
- Breaking: "Removed deprecated AutosarPackage.get_class_by_name() method"
- Breaking: "Changed MarkdownWriter constructor to require output path parameter"
- Breaking: "Renamed CLI command from 'autosar-extract' to 'autosar parse'"

**Process:**
1. Project lead decides on major version bump
2. Plan breaking changes and migration guide
3. Implement breaking changes
4. Update all documentation
5. Update version in `src/autosar_pdf2txt/__init__.py`: `__version__ = "1.0.0"`
6. Create migration guide if needed
7. Commit with message format: `BREAKING CHANGE: description`
8. Create git tag: `git tag v1.0.0`

---

## Commit Message Conventions

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>: <description>

[optional body]

[optional footer]
```

### Commit Types

| Type | Description | Version Impact |
|------|-------------|----------------|
| `fix` | Bug fix | PATCH |
| `feat` | New feature | MINOR |
| `docs` | Documentation only | PATCH |
| `style` | Code style changes (formatting) | PATCH |
| `refactor` | Code refactoring | PATCH (if backward-compatible) |
| `perf` | Performance improvements | PATCH |
| `test` | Adding or updating tests | PATCH |
| `chore` | Build process, tooling, dependencies | PATCH |
| `BREAKING CHANGE` | Breaking change | MAJOR |

### Commit Message Examples

```bash
# Patch version (bug fix)
fix: correct parent attribute type from object to string

# Patch version (documentation)
docs: update docstring for AutosarClass parent attribute

# Minor version (new feature)
feat: add AutosarDoc class with root_classes collection

# Minor version (enhancement)
feat: add --write-class-files CLI option for per-class output

# Major version (breaking change)
BREAKING CHANGE: remove deprecated AutosarPackage.get_class_by_name() method
```

---

## Pre-release Versions

For development versions, use pre-release identifiers:

- `0.2.0-alpha.1` - First alpha release
- `0.2.0-beta.1` - First beta release
- `0.2.0-rc.1` - First release candidate
- `0.2.0` - Final release

---

## Version File Location

The version is defined in: `src/autosar_pdf2txt/__init__.py`

```python
__version__ = "0.1.0"
```

---

## Release Checklist

Before creating a release:

1. **Run full test suite**
   ```bash
   python scripts/run_tests.py --all
   ```

2. **Run linting and type checking**
   ```bash
   ruff check src/ tests/
   mypy src/autosar_pdf2txt/
   ```

3. **Update version number** in `src/autosar_pdf2txt/__init__.py`

4. **Update CHANGELOG.md** (if it exists)

5. **Commit changes**
   ```bash
   git add src/autosar_pdf2txt/__init__.py
   git commit -m "chore: bump version to X.Y.Z"
   ```

6. **Create git tag**
   ```bash
   git tag -a vX.Y.Z -m "Release X.Y.Z"
   git push origin vX.Y.Z
   ```

---

## Current Version

Current version: **0.1.0**

Recent changes:
- Initial release with PDF parsing, markdown output, and CLI
- Support for AUTOSAR classes, enumerations, and packages
- ATP marker extraction and attribute parsing

---

## Requirement Version Synchronization

**Rule: Requirement versions shall be synced with source code.**

### Principle

The codebase and requirements documentation must maintain consistency at all times. When source code changes affect requirements, the requirements must be updated in the same commit.

### Requirement-Code Sync Rules

#### When Adding New Features

1. **Before coding**: Add requirement with maturity `draft`
2. **During coding**: Implement feature with requirement ID in docstrings
3. **After testing**: Change requirement maturity to `accept`
4. **Single commit**: Include both code and requirement changes

```bash
# Example: Adding new feature
# 1. Add requirement to docs/requirements/requirements.md
# 2. Implement feature in src/autosar_pdf2txt/...
# 3. Add tests to tests/...
# 4. Commit all changes together
git add docs/requirements/requirements.md src/autosar_pdf2txt/... tests/...
git commit -m "feat: add AutosarDoc class for document model

- Add SWR_MODEL_00023 requirement
- Implement AutosarDoc with packages and root_classes
- Update parser to return AutosarDoc instead of List[AutosarPackage]"
```

#### When Fixing Bugs

If a bug fix relates to a specific requirement:
1. Update the requirement description if needed
2. Implement the fix
3. Reference requirement ID in commit message

```bash
git add docs/requirements/requirements.md src/autosar_pdf2txt/...
git commit -m "fix: correct parent attribute type to string

- Update SWR_MODEL_00022 to clarify parent as string type
- Fix AutosarClass.parent to use str instead of object reference"
```

#### When Refactoring

1. Review affected requirements
2. Update requirement IDs/references in code docstrings
3. Update requirements document if needed
4. Commit changes together

#### Requirement Maturity Levels

Requirements have three maturity levels that reflect code status:

| Maturity | Description | Code Status |
|----------|-------------|-------------|
| `draft` | New requirement, not yet implemented | Feature not implemented |
| `accept` | Implemented and tested | Feature in codebase |
| `invalid` | Deprecated or superseded | Feature removed |

### Commit Verification Checklist

Before committing, verify:

- [ ] If new feature added → Requirement exists with ID in `docs/requirements/requirements.md`
- [ ] If requirement added → Maturity set to `draft` initially
- [ ] If feature implemented → Requirement maturity updated to `accept`
- [ ] If code references requirement → Requirement ID included in docstring
- [ ] If requirement changed → Code updated to match
- [ ] If feature removed → Requirement maturity set to `invalid`

### Examples

#### ✅ Correct: Feature Addition
```bash
# Single commit with all changes
git add docs/requirements/requirements.md
git add src/autosar_pdf2txt/models/autosar_models.py
git add tests/models/test_autosar_models.py
git commit -m "feat: add AutosarDoc class

- Add SWR_MODEL_00023: AUTOSAR Document Model
- Implement AutosarDoc dataclass with packages and root_classes
- Add validation and query methods
- Update parser to return AutosarDoc
- Add unit tests for AutosarDoc"
```

#### ✅ Correct: Bug Fix
```bash
# Single commit with requirement and code updates
git add docs/requirements/requirements.md
git add src/autosar_pdf2txt/models/autosar_models.py
git commit -m "fix: change parent attribute from object to string

- Update SWR_MODEL_00022 to describe parent as string type
- Modify AutosarClass.parent to Optional[str]
- Update parser to set parent as base class name string
- Update all tests to use string parent"
```

#### ❌ Incorrect: Separate Commits
```bash
# WRONG: Requirement added separately from code
git add docs/requirements/requirements.md
git commit -m "docs: add SWR_MODEL_00023"

git add src/autosar_pdf2txt/models/autosar_models.py
git commit -m "feat: implement AutosarDoc"
```

### Automation Check

Run this command to verify requirement-code sync:

```bash
# Check for orphaned requirements (draft maturity but implemented)
grep -A 2 "Maturity: draft" docs/requirements/requirements.md

# Check for code references without requirements
grep -r "SWR_MODEL_\|SWR_PARSER_\|SWR_WRITER_\|SWR_CLI_" src/ | cut -d: -f3 | \
  grep -oE "SWR_[A-Z]+_[0-9]+" | sort -u
```

### Benefits

- **Traceability**: Every feature has a requirement ID
- **Documentation**: Requirements always reflect actual code
- **Quality**: Code reviews include requirement verification
- **Maintenance**: Easy to understand why features exist
