output "subnet_ocid" {
  value = var.use_existing_network ? var.existing_subnet : oci_core_subnet.this[0].id
}