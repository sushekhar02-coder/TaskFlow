
import re
from datetime import date, timedelta


SYSTEM_PROMPT = """
You are a task parser. Convert a user's free-text task description
into a structured task with title, priority, and due_date_hint.

Priority must be exactly one of:
low, medium, high.

Use these rules:
- urgent or asap -> high
- whenever or low priority -> low
- otherwise -> medium

For due_date_hint, detect:
today, tomorrow, next week,
next monday through next sunday,
or monday through sunday.

Return the matched date phrase in lowercase.
If there is no date phrase, return null.
"""


def build_prompt(description):
    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": description
        }
    ]


def parse_task_description(description):
    # Lower-cased copy used only for matching.
    working = description.lower()

    # -------------------------
    # Priority
    # -------------------------
    if "urgent" in working or "asap" in working:
        priority = "high"
    elif "whenever" in working or "low priority" in working:
        priority = "low"
    else:
        priority = "medium"

    # -------------------------
    # Due-date hint
    # Exact required order
    # -------------------------
    due_date_hint = None

    date_phrases = [
        "today",
        "tomorrow",
        "next week",
        "next monday",
        "next tuesday",
        "next wednesday",
        "next thursday",
        "next friday",
        "next saturday",
        "next sunday",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]

    for phrase in date_phrases:
        if phrase in working:
            due_date_hint = phrase
            break

    # -------------------------
    # Title
    # -------------------------
    title = description

    # Remove ALL priority keywords.
    priority_keywords = [
        "urgent",
        "asap",
        "whenever",
        "low priority",
    ]

    for keyword in priority_keywords:
        title = re.sub(
            re.escape(keyword),
            "",
            title,
            flags=re.IGNORECASE
        )

    # Remove the matched date phrase.
    if due_date_hint:
        title = re.sub(
            re.escape(due_date_hint),
            "",
            title,
            flags=re.IGNORECASE
        )

    # Normalize whitespace.
    title = re.sub(r"\s+", " ", title).strip()

    # Required fallback.
    if not title:
        title = "Untitled task"

    return {
        "title": title,
        "priority": priority,
        "due_date_hint": due_date_hint
    }


def convert_due_date_hint(due_date_hint):
    """
    Convert natural-language date hints into YYYY-MM-DD.
    """

    if not due_date_hint:
        return None

    today = date.today()

    # -------------------------
    # Today
    # -------------------------
    if due_date_hint == "today":
        return today.isoformat()

    # -------------------------
    # Tomorrow
    # -------------------------
    if due_date_hint == "tomorrow":
        return (today + timedelta(days=1)).isoformat()

    # -------------------------
    # Next week
    # -------------------------
    if due_date_hint == "next week":
        return (today + timedelta(days=7)).isoformat()

    # -------------------------
    # Weekdays
    # -------------------------
    weekdays = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }

    # -------------------------
    # Monday through Sunday
    # -------------------------
    if due_date_hint in weekdays:
        target_day = weekdays[due_date_hint]
        current_day = today.weekday()

        days_ahead = (target_day - current_day) % 7

        # If it is today, use the next occurrence.
        if days_ahead == 0:
            days_ahead = 7

        return (today + timedelta(days=days_ahead)).isoformat()

    # -------------------------
    # Next Monday through Sunday
    # -------------------------
    if due_date_hint.startswith("next "):
        weekday_name = due_date_hint.replace("next ", "", 1)

        if weekday_name in weekdays:
            target_day = weekdays[weekday_name]
            current_day = today.weekday()

            days_ahead = (target_day - current_day) % 7

            # "next Monday" means the next occurrence.
            if days_ahead == 0:
                days_ahead = 7

            return (today + timedelta(days=days_ahead)).isoformat()

    return None