# 1. The Pub/Sub topic your scanner will publish findings to
resource "google_pubsub_topic" "secret_findings" {
  name = "secret-findings-topic"
}

# 2. The BigQuery dataset to log our incidents
resource "google_bigquery_dataset" "incident_logs" {
  dataset_id = "incident_logs"
  location   = "US"
}

# 3. The BigQuery table for logs
resource "google_bigquery_table" "revocation_log" {
  dataset_id = google_bigquery_dataset.incident_logs.dataset_id
  table_id   = "key_revocation_log"

  schema = <<EOF
[
  {
    "name": "timestamp",
    "type": "TIMESTAMP",
    "mode": "REQUIRED"
  },
  {
    "name": "key_name",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "status",
    "type": "STRING",
    "mode": "REQUIRED"
  }
]
EOF
  deletion_protection = false
}

# 4. Storage bucket to hold our function's source code
resource "google_storage_bucket" "function_bucket" {
  name     = "${var.project_id}-cf-source-bucket" # Bucket names must be globally unique
  location = "US"
}

# 5. Zip our source code (from the root folder)
data "archive_file" "function_source" {
  type        = "zip"
  output_path = "function-source.zip"

  # Add main.py to the root of the zip
  source {
    content  = file("main.py")
    filename = "main.py"
  }

  # Add requirements.txt to the root of the zip
  source {
    content  = file("requirements.txt")
    filename = "requirements.txt"
  }
}

# 6. Upload the zipped code to the bucket
resource "google_storage_bucket_object" "function_zip" {
  name   = "function-source.zip"
  bucket = google_storage_bucket.function_bucket.name
  source = data.archive_file.function_source.output_path
}

# 7. The runtime service account for our Cloud Function
resource "google_service_account" "function_sa" {
  account_id   = "soar-function-identity"
  display_name = "SOAR Function Runtime SA"
}

# 8. Grant our function permission to disable keys and write to BigQuery
resource "google_project_iam_member" "grant_key_admin" {
  project = var.project_id
  role    = "roles/iam.serviceAccountKeyAdmin" # Powerful! Allows disabling keys.
  member  = "serviceAccount:${google_service_account.function_sa.email}"
}

resource "google_project_iam_member" "grant_bigquery_writer" {
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.function_sa.email}"
}

# 9. The Cloud Function itself
resource "google_cloudfunctions_function" "secret_responder" {
  name        = "soar-secret-responder"
  runtime     = "python310"
  entry_point = "revoke_key" # This must match the function name in your Python code

  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.function_zip.name

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = google_pubsub_topic.secret_findings.name
  }

  service_account_email = google_service_account.function_sa.email
  
  # Set environment variables for the function
  environment_variables = {
    PROJECT_ID = var.project_id
    DATASET_ID = google_bigquery_dataset.incident_logs.dataset_id
    TABLE_ID   = google_bigquery_table.revocation_log.table_id
  }
}