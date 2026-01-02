variable "root_compartment" {}
variable "label" {}
variable "extirpate_compartment" {}
variable "instance_ocid" {}
variable "extirpater_tag" {}

variable "scheduler_id" {
    type = list(string)
}

variable "deploy_in_root" {
    type = bool
    default = false
}