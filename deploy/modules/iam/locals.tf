locals {
    statements = [for id in var.scheduler_id: "Allow any-user to manage instance in compartment id ${var.extirpate_compartment} where all {request.principal.type='resourceschedule',request.principal.id='${id}'}" ]
}