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

variable "deployment_compartment" {
  type = string
  default = null
}

variable "label" {
  # Must be less than 15 characters
  default = "extirpater"
  type = string

  validation {
    condition     = length(var.label) < 15
    error_message = "label must be less than 15 characters."
  }
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

# Tag to tell Extirpater to skip deletion of resource
variable "extirpater_tag" {
  type = map(string)
  default = {extirpater_skip = "true"}
}
