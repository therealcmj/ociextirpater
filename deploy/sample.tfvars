#### REQUIRED ####

# Provider authentication
tenancy_ocid         = "ocid1.tenancy.oc1..<tenancy id>"
fingerprint          = "<fingerprint>"
user_ocid            = "ocid1.user.<user id>"
private_key_path     = "<~/.oci/key.pem>"
private_key_password = "strong_password"
region               = "us-ashburn-1" # https://docs.oracle.com/en-us/iaas/Content/General/Concepts/regions.htm#About

# Extirpater compartment
cleanup_compartment = "ocid1.compartment.oc1..<compartment id>"


#### OPTIONAL ####

# SSH Public Key for instance authentication
ssh_public_key = "ssh-rsa AAAAAAAA"

# Network
use_existing_network = true # Default false
existing_vcn         = "ocid1.vcn.oc1.iad.<vcn id>"
existing_subnet      = "ocid1.subnet.oc1.iad.<subnet id>"
