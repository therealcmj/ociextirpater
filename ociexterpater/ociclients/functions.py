import logging

import oci
from ociexterpater.OCIClient import OCIClient

class functions( OCIClient ):
    service_name = "Functions"
    clientClass = oci.functions.FunctionsManagementClient

    objects = [
        {
            "function_list"    : "list_applications",
            "kwargs_list"      : {
                                 },
            # this is an example of a lambda function to filter out objects with the field "foo" set to "XXX"
            # "filter_func"      : lambda o: not o["foo"] == "XXX",
            "function_delete"  : "delete_application",
            "name_singular"    : "Functions Application",
            "name_plural"      : "Functions Applications",
        }
    ]
