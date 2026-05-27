# Oracle AI DB Ops Demo (Redwood-style)

## Included
- Redwood-style FastAPI web app
- OCI GenAI integration
- Scenario runner
- Add/Edit custom tools in UI
- oracle-db-skills-based prompt/query guidance mapping

## Files
- app.py
- config.py
- tools.json
- static/index.html
- scenario_lock_contention.py
- scenario_lock_waiter.py
- scenario_bad_query.py
- scenario_cleanup.py
- oracle_db_skills_mapping.md

## Quick start on VM
```bash
cd ~/ai-ops-demo
source venv/bin/activate
pip install -r requirements.txt
python3.11 -m uvicorn app:app --host 0.0.0.0 --port 8000
```

## Notes
- Built-in tools remain protected from UI edits.
- UI-created tools must be SELECT/CTE only.
- Lock contention scenario runs in the background and can be stopped from the UI.
