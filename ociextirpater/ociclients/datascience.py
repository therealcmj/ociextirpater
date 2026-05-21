import oci
from ociextirpater.OCIClient import OCIClient

class datascience( OCIClient ):
    service_name = "Data Science"
    clientClass = oci.data_science.DataScienceClient

    objects = [
        {
            "name_singular"      : "Private Endpoint",
            "name_plural"        : "Private Endpoints",
            "function_list"      : "list_data_science_private_endpoints",
            "function_delete"    : "delete_data_science_private_endpoint",
        },

        {
            "name_singular"      : "Job Run",
            "name_plural"        : "Job Runs",
            "function_list"      : "list_job_runs",
            "function_delete"    : "delete_job_run",
        },

        {
            "name_singular"      : "Job",
            "name_plural"        : "Jobs",
            "function_list"      : "list_jobs",
            "function_delete"    : "delete_job",
        },

        {
            "name_singular"      : "Model Deployment",
            "name_plural"        : "Model Deployments",
            "function_list"      : "list_model_deployments",
            "function_delete"    : "delete_model_deployment",
        },


        {
            "name_singular"      : "Model Version Set",
            "name_plural"        : "Model Version Sets",
            "function_list"      : "list_model_version_sets",
            "function_delete"    : "delete_model_version_set",
        },

        {
            "name_singular"      : "Model",
            "name_plural"        : "Models",
            "function_list"      : "list_models",
            "function_delete"    : "delete_model",
        },

        {
            "name_singular"      : "Notebook Session",
            "name_plural"        : "Notebook Sessions",
            "function_list"      : "list_notebook_sessions",
            "function_delete"    : "delete_notebook_session",
        },

        {
            "name_singular"      : "Pipeline Run",
            "name_plural"        : "Pipeline Runs",
            "function_list"      : "list_pipeline_runs",
            "function_delete"    : "delete_pipeline_run",
        },

        {
            "name_singular"      : "Pipeline",
            "name_plural"        : "Pipelines",
            "function_list"      : "list_pipelines",
            "function_delete"    : "delete_pipeline",
        },

        {
            "name_singular"      : "Project",
            "name_plural"        : "Projects",
            "function_list"      : "list_projects",
            "function_delete"    : "delete_project",
        },

        {
            "name_singular"     : "ML Application",
            "name_plural"       : "ML Applications",
            "function_list"     : "list_ml_applications",
            "function_delete"   : "delete_ml_application"
        },

        {
            "name_singular"     : "ML Application Implementation",
            "name_plural"       : "ML Application Implementations",
            "function_list"     : "list_ml_application_implementations",
            "function_delete"   : "delete_ml_application_implementation"
        },

        {
            "name_singular"     : "ML Application Instance",
            "name_plural"       : "ML Application Instances",
            "function_list"     : "list_ml_application_instances",
            "function_delete"   : "delete_ml_application_instance"
        },

        {
            "name_singular"     : "Model Group",
            "name_plural"       : "Model Groups",
            "function_list"     : "list_model_groups",
            "function_delete"   : "delete_model_group",
        },

        {
            "name_singular"     : "Model Group Version History",
            "name_plural"       : "Model Group Version Histories",
            "function_list"     : "list_model_group_version_histories",
            "function_delete"   : "delete_model_group_version_history",
        },

        {
            "name_singular"     : "Model Version Set",
            "name_plural"       : "Model Version Sets",
            "function_list"     : "list_model_version_sets",
            "function_delete"   : "delete_model_version_set",
        },

        {
            "name_singular"     : "Notebook Session",
            "name_plural"       : "Notebook Sessions",
            "function_list"     : "list_notebook_sessions",
            "function_delete"   : "delete_notebook_session"
        },


        {
            "name_singular"     : "Pipeline",
            "name_plural"       : "Pipelines",
            "function_list"     : "list_pipelines",
            "function_delete"   : "delete_pipeline"
        },

        {
            "name_singular"     : "Schedule",
            "name_plural"       : "Schedules",
            "function_list"     : "list_schedules",
            "function_delete"   : "delete_schedule"
        }

        # Things that we don't need to delete explicitly

        # {
        #    def list_ml_application_implementation_versions(self, ml_application_implementation_id, **kwargs):
        #    def delete_model_custom_metadatum_artifact(self, model_id, metadatum_key_name, **kwargs):
        # },

        # {
        #    def delete_model_defined_metadatum_artifact(self, model_id, metadatum_key_name, **kwargs):
        # },

    ]
