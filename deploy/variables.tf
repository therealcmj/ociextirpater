variable "tenancy_ocid" {}
variable "user_ocid" {
  default = null
}
variable "private_key_path" {
  default = null
}
variable "fingerprint" {
  default = null
}
variable "private_key_password" {
  default = null
}
variable "region" {}

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

variable "use_existing_tag" {
  type = bool
  default = false
}

variable "existing_tag" {
  type = string
  default = null
}
