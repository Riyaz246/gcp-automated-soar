# Automated GCP SOAR Pipeline for Leaked Keys

This project is an automated SOAR (Security Orchestration, Automation, and Response) pipeline built 100% on Google Cloud. It automatically detects and revokes a leaked GCP service account key in real-time.

This is a portfolio project demonstrating skills in Cloud Security, Infrastructure as Code (IaC), and Serverless Security Automation.

## 🚀 Features
* **Event-Driven:** Uses Pub/Sub to trigger a Cloud Function.
* **Automated Remediation:** The function automatically revokes the leaked key using the IAM API.
* **Secure Audit Trail:** Logs every revocation action to BigQuery for compliance and incident tracking.
* **Infrastructure as Code:** All cloud resources (Pub/Sub, BigQuery, Cloud Function, IAM roles) are defined and managed by Terraform.

## 🛠️ Tech Stack
* **Cloud:** Google Cloud Platform (GCP)
* **IaC:** Terraform
* **Compute:** Cloud Functions (Python)
* **Messaging:** Pub/Sub
* **Data/Logging:** BigQuery

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


### 5. The Cleanup (`terraform destroy`)
Decommissioning all resources to reduce attack surface and stop billing.

<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/99ace869-ff7e-4e3b-9306-27229b66da2c" />
