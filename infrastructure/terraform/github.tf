/* ------------------------------ Create the SA ----------------------------- */
# give this account bigquery admin role
resource "google_service_account" "service_account" {
  account_id   = "tf-service-account"
  display_name = "Terraform Service Account"
  project      = google_project.main.project_id
}

# Bind the owner role to the service account
resource "google_project_iam_binding" "owner" {
  project = google_project.main.project_id
  role    = "roles/owner"

  members = ["serviceAccount:${google_service_account.service_account.email}"]
}
/* ------------------- Workload Identity Federation for github actions --------- */
resource "google_iam_workload_identity_pool" "idp_pool" {
  workload_identity_pool_id = "github-terraformer"
  project                   = google_project.main.project_id
}

resource "google_iam_workload_identity_pool_provider" "gh_provider" {
  project                            = google_project.main.project_id
  workload_identity_pool_id          = "github-terraformer"
  workload_identity_pool_provider_id = "gh-actions"
  display_name                       = "gh-actions"
  attribute_condition                = "attribute.repository_owner == '${var.github_owner}'"
  oidc {
    allowed_audiences = ["https://iam.googleapis.com/projects/${google_project.main.number}/locations/global/workloadIdentityPools/github-terraformer/providers/gh-actions"]
    issuer_uri        = "https://token.actions.githubusercontent.com"
  }
  attribute_mapping = {
    "google.subject"             = "assertion.sub"
    "attribute.actor"            = "assertion.actor"
    "attribute.repository"       = "assertion.repository"
    "attribute.repository_owner" = "assertion.repository_owner"
  }
}

/* --------------------- Apply Workload Identity Binding -------------------- */
resource "google_service_account_iam_binding" "workload_identity_binding" {
  service_account_id = google_service_account.service_account.id
  role               = "roles/iam.workloadIdentityUser"
  members = [
    # Workload Identity Federation for github actions
    # one repo at a time
    "principalSet://iam.googleapis.com/projects/${google_project.main.number}/locations/global/workloadIdentityPools/github-terraformer/attribute.repository/${var.github_owner}/${var.github_repo}",

    # uncomment to allow all client repos to impersonate the terraform SA
    # "principalSet://iam.googleapis.com/projects/${google_project.main.number}/locations/global/workloadIdentityPools/github-terraformer/attribute.repository_owner/${var.github_owner}",

    # uncomment to use Use Workload Identity with Google Kubernetes Engine, once for each namespace
    # "serviceAccount:${google_project.main.project_id}.svc.id.goog[${NAMESPACE}/${var.service_account}]",
  ]
}
