import oci

from ociextirpater.OCIClient import OCIClient


class dbtools(OCIClient):
    service_name = "Database Tools"
    clientClass = oci.database_tools.DatabaseToolsClient
    compositeClientClass = oci.database_tools.DatabaseToolsClientCompositeOperations 

    _kwargs_delete_wait = {
                        "wait_for_states": [
                            oci.database_tools.models.WorkRequest.STATUS_SUCCEEDED,
                            oci.database_tools.models.WorkRequest.STATUS_FAILED,
                            ]
                    }

    objects = [
        {
            "name_singular"      : "Database Tools MCP Toolset",
            "name_plural"        : "Database Tools MCP Toolsets",
            "function_list"      : "list_database_tools_mcp_toolsets",
            # "function_delete"    : "delete_database_tools_mcp_toolset",
            "c_function_delete"  : "delete_database_tools_mcp_toolset_and_wait_for_state",
            "kwargs_delete"      :  _kwargs_delete_wait
        },

        {
            "name_singular"      : "Database Tools MCP Server",
            "name_plural"        : "Database Tools MCP Servers",
            "function_list"      : "list_database_tools_mcp_servers",
            # "function_delete"    : "delete_database_tools_mcp_server",
            # "function_delete"    : "cascading_delete_database_tools_mcp_server"
            "c_function_delete"  : "delete_database_tools_mcp_server_and_wait_for_state",
            "kwargs_delete"      :  _kwargs_delete_wait
        },

        {
            "name_singular"      : "Database Tools Connection",
            "name_plural"        : "Database Tools Connections",
            "function_list"      : "list_database_tools_connections",
            "function_delete"    : "delete_database_tools_connection",
        },

        {
            "name_singular"      : "Database Tools Private Endpoint",
            "name_plural"        : "Database Tools Private Endpoints",
            "function_list"      : "list_database_tools_private_endpoints",
            "function_delete"    : "delete_database_tools_private_endpoint",
        },
    ]
