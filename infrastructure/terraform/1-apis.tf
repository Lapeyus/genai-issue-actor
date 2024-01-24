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




# # terraform apply -target=google_project_service.monitoring -target=google_project_service.monitoringa -target=google_project_service.monitoringb -target=google_project_service.compute_service -target=google_project_service.container_service -target=google_project_service.cloudbuild_service -target=google_project_service.cloudresourcemanager_service -target=google_project_service.secretmanager_service -target=google_project_service.logging -target=google_project_service.cloudfunctions -target=google_project_service.run -target=google_project_service.cloudscheduler -target=google_project_service.container_a -target=google_project_service.cloudtrace_a -target=google_project_service.container_b -target=google_project_service.cloudtrace_b -target=google_project_service.gkehub_b -target=google_project_service.anthosconfigmanagement -auto-approve
# ###################################################
# ###################################################
# resource "google_project_service" "monitoring" {
#   project            = google_project.main.project_id
#   service            = "monitoring.googleapis.com"
#   disable_on_destroy = false
# }
# resource "google_project_service" "documentai" {
#   project            = google_project.main.project_id
#   service            = "documentai.googleapis.com"
#   disable_on_destroy = false
# }

# resource "google_project_service" "monitoringa" {
#   project            = google_project.a.project_id
#   service            = "monitoring.googleapis.com"
#   disable_on_destroy = false
# }

# resource "google_project_service" "monitoringb" {
#   project            = google_project.b.project_id
#   service            = "monitoring.googleapis.com"
#   disable_on_destroy = false
# }

# ###################################################
# # synthetic monitoring


# # synthetic monitoring
# resource "google_project_service" "container_service" {
#   project                    = google_project.main.project_id
#   service                    = "container.googleapis.com"
#   disable_dependent_services = true
# }

# # synthetic monitoring



# resource "google_project_service" "cloudresourcemanager_service" {
#   project                    = google_project.main.project_id
#   service                    = "cloudresourcemanager.googleapis.com"
#   disable_dependent_services = true
# }

# pub_sub_notification_channel


# resource "google_project_service" "logging" {
#   service            = "logging.googleapis.com"
#   disable_on_destroy = false
# }

# # synthetic monitoring

# # synthetic monitoring


# # synthetic monitoring
# resource "google_project_service" "cloudscheduler" {
#   service            = "cloudscheduler.googleapis.com"
#   disable_on_destroy = false
# }

# ###################################################
# ###################################################
# resource "google_project_service" "container_a" {
#   project            = google_project.a.project_id
#   service            = "container.googleapis.com"
#   disable_on_destroy = false
# }
# resource "google_project_service" "cloudtrace_a" {
#   project            = google_project.a.project_id
#   service            = "cloudtrace.googleapis.com"
#   disable_on_destroy = false
# }
# resource "google_project_service" "cloudprofiler_a" {
#   project            = google_project.a.project_id
#   service            = "cloudprofiler.googleapis.com"
#   disable_on_destroy = false
# }

# ###################################################
# ###################################################
# resource "google_project_service" "container_b" {
#   project            = google_project.b.project_id
#   service            = "container.googleapis.com"
#   disable_on_destroy = false
# }
# resource "google_project_service" "cloudtrace_b" {
#   project            = google_project.b.project_id
#   service            = "cloudtrace.googleapis.com"
#   disable_on_destroy = false
# }
# resource "google_project_service" "gkehub_b" {
#   project            = google_project.b.project_id
#   service            = "gkehub.googleapis.com"
#   disable_on_destroy = false
# }
# resource "google_project_service" "anthosconfigmanagement_b" {
#   project            = google_project.b.project_id
#   service            = "anthosconfigmanagement.googleapis.com"
#   disable_on_destroy = false
# }
# resource "google_project_service" "cloudprofiler_b" {
#   project            = google_project.b.project_id
#   service            = "cloudprofiler.googleapis.com"
#   disable_on_destroy = false
# }
