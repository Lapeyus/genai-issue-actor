output "function_uri" {
  value = google_cloudfunctions2_function.event_handler.service_config[0].uri
}
