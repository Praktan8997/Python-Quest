# Python Quest — Project Specification

## 1. Project Overview

Python Quest is a gamified, interactive Python learning platform designed for students attending a Python bootcamp.

The platform should provide a learning experience inspired by modern gamified coding platforms such as Coddy.tech, but it must be an original implementation with its own UI, branding, content structure, and features.

The goal is to make Python learning:

* Interactive
* Fun
* Practical
* Competitive
* Beginner-friendly
* Progress-oriented

Students should be able to either:

1. Follow a recommended learning path.
2. Directly jump to any Python topic they want.

The platform should not force students to complete topics in a fixed order.

---

# 2. Target Users

## Students

Students can:

* Create/login to their account.
* Browse Python topics.
* Learn concepts.
* Read examples.
* Write and execute Python code.
* Solve coding challenges.
* Take quizzes.
* Earn XP.
* Unlock badges.
* Track progress.
* View leaderboard.
* Jump directly to any topic.
* Continue previously started challenges.

## Instructor

Instructor functionality should eventually allow:

* Creating/managing bootcamp sessions.
* Viewing enrolled students.
* Monitoring student progress.
* Viewing topic completion.
* Viewing quiz/challenge performance.
* Viewing leaderboard.
* Identifying difficult topics.
* Managing challenges and quiz questions.

Instructor functionality can initially be implemented as a basic dashboard and expanded later.

---

# 3. Core Learning Experience

Every topic should follow a consistent structure:

```text
Topic
  ↓
Learn
  ↓
Example
  ↓
Try It
  ↓
Challenge
  ↓
Quiz
  ↓
XP / Progress
```

Example:

```text
Loops
 ├── Learn
 ├── Examples
 ├── Interactive Practice
 ├── Coding Challenges
 └── Quiz
```

Students should receive immediate feedback wherever possible.

---

# 4. Python Curriculum

The initial curriculum consists of:

## Level 1 — Python Basics

1. Python Syntax
2. Comments
3. Variables
4. Data Types
5. Strings
6. Booleans
7. Operators

## Level 2 — Control Flow

8. if
9. elif
10. else
11. for loop
12. while loop

## Level 3 — Collections

13. Lists
14. Tuples
15. Sets
16. Dictionaries

## Level 4 — Functions

17. Functions
18. Function Calling
19. Function Parameters
20. Return Values
21. Function Decorators

## Level 5 — Python Environment

22. PIP
23. Virtual Environment

The curriculum can be expanded later.

---

# 5. Navigation Model

The platform MUST support two learning modes.

## Guided Path

The recommended path should be:

```text
Python Basics
      ↓
Data Types
      ↓
Operators
      ↓
Conditions
      ↓
Loops
      ↓
Collections
      ↓
Functions
      ↓
Decorators
      ↓
PIP
      ↓
Virtual Environment
      ↓
Final Challenge
```

This path is only a recommendation.

It should NOT prevent students from accessing other topics.

## Explore Mode

Students should be able to open any topic directly.

For example:

```text
Topics

Syntax
Variables
Data Types
Strings
Booleans
Operators
If / Else
For Loop
While Loop
Lists
Tuples
Sets
Dictionaries
Functions
Decorators
PIP
Virtual Environment
```

Clicking "Functions" should open Functions regardless of whether previous topics are completed.

---

# 6. Dashboard

The student dashboard should show:

* Welcome message
* Current XP
* Level
* Current streak
* Overall progress
* Topics completed
* Continue Learning
* Recent challenges
* Badges
* Leaderboard preview

Example:

```text
Welcome back, Alex 👋

Level 7
1,250 XP
🔥 4 Day Streak

Overall Progress
████████████░░░░ 78%

Continue Learning
Functions → Challenge 3

Topics Mastered
12 / 23

Leaderboard
1. Team Alpha
2. Team Byte
3. Team Debuggers
```

---

# 7. Topic Page

