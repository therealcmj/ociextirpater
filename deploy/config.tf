module "network" {
  source               = "./modules/network"
  label                = var.label
  extirpater_tag       = var.extirpater_tag
  existing_vcn         = var.existing_vcn
  existing_subnet      = var.existing_subnet
  use_existing_network = var.use_existing_network
  network_compartment  = local.networks_compartment
}

module "compute" {
  source                = "./modules/compute"
  root_compartment      = var.tenancy_ocid
  extirpate_compartment = var.cleanup_compartment
  compute_compartment   = local.resources_compartment
  label                 = var.label
  extirpater_tag        = var.extirpater_tag
  subnet_ocid           = module.network.subnet_ocid
  ssh_public_key        = var.ssh_public_key
}

module "iam" {
  source                = "./modules/iam"
  label                 = var.label
  root_compartment      = var.tenancy_ocid
  extirpate_compartment = var.cleanup_compartment
  resources_compartment = local.resources_compartment
  instance_ocid         = module.compute.instance.id
  extirpater_tag        = var.extirpater_tag
  deploy_in_root = var.use_deployment_compartment
  scheduler_id   = [module.schedule.scheduler_id_on, module.schedule.scheduler_id_off]
}

module "schedule" {
  source         = "./modules/resourcescheduler"
  compartment_id = local.resources_compartment
  resource_id    = module.compute.instance.id
  extirpater_tag = var.extirpater_tag
}