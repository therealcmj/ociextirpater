import logging

import oci
from ociexterpater.OCIClient import OCIClient

class osms( OCIClient ):
    service_name = "OS Management"
    clientClass = oci.os_management.OsManagementClient

    objects = [
        {
            "function_list"    : "list_scheduled_jobs",
            "kwargs_list": {
            },
            "function_delete"  : "delete_scheduled_job",
            "name_singular"    : "OSMS Scheduled Job",
            "name_plural"      : "OSMS Scheduled Jobs",
        },
        {
            "function_list"    : "list_managed_instance_groups",
            "kwargs_list"      : {
                                 },
            "function_delete"  : "delete_managed_instance_group",
            "name_singular"    : "Managed Instance Group",
            "name_plural"      : "Managed Instance Groups",
        },
        {
            "function_list"    : "list_software_sources",
            "kwargs_list"      : {
                                 },
            "function_delete"  : "delete_software_source",
            "name_singular"    : "OSMS Software Source",
            "name_plural"      : "OSMS Software Sources",
        }
    ]
