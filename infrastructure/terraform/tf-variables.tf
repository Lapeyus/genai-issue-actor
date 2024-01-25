variable "folder_display_name" {
  description = "Display name for the new folder."
  type        = string
  default     = ""
}

variable "parent" {
  description = "google_folder_parent"
  type        = string
  default     = "folders/#"
}

variable "org" {
  description = "google_org"
  type        = string
  default     = ""
}

variable "project_name" {
  description = "Name of the new project."
  type        = string
  default     = ""
}

variable "project_id" {
  description = "The ID of the project in which resources will be created."
  default     = ""
  type        = string
}

variable "billing_account" {
  description = "The ID of the organization."
  type        = string
  default     = "yourproject #-#-#"
}

variable "region" {
  description = "The region to use for the created resources."
  type        = string
  default     = "us-central1"
}

variable "github_owner" {
  description = "The region to use for the created resources."
  type        = string
  default     = ""
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
