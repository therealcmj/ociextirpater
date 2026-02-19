provider "oci" {
  tenancy_ocid         = var.tenancy_ocid
  user_ocid            = var.user_ocid
  private_key_path     = var.private_key_path
  fingerprint          = var.fingerprint
  private_key_password = var.private_key_password
  region               = var.region
}

terraform {

  required_providers {
    oci = {
      source  = "oracle/oci"
      version = ">= 4.80.0"
    }

    random = {
      source  = "hashicorp/random"
      version = "3.7.2"
    }
  }
} 