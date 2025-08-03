set -o errexit
echo "--- Installing uv (Build Step) ---"
curl -LsSf https://astral.sh/uv/install.sh | sh
.$HOME/.local/bin/env
uv --version
echo "--- Installing project dependencies using make install (Build Step) ---"
make install
echo "--- Running database migrations (Build Step) ---"
psql -a -d $DATABASE_URL -f database.sql
