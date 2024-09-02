import oci
from ociextirpater.OCIClient import OCIClient

class managementdashboard( OCIClient ):
    service_name = "Management Dashboards"
    clientClass = oci.management_dashboard.dashx_apis_client.DashxApisClient

    objects = [
        {
            "name_singular"      : "Management Dashboard",
            "name_plural"        : "Management Dashboards",
            "function_list"      : "list_management_dashboards",
            "function_delete"    : "delete_management_dashboard",
        },

        {
            "name_singular"      : "Management Saved Search",
            "name_plural"        : "Management Saved Searches",
            "function_list"      : "list_management_saved_searches",
            "function_delete"    : "delete_management_saved_search",
        },
    ]
