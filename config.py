import os
DB_USER = os.getenv("DB_USER", "ai_ops")
DB_PASS = os.getenv("DB_PASS", "")
DB_DSN = os.getenv("DB_DSN", "localhost:1521/ORCLPDB1")
OCI_COMPARTMENT = os.getenv("OCI_COMPARTMENT", "")
OCI_GENAI_ENDPOINT = os.getenv("OCI_GENAI_ENDPOINT", "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com")
OCI_MODEL_ID = os.getenv("OCI_MODEL_ID", "xai.grok-3-fast")
