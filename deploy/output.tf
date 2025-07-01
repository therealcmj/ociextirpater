output "image" {
  value = module.compute.ol_image.images[0]
}

output "instance_id" {
    value = module.compute.instance_ocid
}