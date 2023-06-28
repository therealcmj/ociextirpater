import logging

import oci
from ociextirpater.OCIClient import OCIClient

class bastion( OCIClient ):
    service_name = "Bastion service"
    clientClass = oci.bastion.BastionClient

    objects = [
        {
            "function_list"    : "list_bastions",
            "function_delete"  : "delete_bastion",
            "name_singular"    : "Bastion",
            "name_plural"      : "Bastions",
            "formatter"        : lambda bastion: "Bastion with OCID {} / name '{}' is in state {}".format( bastion.id, bastion.name, bastion.lifecycle_state ),

            "children"         : [
                                    {
                                        "function_list": "list_sessions",
                                        "kwargs_list": {
                                        },
                                        "function_delete": "delete_session",
                                        "name_singular": "Bastion Sessions",
                                        "name_plural": "",
                                    }
                                 ]
        }
    ]