Every topic should have:

```text
Topic Header
    ↓
Concept Explanation
    ↓
Code Example
    ↓
Interactive Code Editor
    ↓
Practice Challenge
    ↓
Quiz
    ↓
Completion / XP
```

Example:

```text
FOR LOOPS

Learn
A for loop is used to repeat a block of code
for each item in a sequence.

Example:

for i in range(5):
    print(i)

[ Try It ]

Challenge:
Print numbers from 1 to 10.

[Run Code]

Result:
✓ Correct!

+100 XP
```

---

# 8. Gamification

Gamification is one of the most important parts of the application.

## XP

Students earn XP from:

* Completing lessons
* Completing challenges
* Passing quizzes
* Daily activity
* Special challenges
* Boss challenges

Example:

```text
Lesson complete     +20 XP
Challenge complete  +50 XP
Quiz passed         +75 XP
Boss challenge      +250 XP
```

Do not make XP values hardcoded throughout the frontend. Store them in configuration/database logic.

---

# 9. Levels

Students should level up based on XP.

Example:

```text
Level 1 → 0 XP
Level 2 → 100 XP
Level 3 → 250 XP
Level 4 → 500 XP
Level 5 → 850 XP
```

The exact XP curve should be configurable.

---

# 10. Badges

Possible badges:

```text
🐍 First Python Program
💡 Variable Master
🔀 Decision Maker
🔁 Loop Warrior
📦 Collection Master
⚙️ Function Builder
🧙 Decorator Apprentice
📦 Package Manager
🚀 Environment Explorer
👑 Python Boss
```

Badges should be stored as data, not hardcoded into UI components.

---

# 11. Coding Challenges

Challenges should contain:

* Title
* Description
* Difficulty
* Topic
* Starter code
* Expected behavior
* Test cases
* XP reward
* Optional hint
* Optional solution explanation

Difficulty levels:

```text
Easy
Medium
Hard
Boss
```

Example:

```text
Challenge: Even or Odd

Difficulty: Easy
XP: 50

Write a Python program that checks whether
a given number is even or odd.

Input:
10

Expected Output:
Even
```

---

# 12. Code Execution

Students must be able to write Python code in an in-browser editor.

The architecture should NOT execute arbitrary student code directly inside the FastAPI application process.

Code execution must be isolated.

Preferred architecture:

```text
React
  ↓
FastAPI
  ↓
Code Execution Service
  ↓
Isolated Python Sandbox
  ↓
Result
```

The sandbox should eventually enforce:

* Execution timeout
* Memory limits
* CPU limits
* Restricted filesystem access
* No unrestricted network access
* Process isolation

For the first prototype, use a safe development approach and clearly separate the execution service from the main backend.

Never expose unrestricted server-side command execution to students.

---

# 13. Quiz System

Quizzes should support:

* Multiple-choice questions
* Four options
* Correct answer
* Explanation
* XP reward
* Score
* Topic association
* Difficulty

Example:

```text
What is the output?

x = 10
print(type(x))

A. string
B. integer
C. float
D. boolean
```

After submission:

```text
Correct!

+25 XP
```

Questions should be stored in the database.

Do not hardcode all quiz questions into React components.

---

# 14. Leaderboard

Leaderboard should support:

* Global ranking
* Bootcamp/session ranking
* XP
* Level
* Completed challenges

Example:

```text
#   Student          XP

1   Alex             2450
2   Rahul            2210
3   Priya            1980
4   Arjun            1840
```

Avoid using rankings as the only indicator of learning.

Students should also be able to see their own progress and achievements.

---

# 15. Instructor Dashboard

Initial instructor dashboard:

```text
Total Students
Active Students
Average Progress
Challenges Completed
Average Quiz Score
```

Topic analytics:

```text
Syntax              92%
Variables           88%
Conditions          79%
Loops               61%
Functions           43%
Decorators          21%
```

