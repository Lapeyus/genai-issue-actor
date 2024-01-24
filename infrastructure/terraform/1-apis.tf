resource "google_project_service" "secretmanager_service" {
  project                    = google_project.main.project_id
  service                    = "secretmanager.googleapis.com"
  disable_dependent_services = true
}

resource "google_project_service" "cloudfunctions" {
  service            = "cloudfunctions.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "compute_service" {
  project                    = google_project.main.project_id
  service                    = "compute.googleapis.com"
  disable_dependent_services = true
}

resource "google_project_service" "run" {
  project            = google_project.main.project_id
  service            = "run.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "cloudbuild_service" {
  project                    = google_project.main.project_id
  service                    = "cloudbuild.googleapis.com"
  disable_dependent_services = true
}

resource "google_project_service" "aiplatform_service" {
  project                    = google_project.main.project_id
  service                    = "aiplatform.googleapis.com"
  disable_dependent_services = true
}

resource "google_project_service" "serviceusage_service" {
  project                    = google_project.main.project_id
  service                    = "serviceusage.googleapis.com"
  disable_dependent_services = true
}


resource "google_project_service" "cloudresourcemanager_service" {
  project                    = google_project.main.project_id
  service                    = "cloudresourcemanager.googleapis.com"
  disable_dependent_services = true
}

resource "google_project_service" "bigquery_service" {
  project                    = google_project.main.project_id
  service                    = "bigquery.googleapis.com"
  disable_dependent_services = true
}