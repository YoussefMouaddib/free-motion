# 🧠 Nonchy Assistant – AI Day Planner (Notion Only)

A lightweight AI-driven daily planning system powered entirely by **Notion**.  
It connects your **Projects** and **Tasks** databases with an AI assistant (like ChatGPT) to help you plan, reflect, and organize your day automatically.

---

## 🚀 Overview

This assistant is composed of two Python scripts:

1. **`morningPrompt.py`** – Reads your **Notion Projects** and **Tasks** databases, and builds a full “morning prompt” to start your day with ChatGPT or another LLM.
2. **`actionNonchy.py`** – Executes structured commands output by your AI (like `ADD_TASK`, `UPDATE_PROJECT`, etc.) directly on your Notion workspace.

No cloud dependencies, no Google API, no credential setup.  
Everything runs through your Notion integration.

---

## 🧩 Requirements

- Python 3.9+
- A Notion workspace with:
  - **Projects** database  
  - **Tasks** database  
- A Notion integration token (Internal Integration Key)
- Internet access for Notion API

---

## 🗂 Folder Structure

nonchy-assistant/
│
├── morningPrompt.py
├── actionNonchy.py
└── README.md

yaml
Copy code

---

## 🧠 Database Setup

You can either **duplicate the ready-made Notion templates** or **create them manually**.

### Option A – Import templates
You can duplicate these template pages into your Notion (once available):  
- **Projects DB Template**
- **Tasks DB Template**

*(If you’re publishing this on GitHub, just add “Duplicate Page” links to your template pages.)*

---

### Option B – Create manually

#### 🧱 Projects Database
Name your database: **Projects**  
Required columns:
| Property Name | Type | Description |
|----------------|------|-------------|
| `Project Name` | Title | Main project title |
| `Status` | Status | Example values: Not Started, In Progress, Complete |
| `Tags` | Multi-select | Keywords (e.g., “Hardware”, “AI”) |
| `Last Step` | Text | Most recent progress or action |
| `Next Step` | Text | Upcoming planned action |
| `Summary` | Text | Short project description |

#### ✅ Tasks Database
Name your database: **Tasks**  
Required columns:
| Property Name | Type | Description |
|----------------|------|-------------|
| `Name` | Title | Task name |
| `Done` | Checkbox | Mark completed tasks |

Both databases **must use the same property names** as listed above.  
If you rename or remove any column, the Python scripts will fail to fetch data.

---

## 🔐 Connect to Notion

1. Go to [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Create a **new internal integration**
3. Copy the **Internal Integration Token**
4. Share your **Projects** and **Tasks** databases with this integration (top-right “Share” → select your integration)

Then, open each `.py` file and paste your credentials:

```python
NOTION_API_KEY = "your_secret_key_here"
NOTION_PROJECTS_DB_ID = "your_projects_db_id"
NOTION_TASKS_DB_ID = "your_tasks_db_id"
To get each Database ID:

Open the database in your browser

Copy the part of the URL after the last /
e.g. https://www.notion.so/.../20cea28cce5a80b7a75fe24ec71c055b

⚙️ Installation
bash
Copy code
pip install notion-client
☕️ Daily Routine
Step 1 – Generate your Morning Prompt
Run:

bash
Copy code
python morningPrompt.py
This prints your daily AI reflection prompt under:

sql
Copy code
------ PROMPT TO COPY INTO CHATGPT ------
Paste it into ChatGPT (or any LLM).
Your assistant will see your live project and task data, then help you plan and reflect.

Step 2 – Execute Actions
When your AI outputs structured commands like:

css
Copy code
ADD_TASK: {"Name": "Submit lab report", "Done": false}
UPDATE_PROJECT: {"project": "Superscalar CPU", "field": "Last Step", "value": "Tested forwarding unit"}
Run:

bash
Copy code
python actionNonchy.py
Paste the command.
It updates your Notion database instantly.

🧠 Supported Commands
Command	Description
ADD_TASK	Create a new task
CHECK_TASK	Mark a task as done
UPDATE_PROJECT	Update the “Last Step” text
ADD_PROJECT	Add a new project

Example:

css
Copy code
ADD_PROJECT: {"Project Name": "SoC Design Blog", "Tags": ["CPU", "Writing"], "Next Step": "Outline article", "Summary": "Writing a technical blog about my CPU project", "Status": "In Progress"}
🔄 Optional: Sync with Google Calendar
If you prefer having your Notion tasks mirrored to Google Calendar,
just connect your Notion calendar view to your Google Calendar from within Notion’s UI.
No credentials, no API setup needed.
