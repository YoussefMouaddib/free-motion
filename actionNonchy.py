import json
from notion_client import Client
from datetime import datetime, timedelta
import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Notion setup
NOTION_API_KEY = "secret_c0omyT15jLQhICgbAEYcszy3q9ZzFD1d6E7nF05sLJY"
NOTION_PROJECTS_DB_ID = "20cea28cce5a80b7a75fe24ec71c055b"
NOTION_TASKS_DB_ID = "210ea28cce5a80c3a6b1d6a1e723a5b1"
notion = Client(auth=NOTION_API_KEY)

SCOPES = ['https://www.googleapis.com/auth/calendar']
def get_calendar_service():
    creds = None
    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pkl', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)

def add_project(data):
    notion.pages.create(
        parent={"database_id": NOTION_PROJECTS_DB_ID},
        properties={
            "Project Name": {"title": [{"text": {"content": data["Project Name"]}}]},
            "Tag": {"multi_select": [{"name": tag} for tag in data.get("Tags", [])]},
            "Last Step": {"rich_text": [{"text": {"content": data.get("Last Step", "")}}]},
            "Next Step": {"rich_text": [{"text": {"content": data.get("Next Step", "")}}]},
            "Summary": {"rich_text": [{"text": {"content": data.get("Summary", "")}}]},
            "Status": {"status": {"name": data.get("Status", "Not Started")}}
        }
    )
    print(f"🧠 Project added: {data['Project Name']}")

def schedule_gcal_event(title, start_time_str, duration_minutes=60):
    service = get_calendar_service()
    start_dt = datetime.fromisoformat(start_time_str)
    end_dt = start_dt + timedelta(minutes=duration_minutes)

    event = {
    'summary': title,
    'start': {'dateTime': start_dt.isoformat(), 'timeZone': 'America/Chicago'},
    'end': {'dateTime': end_dt.isoformat(), 'timeZone': 'America/Chicago'},
    'reminders': {
        'useDefault': False,
        'overrides': [
            {'method': 'popup', 'minutes': 0}
        ]
    }
}

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"📅 Event created: {event.get('htmlLink')}")
def add_task(data):
    notion.pages.create(
        parent={"database_id": NOTION_TASKS_DB_ID},
        properties={
            "Name": {"title": [{"text": {"content": data["Name"]}}]},
            "Done": {"checkbox": data.get("Done", False)}
        }
    )
    print(f"✅ Task added: {data['Name']}")


def check_task(data):
    task_title = data["title"]
    query = notion.databases.query(
        database_id=NOTION_TASKS_DB_ID,
        filter={"property": "Name", "title": {"equals": task_title}}
    )
    if query["results"]:
        page_id = query["results"][0]["id"]
        notion.pages.update(page_id=page_id, properties={"Done": {"checkbox": True}})
        print(f"✅ Task checked: {task_title}")
    else:
        print(f"⚠️ Task not found: {task_title}")


def update_project(data):
    proj_name = data["project"]
    new_value = data["value"]
    query = notion.databases.query(
        database_id=NOTION_PROJECTS_DB_ID,
        filter={"property": "Project Name", "title": {"equals": proj_name}}
    )
    if query["results"]:
        page_id = query["results"][0]["id"]
        notion.pages.update(
            page_id=page_id,
            properties={"Last Step": {"rich_text": [{"text": {"content": new_value}}]}}
        )
        print(f"✅ Project updated: {proj_name} → Last Step = \"{new_value}\"")
    else:
        print(f"⚠️ Project not found: {proj_name}")

def main_loop():
    print("🚀 Enter a structured instruction (or type 'exit'):")
    while True:
        line = input(">>> ").strip()
        if line.lower() in {"exit", "quit"}:
            break
        if ":" not in line:
            print("⚠️ Invalid format. Use CMD: {...}")
            continue
        try:
            cmd, payload = line.split(":", 1)
            data = json.loads(payload.strip())

            if cmd == "ADD_TASK":
                add_task(data)
            elif cmd == "CHECK_TASK":
                check_task(data)
            elif cmd == "UPDATE_PROJECT":
                update_project(data)
            elif cmd == "ADD_PROJECT":
                add_project(data)
            elif cmd == "SCHEDULE_EVENT":
                schedule_gcal_event(
                    title=data["title"],
                    start_time_str=data["date"],
                    duration_minutes=data.get("duration_minutes", 60)
                )
            else:
                print(f"⚠️ Unknown command: {cmd}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main_loop()
