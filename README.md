# Oracle AI Database Operations

A web platform where DBAs ask operational questions about their Oracle database in natural language and get back structured, actionable diagnoses — replacing manual AWR/ASH investigation with AI-powered analysis.

![Oracle](https://img.shields.io/badge/Oracle-26ai%20%7C%20%7C%2019c-C74634?style=flat&logo=oracle&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![OCI](https://img.shields.io/badge/OCI-Generative%20AI-4B286D?style=flat)

## What It Does

- **Real-time diagnosis** — blocking sessions, active session analysis, AWR/ASH slowdown analysis, top SQL by DB time, performance comparison
- **Predictive early warning** — risky query pattern scoring, eight-dimension health scan (Green/Yellow/Red), workload spike detection against rolling baselines
- **Infrastructure health** — tablespace capacity checks, Data Guard health summary
- **AI Tool Creator** — describe a new DBA check in plain English, the AI generates the SQL, validates it against the database, and auto-repairs errors
- **Fully editable tools** — modify SQL, prompts, and categories for any tool; add or remove tools as needed
- **Multi-database support** — single UI with a database selector for fleet-wide operations
- **Time window support** — run any tool against a specific time range
- **Export** — Excel and Word export with AI analysis and raw data for auditability
- **Scenario runner** — simulate real incidents (lock contention, bad queries) for training and demos

## How It Works

```
DBA asks a question
    |
    v
Pre-built Oracle queries run against V$ and DBA_HIST_* views
    |
    v
Results returned as structured JSON
    |
    v
JSON + system prompt sent to OCI Generative AI
    |
    v
Structured diagnosis returned:
Summary, Root Cause, Evidence, Severity, Trend, Recommended Actions
```

**At runtime, the AI never writes SQL.** It only interprets results. When the AI Tool Creator generates SQL for a new tool, it goes through a safety filter (SELECT-only, view allowlist) and is validated against the database before it can be saved.

## Prerequisites

- **Oracle Database** — 19c, or 26ai with Enterprise Edition (Diagnostics Pack for AWR/ASH)
- **OCI account** with access to OCI Generative AI
- **Python 3.11+**
- **OCI CLI config** (`~/.oci/config`) with API key

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/oracle-ai-db-ops.git
cd oracle-ai-db-ops
```

### 2. Set up Python environment

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment

Copy the example files and fill in your values:

```bash
cp .env.example .env
cp databases.example.json databases.json
```

Edit `.env` with your database credentials and OCI compartment OCID:

```
DB_USER=ai_ops
DB_PASS=YourPasswordHere
DB_DSN=your-db-host:1521/your_service_name
OCI_COMPARTMENT=ocid1.compartment.oc1..your_compartment_ocid
OCI_GENAI_ENDPOINT=https://inference.generativeai.us-chicago-1.oci.oraclecloud.com
OCI_MODEL_ID=xai.grok-3-fast
```

Edit `databases.json` with your database connection(s):

```json
[
  {
    "id": "mydb",
    "name": "My Oracle Database",
    "host": "your-db-host",
    "port": 1521,
    "service": "your_service_name",
    "user": "ai_ops",
    "password": "YourPasswordHere",
    "active": true
  }
]
```

### 4. Create the database user

Connect as SYS with SYSDBA and create the read-only AI_OPS user:

```sql
CREATE USER ai_ops IDENTIFIED BY "YourPasswordHere"
  DEFAULT TABLESPACE users QUOTA UNLIMITED ON users;

GRANT CREATE SESSION TO ai_ops;
GRANT CREATE PROCEDURE TO ai_ops;
GRANT CREATE TABLE TO ai_ops;

-- V$ views
GRANT SELECT ON SYS.V_$SESSION TO ai_ops;
GRANT SELECT ON SYS.V_$SQL TO ai_ops;
GRANT SELECT ON SYS.V_$SQL_PLAN TO ai_ops;
GRANT SELECT ON SYS.V_$LOCK TO ai_ops;
GRANT SELECT ON SYS.V_$SYSSTAT TO ai_ops;
GRANT SELECT ON SYS.V_$SYSTEM_EVENT TO ai_ops;
GRANT SELECT ON SYS.V_$PROCESS TO ai_ops;
GRANT SELECT ON SYS.V_$RESOURCE_LIMIT TO ai_ops;
GRANT SELECT ON SYS.V_$PGASTAT TO ai_ops;
GRANT SELECT ON SYS.V_$SQL_WORKAREA_ACTIVE TO ai_ops;
GRANT SELECT ON SYS.V_$UNDOSTAT TO ai_ops;
GRANT SELECT ON SYS.V_$TEMP_SPACE_HEADER TO ai_ops;
GRANT SELECT ON SYS.V_$DATABASE TO ai_ops;
GRANT SELECT ON SYS.V_$DATAGUARD_STATUS TO ai_ops;
GRANT SELECT ON SYS.V_$ARCHIVE_DEST_STATUS TO ai_ops;
GRANT SELECT ON SYS.V_$MANAGED_STANDBY TO ai_ops;
GRANT SELECT ON SYS.V_$DATAGUARD_STATS TO ai_ops;
GRANT SELECT ON SYS.V_$SESSION_WAIT TO ai_ops;
GRANT SELECT ON SYS.V_$SQLAREA TO ai_ops;

-- DBA views
GRANT SELECT ON SYS.DBA_HIST_ACTIVE_SESS_HISTORY TO ai_ops;
GRANT SELECT ON SYS.DBA_HIST_SYSTEM_EVENT TO ai_ops;
GRANT SELECT ON SYS.DBA_HIST_SYSSTAT TO ai_ops;
GRANT SELECT ON SYS.DBA_HIST_SNAPSHOT TO ai_ops;
GRANT SELECT ON SYS.DBA_HIST_SQLSTAT TO ai_ops;
GRANT SELECT ON SYS.DBA_HIST_SQL_PLAN TO ai_ops;
GRANT SELECT ON SYS.DBA_OBJECTS TO ai_ops;
GRANT SELECT ON SYS.DBA_SEGMENTS TO ai_ops;
GRANT SELECT ON SYS.DBA_TABLESPACE_USAGE_METRICS TO ai_ops;
GRANT SELECT ON SYS.DBA_TEMP_FREE_SPACE TO ai_ops;
GRANT SELECT ON SYS.DBA_TABLESPACES TO ai_ops;
GRANT SELECT ON SYS.DBA_HIST_TBSPC_SPACE_USAGE TO ai_ops;
```

### 5. Set up OCI CLI

Make sure you have `~/.oci/config` configured with your API key. See [OCI CLI Configuration](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm).

### 6. Run the application

```bash
source venv/bin/activate
python3.11 -m uvicorn app:app --host 0.0.0.0 --port 8000
```

Open http://localhost:8000 in your browser.

## NNE (Native Network Encryption) Note

If connecting to Oracle DBCS, you may need to change NNE from `REQUIRED` to `ACCEPTED` in `sqlnet.ora` on the database server for `python-oracledb` thin mode to connect:

```
SQLNET.ENCRYPTION_SERVER=ACCEPTED
SQLNET.CRYPTO_CHECKSUM_SERVER=ACCEPTED
SQLNET.ENCRYPTION_CLIENT=ACCEPTED
SQLNET.CRYPTO_CHECKSUM_CLIENT=ACCEPTED
```

## Demo Scenarios

The repo includes scripts to simulate real database incidents:

| Script | What It Does |
|--------|-------------|
| `scenario_lock_contention.py` | Creates a blocking session (row lock holder) |
| `scenario_lock_waiter.py` | Creates a blocked session waiting on the lock |
| `scenario_bad_query.py` | Loads 50K rows and runs repeated full-scan queries |
| `scenario_cleanup.py` | Resets demo tables for a clean rerun |

Run scenarios from the **Scenarios** tab in the UI, or manually:

```bash
# Terminal 1: hold a lock
python3.11 scenario_lock_contention.py

# Terminal 2: blocked session
python3.11 scenario_lock_waiter.py

# Terminal 3: run the app and check Tools 3 and 4
python3.11 -m uvicorn app:app --host 0.0.0.0 --port 8000
```

## 10 Built-in Tools

| # | Tool | Category |
|---|------|----------|
| 1 | AWR/ASH slowdown analysis | Real-time |
| 2 | Top SQL by DB time + plan changes | Real-time |
| 3 | Blocking sessions | Real-time |
| 4 | Active sessions by wait class | Real-time |
| 5 | Performance vs yesterday | Real-time |
| 6 | Risky query patterns | Predictive |
| 7 | Workload spikes | Predictive |
| 8 | Early warning scan | Predictive |
| 9 | Tablespace capacity | Infrastructure |
| 10 | Data Guard health | Infrastructure |

## Project Structure

```
├── app.py                      # FastAPI backend (tools, GenAI, scenarios, export)
├── config.py                   # Environment-based configuration
├── tools.json                  # Tool definitions (queries, prompts, categories)
├── databases.json              # Database connection registry
├── requirements.txt            # Python dependencies
├── static/
│   └── index.html              # Web dashboard (single-page app)
├── scenario_lock_contention.py # Lock holder scenario
├── scenario_lock_waiter.py     # Lock waiter scenario
├── scenario_bad_query.py       # Bad query pattern scenario
├── scenario_cleanup.py         # Cleanup / reset
└── oracle_db_skills_mapping.md # Skills repo reference mapping
```

## Tech Stack

- **Database:** Oracle 19c / 26ai Enterprise Edition (Diagnostics Pack)
- **AI:** OCI Generative AI (model-agnostic — xai.grok-3-fast, Cohere, Llama, etc.)
- **Backend:** Python 3.11, FastAPI, oracledb (thin driver with connection pooling)
- **Frontend:** Single-page HTML/JS dashboard
- **Security:** Read-only database user, SQL safety filter, view allowlist, SELECT-only validation
