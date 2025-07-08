module "network" {
  depends_on = [ module.governance ]

  source         = "./modules/network"
  label = var.label
  extirpater_tag = module.governance.extirpater_tag
  existing_vcn = var.existing_vcn
  existing_subnet = var.existing_subnet
  use_existing_network = var.use_existing_network
  extirpate_compartment = var.cleanup_compartment
}

module "compute" {
  depends_on = [ module.governance ]

  source        = "./modules/compute"
  compartment_ocid = var.tenancy_ocid
  label = var.label
  extirpater_tag = module.governance.extirpater_tag
  subnet_ocid = module.network.subnet_ocid
  ssh_public_key = var.ssh_public_key
  extirpate_compartment = var.cleanup_compartment
}

module "iam" {
  depends_on = [ module.governance ]

  source        = "./modules/iam"
  label = var.label
  compartment_ocid = var.tenancy_ocid
  extirpate_compartment = var.cleanup_compartment
  instance_ocid = module.compute.instance.id
  extirpater_tag = module.governance.extirpater_tag
}

module "governance" {
  source        = "./modules/governance"
  label = var.label
  compartment_ocid = var.tenancy_ocid
  use_existing_tag = var.use_existing_tag
  existing_tag = var.existing_tag
}