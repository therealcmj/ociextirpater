import logging
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


    ]
