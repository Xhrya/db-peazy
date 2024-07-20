resource "google_cloudfunctions_function" "gen1" {
  entry_point           = "hello_get"
  name                  = "tfc-gen1-cloud-function"
  region                = "europe-west1"
  runtime               = "python311"
  service_account_email = var.workload_sa_email
  source_archive_bucket = "hackathon_shared_storage"
  source_archive_object = "cloud-functions-example.zip"
  trigger_http          = true
}

output "gen1_function_uri" {
  value = google_cloudfunctions_function.gen1.https_trigger_url
}

resource "google_cloudfunctions2_function" "gen2" {
  name     = "tfc-gen2-cloud-function"
  location = "europe-west1"

  build_config {
    runtime     = "python311"
    entry_point = "hello_get" # Set the entry point
    source {
      storage_source {
        bucket = "hackathon_shared_storage"
        object = "cloud-functions-example.zip"
      }
    }
    service_account = var.workload_sa_id
  }

  service_config {
    service_account_email = var.workload_sa_email
  }
}

output "gen2_function_uri" {
  value = google_cloudfunctions2_function.gen2.service_config[0].uri
}