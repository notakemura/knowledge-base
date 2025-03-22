import os
import sys
from datetime import date
import re

# Target directory for TIL files
TIL_DIR = "til"

# Markdown template in English
TEMPLATE = """# {date} - {title}

## 🔍 Key Learnings

- 

## 🧪 Experiments / Examples

```sql
-- e.g., queries, code snippets, etc.
```

## 💭 Reflection

- 
"""

def sanitize_title(title):
    """Sanitize the title to create a safe filename (kebab-case)"""
    sanitized = re.sub(r'[^\w\s-]', '', title)  # Remove special characters
    sanitized = sanitized.strip().lower()       # Trim and lowercase
    return re.sub(r'[\s]+', '-', sanitized)     # Replace spaces with hyphens

def create_til(title):
    """Create a TIL markdown file with the given title"""
    today = date.today().isoformat()  # e.g., "2025-03-22"
    safe_title = sanitize_title(title)
    filename = f"{today}-{safe_title}.md"
    filepath = os.path.join(TIL_DIR, filename)

    if not os.path.exists(TIL_DIR):
        os.makedirs(TIL_DIR)

    if os.path.exists(filepath):
        print(f"⚠️ TIL already exists: {filepath}")
        return

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(TEMPLATE.format(date=today, title=title))

    print(f"✅ TIL created: {filepath}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python til.py \"Your TIL Title Here\"")
    else:
        title = " ".join(sys.argv[1:])
        create_til(title)