The instructor should be able to identify where students are struggling.

---

# 16. Technology Stack

Preferred initial stack:

## Frontend

* React
* Vite
* Tailwind CSS
* React Router
* JavaScript or TypeScript

Use TypeScript if practical.

## Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy

## Database

* MySQL

## Authentication

Implement a secure authentication system.

Passwords must never be stored as plain text.

Use password hashing.

## Code Editor

Use a browser code editor such as Monaco Editor if appropriate.

Do not reinvent a full code editor.

---

# 17. Suggested Project Structure

```text
python-quest/

├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── layouts/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── context/
│   │   ├── utils/
│   │   └── types/
│   ├── public/
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── core/
│   │   └── utils/
│   ├── tests/
│   └── requirements.txt
│
├── execution-service/
│   └── ...
│
├── database/
│   ├── migrations/
│   └── seed/
│
├── docs/
│
├── .env.example
├── .gitignore
├── README.md
├── gemini.md
└── agents.md
```

---

# 18. Database Entities

Initial entities:

```text
User
StudentProfile
InstructorProfile
Topic
Lesson
Challenge
ChallengeTestCase
Quiz
QuizQuestion
QuizOption
Submission
Progress
Badge
UserBadge
XPTransaction
Leaderboard
BootcampSession
Enrollment
```

Relationships should be normalized.

Do not duplicate data unnecessarily.

---

# 19. API Design

Use REST APIs.

Example:

```text
POST   /api/auth/register
POST   /api/auth/login
GET    /api/users/me

GET    /api/topics
GET    /api/topics/{topic_id}

GET    /api/topics/{topic_id}/lessons
GET    /api/topics/{topic_id}/challenges

POST   /api/challenges/{challenge_id}/submit

GET    /api/quizzes/{quiz_id}
POST   /api/quizzes/{quiz_id}/submit

GET    /api/progress
GET    /api/leaderboard

GET    /api/badges
GET    /api/users/me/badges
```

Keep business logic out of route files where possible.

---

# 20. UI / UX Direction

The UI should feel:

* Modern
* Young
* Developer-focused
* Gamified
* Clean
* Fast
* Responsive

Avoid making it look like a generic college management system.

Use:

* Cards
* Progress bars
* XP indicators
* Topic icons
* Code blocks
* Interactive states
* Achievement animations
* Clear hierarchy

Do not overuse animations.

The interface should remain usable on:

* Laptop
* Desktop
* Tablet
* Mobile

---

# 21. Design Philosophy

The product should feel like:

```text
Duolingo-style progression
        +
Coding practice
        +
Game-like XP
        +
Bootcamp competition
```

But it should have original branding and UI.

Do not copy Coddy.tech's exact interface, assets, wording, or visual design.

---

# 22. MVP

The first version MUST NOT attempt to build every feature.

MVP should contain:

1. Student registration/login
2. Dashboard
3. Topic list
4. Topic details
5. Lesson content
6. Code editor
7. Basic Python execution
8. Coding challenges
9. Quiz
10. XP
11. Progress tracking
12. Leaderboard

After MVP is stable:

```text
Phase 2:
- Badges
- Streaks
- Instructor dashboard
- Bootcamp sessions
- Advanced challenges

Phase 3:
- Advanced sandbox
- Analytics
- Certificates
- More languages
- AI hints
```

---

# 23. Development Philosophy

Build incrementally.

Do NOT generate the entire application in one giant implementation.

Recommended order:

```text
1. Project setup
2. Database
3. Authentication
4. Topic system
5. Student dashboard
6. Lesson system
7. Challenge system
8. Code execution
9. Quiz system
10. XP / progress
11. Leaderboard
12. Instructor dashboard
```

Each phase must be tested before moving to the next.

---

# 24. Environment Variables

Use `.env`.

Example:

```env
DATABASE_URL=
SECRET_KEY=
JWT_SECRET=
CODE_EXECUTION_URL=
```

