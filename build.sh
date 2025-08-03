set -o errexit

echo "--- Installing uv (Build Step) ---"

curl -LsSf https://astral.sh/uv/install.sh | sh

source $HOME/.local/bin/env

uv --version

echo "--- Installing project dependencies using make install (Build Step) ---"

make install

echo "--- Running database migrations (Build Step) ---"

DATABASE_URL из переменных окружения Render

psql -a -d $DATABASE_URL -f database.sql

echo "--- Build finished ---"