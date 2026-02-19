resource "oci_resource_scheduler_schedule" "on" {
  action             = "START_RESOURCE"
  compartment_id     = var.compartment_id
  recurrence_details = "45 0 * * *"
  recurrence_type    = "CRON"

  resources {
    id = var.resource_id
  }

  display_name  = "Extirpater-Start"
  description   = "Schedule to start extirpater instance"
  freeform_tags = var.extirpater_tag
}

resource "oci_resource_scheduler_schedule" "off" {
  action             = "STOP_RESOURCE"
  compartment_id     = var.compartment_id
  recurrence_details = "45 5 * * *"
  recurrence_type    = "CRON"

  resources {
    id = var.resource_id
  }

  display_name  = "Extirpater-Stop"
  description   = "Schedule to stop extirpater instance"
  freeform_tags = var.extirpater_tag
}