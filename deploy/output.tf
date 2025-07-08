output "image" {
  value = module.compute.ol_image.images[0]
}

output "instance" {
    value = module.compute.instance
}

output "extirpater_tag" {
  value = module.governance.extirpater_tag
}