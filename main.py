import base64
import json
import os
import datetime

# This is your new, correct import
from google.cloud import iam_admin_v1
from google.cloud import bigquery

def revoke_key(event, context):
    """
    Triggered by a Pub/Sub message.
    Assumes event data is a JSON string: {"key_name": "full_key_name_to_revoke"}
    """

    # --- Config ---
    project_id = os.environ.get("PROJECT_ID")
    dataset_id = os.environ.get("DATASET_ID")
    table_id = os.environ.get("TABLE_ID")

    # This is your new, correct client
    iam_client = iam_admin_v1.IAMClient()
    bq_client = bigquery.Client()

    log_status = "FAILURE"

    # --- 1. Parse Pub/Sub Message ---
    try:
        data_str = base64.b64decode(event['data']).decode('utf-8')
        data = json.loads(data_str)
        key_to_revoke = data['key_name']

        if not key_to_revoke.startswith("projects/"):
            raise ValueError("Invalid key name format. Key must start with 'projects/'.")

    except Exception as e:
        print(f"Error parsing message: {e}")
        log_key = "unknown"
        log_status = f"PARSE_FAILURE: {e}"
        log_to_bigquery(bq_client, dataset_id, table_id, log_key, log_status)
        return

    print(f"Attempting to revoke key: {key_to_revoke}")

    # --- 2. Revoke the Key (The SOAR Action) ---
    try:
        # This is the new, simpler method call
        iam_client.disable_service_account_key(name=key_to_revoke)

        print(f"Successfully disabled key: {key_to_revoke}")
        log_status = "SUCCESS_DISABLED"

    except Exception as e:
        print(f"Error disabling key: {e}")
        log_status = f"REVOKE_FAILURE: {e}"

    # --- 3. Log to BigQuery (The Audit Trail) ---
    log_to_bigquery(bq_client, dataset_id, table_id, key_to_revoke, log_status)

def log_to_bigquery(client, dataset, table, key_name, status):
    """Helper function to insert a log row into our incident table."""

    table_ref = client.dataset(dataset).table(table)

    row_to_insert = [{
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "key_name": key_name,
        "status": status
    }]

    errors = client.insert_rows_json(table_ref, row_to_insert)
    if errors == []:
        print("Log entry added to BigQuery.")
    else:
        print(f"Error logging to BigQuery: {errors}")