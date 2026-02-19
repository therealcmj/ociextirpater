# Optional remote state backend for Terraform CLI users
# Uncomment and provide values below to enable state locking in OCI Object Storage.
# This block is intentionally disabled so Oracle Resource Manager deployments are unaffected.
/*
terraform {
  backend "oci" {
    bucket               = "<state bucket name>"
    namespace            = "<object storage namespace>"
    region               = "<oci-region>"
    compartment_id       = "<compartment ocid hosting the bucket>"
    key                  = "<key_location>"
    auth                 = "APIKey"
  }
}
*/