# AI Coding Agent Instructions — Python Quest

## 1. Role

You are the primary software engineering agent working on the Python Quest project.

Your responsibility is to design, implement, test, debug, and document the application while following the requirements defined in `gemini.md`.

Treat `gemini.md` as the product specification.

Treat this file as the development and engineering rules.

---

# 2. Before Writing Code

Before implementing any feature:

1. Inspect the existing project structure.
2. Read `gemini.md`.
3. Inspect related existing files.
4. Understand the current architecture.
5. Check whether the requested feature already partially exists.
6. Reuse existing components/services where appropriate.
7. Avoid creating duplicate implementations.

Do not blindly generate new files.

---

# 3. Development Approach

Always work incrementally.

For a new feature:

```text
Understand
   ↓
Plan
   ↓
Implement
   ↓
Run
   ↓
Test
   ↓
Fix
   ↓
Document
```

Do not attempt to build the entire platform in one operation.

---

# 4. Project Architecture

Follow:

```text
Frontend
React + Vite
      ↓
REST API
      ↓
FastAPI
      ↓
Service Layer
      ↓
Repository / ORM
      ↓
MySQL
```

Keep responsibilities separated.

Frontend should handle:

* UI
* User interactions
* Client-side state
* API communication
* Navigation

Backend should handle:

* Authentication
* Authorization
* Validation
* Business logic
* Database operations
* XP calculation
* Progress calculation
* Challenge evaluation
* Quiz evaluation

---

# 5. Frontend Rules

Use reusable components.

Prefer:

```text
components/
pages/
layouts/
hooks/
services/
utils/
types/
```

Do not create massive components containing hundreds of lines of unrelated logic.

Avoid:

```text
Dashboard.jsx
```

containing the entire dashboard application.

Prefer:

```text
Dashboard
├── StatsCard
├── ProgressCard
├── ContinueLearning
├── RecentChallenges
└── LeaderboardPreview
```

Use consistent naming.

---

# 6. API Communication

Do not place raw API calls throughout random React components.

Create a service layer.

Example:

```text
services/
├── authService
├── topicService
├── challengeService
├── quizService
├── progressService
└── leaderboardService
```

Handle:

* Loading
* Success
* Errors
* Authentication failures
* Empty states

---

# 7. Backend Rules

FastAPI route files should remain thin.

Prefer:

```text
Route
  ↓
Service
  ↓
Repository
  ↓
Database
```

Do not put complex business logic directly inside route functions.

Use Pydantic schemas for request/response validation.

Use SQLAlchemy models for database entities.

---

# 8. Database Rules

Use normalized database design.

Do not duplicate information unnecessarily.

Use foreign keys where relationships exist.

Use timestamps where useful:

```text
created_at
updated_at
```

Use migrations instead of manually modifying production tables.

Never delete data casually.

Before destructive database operations, verify the consequences.

---

# 9. Authentication

Authentication must be implemented securely.

Never:

* Store plaintext passwords.
* Commit secrets.
* Hardcode JWT secrets.
* Put credentials in frontend source code.

Use environment variables.

Validate authenticated requests on the backend.

Do not trust user-provided user IDs for authorization.

---

# 10. Code Execution Security

This is a critical requirement.

Students will submit Python code.

NEVER execute arbitrary student code directly using:

```python
exec()
eval()
subprocess
os.system()
```

inside the main FastAPI process.

Use an isolated execution service/sandbox architecture.

The execution environment should eventually enforce:

* Time limits
* Memory limits
* CPU limits
* Process limits
* Filesystem restrictions
* Network restrictions

If a secure sandbox is not yet implemented, create a clearly separated development abstraction rather than pretending the execution system is production-safe.

---

# 11. Challenge Architecture

A challenge should be represented as data.

Example:

```text
Challenge
├── id
├── title
├── description
├── topic_id
├── difficulty
├── starter_code
├── xp_reward
├── hint
└── test_cases
```

Do not hardcode challenge logic into React.

Challenge evaluation belongs on the backend/execution service.

---

# 12. Quiz Architecture

Quiz questions should come from the database.

Do not write large collections of quiz questions directly inside JSX.

The frontend should receive quiz data from the API.

Quiz submission should be validated server-side.

Never trust the frontend to determine the final score.

---

# 13. XP System

XP calculations should happen on the backend.

The frontend may display XP but should not be the authority for awarding XP.

Use an XP transaction/history system where practical.

Example:

```text
XPTransaction

id
user_id
amount
reason
reference_type
reference_id
created_at
```

This makes XP changes auditable.

---

# 14. Progress System

Track progress independently for each topic.

Example:

```text
User
  ↓
Topic Progress

Learned
Practice
Challenges
Quiz
Completion
```

A student must be able to jump directly to any topic.

