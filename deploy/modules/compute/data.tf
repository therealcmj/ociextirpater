# Get newest image of Oracle Autonomous Linux 9
data "oci_core_images" "this" {
  compartment_id           = var.root_compartment
  operating_system         = "Oracle Autonomous Linux"
  operating_system_version = 9
  sort_by                  = "TIMECREATED"
}

data "oci_identity_availability_domains" "this" {
  compartment_id = var.root_compartment
}
