#!/bin/bash

# === CONFIG ===
PROJECT_DIR="$(pwd)"
VENV_DIR="$PROJECT_DIR/.venv"
BIN_PATH="/usr/local/bin/syncify"

echo "📦 Setting up Syncify..."

# 1. Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
  echo "🔧 Creating virtual environment..."
  python3 -m venv "$VENV_DIR"
fi

# 2. Activate virtual environment and install packages
echo "📥 Installing dependencies..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r "$PROJECT_DIR/requirements.txt"

# 3. Create CLI wrapper
echo "⚙️ Creating global 'syncify' command..."

cat > syncify <<EOF
#!/bin/bash
source "$PROJECT_DIR/.venv/bin/activate"

if [ -f "$PROJECT_DIR/.env" ]; then
  export \$(grep -v '^#' "$PROJECT_DIR/.env" | xargs)
fi

cd "$PROJECT_DIR"
python sync.py "\$@"
EOF

chmod +x syncify
sudo mv syncify "$BIN_PATH"

echo "✅ Syncify installed! You can now run it from anywhere using:"
echo "   syncify list"
echo "   syncify add <playlist_id>"
echo "   syncify sync"