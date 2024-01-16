variable "folder_display_name" {
  description = "Display name for the new folder."
  type        = string
  default     = "genai-issue-actor"
}

variable "parent" {
  description = "google_folder_parent"
  type        = string
  default     = "folders/247598731200"
}

variable "project_name" {
  description = "Name of the new project."
  type        = string
  default     = "genai-issue-actor"
}

variable "project_id" {
  description = "The ID of the project in which resources will be created."
  default     = "genai-issue-actor"
  type        = string
}

variable "billing_account" {
  description = "The ID of the organization."
  type        = string
  default     = "012F00-93BFC2-44CBB0"
}

variable "region" {
  description = "The region to use for the created resources."
  type        = string
  default     = "us-central1"
}

variable "github_owner" {
  description = "The region to use for the created resources."
  type        = string
  default     = "Lapeyus"
}

variable "github_repo" {
  description = "The region to use for the created resources."
  type        = string
  default     = "genai-issue-actor"
}

variable "llm" {
  description = "llm"
  type        = string
  default     = "gemini-pro"
}
