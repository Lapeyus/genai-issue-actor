resource "google_secret_manager_secret" "github_pat_secret" {
  project   = google_project.main.project_id
  secret_id = "github-pat"
  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret" "private_key_secret" {
  project   = google_project.main.project_id
  secret_id = "private-key"
  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret" "public_key_secret" {
  project   = google_project.main.project_id
  secret_id = "public-key"
  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

# resource "google_secret_manager_secret_version" "private_key_version" {
#   secret      = google_secret_manager_secret.private_key_secret.id
#   secret_data = random_id.default.hex
# }
# resource "google_secret_manager_secret_version" "github_pat_version" {
#   secret      = google_secret_manager_secret.github_pat_secret.id
#   secret_data = random_id.default.hex
# }
# resource "google_secret_manager_secret_version" "public_key_version" {
#   secret      = google_secret_manager_secret.public_key_secret.id
#   secret_data = random_id.default.hex
# }
