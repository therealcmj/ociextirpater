output "image" {
  value = module.compute.ol_image.images[0]
}

output "instance" {
  value = module.compute.instance
}