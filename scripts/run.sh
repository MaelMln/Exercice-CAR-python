#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Script de lancement — dev ou prod
# -----------------------------------------------------------------------------
# Variables d’environnement reconnues :
#   ENV   : dev (défaut) ou prod   → active / désactive l’auto‑reload
#   HOST  : interface d’écoute     → si absent, lecture dans .env ou fallback 0.0.0.0
#   PORT  : port d’écoute          → idem
# -----------------------------------------------------------------------------
set -euo pipefail

# 1) Installer les dépendances si nécessaire
python -m pip install --upgrade pip >/dev/null
pip install -r requirements.txt --quiet

# 2) Charger les variables depuis .env si elles ne sont pas déjà définies
#    (utile quand on exécute sans passer par un shell qui source dotenv)
if [ -f .env ]; then
  # shellcheck disable=SC2046,SC2002
  export $(cat .env | grep -v '^#' | xargs)  # HOST, PORT, etc.
fi

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
MODE=${ENV:-dev}

# 3) Lancer Uvicorn
if [[ "$MODE" == "prod" ]]; then
  exec uvicorn app.main:app --host "$HOST" --port "$PORT"
else
  exec uvicorn app.main:app --reload --host "$HOST" --port "$PORT"
fi
```bash
#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip
pip install -r requirements.txt

export PYTHONPATH="${PYTHONPATH}:$(pwd)"

MODE=${ENV:-dev}

if [[ "$MODE" == "prod" ]]; then
  exec uvicorn app.main:app --host 0.0.0.0 --port 8000
else
  exec uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
fi