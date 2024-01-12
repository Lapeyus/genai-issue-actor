resource "google_folder" "main" {
  display_name = var.folder_display_name
  parent       = var.parent
}

resource "google_project" "main" {
  name                = var.project_name
  project_id          = var.project_id
  billing_account     = var.billing_account
  folder_id           = google_folder.main.id
  auto_create_network = true
}
