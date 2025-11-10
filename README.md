# GenAI-Powered GCP SOAR Pipeline for Leaked Keys

This project is an automated, "zero-toil" SOAR (Security Orchestration, Automation, and Response) pipeline built 100% on Google Cloud.

It automatically detects a leaked GCP service account key, **immediately contains the threat** by revoking the key via the IAM API, **logs the event** to BigQuery for compliance, and **uses the Vertex AI API** to auto-triage the incident and generate a human-readable summary for the on-call engineer.

This is a portfolio project demonstrating advanced, real-world skills in:
* Cloud-Native Security (SecOps)
* Infrastructure as Code (IaC)
* Serverless Security Automation
* AI-Powered Incident Triage (GenAI)

## 🚀 Features
* **Event-Driven:** Uses Pub/Sub to trigger a serverless Cloud Function in real-time.
* **Automated Containment:** The function automatically revokes the leaked key using the IAM API, containing the threat in seconds.
* **AI-Powered Triage (GenAI):** Uses the **Vertex AI API** and **Prompt Engineering** to analyze the raw alert and generate a "zero-toil" summary, explaining what happened, what the robot did, and what the human needs to do next.
* **Immutable Audit Trail:** Logs every remediation action to BigQuery for compliance and incident tracking.
* **Infrastructure as Code:** All 9 cloud resources (Pub/Sub, BigQuery, Cloud Function, IAM roles) are defined and managed by **Terraform** for reliable, repeatable deployment.

## 🛠️ Tech Stack
* **Cloud:** Google Cloud Platform (GCP)
* **IaC:** Terraform
* **Compute:** Cloud Functions (Python)
* **Messaging:** Pub/Sub
* **Data/Logging:** BigQuery
* **AI / GenAI:** Vertex AI (GenAI APIs), Prompt Engineering

---

## 📸 Project Showcase (The Full Lifecycle)

This project was built, tested, and decommissioned following professional IaC and SecOps practices.

### 1. The Plan (`terraform plan`)
Defines the 9 cloud resources to be built as code.

<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/8465e0da-0df3-4315-9264-d29811586513" />


### 2. The Build (`terraform apply`)
The final "Apply complete!" message, proving successful deployment.

<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/0291f26e-b4a0-4508-982d-83d2d7f61c9a" />


### 3. The Proof: Remediation (The "Response")
The SOAR pipeline automatically disabling the dummy test key in IAM.

<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/f10aa24e-7a27-4958-ba39-fd544d3a152b" />


### 4. The Proof: Audit Trail (The "Logging")
The "SUCCESS_DISABLED" log is written to BigQuery for compliance.

<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/9c280bce-7601-4919-94c6-fe51310661c1" />


### 5. The "GenAI-SOAR" Upgrade (AI-Powered Triage)
A complete pipeline doesn't just *act*; it *reports*. The final step of the Cloud Function is to auto-triage the incident with AI.

The function takes the raw alert, combines it with its own remediation log ("SUCCESS_DISABLED"), and feeds it to the Vertex AI API using a custom-engineered prompt.

(This step is demonstrated by the `genai_soar_function.py` script in this repo).

This script is the 'brains' of the upgrade. It generates a clean, human-readable report—not a raw log. It explains the threat clearly and even gives actionable *next steps* for the human analyst, which is what a "zero-toil" system *actually* needs.

### 6. The Cleanup (terraform destroy)
Decommissioning all resources to reduce attack surface and stop billing.

<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/99ace869-ff7e-4e3b-9306-27229b66da2c" />

## Conclusion
This project demonstrates a complete, end-to-end **"Detect -> Contain -> Triage -> Log"** workflow, which is the core of a modern, hyperscale-ready SOAR.

By using Terraform, I've proven I can build *repeatable* security solutions. By using Cloud Functions and Pub/Sub, I've shown I can build *scalable, serverless* automation. And by integrating the **Vertex AI API**, I've demonstrated how to *solve the 'alert fatigue' problem* by transforming a simple alert into an automated, fully-triaged incident report.

## Solution Architecture

```mermaid
graph TD
    subgraph GCP Environment & Alerting
        Alert[Cloud Logging Alert (e.g., "Leaked Key Found")] -- 1. Triggers on Match --> PubSub[Cloud Pub/Sub (Alert Topic)]
    end

    subgraph GenAI-SOAR Pipeline (Cloud Function)
        PubSub -- 2. Triggers Function --> SOAR_Function[Cloud Function (genai_soar_function.py)]
        SOAR_Function -- 3. [RESPONSE] Calls API --> IAM[IAM API (Disable Key)]
        SOAR_Function -- 4. [AUDIT] Writes Log --> BigQuery[BigQuery (Audit Trail)]
        SOAR_Function -- 5. [TRIAGE] Sends Log/Alert --> VertexAI[Vertex AI API]
        VertexAI -- 6. Returns Summary --> SOAR_Function
        SOAR_Function -- 7. [NOTIFY] Sends Final Report --> Notify[Analyst (via Email/Slack)]
    end
