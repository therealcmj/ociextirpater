import oci
from ociextirpater.OCIClient import OCIClient

class mysqlconfig( OCIClient ):
    service_name = "MYSQL Configurations"
    clientClass = oci.mysql.MysqlaasClient

    objects = [
        {
            "name_singular"      : "mySQL Config",
            "name_plural"        : "mySQL Configs",
            "function_list"      : "list_configurations",
            "kwargs_list"        : { "type": ["CUSTOM"] },
            "check2delete"       : lambda config: hasattr(config, "type") and config.type != "DEFAULT",
            "function_delete"    : "delete_configuration",
        },
    ]
