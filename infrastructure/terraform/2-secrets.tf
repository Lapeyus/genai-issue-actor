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

resource "google_secret_manager_secret" "git_key_passphrase" {
  project   = google_project.main.project_id
  secret_id = "git-key-passphrase"
  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret" "gemini_api_key" {
  project   = google_project.main.project_id
  secret_id = "gemini-api-key"
  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret_version" "github_pat_version" {
  secret      = google_secret_manager_secret.github_pat_secret.id
  secret_data = random_id.default.hex
}

resource "google_secret_manager_secret_version" "public_key_version" {
  secret                = google_secret_manager_secret.public_key_secret.id
  is_secret_data_base64 = false
  secret_data           = random_id.default.hex #filebase64("~/.ssh/id_rsa.pub")
}

resource "google_secret_manager_secret_version" "private_key_secret" {
  secret                = google_secret_manager_secret.private_key_secret.id
  is_secret_data_base64 = false
  secret_data           = random_id.default.hex #filebase64("~/.ssh/id_rsa")
}

resource "google_secret_manager_secret_version" "git_key_passphrase_version" {
  secret      = google_secret_manager_secret.git_key_passphrase.id
  secret_data = " "
}


resource "google_secret_manager_secret_version" "gemini_api_key" {
  secret      = google_secret_manager_secret.gemini_api_key.id
  secret_data = " "
}
