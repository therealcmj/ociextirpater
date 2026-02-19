#### REQUIRED ####

# Provider authentication
tenancy_ocid         = "ocid1.tenancy.oc1..<tenancy id>"
fingerprint          = "<fingerprint>"
user_ocid            = "ocid1.user.<user id>"
private_key_path     = "<~/.oci/key.pem>"
private_key_password = "strong_password"
region               = "us-ashburn-1" # https://docs.oracle.com/en-us/iaas/Content/General/Concepts/regions.htm#About

# Compartment for resources to be removed by Extirpater
cleanup_compartment = "ocid1.compartment.oc1..<compartment id>"

# Deploy resources to a different compartment than the cleanup target
use_deployment_compartment = false
# deployment_compartment     = "ocid1.compartment.oc1..<deployment compartment id>" # Not required when use_deployment_compartment set to false


#### OPTIONAL ####

# Optional label prefix applied to created resources (default: extirpater)
label = "extirpater"

# SSH Public Key for instance authentication
ssh_public_key = "ssh-rsa AAAAAAAA"

# Network
use_existing_network = true # Default false
existing_vcn         = "ocid1.vcn.oc1.iad.<vcn id>"
existing_subnet      = "ocid1.subnet.oc1.iad.<subnet id>"

# Optional network compartment override (defaults to resources compartment)
network_compartment = "ocid1.compartment.oc1..<network compartment id>"

# Freeform tags used to skip resources during cleanup
extirpater_tag = {
  extirpater_skip = "true"
}