Never commit real secrets.

Provide `.env.example`.

---

# 25. Important Rules

* Do not hardcode secrets.
* Do not hardcode database credentials.
* Do not put business logic inside React components.
* Do not put all backend logic inside `main.py`.
* Do not execute untrusted Python directly inside FastAPI.
* Validate all API input.
* Handle errors properly.
* Use meaningful HTTP status codes.
* Keep components reusable.
* Keep API services separate from UI components.
* Write clean, readable code.
* Avoid unnecessary dependencies.
* Do not modify unrelated files without reason.
* Preserve existing functionality when implementing new features.

---

# 26. Definition of Done

A feature is not complete merely because the UI exists.

A feature is complete when:

```text
UI
 ↓
API
 ↓
Database
 ↓
Business Logic
 ↓
Error Handling
 ↓
Validation
 ↓
Testing
```

all work together.

The application should be runnable by another developer using the README instructions.

---

# 27. Future Vision

Python Quest should eventually become a platform where a bootcamp organizer can create a complete coding learning experience.

Future possibilities:

* Multiple programming languages
* AI coding hints
* AI explanations
* Classroom sessions
* Real-time competitions
* Team battles
* Certificates
* Code reviews
* Coding tournaments
* Instructor-created courses
* Public challenge library

However, future features should not complicate the MVP.

# 28. Deployment

Deployment is part of the project requirements.

The application must be deployable to a production environment and should not depend on localhost-specific configuration.

## Production Architecture

Preferred architecture:

Frontend:
- React + Vite
- Deploy to Vercel or equivalent static hosting

Backend:
- FastAPI
- Deploy to Render, Railway, or equivalent cloud platform

Database:
- Managed MySQL database

Code Execution:
- Separate isolated execution service/container
- Never execute untrusted student code directly inside the main FastAPI server

## Production Environment Variables

Frontend may require:

VITE_API_BASE_URL=

Backend may require:

DATABASE_URL=
SECRET_KEY=
JWT_SECRET=
CORS_ORIGINS=
CODE_EXECUTION_URL=

Never commit production secrets.

## CORS

The FastAPI backend must allow requests from the deployed frontend domain.

Do not use unrestricted:

allow_origins=["*"]

in production when credentials/authentication are involved.

Configure allowed origins through environment variables.

## Database

Production database configuration must come from environment variables.

Do not hardcode:

- Host
- Username
- Password
- Database name
- Port

Use database migrations.

## Production Build

Frontend:

npm install
npm run build

Backend:

Use a production ASGI server configuration.

Example:

uvicorn app.main:app --host 0.0.0.0 --port $PORT

The exact deployment command should match the selected hosting provider.

## Deployment Files

Create appropriate deployment configuration files when required by the chosen platform.

Examples may include:

- Dockerfile
- .dockerignore
- render.yaml
- railway configuration
- vercel configuration

Do not create unnecessary deployment files for platforms that are not being used.

## Health Check

Backend should provide:

GET /health

Response:

{
  "status": "ok"
}

The endpoint should not require authentication.

## Deployment Documentation

README.md must contain:

1. Local setup
2. Environment variables
3. Database setup
4. Frontend deployment
5. Backend deployment
6. Database deployment
7. Code execution service deployment
8. Production troubleshooting

## Deployment Verification

Before declaring deployment complete, verify:

- Frontend loads
- Frontend can communicate with backend
- Authentication works
- Database connection works
- Topics load
- Challenges load
- Quiz submission works
- XP updates correctly
- Leaderboard loads
- API health check works

Do not claim deployment is successful without actually verifying the deployed application.

## Deployment Priority

The agent should first make the application locally stable.

Then prepare production configuration.

Then deploy each service.

Recommended order:

1. Database
2. Backend
3. Frontend
4. Code execution service
5. Connect production services
6. Run end-to-end tests
7. Update README with production URLs
