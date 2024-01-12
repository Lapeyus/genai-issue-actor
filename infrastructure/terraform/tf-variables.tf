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







# variable "service_account_id" {
#   description = "ID for the service account."
#   type        = string
#   default     = "genai"
# }

# variable "service_account_display_name" {
#   description = "Display name for the service account."
#   type        = string
#   default     = "genai"
# }

# variable "vpc_name" {
#   description = "Name for the VPC."
#   type        = string
#   default     = "genai"
# }

# variable "subnet_name" {
#   description = "Name for the subnet."
#   type        = string
#   default     = "genai"
# }

# variable "subnet_cidr" {
#   description = "CIDR range for the subnet."
#   type        = string
#   default     = "10.0.0.0/16" #22
# }

# variable "trusted_sources" {
#   description = "CIDR ranges that are allowed to communicate with the GKE nodes."
#   type        = list(string)
#   default     = ["0.0.0.0/0"]
# }
