variable "label" {}
variable "root_compartment" {}      # Tenancy root
variable "extirpate_compartment" {} # Cleanup compartment
variable "resources_compartment" {} # Extirpater resources compartment
variable "instance_ocid" {}
variable "extirpater_tag" {}

variable "scheduler_id" {
  type = list(string)
}

variable "deploy_in_root" {
  type    = bool
  default = false
}