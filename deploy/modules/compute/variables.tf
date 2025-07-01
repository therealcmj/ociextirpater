variable "compartment_ocid" {}
variable "subnet_ocid" {}
variable "label" {}
variable "extirpate_compartment" {}

variable "ssh_public_key" {
    type = string
    default = null
}