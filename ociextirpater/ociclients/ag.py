import oci
from ociextirpater.OCIClient import OCIClient

class ag( OCIClient ):
    service_name = "Access Governance"

    class MyAccessGovernanceCPClient(oci.access_governance_cp.AccessGovernanceCPClient):
        def __init__(self, config, **kwargs):
            super().__init__(config, **{
                                            "service_endpoint":"https://access-governance.{}.oci.oraclecloud.com".format(config["region"])
                                        }
                             )
    clientClass = MyAccessGovernanceCPClient

    objects = [
        {
            "name_singular"      : "Access Governance Instance",
            "name_plural"        : "Access Governance Instances",

            "function_list"      : "list_governance_instances",
            "function_delete"    : "delete_governance_instance",
        },
    ]
