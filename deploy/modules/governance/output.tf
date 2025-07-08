output "extirpater_tag" {
  value = var.use_existing_tag ? var.existing_tag : "${oci_identity_tag_namespace.this[0].name}.${oci_identity_tag.this[0].name}"
}