variable "tenancy_ocid" {}
variable "user_ocid" {}
variable "private_key_path" {}
variable "fingerprint" {}
variable "private_key_password" {}
variable "region" {}

# Mandatory
variable "compartment_id" {
  type = string
}

variable "cleanup_compartment" {
  type = string
}

# Optional

variable "label" {
  # Must be less than 15 characters
  default = "extirpater"
  type = string
}

variable "ssh_public_key" {
  type = string
  default = ""
}

variable "use_existing_network" {
  type = bool
  default = false
}

variable "existing_vcn" {
  type = string
  default = null
}

variable "existing_subnet" {
  type = string
  default = null
}
