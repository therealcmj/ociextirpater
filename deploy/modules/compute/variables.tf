variable "root_compartment" {}
variable "subnet_ocid" {}
variable "label" {}
variable "extirpate_compartment" {}
variable "extirpater_tag" {}
variable "compute_compartment" {}

variable "ssh_public_key" {
  type    = string
  default = null
}