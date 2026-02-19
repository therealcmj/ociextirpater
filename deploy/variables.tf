variable "tenancy_ocid" {
  description = "OCID of the tenancy hosting the deployment"
  type        = string
}

variable "user_ocid" {
  description = "OCID of the user or resource principal running Terraform (required for CLI runs)"
  type        = string
  default     = null
}

variable "private_key_path" {
  description = "Filesystem path to the API signing key (CLI deployments only)"
  type        = string
  default     = null
}

variable "fingerprint" {
  description = "Fingerprint for the API signing key (CLI deployments only)"
  type        = string
  default     = null
}

variable "private_key_password" {
  description = "Optional passphrase for the API signing key"
  type        = string
  default     = null
}

variable "region" {
  description = "OCI region in which to deploy"
  type        = string
}

variable "cleanup_compartment" {
  description = "Compartment whose resources should be cleaned up"
  type        = string
}

variable "use_deployment_compartment" {
  description = "Set true to deploy Extirpater resources to a compartment other than the cleanup compartment"
  type        = bool
  default     = false
}

variable "deployment_compartment" {
  description = "Compartment OCID for Extirpater resources when use_deployment_compartment is true"
  type        = string
  default     = ""
}

variable "network_compartment" {
  description = "Compartment OCID for network resources (defaults to the resources compartment)"
  type        = string
  default     = ""
}

variable "label" {
  description = "Label prefix applied to created resources (must be < 15 characters)"
  type        = string
  default     = "extirpater"

  validation {
    condition     = length(var.label) < 15
    error_message = "label must be less than 15 characters."
  }
}

variable "ssh_public_key" {
  description = "Public SSH key(s) added to the compute instance"
  type        = string
  default     = ""
}

variable "use_existing_network" {
  description = "Deploy into an existing VCN and subnet instead of creating a new one"
  type        = bool
  default     = false
}

variable "existing_vcn" {
  description = "Existing VCN OCID used when use_existing_network is true"
  type        = string
  default     = null
}

variable "existing_subnet" {
  description = "Existing subnet OCID used when use_existing_network is true"
  type        = string
  default     = null
}

# Tag to tell Extirpater to skip deletion of resource
variable "extirpater_tag" {
  description = "Map of freeform tags used to mark resources that Extirpater should skip"
  type        = map(string)
  default     = { extirpater_skip = "true" }
}
