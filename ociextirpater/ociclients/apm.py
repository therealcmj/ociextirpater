import logging
import oci
from ociextirpater.OCIClient import OCIClient

class apm( OCIClient ):
    service_name = "App Performance Management"
    clientClass = oci.apm_control_plane.ApmDomainClient

    objects = [
        {
            "name_singular"      : "APM Domain",
            "name_plural"        : "APM Domains",
            "function_list"      : "list_apm_domains",
            "function_delete"    : "delete_apm_domain",
        },

    ]
