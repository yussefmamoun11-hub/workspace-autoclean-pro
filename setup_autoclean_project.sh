#!/bin/bash

set -e

PROJECT_NAME="workspace-autoclean-pro"
GITHUB_REPO_URL="https://github.com/yussefmamoun11-hub/workspace-autoclean-pro.git"
PYTHON_FILE="main.py"

echo "🚀 Professional Auto Setup Started..."

# ===============================
# Detect project root
# ===============================
if [ -f "$PYTHON_FILE" ]; then
    echo "📍 Running inside project directory"
    PROJECT_DIR="$(pwd)"
else
    echo "📁 Creating project directory..."
    mkdir -p "$PROJECT_NAME"
    PROJECT_DIR="$PROJECT_NAME"

    if [ -f "../$PYTHON_FILE" ]; then
        cp "../$PYTHON_FILE" "$PROJECT_DIR/"
        echo "✔ main.py copied into project"
    else
        echo "❌ main.py not found"
        echo "👉 Put main.py next to the script or inside the project"
        exit 1
    fi
fi

cd "$PROJECT_DIR"

# ===============================
# .gitignore
# ===============================
cat <<EOF > .gitignore
__pycache__/
*.pyc
.env
exports/
EOF

echo "✔ .gitignore created"

# ===============================
# README.md
# ===============================
cat <<EOF > README.md
# 🚀 WorkSpace AutoClean Pro

Professional Python automation tool demonstrating real-world file organization and data cleaning workflows.

---

## 🎯 What It Does
- Organizes files by type
- Cleans and normalizes text data
- Removes duplicates
- Generates TXT & JSON reports
- Runs as interactive CLI tool

---

## 🛠 Tech Stack
- Python 3
- CLI Automation
- File System Operations

---

## 📂 Project Structure
\`\`\`
workspace-autoclean-pro/
├── main.py
├── README.md
├── requirements.txt
├── exports/
└── .gitignore
\`\`\`

---

## ▶️ Run
\`\`\`bash
python3 main.py
\`\`\`

---

## 👤 Author
**Yussef Mamoun**  
Python Automation Engineer

---

## 📜 License
Portfolio & educational use.
EOF

echo "✔ README.md created"

# ===============================
# requirements.txt
# ===============================
cat <<EOF > requirements.txt
# Standard library only
EOF

echo "✔ requirements.txt created"

# ===============================
# Git setup
# ===============================
if [ ! -d ".git" ]; then
    git init
    git branch -M main
    git remote add origin "$GITHUB_REPO_URL"
fi

git add .
git commit -m "Professional project structure & documentation"

git push -u origin main

echo ""
echo "======================================"
echo "✅ SETUP COMPLETE"
echo "🚀 Repository updated successfully"
echo "💼 Ready for portfolio & freelancing"
echo "======================================"