Do not enforce prerequisite locks unless the product specification explicitly changes.

---

# 15. Gamification

Gamification should enhance learning rather than make the UI distracting.

Use:

* XP
* Levels
* Progress bars
* Badges
* Streaks
* Challenges
* Leaderboards

Avoid excessive animations.

Respect reduced-motion preferences where practical.

---

# 16. UI Design

The UI should be:

* Clean
* Modern
* Responsive
* Developer-oriented
* Gamified
* Easy for beginners

Avoid:

* Excessive gradients
* Excessive animations
* Cluttered dashboards
* Tiny text
* Poor contrast
* Huge unnecessary components

Use a consistent design system.

Do not randomly introduce new colors or styles for every component.

---

# 17. Error Handling

Every API should have meaningful error handling.

Frontend should display useful messages.

Bad:

```text
Something went wrong
```

Better:

```text
Unable to load challenges.
Please try again.
```

Backend errors should be logged appropriately without exposing sensitive information.

---

# 18. Testing

Every significant backend feature should have tests.

At minimum test:

* Authentication
* Topic retrieval
* Challenge retrieval
* Challenge submission
* Quiz submission
* XP calculation
* Progress updates

Frontend should be manually tested after major UI changes.

Before declaring a feature complete:

```text
Run application
Test happy path
Test invalid input
Test empty state
Test error state
```

---

# 19. Debugging

When an error occurs:

1. Read the complete error.
2. Identify the root cause.
3. Inspect related code.
4. Fix the root cause.
5. Re-run the affected functionality.
6. Check for regressions.

Do not repeatedly apply random changes.

Do not hide errors by adding broad exception handlers.

---

# 20. Dependencies

Before installing a package:

1. Check whether an existing dependency can solve the problem.
2. Check whether the package is necessary.
3. Prefer stable and maintained packages.
4. Avoid dependency bloat.

After adding a dependency, update the relevant dependency file.

---

# 21. Environment Configuration

Use:

```text
.env
.env.example
```

Never commit:

```text
.env
```

The `.env.example` file should document required variables without containing real secrets.

---

# 22. Git Practices

Make changes that are logically grouped.

Use meaningful commit messages when commits are requested.

Example:

```text
feat: add topic progress tracking
feat: add challenge submission API
fix: handle expired authentication token
refactor: separate challenge service
```

Do not overwrite unrelated user changes.

---

# 23. Existing User Work

The user may already have code in the project.

Before modifying a file:

* Read it.
* Understand it.
* Preserve useful existing functionality.
* Do not rewrite working code unnecessarily.

Never replace an entire project with a generated template unless explicitly instructed.

---

# 24. Documentation

Keep README updated when setup or architecture changes.

Document:

* Installation
* Environment variables
* Database setup
* Frontend setup
* Backend setup
* Running the application
* Testing
* Development workflow

If a complex architectural decision is introduced, document it.

---

# 25. Response Style

When reporting progress to the user:

Be concise and practical.

Use:

```text
Implemented
Changed
Tested
Next
```

Example:

```text
Implemented:
- Topic API
- Topic database model
- Topic list UI

Tested:
- GET /api/topics
- Topic navigation
- Empty state

Next:
- Challenge system
```

Do not claim something works unless it was actually tested.

---

# 26. Do Not Overengineer

The project is initially a bootcamp MVP.

Prefer simple solutions.

Do not introduce:

* Microservices everywhere
* Complex event buses
* Kubernetes
* Distributed systems
* Unnecessary AI infrastructure

unless the project actually requires them.

The architecture should be scalable enough to grow but simple enough for a student project.

---

# 27. Implementation Priority

When deciding what to build next, use this priority:

```text
1. Core functionality
2. Security
3. Data correctness
4. User experience
5. Performance
6. Visual polish
7. Advanced features
```

Do not prioritize animations over broken functionality.

---

# 28. Current MVP Order

Build in this order:

### Phase 1

```text
Project setup
Frontend
FastAPI
MySQL
Basic routing
```

### Phase 2

```text
Authentication
User model
Student dashboard
```

### Phase 3

```text
Topics
Lessons
Topic navigation
Progress
```

### Phase 4

```text
Code editor
Challenge system
Code execution abstraction
```

### Phase 5

```text
Quiz
XP
Leaderboard
```

### Phase 6

```text
Badges
Streaks
Instructor dashboard
```

### Phase 7

```text
Secure code sandbox
Advanced analytics
AI hints
Bootcamp management
```

---

# 29. Final Rule

The goal is not to generate the maximum amount of code.

The goal is to build a working, maintainable Python learning platform.

Before adding complexity, ask:

> Does this directly improve Python Quest for its students or instructors?

If not, avoid it.

Always prefer:

```text
Simple + Working + Tested
```

over:

```text
Complex + Unfinished + Untested
```
