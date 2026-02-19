locals {
  scheduler_statements = [for id in var.scheduler_id : "Allow any-user to manage instance in compartment id ${var.extirpate_compartment} where all {request.principal.type='resourceschedule',request.principal.id='${id}'}"]
  dynamic_group_statements = ["Allow dynamic-group ${oci_identity_dynamic_group.this.name} to manage all-resources in compartment id ${var.extirpate_compartment}"]
}