output "instance_ocid" {
  value = oci_core_instance.this.id
}

output "ol_image" {
  value = data.oci_core_images.this
}