resource "google_pubsub_topic" "issue_processing_topic" {
  name = "issue-processing-topic"
}

resource "google_project_iam_member" "service_account_token_creator" {
  project = var.project_id
  role    = "roles/iam.serviceAccountTokenCreator"
  member  = "serviceAccount:service-${google_project.main.number}@gcp-sa-pubsub.iam.gserviceaccount.com"
}
