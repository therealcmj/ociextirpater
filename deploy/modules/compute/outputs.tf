output "instance" {
  value = oci_core_instance.this
}

output "ol_image" {
  value = data.oci_core_images.this
}