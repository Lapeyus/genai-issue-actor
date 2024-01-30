resource "random_id" "default" {
  byte_length = 8
}

resource "google_storage_bucket" "default" {
  name                        = "${random_id.default.hex}-gcf-source"
  location                    = "US"
  uniform_bucket_level_access = true
}

data "archive_file" "default" {
  type        = "zip"
  output_path = "function-source.zip"
  source_dir  = "../cloud_function/"
}

resource "google_storage_bucket_object" "object" {
  name   = "function-source.zip"
  bucket = google_storage_bucket.default.name
  source = data.archive_file.default.output_path
}

resource "google_cloudfunctions2_function" "default" {
  name        = "autoencoder"
  location    = var.region
  description = "a new function"

  build_config {
    runtime     = "python312"
    entry_point = "handle_issue"
    source {
      storage_source {
        bucket = google_storage_bucket.default.name
        object = google_storage_bucket_object.object.name
      }
    }

    environment_variables = {
      PROJECT_ID   = google_project.main.project_id
      PUBSUB_TOPIC = google_pubsub_topic.issue_processing_topic.name
    }
  }

  service_config {
    max_instance_count = 1
    available_memory   = "256M"
    timeout_seconds    = 60
    available_cpu      = "167m"

    environment_variables = {
      PROJECT_ID   = google_project.main.project_id
      PUBSUB_TOPIC = google_pubsub_topic.issue_processing_topic.name
    }

  }
}

resource "google_cloud_run_service_iam_member" "member" {
  location = google_cloudfunctions2_function.default.location
  service  = google_cloudfunctions2_function.default.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
