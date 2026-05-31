import oci
from ociextirpater.OCIClient import OCIClient

import logging

class loganalytics( OCIClient ):
    service_name = "Log Analytics"
    clientClass = oci.log_analytics.LogAnalyticsClient
    compositeClientClass = oci.log_analytics.LogAnalyticsClientCompositeOperations

    namespace = None
    def __init__(self,config):
        super().__init__(config)

        # we need the namespace
        self.namespace = self.clients[ config.home_region ].list_namespaces(config.ociconfig["tenancy"]).data.items[0].namespace_name
        logging.debug("Logging Analytics namespace is {}".format(self.namespace))

        # log analytics may not be onboarded in every region.
        # once we've initialized the clients (above) we can iterate through them and check
        for region in list(self.clients.keys()):
            logging.debug("Checking if Log Analytics is onboarded in region {}".format(region))
            try:
                d = self.clients[region].get_namespace(self.namespace).data
                logging.debug("Log Analytics is onboarded in region {}".format(region))
                
            except oci.exceptions.ServiceError as e:
                if e.status == 404:
                    logging.warning("Log Analytics does not appear to be onboarded in region {}. Removing client for that region.".format(region))
                    del self.clients[region]
                else:
                    raise
        logging.debug("Log Analytics clients initialized for regions: {}".format(list(self.clients.keys())))
    
    objects = [
        {
            "name_singular"      : "Log Analytics Source",
            "name_plural"        : "Log Analytics Sources",
            "function_list"      : "list_sources",
            # "kwargs_list"        : {
            #                             "is_system": "CUSTOM"
            #                        },
            "formatter"          : lambda source: "Logging source with name '{}' (ID {}) system defined: {}".format(source.name, source.source_id, source.is_system),
            "function_get"       : "get_log_source",
            "function_delete"    : "delete_source",
        },

        {
            "name_singular"      : "Log Analytics Entity",
            "name_plural"        : "Log Analytics Entities",
            "function_list"      : "list_log_analytics_entities",
            "formatter"          : lambda obj: "Log Analytics Entity with OCID {} / name '{}' is in state {}".format( obj.id, obj.name, obj.lifecycle_state ),
            "function_delete"    : "delete_log_analytics_entity",
        },

        {
            "name_singular"      : "Log Analytics Log Group",
            "name_plural"        : "Log Analytics Log Groups",
            "function_list"      : "list_log_analytics_log_groups",
            "formatter"          : lambda lg: "Log Group with OCID {} / name '{}'".format(lg.id, lg.display_name),
            "function_delete"    : "delete_log_analytics_log_group",
        },


        {
            "name_singular"      : "Scheduled Task",
            "name_plural"        : "Scheduled Tasks",
            "function_list"      : "list_scheduled_tasks",
            # "formatter"          : lambda st: "Scheduled task with OCID {} / name '{}'".format(st.id, st.display_name),
            "function_delete"    : "delete_scheduled_task",
        },
    ]

    # I override the findAllInCompartment from OCIClient.py because Log Analytics has an extra param
    def findAllInCompartment(self, region, o, this_compartment, **kwargs):
        # TODO: why am I passing kwargs in? I can't remember and that seems wrong

        if o["name_plural"].startswith("Scheduled Tasks"):
            # scheduled tasks require a different call than the others in Log Analytics
            return_date = []
            for tt in ["SAVED_SEARCH", "ACCELERATION", "PURGE"]:
                logging.debug("Calling {} for task type {}".format( o["function_list"], tt))
                os = oci.pagination.list_call_get_all_results(getattr((self.clients[region]), o["function_list"]),
                                                              self.namespace,
                                                              tt,
                                                              this_compartment,
                                                              **kwargs).data
                if os:
                    logging.debug("Found {} scheduled tasks of type {}".format(len(os), tt))
                    return_date.extend(os)
            
            logging.debug("Total scheduled tasks found: {}".format(len(return_date)))
            return return_date

        # every other LOGAN method takes namespace and compartment ID
        logging.debug("Calling {}".format( o["function_list"]))
        os = oci.pagination.list_call_get_all_results(getattr((self.clients[region]), o["function_list"]),
                                                      self.namespace,
                                                      this_compartment,
                                                      **kwargs).data

        # function_list get all of the "objects". Nearly every object includes a field for the compartrment ID but
        # Log Analytics "Sources" (for reasons that aren't important) does not.
        # I do need it later (to delete the Source), so for this special case I manually add the compartment ID to each item
        if o["name_singular"] == "Log Analytics Source":
            logging.debug("adding compartment field to returned objects")
            for i in range(0,len(os)):
                os[i].compartment_id = this_compartment

        return os

    def delete_object(self, object, region, found_object):
        func_name = object.get("function_delete")
        logging.debug("Delete function is {}".format(func_name))

        if object["name_singular"] == "Log Analytics Log Group":
            import datetime
            logging.debug("Purging log group {} with OCID {}".format(found_object.display_name, found_object.id))
            # self.compositeClients[region].purge_storage_data_and_wait_for_state(
            #     self.namespace,
            #     oci.log_analytics.models.PurgeStorageDataDetails(
            #         compartment_id = found_object.compartment_id,
            #         time_data_ended = datetime.datetime.now(),
            #         purge_query_string = "*",
            #     ),
            #     [oci.log_analytics.models.WorkRequest.STATUS_SUCCEEDED],
            #     waiter_kwargs=
            #      {
            #          "max_wait_seconds": 1200
            #      }
            # )

            operation_result = self.clients[region].purge_storage_data(
                self.namespace,
                oci.log_analytics.models.PurgeStorageDataDetails(
                    compartment_id = found_object.compartment_id,
                    time_data_ended = datetime.datetime.now(),
                    purge_query_string = "*",
                )
            )

            logging.debug("Purge operation result: {}".format(operation_result.status))
            logging.info("Waiting for log group {} with OCID {} purge request to complete - work request ID: {}".format(found_object.display_name, found_object.id, operation_result.headers["opc-work-request-id"]))
            oci.wait_until(
                self.clients[region],
                self.clients[region].get_storage_work_request(operation_result.headers["opc-work-request-id"], self.namespace),
                evaluate_response=lambda r: getattr(r.data, 'status') and getattr(r.data, 'status').lower() in ["succeeded"],
                max_wait_seconds=1200
            )
            logging.info("Log group {} with OCID {} purged successfully. Proceeding to delete log group.".format(found_object.display_name, found_object.id))

        kwargs = {}
        if object["name_singular"] == "Log Analytics Source":
            if found_object.is_auto_association_enabled:
                logging.info("Auto association is enabled for Log Source {}. Disabling".format(found_object.display_name))
                r = self.clients[region].disable_auto_association(
                    self.namespace,
                    found_object.name,
                    disable_auto_association_details=oci.log_analytics.models.DisableAutoAssociationDetails(
                        items=[
                            oci.log_analytics.models.DisableAutoAssociationDetail(
                                delete_existing_associations=True
                            )
                        ]
                    )
                )
                logging.debug(r)
            
            # see comment above for info about why we are searching for ALL sources (i.e. not exluding system defined ones)
            if found_object.is_system:
                logging.info("{} is a System defined source and so will not be deleted.".format(found_object.display_name))
                return

            # # the Etag was required in order to delete the log source. This has been fixed.
            # I am leaving the code here for a moment for historical reasons and reference should I ever need it again.
            # # LOGAN-23882
            # r = self.clients[region].get_source( self.namespace, found_object.name, found_object.compartment_id)
            # kwargs = {
            #         "if_match": r.headers["ETag"]
            #     }

        func = getattr((self.clients[region]), func_name)
        logging.debug("Calling delete function {} with namespace {} and id {}".format(func_name, self.namespace, found_object.id))
        return func(self.namespace, found_object.id,**kwargs)
