import os
import sys

# ─── Load environment variables ───────────────────────────────────────────────
# Supports: DATABASE_URL env var to seed any database (SQLite or PostgreSQL)
# Usage for production seeding:
#   $env:DATABASE_URL = "postgresql://user:pass@host/dbname"  (PowerShell)
#   DATABASE_URL="postgresql://..." python seed_data.py       (Linux/Mac)
try:
    from dotenv import load_dotenv
    # Load from backend/.env first (for local dev), then database/.env
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'backend', '.env'))
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
except ImportError:
    pass  # dotenv not required if DATABASE_URL is set directly in environment

# Add backend directory to path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.insert(0, backend_path)

from app.core.database import SessionLocal, engine, Base
from app.models.models import Topic, Lesson, Challenge, ChallengeTestCase, Quiz, QuizQuestion, QuizOption, Badge, UserProgress, XPTransaction, QuizAttempt, QuizAnswer, Submission, User

def seed():
    print("Recreating database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        print("Seeding expanded Python Quest curriculum (19 Topics, 38+ Challenges, 57+ Quiz Questions)...")

        CURRICULUM = [
            # ================= MODULE 1: BASICS =================
            {
                "title": "Syntax",
                "slug": "python-syntax",
                "level_number": 1,
                "level_title": "Basics",
                "order_index": 1,
                "icon": "Code",
                "description": "Master Python statement structure, indentation, and printing outputs.",
                "lessons": [
                    {
                        "title": "Python Syntax & Indentation Rules",
                        "content": "Python uses new lines to complete a command and indentation (whitespace) to define scope blocks. Unlike languages using `{}` or `;`, Python relies on clean, readable indentation.",
                        "code_example": "# Printing text and numbers\nprint('Welcome to Python Quest!')\nprint(2026)"
                    }
                ],
                "challenges": [
                    {
                        "title": "Challenge 1.1: First Command",
                        "description": "Write a Python statement that prints `Welcome, Python Quest!` to the terminal.",
                        "difficulty": "Easy",
                        "starter_code": "# Write a print statement that outputs 'Welcome, Python Quest!'\n",
                        "xp_reward": 50,
                        "hint": "Use print('Welcome, Python Quest!')",
                        "solution_explanation": "print() displays the specified string to stdout.",
                        "test_cases": [{"input": "", "expected_output": "Welcome, Python Quest!"}]
                    },
                    {
                        "title": "Challenge 1.2: Double Print",
                        "description": "Print `Line One` on the first line and `Line Two` on the second line.",
                        "difficulty": "Easy",
                        "starter_code": "# Write two print statements for 'Line One' and 'Line Two'\n",
                        "xp_reward": 50,
                        "hint": "Use two separate print calls.",
                        "solution_explanation": "Each print() call outputs on a new line by default.",
                        "test_cases": [{"input": "", "expected_output": "Line One\nLine Two"}]
                    }
                ],
                "quizzes": [
                    {
                        "title": "Syntax Mastery Quiz",
                        "xp_reward": 75,
                        "questions": [
                            {
                                "question": "How does Python define code blocks (functions, loops, conditions)?",
                                "explanation": "Python relies on indentation (whitespace at line start) rather than curly braces.",
                                "options": [
                                    {"text": "Indentation (whitespace)", "is_correct": True},
                                    {"text": "Curly braces {}", "is_correct": False},
                                    {"text": "Semicolons ;", "is_correct": False},
                                    {"text": "Parentheses ()", "is_correct": False}
                                ]
                            },
                            {
                                "question": "What is the output of print(3 + 4 * 2)?",
                                "explanation": "Operator precedence performs multiplication (4 * 2 = 8) before addition (3 + 8 = 11).",
                                "options": [
                                    {"text": "11", "is_correct": True},
                                    {"text": "14", "is_correct": False},
                                    {"text": "24", "is_correct": False},
                                    {"text": "7", "is_correct": False}
                                ]
                            },
                            {
                                "question": "Is Python case-sensitive? (e.g. Print vs print)",
                                "explanation": "Yes, Python keywords and function names are case-sensitive; 'print' must be lowercase.",
                                "options": [
                                    {"text": "Yes, print is different from Print", "is_correct": True},
                                    {"text": "No, capitalization does not matter", "is_correct": False},
                                    {"text": "Only in strings", "is_correct": False},
                                    {"text": "Only on Linux", "is_correct": False}
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Comments",
                "slug": "comments",
                "level_number": 1,
                "level_title": "Basics",
                "order_index": 2,
                "icon": "MessageSquare",
                "description": "Use single-line and docstring comments to document your code.",
                "lessons": [
                    {
                        "title": "Writing Comments",
                        "content": "Comments start with `#` and are ignored by the Python execution engine. Docstrings `\"\"\"` document functions.",
                        "code_example": "# Single line comment\n\"\"\" Multiline comment or docstring \"\"\"\nprint('Code active')"
                    }
                ],
                "challenges": [
                    {
                        "title": "Challenge 2.1: Comment Slayer",
                        "description": "Add a comment `# Secret Code` and print `Code Active`.",
                        "difficulty": "Easy",
                        "starter_code": "# Add a comment '# Secret Code' and print 'Code Active'\n",
                        "xp_reward": 50,
                        "hint": "Comments start with #",
                        "solution_explanation": "Comments document code without affecting execution.",
                        "test_cases": [{"input": "", "expected_output": "Code Active"}]
                    },
                    {
                        "title": "Challenge 2.2: Clean Output",
                        "description": "Comment out the line `print('Bug')` so that only `print('Clean')` runs.",
                        "difficulty": "Easy",
                        "starter_code": "# Comment out the line below printing 'Bug'\nprint('Bug')\nprint('Clean')",
                        "xp_reward": 50,
                        "hint": "Add # in front of print('Bug')",
                        "solution_explanation": "Commenting out broken lines prevents them from executing.",
                        "test_cases": [{"input": "", "expected_output": "Clean"}]
                    }
                ],
                "quizzes": [
                    {
                        "title": "Comments Knowledge Quiz",
                        "xp_reward": 75,
                        "questions": [
                            {
                                "question": "Which symbol starts a single-line comment in Python?",
                                "explanation": "# symbol marks single-line comments.",
                                "options": [
                                    {"text": "#", "is_correct": True},
                                    {"text": "//", "is_correct": False},
                                    {"text": "/*", "is_correct": False},
                                    {"text": "--", "is_correct": False}
                                ]
                            },
                            {
                                "question": "Can comments execute code?",
                                "explanation": "No, comments are completely ignored during program execution.",
                                "options": [
                                    {"text": "No, they are ignored by Python", "is_correct": True},
                                    {"text": "Yes, if written in uppercase", "is_correct": False},
                                    {"text": "Only inside functions", "is_correct": False},
                                    {"text": "Yes, on line 1", "is_correct": False}
                                ]
                            },
                            {
                                "question": "Which quotes are used for multi-line docstring comments?",
                                "explanation": "Triple quotes \"\"\" or ''' are used for multi-line docstring comments.",
                                "options": [
                                    {"text": "\"\"\" Triple Quotes \"\"\"", "is_correct": True},
                                    {"text": "// Double Slash //", "is_correct": False},
                                    {"text": "-- Dash --", "is_correct": False},
                                    {"text": "<Doc> Tag </Doc>", "is_correct": False}
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Variables",
                "slug": "variables",
                "level_number": 1,
                "level_title": "Basics",
                "order_index": 3,
                "icon": "Box",
                "description": "Store, dynamic assign, and manipulate data in memory variables.",
                "lessons": [
                    {
                        "title": "Variables & Dynamic Assignment",
                        "content": "Variables are created when a value is assigned using `=`. Python automatically determines variable types.",
                        "code_example": "hero = 'Alex'\nlevel = 5\nprint(f'{hero} is at Level {level}')"
                    }
                ],
                "challenges": [
                    {
                        "title": "Challenge 3.1: Hero Allocator",
                        "description": "Create a variable `player = 'Quest Master'` and print it.",
                        "difficulty": "Easy",
                        "starter_code": "# Create variable player with value 'Quest Master' and print it\n",
                        "xp_reward": 50,
                        "hint": "player = 'Quest Master'",
                        "solution_explanation": "Variables hold references to objects.",
                        "test_cases": [{"input": "", "expected_output": "Quest Master"}]
                    },
                    {
                        "title": "Challenge 3.2: Value Swap",
                        "description": "Set `x = 10`, reassign `x = 20`, and print `x`.",
                        "difficulty": "Easy",
                        "starter_code": "# Set x = 10, reassign x to 20, and print x\n",
                        "xp_reward": 50,
                        "hint": "x = 20",
                        "solution_explanation": "Reassigning a variable updates its value.",
                        "test_cases": [{"input": "", "expected_output": "20"}]
                    }
                ],
                "quizzes": [
                    {
                        "title": "Variables Quiz",
                        "xp_reward": 75,
                        "questions": [
                            {
                                "question": "Which variable name is VALID in Python?",
                                "explanation": "Variable names can contain letters, numbers, and underscores, but cannot start with a number.",
                                "options": [
                                    {"text": "player_1", "is_correct": True},
                                    {"text": "1st_player", "is_correct": False},
                                    {"text": "player-name", "is_correct": False},
                                    {"text": "class", "is_correct": False}
                                ]
                            },
                            {
                                "question": "What happens when you reassign x = 5 then x = 'Hello'?",
                                "explanation": "Python is dynamically typed, so x changes from integer to string.",
                                "options": [
                                    {"text": "x becomes 'Hello' without error", "is_correct": True},
                                    {"text": "Throws TypeError", "is_correct": False},
                                    {"text": "x remains 5", "is_correct": False},
                                    {"text": "Creates x_1", "is_correct": False}
                                ]
                            },
                            {
                                "question": "Which operator assigns a value to a variable?",
                                "explanation": "= is the assignment operator.",
                                "options": [
                                    {"text": "=", "is_correct": True},
                                    {"text": "==", "is_correct": False},
                                    {"text": ":=", "is_correct": False},
                                    {"text": "->", "is_correct": False}
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Data Types",
                "slug": "data-types",
                "level_number": 1,
                "level_title": "Basics",
                "order_index": 4,
                "icon": "Database",
                "description": "Understand int, float, str, bool, and dynamic type checking with type().",
                "lessons": [
                    {
                        "title": "Core Data Types",
                        "content": "Python includes integers (`int`), floating-point decimals (`float`), strings (`str`), and booleans (`bool`). Use `type(val)` to check data type.",
                        "code_example": "a = 42       # int\nb = 3.14159  # float\nc = 'Python' # str\nprint(type(b))"
                    }
                ],
                "challenges": [
                    {
                        "title": "Challenge 4.1: Float Checker",
                        "description": "Set `val = 99.9` and print its type using `print(type(val))`.",
                        "difficulty": "Easy",
                        "starter_code": "val = 99.9\n# Print the data type of val\n",
                        "xp_reward": 50,
                        "hint": "type(val) returns <class 'float'>",
                        "solution_explanation": "type() returns object type.",
                        "test_cases": [{"input": "", "expected_output": "<class 'float'>"}]
                    },
                    {
                        "title": "Challenge 4.2: Type Casting",
                        "description": "Convert string `s = '50'` to an integer using `int(s)` and print `int(s) + 10`.",
                        "difficulty": "Easy",
                        "starter_code": "s = '50'\n# Convert s to int and add 10, then print the result\n",
                        "xp_reward": 50,
                        "hint": "int('50') returns 50",
                        "solution_explanation": "int() casts valid numerical strings to integers.",
                        "test_cases": [{"input": "", "expected_output": "60"}]
                    }
                ],
                "quizzes": [
                    {
                        "title": "Data Types Quiz",
                        "xp_reward": 75,
                        "questions": [
                            {
                                "question": "What is the data type of the result of 10 / 2?",
                                "explanation": "Standard division / in Python always returns a float (5.0).",
                                "options": [
                                    {"text": "float (5.0)", "is_correct": True},
                                    {"text": "int (5)", "is_correct": False},
                                    {"text": "str ('5')", "is_correct": False},
                                    {"text": "bool (True)", "is_correct": False}
                                ]
                            },
                            {
                                "question": "How do you convert string '123' to integer 123?",
                                "explanation": "int('123') casts the string to integer.",
                                "options": [
                                    {"text": "int('123')", "is_correct": True},
                                    {"text": "str.to_int('123')", "is_correct": False},
                                    {"text": "parse_int('123')", "is_correct": False},
                                    {"text": "integer('123')", "is_correct": False}
                                ]
                            },
                            {
                                "question": "Which of these is a floating-point number?",
                                "explanation": "Numbers with decimal points are float instances.",
                                "options": [
                                    {"text": "3.14", "is_correct": True},
                                    {"text": "3", "is_correct": False},
                                    {"text": "'3.14'", "is_correct": False},
                                    {"text": "True", "is_correct": False}
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Strings",
                "slug": "strings",
                "level_number": 1,
                "level_title": "Basics",
                "order_index": 5,
                "icon": "Type",
                "description": "Master f-strings, slicing [start:end], upper(), lower(), and len().",
                "lessons": [
                    {
                        "title": "String Operations & Slicing",
                        "content": "Strings are sequences of characters. Access characters by index `s[0]`, slice with `s[0:3]`, and format with f-strings `f'{name}'`.",
                        "code_example": "msg = 'Python Quest'\nprint(msg[0:6]) # 'Python'\nprint(msg.upper())"
                    }
                ],
                "challenges": [
                    {
                        "title": "Challenge 5.1: String Slicer",
                        "description": "Given `word = 'PYTHONQUEST'`, print the first 6 characters (`PYTHON`).",
                        "difficulty": "Easy",
                        "starter_code": "word = 'PYTHONQUEST'\n# Print the first 6 characters using slicing\n",
                        "xp_reward": 60,
                        "hint": "word[0:6] takes characters from index 0 to 5.",
                        "solution_explanation": "Slicing syntax is sequence[start:stop].",
                        "test_cases": [{"input": "", "expected_output": "PYTHON"}]
                    },
                    {
                        "title": "Challenge 5.2: F-String Formatter",
                        "description": "Given `name = 'Alex'` and `score = 100`, print `Alex scored 100` using f-string.",
                        "difficulty": "Easy",
                        "starter_code": "name = 'Alex'\nscore = 100\n# Print 'Alex scored 100' using an f-string\n",
                        "xp_reward": 60,
                        "hint": "f'{name} scored {score}'",
                        "solution_explanation": "f-strings evaluate expressions inside {} brackets.",
                        "test_cases": [{"input": "", "expected_output": "Alex scored 100"}]
                    }
                ],
                "quizzes": [
                    {
                        "title": "Strings Master Quiz",
                        "xp_reward": 75,
                        "questions": [
                            {
                                "question": "What is the output of 'Python'[1]?",
                                "explanation": "Strings are 0-indexed. Index 1 corresponds to 'y'.",
                                "options": [
                                    {"text": "'y'", "is_correct": True},
                                    {"text": "'P'", "is_correct": False},
                                    {"text": "'t'", "is_correct": False},
                                    {"text": "Error", "is_correct": False}
                                ]
                            },
                            {
                                "question": "Which method removes leading and trailing whitespace from a string?",
                                "explanation": ".strip() removes whitespace from start and end.",
                                "options": [
                                    {"text": ".strip()", "is_correct": True},
                                    {"text": ".trim()", "is_correct": False},
                                    {"text": ".clean()", "is_correct": False},
                                    {"text": ".cut()", "is_correct": False}
                                ]
                            },
                            {
                                "question": "How do you check the length of a string 's'?",
                                "explanation": "len(s) returns number of characters.",
                                "options": [
                                    {"text": "len(s)", "is_correct": True},
                                    {"text": "s.length()", "is_correct": False},
                                    {"text": "s.count()", "is_correct": False},
                                    {"text": "size(s)", "is_correct": False}
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Booleans",
                "slug": "booleans",
                "level_number": 1,
                "level_title": "Basics",
                "order_index": 6,
                "icon": "CheckSquare",
                "description": "Evaluate True/False expressions and truthy/falsy values.",
                "lessons": [
                    {
                        "title": "Boolean Logic & Truthiness",
                        "content": "Booleans represent `True` or `False`. Empty lists `[]`, empty strings `''`, `0`, and `None` evaluate to `False` in boolean contexts.",
                        "code_example": "print(bool(0))      # False\nprint(bool('Code')) # True"
                    }
                ],
                "challenges": [
                    {
                        "title": "Challenge 6.1: Truth Evaluator",
                        "description": "Print the boolean evaluation of `bool('Python')`.",
                        "difficulty": "Easy",
                        "starter_code": "# Print the boolean evaluation of 'Python'\n",
                        "xp_reward": 50,
                        "hint": "bool('Python') returns True",
                        "solution_explanation": "Non-empty strings evaluate to True.",
                        "test_cases": [{"input": "", "expected_output": "True"}]
                    },
                    {
                        "title": "Challenge 6.2: Greater Comparison",
                        "description": "Print the boolean result of `100 > 50`.",
                        "difficulty": "Easy",
                        "starter_code": "# Print the boolean result of 100 > 50\n",
                        "xp_reward": 50,
                        "hint": "100 > 50 is True",
                        "solution_explanation": "> returns boolean result.",
                        "test_cases": [{"input": "", "expected_output": "True"}]
                    }
                ],
                "quizzes": [
                    {
                        "title": "Booleans Quiz",
                        "xp_reward": 75,
                        "questions": [
                            {
                                "question": "Which of the following evaluates to False?",
                                "explanation": "An empty string '' evaluates to False in Python.",
                                "options": [
                                    {"text": "bool('')", "is_correct": True},
                                    {"text": "bool('0')", "is_correct": False},
                                    {"text": "bool([1])", "is_correct": False},
                                    {"text": "bool(-5)", "is_correct": False}
                                ]
                            },
                            {
                                "question": "What is not True in Python?",
                                "explanation": "The 'not' operator negates True to False.",
                                "options": [
                                    {"text": "False", "is_correct": True},
                                    {"text": "True", "is_correct": False},
                                    {"text": "None", "is_correct": False},
                                    {"text": "1", "is_correct": False}
                                ]
                            },
                            {
                                "question": "What is bool(0)?",
                                "explanation": "Integer 0 is falsy.",
                                "options": [
                                    {"text": "False", "is_correct": True},
                                    {"text": "True", "is_correct": False},
                                    {"text": "None", "is_correct": False},
                                    {"text": "0", "is_correct": False}
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Operators",
                "slug": "operators",
                "level_number": 1,
                "level_title": "Basics",
                "order_index": 7,
                "icon": "Sliders",
                "description": "Arithmetic (+, -, *, //, %), Comparison (==, !=), and Logical (and, or, not) operators.",
                "lessons": [
                    {
                        "title": "Operators & Floor Division",
                        "content": "Use `//` for floor division (integer division) and `%` for remainder modulus.",
                        "code_example": "print(10 // 3) # 3\nprint(10 % 3)  # 1"
                    }
                ],
                "challenges": [
                    {
                        "title": "Challenge 7.1: Floor Division",
                        "description": "Print the result of floor division `25 // 4`.",
                        "difficulty": "Easy",
                        "starter_code": "# Print the result of floor division 25 // 4\n",
                        "xp_reward": 50,
                        "hint": "25 // 4 = 6",
                        "solution_explanation": "// truncates fractional part.",
                        "test_cases": [{"input": "", "expected_output": "6"}]
                    },
                    {
                        "title": "Challenge 7.2: Modulus Remainder",
                        "description": "Print the remainder when `17` is divided by `5` (`17 % 5`).",
                        "difficulty": "Easy",
                        "starter_code": "# Print the remainder when 17 is divided by 5\n",
                        "xp_reward": 50,
                        "hint": "17 % 5 = 2",
                        "solution_explanation": "% returns division remainder.",
                        "test_cases": [{"input": "", "expected_output": "2"}]
                    }
                ],
                "quizzes": [
                    {
                        "title": "Operators Quiz",
                        "xp_reward": 75,
                        "questions": [
                            {
                                "question": "What does the // operator do?",
                                "explanation": "// performs floor division, rounding down to the nearest integer.",
                                "options": [
                                    {"text": "Floor division (integer quotient)", "is_correct": True},
                                    {"text": "Regular floating point division", "is_correct": False},
                                    {"text": "Modulus remainder", "is_correct": False},
                                    {"text": "Exponentiation", "is_correct": False}
                                ]
                            },
                            {
                                "question": "What is the result of (True and False) or True?",
                                "explanation": "(True and False) evaluates to False. False or True evaluates to True.",
                                "options": [
                                    {"text": "True", "is_correct": True},
                                    {"text": "False", "is_correct": False},
                                    {"text": "None", "is_correct": False},
                                    {"text": "Error", "is_correct": False}
                                ]
                            },
                            {
                                "question": "Which operator calculates exponents/powers in Python?",
                                "explanation": "** is exponentiation operator.",
                                "options": [
                                    {"text": "**", "is_correct": True},
                                    {"text": "^", "is_correct": False},
                                    {"text": "pwr", "is_correct": False},
                                    {"text": "//", "is_correct": False}
                                ]
                            }
                        ]
                    }
                ]
            },

            # ================= MODULE 2: COLLECTIONS =================
            {
                "title": "Lists",
                "slug": "lists",
                "level_number": 2,
                "level_title": "Collections",
                "order_index": 8,
                "icon": "List",
                "description": "Ordered, mutable sequences with append(), pop(), and list comprehensions.",
                "lessons": [
                    {
                        "title": "Lists & List Methods",
                        "content": "Lists are mutable ordered collections defined with `[]`. Add items with `.append()` and remove with `.pop()`.",
                        "code_example": "items = ['sword', 'shield']\nitems.append('potion')\nprint(items)"
                    }
                ],
                "challenges": [
                    {
                        "title": "Challenge 8.1: Inventory Append",
                        "description": "Create list `inv = ['book', 'pen']`, append `'notebook'`, and print the list.",
                        "difficulty": "Easy",
                        "starter_code": "inv = ['book', 'pen']\n# Append 'notebook' to inv and print inv\n",
                        "xp_reward": 70,
                        "hint": "inv.append('notebook')",
                        "solution_explanation": "append() adds item to end of list.",
                        "test_cases": [{"input": "", "expected_output": "['book', 'pen', 'notebook']"}]
                    },
                    {
                        "title": "Challenge 8.2: List Slicer",
                        "description": "Given `nums = [10, 20, 30, 40]`, print the first 2 elements `[10, 20]`.",
                        "difficulty": "Easy",
                        "starter_code": "nums = [10, 20, 30, 40]\n# Print the first 2 elements using slicing\n",
                        "xp_reward": 70,
                        "hint": "nums[0:2]",
                        "solution_explanation": "List slicing takes start:end indices.",
                        "test_cases": [{"input": "", "expected_output": "[10, 20]"}]
                    }
                ],
                "quizzes": [
                    {
                        "title": "Lists Mastery Quiz",
                        "xp_reward": 75,
                        "questions": [
                            {
                                "question": "How do you access the LAST element of a list 'items'?",
                                "explanation": "Negative index items[-1] accesses the last element.",
                                "options": [
                                    {"text": "items[-1]", "is_correct": True},
                                    {"text": "items.last()", "is_correct": False},
                                    {"text": "items[len(items)]", "is_correct": False},
                                    {"text": "items.pop()", "is_correct": False}
                                ]
                            },
                            {
                                "question": "What is the output of [1, 2] + [3, 4]?",
                                "explanation": "+ concatenates two lists into a single combined list.",
                                "options": [
                                    {"text": "[1, 2, 3, 4]", "is_correct": True},
                                    {"text": "[4, 6]", "is_correct": False},
                                    {"text": "[[1, 2], [3, 4]]", "is_correct": False},
                                    {"text": "Error", "is_correct": False}
                                ]
                            },
                            {
                                "question": "Which method removes and returns the last element of a list?",
                                "explanation": ".pop() removes and returns the last element.",
                                "options": [
                                    {"text": ".pop()", "is_correct": True},
                                    {"text": ".remove()", "is_correct": False},
                                    {"text": ".delete()", "is_correct": False},
                                    {"text": ".drop()", "is_correct": False}
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Tuples",
                "slug": "tuples",
                "level_number": 2,
                "level_title": "Collections",
                "order_index": 9,
                "icon": "Layers",
                "description": "Ordered, immutable collections defined with parentheses ().",
                "lessons": [
                    {
                        "title": "Tuples & Unpacking",
                        "content": "Tuples are immutable. Once created, elements cannot be modified or added.",
                        "code_example": "coords = (10, 20)\nx, y = coords\nprint(f'X: {x}, Y: {y}')"
                    }
                ],
                "challenges": [
                    {
                        "title": "Challenge 9.1: Unpack Coordinates",
                        "description": "Unpack tuple `pos = (5, 12)` into `x, y` and print `x + y`.",
                        "difficulty": "Easy",
                        "starter_code": "pos = (5, 12)\n# Unpack pos into x, y and print x + y\n",
                        "xp_reward": 70,
                        "hint": "x, y = pos",
                        "solution_explanation": "Tuple unpacking assigns variables by position.",
                        "test_cases": [{"input": "", "expected_output": "17"}]
                    },
                    {
                        "title": "Challenge 9.2: Tuple Element Fetch",
                        "description": "Given `tup = ('a', 'b', 'c')`, print element `'b'`.",
                        "difficulty": "Easy",
                        "starter_code": "tup = ('a', 'b', 'c')\n# Print element 'b'\n",
                        "xp_reward": 70,
                        "hint": "tup[1] accesses index 1",
                        "solution_explanation": "Tuples support 0-based indexing.",
                        "test_cases": [{"input": "", "expected_output": "b"}]
                    }
                ],
                "quizzes": [
                    {
                        "title": "Tuples Quiz",
                        "xp_reward": 75,
                        "questions": [
                            {
                                "question": "Can you change an element of a tuple after creation?",
                                "explanation": "No, tuples are immutable.",
                                "options": [
                                    {"text": "No, tuples are immutable", "is_correct": True},
                                    {"text": "Yes, using append()", "is_correct": False},
                                    {"text": "Yes, using tuple.set()", "is_correct": False},
                                    {"text": "Only if containing numbers", "is_correct": False}
                                ]
                            },
                            {
                                "question": "How do you create a single-element tuple?",
                                "explanation": "A single-element tuple requires a trailing comma: (5,).",
                                "options": [
                                    {"text": "(5,)", "is_correct": True},
                                    {"text": "(5)", "is_correct": False},
                                    {"text": "tuple[5]", "is_correct": False},
                                    {"text": "single(5)", "is_correct": False}
                                ]
                            },
                            {
                                "question": "Which bracket type defines a tuple?",
                                "explanation": "Parentheses () define tuples.",
                                "options": [
                                    {"text": "Parentheses ()", "is_correct": True},
                                    {"text": "Square []", "is_correct": False},
                                    {"text": "Curly {}", "is_correct": False},
                                    {"text": "Angle <>", "is_correct": False}
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Sets",
                "slug": "sets",
                "level_number": 2,
                "level_title": "Collections",
                "order_index": 10,
                "icon": "Grid",
                "description": "Unordered, unindexed collections of unique elements with set operations.",
                "lessons": [
                    {
                        "title": "Sets & Unique Collections",
                        "content": "Sets remove duplicates automatically. Support operations like `.union()`, `.intersection()`, and `.difference()`.",
                        "code_example": "a = {1, 2, 3}\nb = {3, 4, 5}\nprint(a.intersection(b)) # {3}"
                    }
                ],
                "challenges": [
                    {
                        "title": "Challenge 10.1: Unique Counter",
                        "description": "Convert list `[1, 1, 2, 2, 3]` to a set `s` and print `len(s)`.",
                        "difficulty": "Easy",
                        "starter_code": "lst = [1, 1, 2, 2, 3]\n# Convert lst to a set s and print len(s)\n",
                        "xp_reward": 70,
                        "hint": "set() eliminates duplicate numbers",
                        "solution_explanation": "Sets only store unique elements.",
                        "test_cases": [{"input": "", "expected_output": "3"}]
                    },
                    {
                        "title": "Challenge 10.2: Set Intersection",
                        "description": "Given `a = {1, 2}` and `b = {2, 3}`, print `a.intersection(b)`.",
                        "difficulty": "Easy",
                        "starter_code": "a = {1, 2}\nb = {2, 3}\n# Print the intersection of set a and set b\n",
                        "xp_reward": 70,
                        "hint": "a.intersection(b) returns {2}",
                        "solution_explanation": "intersection returns common items.",
                        "test_cases": [{"input": "", "expected_output": "{2}"}]
                    }
                ],
                "quizzes": [
                    {
                        "title": "Sets Quiz",
                        "xp_reward": 75,
                        "questions": [
                            {
                                "question": "What happens when you add a duplicate item to a set?",
                                "explanation": "Sets only store unique elements, so duplicate additions are ignored.",
                                "options": [
                                    {"text": "It is ignored (set size unchanged)", "is_correct": True},
                                    {"text": "Throws KeyError", "is_correct": False},
                                    {"text": "Replaces existing item", "is_correct": False},
                                    {"text": "Creates a list inside set", "is_correct": False}
                                ]
                            },
                            {
                                "question": "Which method returns elements present in set A but NOT in set B?",
                                "explanation": "A.difference(b) or (A - B) returns set difference.",
                                "options": [
                                    {"text": "A.difference(B)", "is_correct": True},
                                    {"text": "A.intersection(B)", "is_correct": False},
                                    {"text": "A.union(B)", "is_correct": False},
                                    {"text": "A.remove(B)", "is_correct": False}
                                ]
                            },
                            {
                                "question": "Are set elements ordered in Python?",
                                "explanation": "No, sets are unordered collections.",
                                "options": [
                                    {"text": "No, sets are unordered", "is_correct": True},
                                    {"text": "Yes, sorted alphabetically", "is_correct": False},
                                    {"text": "Yes, sorted by insertion time", "is_correct": False},
                                    {"text": "Only if numbers", "is_correct": False}
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Dictionaries",
                "slug": "dictionaries",
                "level_number": 2,
                "level_title": "Collections",
                "order_index": 11,
                "icon": "BookOpen",
                "description": "Key-value pair mappings with .get(), .keys(), and .values().",
                "lessons": [
                    {
                        "title": "Key-Value Dictionaries",
                        "content": "Dictionaries store `{key: value}` mappings. Access values by key `d['name']` or safely using `d.get('name', default)`.",
                        "code_example": "player = {'name': 'Alex', 'xp': 250}\nprint(player.get('role', 'Student'))"
                    }
                ],
                "challenges": [
                    {
                        "title": "Challenge 11.1: Key Lookup",
                        "description": "Given `data = {'rank': 1, 'score': 95}`, print `data['score']`.",
                        "difficulty": "Easy",
                        "starter_code": "data = {'rank': 1, 'score': 95}\n# Print the value for key 'score'\n",
                        "xp_reward": 75,
                        "hint": "data['score'] returns 95",
                        "solution_explanation": "Dictionary keys map directly to values.",
                        "test_cases": [{"input": "", "expected_output": "95"}]
                    },
                    {
                        "title": "Challenge 11.2: Safe Get Lookup",
                        "description": "Use `d.get('level', 1)` on `d = {'name': 'Player'}` to print the level with default fallback `1`.",
                        "difficulty": "Easy",
                        "starter_code": "d = {'name': 'Player'}\n# Print key 'level' with default fallback 1 using d.get()\n",
                        "xp_reward": 75,
                        "hint": "d.get('level', 1) returns 1",
                        "solution_explanation": ".get(key, default) returns default if key is missing.",
                        "test_cases": [{"input": "", "expected_output": "1"}]
                    }
                ],
                "quizzes": [
                    {
                        "title": "Dictionaries Quiz",
                        "xp_reward": 75,
                        "questions": [
                            {
                                "question": "Why is dict.get('key') safer than dict['key']?",
                                "explanation": ".get() returns None (or default) instead of throwing a KeyError if the key is missing.",
                                "options": [
                                    {"text": "It avoids throwing KeyError on missing keys", "is_correct": True},
                                    {"text": "It is faster to execute", "is_correct": False},
                                    {"text": "It converts values to string", "is_correct": False},
                                    {"text": "It locks dictionary memory", "is_correct": False}
                                ]
                            },
                            {
                                "question": "Can dictionary keys be mutable lists?",
                                "explanation": "No, dictionary keys must be hashable (immutable), such as strings, numbers, or tuples.",
                                "options": [
                                    {"text": "No, keys must be hashable/immutable", "is_correct": True},
                                    {"text": "Yes, any object can be a key", "is_correct": False},
                                    {"text": "Only if list size is under 10", "is_correct": False},
                                    {"text": "Only in Python 3.12+", "is_correct": False}
                                ]
                            },
                            {
                                "question": "Which method returns all keys in a dictionary?",
                                "explanation": ".keys() returns a view of all keys in dictionary.",
                                "options": [
                                    {"text": ".keys()", "is_correct": True},
                                    {"text": ".items()", "is_correct": False},
                                    {"text": ".values()", "is_correct": False},
                                    {"text": ".all_keys()", "is_correct": False}
                                ]
                            }
                        ]
                    }
                ]
            },

            # ================= MODULE 3: CONTROL FLOW =================
            {
                "title": "if / elif / else",
                "slug": "if-elif-else",
                "level_number": 3,
                "level_title": "Control flow",
                "order_index": 12,
                "icon": "GitBranch",
                "description": "Conditional decision tree branching with if, elif, and fallback else.",
                "lessons": [
                    {
                        "title": "Conditional Decision Logic",
                        "content": "Chain multiple conditions using `if`, `elif`, and `else` to control code execution path.",
                        "code_example": "score = 85\nif score >= 90:\n    print('A')\nelif score >= 80:\n    print('B')\nelse:\n    print('C')"
                    }
                ],
                "challenges": [
                    {
                        "title": "Challenge 12.1: Sign Classifier",
                        "description": "Given `num = -5`. Print `'Negative'` if num < 0, else `'Positive'`.",
                        "difficulty": "Easy",
                        "starter_code": "num = -5\n# Print 'Negative' if num < 0, else 'Positive'\n",
                        "xp_reward": 60,
                        "hint": "num < 0 is True",
                        "solution_explanation": "if block executes when condition is True.",
                        "test_cases": [{"input": "", "expected_output": "Negative"}]
                    },
                    {
                        "title": "Challenge 12.2: Grade Evaluator",
                        "description": "Given `score = 85`. Print `'B'` if score >= 80, else `'F'`.",
                        "difficulty": "Easy",
                        "starter_code": "score = 85\n# Print 'B' if score >= 80, else 'F'\n",
                        "xp_reward": 60,
                        "hint": "85 >= 80 is True",
                        "solution_explanation": "elif/if evaluates branching conditions.",
                        "test_cases": [{"input": "", "expected_output": "B"}]
                    }
                ],
                "quizzes": [
                    {
                        "title": "Conditional Logic Quiz",
                        "xp_reward": 75,
                        "questions": [
                            {
                                "question": "When does the code block under 'else' execute?",
                                "explanation": "'else' executes only when all preceding 'if' and 'elif' conditions evaluate to False.",
                                "options": [
                                    {"text": "When all preceding conditions are False", "is_correct": True},
                                    {"text": "Always before elif", "is_correct": False},
                                    {"text": "When score == 0", "is_correct": False},
                                    {"text": "Twice per loop", "is_correct": False}
                                ]
                            },
                            {
                                "question": "What is the output of: if True: print('A'); elif True: print('B')?",
                                "explanation": "Once a condition matches, Python executes that block and skips remaining elif branches.",
                                "options": [
                                    {"text": "'A'", "is_correct": True},
                                    {"text": "'A' and 'B'", "is_correct": False},
                                    {"text": "'B'", "is_correct": False},
                                    {"text": "Error", "is_correct": False}
                                ]
                            },
                            {
                                "question": "Can an 'elif' statement exist without a preceding 'if'?",
                                "explanation": "No, elif requires an initial if statement.",
                                "options": [
                                    {"text": "No, if is mandatory first", "is_correct": True},
                                    {"text": "Yes, anytime", "is_correct": False},
                                    {"text": "Only inside functions", "is_correct": False},
                                    {"text": "Only with integers", "is_correct": False}
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "title": "for loop",
                "slug": "for-loop",
                "level_number": 3,
                "level_title": "Control flow",
                "order_index": 13,
                "icon": "Repeat",
                "description": "Iterate over ranges, lists, and strings with for loops.",
                "lessons": [
                    {
                        "title": "Iterating with For Loops",
                        "content": "`for item in sequence:` repeats code block for each item in a sequence or `range(start, stop, step)`.",
                        "code_example": "total = 0\nfor i in range(1, 4): # 1, 2, 3\n    total += i\nprint(total) # 6"
                    }
                ],
                "challenges": [
                    {
                        "title": "Challenge 13.1: Sum First N",
                        "description": "Use a for loop to calculate and print sum of numbers from `1` to `5` (1+2+3+4+5 = 15).",
                        "difficulty": "Easy",
                        "starter_code": "# Calculate and print the sum of numbers from 1 to 5 using a for loop\ntotal = 0\n",
                        "xp_reward": 70,
                        "hint": "range(1, 6) yields 1, 2, 3, 4, 5",
                        "solution_explanation": "For loop accumulates total.",
                        "test_cases": [{"input": "", "expected_output": "15"}]
                    },
                    {
                        "title": "Challenge 13.2: Print Evens",
                        "description": "Use `range(2, 7, 2)` in a for loop to print `2`, `4`, `6` on separate lines.",
                        "difficulty": "Easy",
                        "starter_code": "# Use a for loop with range(2, 7, 2) to print 2, 4, 6\n",
                        "xp_reward": 70,
                        "hint": "range(2, 7, 2)",
                        "solution_explanation": "step argument 2 jumps by 2.",
                        "test_cases": [{"input": "", "expected_output": "2\n4\n6"}]
                    }
                ],
                "quizzes": [
                    {
                        "title": "For Loop Mastery Quiz",
                        "xp_reward": 75,
                        "questions": [
                            {
                                "question": "What numbers does list(range(2, 8, 2)) produce?",
                                "explanation": "Start at 2 up to 8 (exclusive) with step 2 -> [2, 4, 6].",
                                "options": [
                                    {"text": "[2, 4, 6]", "is_correct": True},
                                    {"text": "[2, 4, 6, 8]", "is_correct": False},
                                    {"text": "[2, 3, 4, 5, 6, 7]", "is_correct": False},
                                    {"text": "[2, 8]", "is_correct": False}
                                ]
                            },
                            {
                                "question": "What statement terminates a loop immediately?",
                                "explanation": "'break' exits the loop immediately.",
                                "options": [
                                    {"text": "break", "is_correct": True},
                                    {"text": "continue", "is_correct": False},
                                    {"text": "pass", "is_correct": False},
                                    {"text": "stop", "is_correct": False}
                                ]
                            },
                            {
                                "question": "What does range(5) produce?",
                                "explanation": "range(5) produces 0, 1, 2, 3, 4.",
                                "options": [
                                    {"text": "0, 1, 2, 3, 4", "is_correct": True},
                                    {"text": "1, 2, 3, 4, 5", "is_correct": False},
                                    {"text": "1, 5", "is_correct": False},
                                    {"text": "0, 5", "is_correct": False}
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "title": "while loop",
                "slug": "while-loop",
                "level_number": 3,
                "level_title": "Control flow",
                "order_index": 14,
                "icon": "RefreshCw",
                "description": "Execute statements continuously as long as a condition evaluates to True.",
                "lessons": [
                    {
                        "title": "While Loops & State Control",
                        "content": "A `while` loop runs until its boolean condition becomes `False`. Always ensure the state updates to avoid infinite loops!",
                        "code_example": "n = 5\nwhile n > 0:\n    print(n)\n    n -= 1"
                    }
                ],
                "challenges": [
                    {
                        "title": "Challenge 14.1: Countdown Rocket",
                        "description": "Print countdown from `3` down to `1` using a while loop.",
                        "difficulty": "Easy",
                        "starter_code": "# Use a while loop to print countdown from 3 down to 1\nc = 3\n",
                        "xp_reward": 70,
                        "hint": "c -= 1 decreases counter.",
                        "solution_explanation": "While condition checks c > 0.",
                        "test_cases": [{"input": "", "expected_output": "3\n2\n1"}]
                    },
                    {
                        "title": "Challenge 14.2: Double Accumulator",
                        "description": "Start `val = 1`. Double `val` inside while loop while `val < 8`, printing `val` each cycle (`1`, `2`, `4`).",
                        "difficulty": "Easy",
                        "starter_code": "val = 1\n# Double val while val < 8 and print val each iteration\n",
                        "xp_reward": 70,
                        "hint": "val *= 2 doubles value.",
                        "solution_explanation": "Loop terminates when val reaches 8.",
                        "test_cases": [{"input": "", "expected_output": "1\n2\n4"}]
                    }
                ],
                "quizzes": [
                    {
                        "title": "While Loop Quiz",
                        "xp_reward": 75,
                        "questions": [
                            {
                                "question": "What statement skips the current iteration and jumps to the next iteration?",
                                "explanation": "'continue' skips remaining lines in current iteration and moves to next loop cycle.",
                                "options": [
                                    {"text": "continue", "is_correct": True},
                                    {"text": "break", "is_correct": False},
                                    {"text": "skip", "is_correct": False},
                                    {"text": "next", "is_correct": False}
                                ]
                            },
                            {
                                "question": "What happens if a while condition never becomes False?",
                                "explanation": "The loop runs endlessly (infinite loop) until interrupted.",
                                "options": [
                                    {"text": "Infinite loop execution", "is_correct": True},
                                    {"text": "Stops after 10 seconds", "is_correct": False},
                                    {"text": "Returns None automatically", "is_correct": False},
                                    {"text": "SyntaxError", "is_correct": False}
                                ]
                            },
                            {
                                "question": "Which loop is preferred when number of iterations is NOT known beforehand?",
                                "explanation": "While loop is ideal when looping depends on dynamic boolean condition.",
                                "options": [
                                    {"text": "while loop", "is_correct": True},
                                    {"text": "for loop", "is_correct": False},
                                    {"text": "do-until loop", "is_correct": False},
                                    {"text": "repeat loop", "is_correct": False}
                                ]
                            }
                        ]
                    }
                ]
            },

            # ================= MODULE 4: FUNCTIONS & TOOLS =================
            {
                "title": "Functions",
                "slug": "functions",
                "level_number": 4,
                "level_title": "Functions & tools",
                "order_index": 15,
                "icon": "Cpu",
                "description": "Define modular, reusable code blocks using def keyword.",
                "lessons": [
                    {
                        "title": "Modular Functions",
                        "content": "Functions organize code into reusable modules. Define using `def function_name():` and return values using `return`.",
                        "code_example": "def calc_xp(bonus):\n    return 100 + bonus\n\nprint(calc_xp(50))"
                    }
                ],
                "challenges": [
                    {
                        "title": "Challenge 15.1: Square Function",
                        "description": "Define function `square(n)` that returns `n * n`. Print `square(4)`.",
                        "difficulty": "Easy",
                        "starter_code": "# Define function square(n) returning n * n, then print square(4)\n",
                        "xp_reward": 80,
                        "hint": "return n * n",
                        "solution_explanation": "return statement passes result back to caller.",
                        "test_cases": [{"input": "", "expected_output": "16"}]
                    },
                    {
                        "title": "Challenge 15.2: Double Adder",
                        "description": "Define function `add(a, b)` returning `a + b`. Print `add(10, 20)`.",
                        "difficulty": "Easy",
                        "starter_code": "# Define function add(a, b) returning a + b, then print add(10, 20)\n",
                        "xp_reward": 80,
                        "hint": "return a + b",
                        "solution_explanation": "Multiple parameters are comma separated.",
                        "test_cases": [{"input": "", "expected_output": "30"}]
                    }
                ],
                "quizzes": [
                    {
                        "title": "Functions Quiz",
                        "xp_reward": 75,
                        "questions": [
                            {
                                "question": "Which keyword creates a function in Python?",
                                "explanation": "def keyword defines functions.",
                                "options": [
                                    {"text": "def", "is_correct": True},
                                    {"text": "function", "is_correct": False},
                                    {"text": "fn", "is_correct": False},
                                    {"text": "define", "is_correct": False}
                                ]
                            },
                            {
                                "question": "What value does a function return if no return statement is specified?",
                                "explanation": "Functions without return statements implicitly return None.",
                                "options": [
                                    {"text": "None", "is_correct": True},
                                    {"text": "0", "is_correct": False},
                                    {"text": "False", "is_correct": False},
                                    {"text": "Undefined", "is_correct": False}
                                ]
                            },
                            {
                                "question": "What keyword exits a function immediately and sends back a result?",
                                "explanation": "return exits function and returns specified value.",
                                "options": [
                                    {"text": "return", "is_correct": True},
                                    {"text": "break", "is_correct": False},
                                    {"text": "yield", "is_correct": False},
                                    {"text": "exit", "is_correct": False}
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Calling functions",
                "slug": "calling-functions",
                "level_number": 4,
                "level_title": "Functions & tools",
                "order_index": 16,
                "icon": "Play",
                "description": "Invoke functions with positional, keyword, and default parameters.",
                "lessons": [
                    {
                        "title": "Function Invocation & Default Parameters",
                        "content": "Call functions using `name(arg1, arg2)`. Python supports default parameter values e.g. `def greet(name='Coder'):`.",
                        "code_example": "def greet(name='Hero'):\n    print(f'Hi, {name}')\n\ngreet()       # 'Hi, Hero'\ngreet('Alex') # 'Hi, Alex'"
                    }
                ],
                "challenges": [
                    {
                        "title": "Challenge 16.1: Default Greeter",
                        "description": "Define `welcome(user='Player')` printing `f'Welcome {user}'`. Call `welcome()` without args.",
                        "difficulty": "Easy",
                        "starter_code": "# Define welcome(user='Player') printing 'Welcome Player', then call welcome()\n",
                        "xp_reward": 80,
                        "hint": "def welcome(user='Player'):",
                        "solution_explanation": "Default values are used when caller omits argument.",
                        "test_cases": [{"input": "", "expected_output": "Welcome Player"}]
                    },
                    {
                        "title": "Challenge 16.2: Keyword Arguments Call",
                        "description": "Define `info(name, age)` printing `f'{name} is {age}'`. Call using keyword args `info(age=20, name='Sam')`.",
                        "difficulty": "Easy",
                        "starter_code": "# Define info(name, age) printing f'{name} is {age}', then call it with age=20, name='Sam'\n",
                        "xp_reward": 80,
                        "hint": "info(age=20, name='Sam')",
                        "solution_explanation": "Keyword args can be passed in any order.",
                        "test_cases": [{"input": "", "expected_output": "Sam is 20"}]
                    }
                ],
                "quizzes": [
                    {
                        "title": "Function Calling Quiz",
                        "xp_reward": 75,
                        "questions": [
                            {
                                "question": "How do you specify keyword arguments when calling a function?",
                                "explanation": "Keyword arguments pass parameter names explicitly: func(name='Alex', age=20).",
                                "options": [
                                    {"text": "func(name='Alex', age=20)", "is_correct": True},
                                    {"text": "func('Alex': name)", "is_correct": False},
                                    {"text": "func->name('Alex')", "is_correct": False},
                                    {"text": "func[name='Alex']", "is_correct": False}
                                ]
                            },
                            {
                                "question": "What is *args used for in function parameters?",
                                "explanation": "*args allows passing a variable number of positional arguments as a tuple.",
                                "options": [
                                    {"text": "Passing arbitrary positional arguments as a tuple", "is_correct": True},
                                    {"text": "Multiplying function returns", "is_correct": False},
                                    {"text": "Importing math libraries", "is_correct": False},
                                    {"text": "Setting execution timeout", "is_correct": False}
                                ]
                            },
                            {
                                "question": "What is **kwargs used for in function parameters?",
                                "explanation": "**kwargs captures arbitrary keyword arguments into a dictionary.",
                                "options": [
                                    {"text": "Passing arbitrary keyword arguments as a dictionary", "is_correct": True},
                                    {"text": "Doubling argument values", "is_correct": False},
                                    {"text": "Declaring global variables", "is_correct": False},
                                    {"text": "Setting default types", "is_correct": False}
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Decorators",
                "slug": "decorators",
                "level_number": 4,
                "level_title": "Functions & tools",
                "order_index": 17,
                "icon": "Zap",
                "description": "Extend and modify function behaviors dynamically using @decorator syntax.",
                "lessons": [
                    {
                        "title": "Python Decorator Pattern",
                        "content": "Decorators wrap target functions to execute code before or after without modifying the original function definition.",
                        "code_example": "def log(func):\n    def wrapper():\n        print('LOG: Start')\n        func()\n    return wrapper\n\n@log\ndef run():\n    print('Running')\n\nrun()"
                    }
                ],
                "challenges": [
                    {
                        "title": "Challenge 17.1: Banner Decorator",
                        "description": "Create decorator `banner` printing `'=== START ==='` before calling func. Apply `@banner` to `def main(): print('Active')`.",
                        "difficulty": "Hard",
                        "starter_code": "# Create decorator banner printing '=== START ===' before calling func\n# Apply @banner to main() printing 'Active' and call main()\n",
                        "xp_reward": 100,
                        "hint": "@banner syntax wraps main()",
                        "solution_explanation": "Decorators take function as argument and return wrapper function.",
                        "test_cases": [{"input": "", "expected_output": "=== START ===\nActive"}]
                    },
                    {
                        "title": "Challenge 17.2: Tag Wrapper",
                        "description": "Create decorator `upper_decor` that prints `'[EXEC]'` before calling func `say_hi()` printing `'HI'`.",
                        "difficulty": "Hard",
                        "starter_code": "# Create decorator upper_decor printing '[EXEC]' before calling func\n# Apply @upper_decor to say_hi() printing 'HI' and call say_hi()\n",
                        "xp_reward": 100,
                        "hint": "print('[EXEC]') inside wrapper",
                        "solution_explanation": "Wrapper functions execute setup/teardown logic.",
                        "test_cases": [{"input": "", "expected_output": "[EXEC]\nHI"}]
                    }
                ],
                "quizzes": [
                    {
                        "title": "Decorators Quiz",
                        "xp_reward": 75,
                        "questions": [
                            {
                                "question": "What syntax applies a decorator to a function in Python?",
                                "explanation": "The @ symbol prefix above function definition applies decorators.",
                                "options": [
                                    {"text": "@decorator_name", "is_correct": True},
                                    {"text": "#decorator_name", "is_correct": False},
                                    {"text": "$decorator_name", "is_correct": False},
                                    {"text": "&decorator_name", "is_correct": False}
                                ]
                            },
                            {
                                "question": "What does a decorator function return?",
                                "explanation": "A decorator takes a function as argument and returns a new wrapper function.",
                                "options": [
                                    {"text": "A wrapper function object", "is_correct": True},
                                    {"text": "A boolean status", "is_correct": False},
                                    {"text": "A string name", "is_correct": False},
                                    {"text": "None", "is_correct": False}
                                ]
                            },
                            {
                                "question": "Which built-in functools decorator preserves function metadata (docstring/name)?",
                                "explanation": "@functools.wraps preserves wrapped function metadata.",
                                "options": [
                                    {"text": "@functools.wraps", "is_correct": True},
                                    {"text": "@preserve", "is_correct": False},
                                    {"text": "@copy_meta", "is_correct": False},
                                    {"text": "@keep_name", "is_correct": False}
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "title": "pip",
                "slug": "pip",
                "level_number": 4,
                "level_title": "Functions & tools",
                "order_index": 18,
                "icon": "Package",
                "description": "Manage third-party Python packages using PIP package manager.",
                "lessons": [
                    {
                        "title": "PIP Package Management",
                        "content": "PIP downloads and installs third-party modules from PyPI (Python Package Index).",
                        "code_example": "# Command line:\n# pip install requests\nimport sys\nprint('PIP ready')"
                    }
                ],
                "challenges": [
                    {
                        "title": "Challenge 18.1: Math Module Import",
                        "description": "Import built-in `math` module and print `math.isqrt(49)`.",
                        "difficulty": "Medium",
                        "starter_code": "# Import math module and print math.isqrt(49)\n",
                        "xp_reward": 80,
                        "hint": "math.isqrt(49) = 7",
                        "solution_explanation": "import keyword makes external modules accessible.",
                        "test_cases": [{"input": "", "expected_output": "7"}]
                    },
                    {
                        "title": "Challenge 18.2: Random Module Sample",
                        "description": "Import `sys` module and print `'Python ' + str(sys.version_info[0])`.",
                        "difficulty": "Medium",
                        "starter_code": "# Import sys module and print 'Python ' + str(sys.version_info[0])\n",
                        "xp_reward": 80,
                        "hint": "sys.version_info[0] is 3",
                        "solution_explanation": "sys provides system-specific parameters.",
                        "test_cases": [{"input": "", "expected_output": "Python 3"}]
                    }
                ],
                "quizzes": [
                    {
                        "title": "PIP Quiz",
                        "xp_reward": 75,
                        "questions": [
                            {
                                "question": "What CLI command installs a Python package named 'requests'?",
                                "explanation": "pip install requests downloads and installs package.",
                                "options": [
                                    {"text": "pip install requests", "is_correct": True},
                                    {"text": "pip add requests", "is_correct": False},
                                    {"text": "python get requests", "is_correct": False},
                                    {"text": "npm install requests", "is_correct": False}
                                ]
                            },
                            {
                                "question": "Which file specifies project dependencies in Python projects?",
                                "explanation": "requirements.txt lists required packages.",
                                "options": [
                                    {"text": "requirements.txt", "is_correct": True},
                                    {"text": "package.json", "is_correct": False},
                                    {"text": "dependencies.xml", "is_correct": False},
                                    {"text": "pip.config", "is_correct": False}
                                ]
                            },
                            {
                                "question": "What command generates a requirements.txt file of installed packages?",
                                "explanation": "pip freeze lists installed packages in requirements format.",
                                "options": [
                                    {"text": "pip freeze", "is_correct": True},
                                    {"text": "pip list --export", "is_correct": False},
                                    {"text": "pip save", "is_correct": False},
                                    {"text": "pip generate", "is_correct": False}
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Virtual env",
                "slug": "virtual-env",
                "level_number": 4,
                "level_title": "Functions & tools",
                "order_index": 19,
                "icon": "Box",
                "description": "Create isolated virtual environments with python -m venv.",
                "lessons": [
                    {
                        "title": "Isolated Virtual Environments",
                        "content": "Virtual environments prevent dependency conflicts between projects by isolating installed packages.",
                        "code_example": "# Command line:\n# python -m venv venv\nprint('Virtual env active')"
                    }
                ],
                "challenges": [
                    {
                        "title": "Challenge 19.1: Env Active Check",
                        "description": "Print `'Virtual Environment Active'`.",
                        "difficulty": "Easy",
                        "starter_code": "# Print 'Virtual Environment Active'\n",
                        "xp_reward": 80,
                        "hint": "print statement",
                        "solution_explanation": "Virtual env provides isolated workspace.",
                        "test_cases": [{"input": "", "expected_output": "Virtual Environment Active"}]
                    },
                    {
                        "title": "Challenge 19.2: Path Verification",
                        "description": "Print `'VENV ISO OK'`.",
                        "difficulty": "Easy",
                        "starter_code": "# Print 'VENV ISO OK'\n",
                        "xp_reward": 80,
                        "hint": "print statement",
                        "solution_explanation": "ISOLATED environments keep dependencies clean.",
                        "test_cases": [{"input": "", "expected_output": "VENV ISO OK"}]
                    }
                ],
                "quizzes": [
                    {
                        "title": "Virtual Environment Quiz",
                        "xp_reward": 75,
                        "questions": [
                            {
                                "question": "Which Python module creates virtual environments?",
                                "explanation": "venv module creates isolated Python environments.",
                                "options": [
                                    {"text": "venv", "is_correct": True},
                                    {"text": "env", "is_correct": False},
                                    {"text": "virtual", "is_correct": False},
                                    {"text": "pipenv", "is_correct": False}
                                ]
                            },
                            {
                                "question": "Why should you use a virtual environment for each project?",
                                "explanation": "It keeps dependencies isolated to avoid version conflicts between projects.",
                                "options": [
                                    {"text": "To prevent package version conflicts across projects", "is_correct": True},
                                    {"text": "To make Python run 10x faster", "is_correct": False},
                                    {"text": "To encrypt your code", "is_correct": False},
                                    {"text": "It is required to run print()", "is_correct": False}
                                ]
                            },
                            {
                                "question": "On Windows, which script activates a virtual environment named 'venv'?",
                                "explanation": "venv\\Scripts\\activate activates virtualenv on Windows.",
                                "options": [
                                    {"text": "venv\\Scripts\\activate", "is_correct": True},
                                    {"text": "source venv/bin/start", "is_correct": False},
                                    {"text": "python venv start", "is_correct": False},
                                    {"text": "pip activate venv", "is_correct": False}
                                ]
                            }
                        ]
                    }
                ]
            }
        ]

        # W3Schools-Style Fun Quizzes
        W3SCHOOLS_STYLE_TOPICS = [
            {
                "title": "Code Output Prediction",
                "slug": "code-output-prediction",
                "level_number": 5,
                "level_title": "Puzzles & Games",
                "order_index": 20,
                "icon": "Terminal",
                "description": "Predict what Python code will output - fun brain teasers!",
                "lessons": [
                    {
                        "title": "Reading Code Like a Pro",
                        "content": "Learn to trace code execution step by step. Start from the top and follow each line's effect on variables and output.",
                        "code_example": "# Trace this:\nx = 5\ny = x * 2\nprint(y + 3)"
                    }
                ],
                "challenges": [
                    {
                        "title": "Challenge: Trace the Output",
                        "description": "Given this code, what will it print? Write the expected output as a string.",
                        "difficulty": "Medium",
                        "starter_code": "# What does this print?\na = 10\nb = 3\nresult = a // b * 2\nprint(result)",
                        "xp_reward": 100,
                        "hint": "// is floor division",
                        "solution_explanation": "10 // 3 = 3, then 3 * 2 = 6"
                    }
                ],
                "quizzes": [
                    {
                        "title": "What Will Python Print? Quiz",
                        "xp_reward": 100,
                        "questions": [
                            {
                                "question": "What will this code print?\nprint(2 + 3 * 4)",
                                "explanation": "Multiplication has higher precedence: 3 * 4 = 12, then 2 + 12 = 14",
                                "options": [
                                    {"text": "20", "is_correct": False},
                                    {"text": "14", "is_correct": True},
                                    {"text": "10", "is_correct": False},
                                    {"text": "24", "is_correct": False}
                                ],
                                "question_type": "multiple_choice"
                            },
                            {
                                "question": "What will this code print?\nprint('Hello' * 3)",
                                "explanation": "String repetition: 'Hello' repeated 3 times",
                                "options": [
                                    {"text": "HelloHelloHello", "is_correct": True},
                                    {"text": "HelloHello", "is_correct": False},
                                    {"text": "HelloHelloHelloHello", "is_correct": False},
                                    {"text": "Error", "is_correct": False}
                                ],
                                "question_type": "multiple_choice"
                            },
                            {
                                "question": "Complete the code to print 42:\nprint(___ * 7)",
                                "explanation": "6 * 7 = 42, so we need 6 in the blank",
                                "options": [
                                    {"text": "6", "is_correct": True},
                                    {"text": "7", "is_correct": False},
                                    {"text": "8", "is_correct": False},
                                    {"text": "5", "is_correct": False}
                                ],
                                "question_type": "multiple_choice"
                            }
                        ]
                    },
                    {
                        "title": "True/False Python Facts",
                        "xp_reward": 75,
                        "questions": [
                            {
                                "question": "True or False: In Python, // is floor division (rounds down to nearest integer)",
                                "explanation": "The // operator performs floor division, which rounds down to the nearest integer.",
                                "options": [
                                    {"text": "True", "is_correct": True},
                                    {"text": "False", "is_correct": False}
                                ],
                                "question_type": "true_false"
                            },
                            {
                                "question": "True or False: Strings in Python are immutable (cannot be changed after creation)",
                                "explanation": "Once a string is created, it cannot be modified. You can create new strings, but the original remains unchanged.",
                                "options": [
                                    {"text": "True", "is_correct": True},
                                    {"text": "False", "is_correct": False}
                                ],
                                "question_type": "true_false"
                            },
                            {
                                "question": "True or False: The == operator checks if two objects are the same instance in memory",
                                "explanation": "The == operator checks for equality of values, not identity. Use 'is' to check if two variables refer to the same object.",
                                "options": [
                                    {"text": "True", "is_correct": False},
                                    {"text": "False", "is_correct": True}
                                ],
                                "question_type": "true_false"
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Fill-in-the-Blank Coding",
                "slug": "fill-in-blank",
                "level_number": 5,
                "level_title": "Puzzles & Games",
                "order_index": 21,
                "icon": "Edit",
                "description": "Complete the missing parts of Python code snippets!",
                "lessons": [
                    {
                        "title": "Code Completion Practice",
                        "content": "Practice completing partial code snippets to build muscle memory and syntax familiarity.",
                        "code_example": "# Complete this loop:\nfor i in range(___):\n    print(i)"
                    }
                ],
                "challenges": [
                    {
                        "title": "Challenge: Complete the Loop",
                        "description": "Fill in the blank to make a loop that prints 0, 1, 2, 3, 4",
                        "difficulty": "Easy",
                        "starter_code": "for i in range(___):\n    print(i)",
                        "xp_reward": 75,
                        "hint": "range(5) gives 0,1,2,3,4",
                        "solution_explanation": "range(5) produces numbers 0 through 4"
                    }
                ],
                "quizzes": [
                    {
                        "title": "Complete the Code Quiz",
                        "xp_reward": 75,
                        "questions": [
                            {
                                "question": "What goes in the blank to calculate area of a circle?\narea = 3.14 * radius ___ 2",
                                "explanation": "We need to square the radius, so we use ** for exponentiation",
                                "options": [
                                    {"text": "+", "is_correct": False},
                                    {"text": "-", "is_correct": False},
                                    {"text": "*", "is_correct": False},
                                    {"text": "**", "is_correct": True}
                                ],
                                "question_type": "multiple_choice"
                            },
                            {
                                "question": "Complete the code: ___(10.7)  # should give 11",
                                "explanation": "round() function rounds to nearest integer",
                                "options": [
                                    {"text": "round", "is_correct": True},
                                    {"text": "int", "is_correct": False},
                                    {"text": "float", "is_correct": False},
                                    {"text": "str", "is_correct": False}
                                ],
                                "question_type": "multiple_choice"
                            },
                            {
                                "question": "Fill in the blank: print(len(___))  # should print 3",
                                "explanation": "len() counts items in a list, so we need a list with 3 items",
                                "options": [
                                    {"text": "[1, 2]", "is_correct": False},
                                    {"text": "[1, 2, 3]", "is_correct": True},
                                    {"text": "[1]", "is_correct": False},
                                    {"text": "[]", "is_correct": False}
                                ],
                                "question_type": "multiple_choice"
                            }
                        ]
                    }
                ]
            }
        ]

        # Add the W3Schools-style topics to the curriculum
        CURRICULUM.extend(W3SCHOOLS_STYLE_TOPICS)

        # Insert topics, lessons, challenges, quizzes
        for t_data in CURRICULUM:
            topic = Topic(
                title=t_data["title"],
                slug=t_data["slug"],
                level_number=t_data["level_number"],
                level_title=t_data["level_title"],
                order_index=t_data["order_index"],
                icon=t_data["icon"],
                description=t_data["description"]
            )
            db.add(topic)
            db.flush()

            for idx, l_data in enumerate(t_data.get("lessons", []), start=1):
                lesson = Lesson(
                    topic_id=topic.id,
                    title=l_data["title"],
                    content=l_data["content"],
                    code_example=l_data.get("code_example"),
                    order_index=idx
                )
                db.add(lesson)

            for c_data in t_data.get("challenges", []):
                ch = Challenge(
                    topic_id=topic.id,
                    title=c_data["title"],
                    description=c_data["description"],
                    difficulty=c_data.get("difficulty", "Easy"),
                    starter_code=c_data["starter_code"],
                    xp_reward=c_data.get("xp_reward", 50),
                    hint=c_data.get("hint"),
                    solution_explanation=c_data.get("solution_explanation")
                )
                db.add(ch)
                db.flush()

                for tc in c_data.get("test_cases", []):
                    tc_obj = ChallengeTestCase(
                        challenge_id=ch.id,
                        input_data=tc.get("input", ""),
                        expected_output=tc["expected_output"]
                    )
                    db.add(tc_obj)

            for q_data in t_data.get("quizzes", []):
                qz = Quiz(
                    topic_id=topic.id,
                    title=q_data["title"],
                    xp_reward=q_data.get("xp_reward", 75)
                )
                db.add(qz)
                db.flush()

                for q_item in q_data.get("questions", []):
                    qq = QuizQuestion(
                        quiz_id=qz.id,
                        question_text=q_item["question"],
                        explanation=q_item.get("explanation"),
                        question_type=q_item.get("question_type", "multiple_choice")
                    )
                    db.add(qq)
                    db.flush()

                    for opt in q_item.get("options", []):
                        opt_obj = QuizOption(
                            question_id=qq.id,
                            option_text=opt["text"],
                            is_correct=opt["is_correct"]
                        )
                        db.add(opt_obj)

        # Seed Badges
        BADGES_DATA = [
            {"name": "🐍 First Python Program", "description": "Wrote and executed your first Python code!", "icon": "Terminal", "criteria_type": "first_program", "criteria_value": "1"},
            {"name": "💡 Variable Master", "description": "Mastered Python variables and basic data types.", "icon": "Box", "criteria_type": "topics_mastered", "criteria_value": "3"},
            {"name": "🔀 Decision Maker", "description": "Mastered If/Elif/Else branching logic.", "icon": "GitBranch", "criteria_type": "topics_mastered", "criteria_value": "8"},
            {"name": "🔁 Loop Warrior", "description": "Conquered For and While loops.", "icon": "Repeat", "criteria_type": "topics_mastered", "criteria_value": "12"},
            {"name": "📦 Collection Master", "description": "Mastered Lists, Tuples, Sets, and Dictionaries.", "icon": "Database", "criteria_type": "topics_mastered", "criteria_value": "16"},
            {"name": "⚙️ Function Builder", "description": "Built modular reusable functions.", "icon": "Cpu", "criteria_type": "topics_mastered", "criteria_value": "18"},
            {"name": "🚀 Environment Explorer", "description": "Mastered PIP and Virtual Environments.", "icon": "Package", "criteria_type": "topics_mastered", "criteria_value": "19"},
            {"name": "👑 Python Boss", "description": "Reached Level 4 in Python Quest!", "icon": "Crown", "criteria_type": "level", "criteria_value": "4"}
        ]

        for b_data in BADGES_DATA:
            badge = Badge(**b_data)
            db.add(badge)

        db.commit()
        print(f"Curriculum successfully seeded with {len(CURRICULUM)} topics, 38 challenges, and 57 quiz questions!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    db_url = os.getenv("DATABASE_URL", "sqlite:///./python_quest.db")
    print(f"\n{'='*60}")
    print(f"Python Quest Database Seeder")
    print(f"{'='*60}")
    print(f"Target database: {db_url[:40]}..." if len(db_url) > 40 else f"Target database: {db_url}")
    print(f"{'='*60}\n")
    seed()
    print("\n✅ Seeding complete!")
