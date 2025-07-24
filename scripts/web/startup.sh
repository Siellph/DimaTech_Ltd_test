#!/usr/bin/env bash

echo "Start service"

# migrate database
python scripts/migrate.py

# load fixtures
python scripts/load_data.py fixture/billing/billing.user.json
python scripts/load_data.py fixture/billing/billing.account.json
python scripts/load_data.py fixture/billing/billing.transaction.json

# start web server
sanic webapp.server:create_app --host=0.0.0.0 --port=8000
