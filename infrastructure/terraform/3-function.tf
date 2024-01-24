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
  output_path = "../cloud_function/function-source.zip"
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
    runtime     = "python310"
    entry_point = "handle_issue"
    source {
      storage_source {
        bucket = google_storage_bucket.default.name
        object = google_storage_bucket_object.object.name
      }
    }

    environment_variables = {
      PROJECT_ID  = google_project.main.project_id
      LOCATION    = var.region
      GENAI_MODEL = var.llm
    }
  }

  service_config {
    max_instance_count = 1
    available_memory   = "2G"
    timeout_seconds    = 60
    available_cpu      = "1"

    environment_variables = {
      PROJECT_ID  = google_project.main.project_id
      LOCATION    = var.region
      GENAI_MODEL = var.llm
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

resource "google_cloud_run_service_iam_member" "member" {
  location = google_cloudfunctions2_function.default.location
  service  = google_cloudfunctions2_function.default.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
