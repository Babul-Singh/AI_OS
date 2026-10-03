
import chromadb
import hashlib
import json
import os

# Database paths
DATABASE_PATH = "database"
PROFILE_PATH = os.path.join(DATABASE_PATH, "user_profile.json")
CHROMA_PATH = os.path.join(DATABASE_PATH, "chroma_db")

os.makedirs(DATABASE_PATH, exist_ok=True)

# Initialize ChromaDB
client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name="ai_os_memory"
)

# In-memory conversation history
conversation_history = []


def normalize_text(text):
    """Normalize text for consistent storage and comparison."""
    if not isinstance(text, str):
        return ""

    return " ".join(text.split())


def save_memory(text):
    """Save a memory without creating duplicate records."""
    text = normalize_text(text)

    if not text:
        return

    # Stable ID: identical text reuses the same record
    memory_id = hashlib.sha256(
        text.casefold().encode("utf-8")
    ).hexdigest()

    # upsert creates a new record or updates the existing one
    collection.upsert(
        documents=[text],
        ids=[memory_id]
    )

    # Keep in-memory history free of duplicate messages
    if not any(
        item.casefold() == text.casefold()
        for item in conversation_history
    ):
        conversation_history.append(text)


def search_memory(query, limit=5):
    """Return a flat list of relevant, unique memories."""
    query = normalize_text(query)

    if not query:
        return []

    results = collection.query(
        query_texts=[query],
        n_results=max(1, limit)
    )

    documents = results.get("documents") or []
    if not documents:
        return []

    # Chroma returns a list of result lists
    retrieved = documents[0] if documents else []

    cleaned = []
    seen = set()

    for document in retrieved:
        text = normalize_text(document)

        if not text:
            continue

        key = text.casefold()

        if key not in seen:
            seen.add(key)
            cleaned.append(text)

    return cleaned


def get_conversation_history():
    return list(conversation_history)


# Load the user profile
if os.path.exists(PROFILE_PATH):
    with open(PROFILE_PATH, "r", encoding="utf-8") as file:
        user_profile = json.load(file)
else:
    user_profile = {
        "name": "",
        "career_goal": "",
        "interests": [],
        "projects": []
    }


def add_unique(items, value):
    """Append a value only if it is not already present."""
    value = normalize_text(value)

    if value and not any(
        isinstance(item, str)
        and item.casefold() == value.casefold()
        for item in items
    ):
        items.append(value)


def update_user_profile(text):
    """Update profile fields without duplicate entries."""
    text = normalize_text(text)

    if not text:
        return

    text_lower = text.casefold()

    if "ai engineer" in text_lower:
        user_profile["career_goal"] = "AI Engineer"

    if "machine learning" in text_lower:
        add_unique(
            user_profile["interests"],
            "Machine Learning"
        )

    if "agents" in text_lower:
        add_unique(
            user_profile["interests"],
            "AI Agents"
        )

    if "project" in text_lower:
        add_unique(user_profile["projects"], text)

    import re

    match = re.search(
        r"\bmy name is\s+([A-Za-z][A-Za-z .'-]*)",
        text,
        re.IGNORECASE
    )

    if match:
        user_profile["name"] = match.group(1).strip()

    with open(PROFILE_PATH, "w", encoding="utf-8") as file:
        json.dump(user_profile, file, indent=4)


def get_user_profile():
    return user_profile

