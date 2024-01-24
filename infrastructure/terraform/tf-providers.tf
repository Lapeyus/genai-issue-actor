terraform {
  required_version = ">= 1.5.6"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.58.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.1.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = ">= 2.2.0"
    }
  }
}


provider "google" {
  project = "genai-issue-actor"
  region  = "us-central1"
  zone    = "us-central1-c"
}
