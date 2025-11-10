"""
AI-POWERED "ZERO-TOIL" SOAR FUNCTION
--------------------------------------
THIS IS THE "UPGRADE" to the "Automated SOAR for Leaked Secrets" project.

This single Cloud Function is a "Mini-SOAR" pipeline. It is triggered by
a Pub/Sub message from a Cloud Logging alert (e.g., detecting a
'iam.serviceAccounts.keys.create' event).

It demonstrates the "Hyperscale / Zero-Toil" solution by:
1.  Receiving the raw alert from Pub/Sub.
2.  (SIMULATED) Immediately calling the IAM API to **contain** the threat
    by disabling the leaked/compromised key.
3.  Querying BigQuery/Logging to get the *full, raw log* of the threat.
4.  Feeding that raw log to the **Vertex AI API** with a specific
    "post-containment" prompt.
5.  Generating a human-readable, "zero-toil" incident summary that
    informs the on-call engineer of the threat *and* the action
    already taken.

THIS IS THE "PROOF" for the Mistral / Helsing pitch.
"""

import base64
import json

# We can't import these in a locked account, but we include them
# to show the full, correct architecture.
# from google.cloud import iam_admin_v1
# from google.cloud import bigquery
# from vertexai.generative_models import GenerativeModel, Part

# --- 1. MOCK DATA (The Pub/Sub message from the Logging Alert) ---
# This is a mock of the 'data' payload that Pub/Sub sends.
# It's base64 encoded, just like in a real event.
mock_pubsub_data = {
    "data": base64.b64encode(json.dumps({
        "incident": {
            "incident_id": "i-5678abcd",
            "resource_name": "//iam.googleapis.com/projects/your-project/serviceAccounts/sa-compromised@your-project.iam.gserviceaccount.com/keys/a1b2c3d4e5f6g7h8",
            "summary": "Suspicious Service Account Key creation detected."
        },
        "logEntry": {
            "protoPayload": {
                "authenticationInfo": {
                    "principalEmail": "attacker@compromised-vm.com"
                },
                "methodName": "google.iam.admin.v1.CreateServiceAccountKey",
                "resourceName": "//iam.googleapis.com/projects/your-project/serviceAccounts/sa-compromised@your-project.iam.gserviceaccount.com",
                "request": {
                    "keyAlgorithm": "KEY_ALG_RSA_2048"
                }
            },
            "resource": {
                "type": "service_account",
                "labels": {
                    "project_id": "your-project",
                    "email_id": "sa-compromised@your-project.iam.gserviceaccount.com"
                }
            },
            "timestamp": "2025-11-10T09:30:00Z",
            "severity": "ERROR",
            "logName": "projects/your-project/logs/cloudaudit.googleapis.com%2Factivity"
        }
    }).encode('utf-8')).decode('utf-8')
}


def simulate_automated_containment(key_name: str) -> bool:
    """
    This function simulates calling the IAM API to disable the key.
    """
    print(f"\n--- 2. AUTOMATED RESPONSE (ACTION) ---")
    print(f"[ACTION]: Calling iam.serviceAccounts.keys.disable() on key: {key_name}")
    print(f"[STATUS]: Key {key_name} has been DISABLED.")
    
    # In a real script:
    # try:
    #     client = iam_admin_v1.IAMClient()
    #     request = iam_admin_v1.DisableServiceAccountKeyRequest(name=key_name)
    #     client.disable_service_account_key(request=request)
    #     return True
    # except Exception as e:
    #     print(f"Error disabling key: {e}")
    #     return False
    return True

def get_ai_triage_and_summary(raw_log_json: str, key_name: str, containment_success: bool) -> str:
    """
    This function simulates calling the Vertex AI API for "post-containment"
    triage and summarization.
    """
    
    # --- 3. THE PROMPT (The "Secret Sauce" for a SOAR) ---
    # This prompt is different. It reports on an *action already taken*.
    prompt_to_vertex_ai = f"""
    You are a "Zero-Toil" Google Cloud SOAR analyst.
    A high-priority "CreateServiceAccountKey" alert was just detected.
    
    I have ALREADY taken an automated containment action:
    - Target Key: {key_name}
    - Action Taken: DisableServiceAccountKey
    - Containment Success: {containment_success}

    Your job is to parse the following raw JSON log, confirm the automated
    action, and write an "Incident & Response Summary" for the on-call
    SecOps engineer. The engineer needs to know what happened, what the
    robot (you) did, and what they need to do *next* (investigation).

    Raw JSON Log:
    {raw_log_json}
    """
    
    # --- 4. THE SIMULATED AI OUTPUT ---
    # This is the "zero-toil" alert that goes to the on-call engineer.
    
    simulated_ai_output = """
**Incident & Response Summary (GenAI-SOAR)**

* **What Happened:** A new service account key was created for `sa-compromised@your-project.iam.gserviceaccount.com`. The request was made by the principal `attacker@compromised-vm.com`, which is not a recognized administrator.
* **Automated Action Taken:** The "GenAI-SOAR" pipeline has **successfully DISABLED** the newly created key (`a1b2c3d4e5f6g7h8`) via the IAM API. The immediate threat is contained.
* **Your Next Steps (Investigation):**
    1.  **Investigate the Principal:** Analyze all audit logs for the actor `attacker@compromised-vm.com` to determine the "blast radius" and initial point of compromise.
    2.  **Validate the Service Account:** Confirm if `sa-compromised` is a legitimate service account or if it was created by the attacker.
    3.  **Sweep for Other Keys:** Query for any *other* keys created by this principal in the last 24 hours.
"""
    
    print("\n--- 3. AI TRIAGE (ANALYSIS) ---")
    print(f"[INFO]: Sending raw log and containment status to Vertex AI...")
    
    print("\n" + "="*80 + "\n")
    print("--- SIMULATED AI RESPONSE (This is the 'Zero-Toil' Alert) ---")
    print(simulated_ai_output)
    
    return simulated_ai_output

# --- 5. Run the "Solution Blueprint" ---
# This simulates the main Cloud Function body
def main_soar_handler(event_data: dict):
    
    print("--- 1. ALERT DETECTED ---")
    print("[INFO]: Pub/Sub message received from Cloud Monitoring.")
    
    # Decode the Pub/Sub message
    try:
        payload_str = base64.b64decode(event_data['data']).decode('utf-8')
        alert_payload = json.loads(payload_str)
        
        # Extract the critical data
        key_name = alert_payload['incident']['resource_name']
        raw_log = json.dumps(alert_payload['logEntry'], indent=2)
        
        # --- Run the SOAR pipeline ---
        
        # Step 1: Contain the threat
        containment_success = simulate_automated_containment(key_name)
        
        # Step 2: Triage and summarize with AI
        if containment_success:
            get_ai_triage_and_summary(raw_log, key_name, containment_success)
        else:
            print("[ERROR]: Containment failed. Escalating to P0 on-call.")

    except Exception as e:
        print(f"Error processing alert: {e}")

if __name__ == "__main__":
    main_soar_handler(mock_pubsub_data)
