import datetime
from notion_client import Client
from datetime import datetime, timedelta


# Set up Notion client and DB IDs
NOTION_API_KEY = "secret_c0omyT15jLQhICgbAEYcszy3q9ZzFD1d6E7nF05sLJY"
NOTION_PROJECTS_DB_ID = "20cea28cce5a80b7a75fe24ec71c055b"
NOTION_TASKS_DB_ID = "210ea28cce5a80c3a6b1d6a1e723a5b1"



notion = Client(auth=NOTION_API_KEY)

chat_history = []  # This can be loaded from a file or stored session if needed


def get_active_projects():
    projects = []
    next_cursor = None

    while True:
        response = notion.databases.query(
            database_id=NOTION_PROJECTS_DB_ID,
            filter={
                "property": "Status",
                "status": {"equals": "In Progress"}
            },
            start_cursor=next_cursor,
            page_size=100
        )

        for result in response["results"]:
            props = result["properties"]
            title = props["Project Name"]["title"][0]["text"]["content"]
            status = props["Status"]["status"]["name"]
            tags = ", ".join([t["name"] for t in props.get("Tags", {}).get("multi_select", [])])
            last_step = props.get("Last Step", {}).get("rich_text", [{}])[0].get("text", {}).get("content", "")
            next_step = props.get("Next Step", {}).get("rich_text", [{}])[0].get("text", {}).get("content", "")
            summary = props.get("Summary", {}).get("rich_text", [{}])[0].get("text", {}).get("content", "")

            projects.append({
                "name": title,
                "status": status,
                "tags": tags,
                "last_step": last_step,
                "next_step": next_step,
                "summary": summary
            })

        if not response.get("has_more"):
            break
        next_cursor = response.get("next_cursor")

    return projects


def get_todays_tasks():
    tasks = []
    next_cursor = None

    while True:
        response = notion.databases.query(
            database_id=NOTION_TASKS_DB_ID,
            filter={
                "property": "Done",
                "checkbox": {"equals": False}
            },
            start_cursor=next_cursor,
            page_size=100
        )

        for result in response["results"]:
            props = result["properties"]
            title = props["Name"]["title"][0]["text"]["content"]
            tasks.append({"title": title})

        if not response.get("has_more"):
            break
        next_cursor = response.get("next_cursor")

    return tasks





def build_prompt():
    today = datetime.now().strftime("%A, %B %d, %Y")
    now = datetime.now().strftime("%I:%M %p")

    projects = get_active_projects()
    tasks = get_todays_tasks()


    project_block = "\n".join(
        [f"{i+1}. {p['name']} – {p['status']} – Tags: {p['tags']}\n"
         f"   • Last: {p['last_step']}\n"
         f"   • Next: {p['next_step']}\n"
         f"   • Summary: {p['summary']}" for i, p in enumerate(projects)]
    )

    task_block = "\n".join(
        [f"[ ] {t['title']}" for t in tasks]
    )

    history_text = "\n".join(
        [f"Nonchy: {u}\nAssistant: {a}" for u, a in chat_history]
    )

    prompt = f"""
You are Nonchy's AI assistant.

Today is {today}, and the time is {now}.
Nonchy is a computer engineering student and recording artist, working on technical and creative projects.
He is starting his day by chatting with you over coffee to reflect on priorities and build his schedule.

Here is his current project list with recent updates:
{project_block}

Here are today's active tasks:
{task_block}


--- INSTRUCTIONS ---
At the end of the conversation, or whenever appropriate, output clearly structured commands in this format:

ADD_TASK: {{"Name": "...", "Done": false}}
CHECK_TASK: {{"title": "..."}}
UPDATE_PROJECT: {{"project": "...", "field": "...", "value": "..."}}
SCHEDULE_EVENT: {{"title": "Event title", "date": "2025-06-19T15:00:00", "duration_minutes": 60}}
ADD_PROJECT: {{"Project Name": "Superscalar CPU","Tags": ["LEGv8", "OOO", "Verilog"],"Last Step": "Testing datapath muxes", "Next Step": "CDB + rename","Summary": "An out-of-order superscalar ARM-based CPU in Verilog.","Status": "In Progress"}}


Only output a command when Nonchy clearly implies or agrees on an action.
Avoid redundancy and don’t generate future conversation.
Name the conversation "(today's date) Nonchy AI"
----------------------

Start by greeting Nonchy and telling him about any news related to hardware computer engineering, ai engineering, and texas software/hardware engineering jobs. as well as the most notable papers within the last month about hardware engineering and/or ai and/or computer architecture. 

"""

    return prompt.strip()


if __name__ == "__main__":
    
    final_prompt = build_prompt()
    print("\n\n------ PROMPT TO COPY INTO CHATGPT ------\n")
    print(final_prompt)
