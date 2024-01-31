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
  output_path = "event_handler.zip"
  source_dir  = "../cloud_functions/event_handler/"
}

resource "google_storage_bucket_object" "object" {
  name   = "event_handler.zip"
  bucket = google_storage_bucket.default.name
  source = data.archive_file.default.output_path
}

resource "google_cloudfunctions2_function" "event_handler" {
  name        = "event_handler"
  location    = var.region
  description = "event_handler"

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
    ingress_settings   = "ALLOW_ALL"

    environment_variables = {
      PROJECT_ID   = google_project.main.project_id
      PUBSUB_TOPIC = google_pubsub_topic.issue_processing_topic.name
    }

  }
}

resource "google_cloudfunctions2_function_iam_member" "invoker" {
  project        = google_cloudfunctions2_function.event_handler.project
  location       = var.region
  cloud_function = google_cloudfunctions2_function.event_handler.name
  role           = "roles/cloudfunctions.invoker"
  member         = "allUsers"
}

################################################################################################################
################################################################################################
data "archive_file" "event_processor" {
  type        = "zip"
  output_path = "event_processor.zip"
  source_dir  = "../cloud_functions/event_processor/"
}

resource "google_storage_bucket_object" "event_processor" {
  name   = "event_processor.zip"
  bucket = google_storage_bucket.default.name
  source = data.archive_file.event_processor.output_path
}

resource "google_cloudfunctions2_function" "event_processor" {
  name        = "event_processor"
  location    = var.region
  description = "event_processor"
  event_trigger {
    service_account_email = "${google_project.main.number}-compute@developer.gserviceaccount.com"
    event_type            = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic          = google_pubsub_topic.issue_processing_topic.id
    trigger_region        = var.region
    retry_policy          = "RETRY_POLICY_DO_NOT_RETRY"
  }


  build_config {
    runtime     = "python312"
    entry_point = "event_processor"
    source {
      storage_source {
        bucket = google_storage_bucket.default.name
        object = google_storage_bucket_object.event_processor.name
      }
    }

    environment_variables = {
      PROJECT_ID   = google_project.main.project_id
      LOCATION     = var.region
      GENAI_MODEL  = var.llm
      PUBSUB_TOPIC = google_pubsub_topic.issue_processing_topic.id
    }
  }

  service_config {
    available_memory                 = "2G"
    timeout_seconds                  = 60
    available_cpu                    = "1"
    min_instance_count               = 0
    max_instance_count               = 5
    max_instance_request_concurrency = 1
    service_account_email            = "${google_project.main.number}-compute@developer.gserviceaccount.com"
    ingress_settings                 = "ALLOW_INTERNAL_ONLY"
    all_traffic_on_latest_revision   = true

    environment_variables = {
      PROJECT_ID              = google_project.main.project_id
      LOCATION                = var.region
      GENAI_MODEL             = var.llm
      PUBSUB_TOPIC            = google_pubsub_topic.issue_processing_topic.id
      FUNCTION_SIGNATURE_TYPE = "event"
    }

    secret_environment_variables {
      key        = "GITHUB_PAT"
      project_id = google_project.main.project_id
      secret     = google_secret_manager_secret.github_pat_secret.secret_id
      version    = "latest"
    }

    secret_environment_variables {
      key        = "PRIVATE_KEY"
      project_id = google_project.main.project_id
      secret     = google_secret_manager_secret.private_key_secret.secret_id
      version    = "latest"
    }

    secret_environment_variables {
      key        = "PUBLIC_KEY"
      project_id = google_project.main.project_id
      secret     = google_secret_manager_secret.public_key_secret.secret_id
      version    = "latest"
    }

    secret_environment_variables {
      key        = "PASS_KEY"
      project_id = google_project.main.project_id
      secret     = google_secret_manager_secret.git_key_passphrase.secret_id
      version    = "latest"
    }

    secret_environment_variables {
      key        = "GEMINI_API_KEY"
      project_id = google_project.main.project_id
      secret     = google_secret_manager_secret.gemini_api_key.secret_id
      version    = "latest"
    }

  }
}
