#!/bin/bash
set -e

REPO="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO"

echo ""
echo "=== Voice Agent Startup ==="
echo ""

# 1. Activate venv first (everything depends on it)
source "$REPO/venv/bin/activate"
echo "[✓] venv (Python $(python3 --version | cut -d' ' -f2))"

# 2. Postgres
echo -n "[ ] Postgres..."
python3 -c "
import psycopg2, os
from dotenv import load_dotenv
load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
conn.close()
" 2>/dev/null && echo -e "\r[✓] Postgres" || {
    echo -e "\r[✗] Postgres not reachable"
    echo "    → Run: brew services start postgresql"
    exit 1
}

# 3. Ollama
echo -n "[ ] Ollama..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "\r[✓] Ollama"
else
    echo -e "\r[~] Ollama not running — starting it..."
    ollama serve &>/tmp/ollama.log &
    sleep 3
    curl -s http://localhost:11434/api/tags > /dev/null 2>&1 \
        && echo "[✓] Ollama started" \
        || { echo "[✗] Ollama failed — check /tmp/ollama.log"; exit 1; }
fi

echo ""
echo "All systems go. Speak into your mic — press Ctrl+C to stop."
echo ""

python3 -m voice_agent.main console
