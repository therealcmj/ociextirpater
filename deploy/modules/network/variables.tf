variable "label" {
  description = "Label prefix applied to created network resources"
  type        = string
}

variable "use_existing_network" {
  description = "Whether to deploy into an existing VCN/subnet"
  type        = bool
}

variable "existing_vcn" {
  description = "Existing VCN OCID provided when use_existing_network is true"
  type        = string
  default     = null
}

variable "existing_subnet" {
  description = "Existing subnet OCID provided when use_existing_network is true"
  type        = string
  default     = null
}

variable "extirpater_tag" {
  description = "Freeform tags applied to resources created by this module"
  type        = map(string)
}

variable "network_compartment" {
  description = "Compartment OCID in which to create network resources"
  type        = string
}