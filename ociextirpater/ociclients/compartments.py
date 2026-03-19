import logging

import oci
from ociextirpater.OCIClient import OCIClient

numDeletedCompartments = 0
maxCompartmentsToDelete = 2


def checkIt(compartment):
    # leaky abstractions are leaky
    # if c.numDeletedCompartments >= c.maxCompartmentsToDelete:
    if numDeletedCompartments >= maxCompartmentsToDelete:
        logging.info("Maximum number of compartments to delete has been reached. Skipping this and all subsequent compartments during this run.")
        return False

    if "ExtirpateAttempted" in compartment.freeform_tags:
        exAttempt = compartment.freeform_tags["ExtirpateAttempted"]
        logging.info('Freeform tag "ExtirpateAttempted" present with value "{}". Compartment will NOT be deleted'.format(exAttempt))
        logging.debug("If you want it to be deleted simply remove that Freeform Tag")
        return False
    else:
        logging.debug("No freeform tag 'ExtirpateAttempted'")

    # because we don't have access to config or the class instance here I had to resort to a global variable.
    # I do not like it, but I don't have a better answer
    for c in compartment_data:
        if c.compartment_id == compartment.id and c.lifecycle_state == "ACTIVE":
            logging.info("Compartment has ACTIVE child compartments. Skipping.")
            return False
    
    logging.debug("All pre-checks complete. Compartment should be deleted.")
    return True


class compartments( OCIClient ):
    service_name = "Compartments"
    isRegional = False
    clientClass = oci.identity.IdentityClient
    compositeClientClass = oci.identity.IdentityClientCompositeOperations

    logging.info("***********************************************************************************")
    logging.info("****************                 NOTE:                 ****************************")
    logging.info("***********************************************************************************")
    logging.info("*** Only {} compartments will be deleted. Please see documentation for more info ***".format( maxCompartmentsToDelete))
    logging.info("***********************************************************************************")

    # maxCompartmentsToDelete = 2
    # numDeletedCompartments = 0

    objects = [
        {
            "name_singular"      : "Compartment",
            "name_plural"        : "Compartments",

            # I HATE HATE HATE that I have to pass "compartments" in. I feel so dirty. But I don't have a better way yet
            "check2delete"       : lambda compartment: checkIt(compartment),

            "function_list"      : "list_compartments",
            "kwargs_list"        : {
                                        "lifecycle_state" : "ACTIVE"
                                   },
            "formatter"          : lambda compartment: "Compartment with OCID {} / name '{}' is in state {}".format(compartment.id, compartment.name, compartment.lifecycle_state),
            "function_delete"    : "delete_compartment",
        },

    ]

    def __init__(self, config):
        super().__init__(config)

        global compartment_data 
        compartment_data = self.config.compartment_data

    def predelete(self, object, region, found_object):
        # this is wasteful - I could do this one time up above and save importing time and calculating today for every
        # compartment I'm about to delete. But in the grand scheme of things this is nothing compared to some of the
        # other stuff I'm doing wastefully. So &shrug;
        global numDeletedCompartments
        import time
        t = time.gmtime()
        today = "{}-{:02}-{:02}".format(t.tm_year, t.tm_mon, t.tm_mday)

        # we **SHOULD** re-read the compartment here in case it got changed. But since I'm deleting it anyway I'm not
        # going to bother with that.
        # I'm also not really bothering to make sure the update worked. Again, &shrug;

        logging.debug("Adding ExtirpateAttempted to tags")
        found_object.freeform_tags["ExtirpateAttempted"] = today

        logging.debug("Writing back and waiting")
        self.compositeClients[self.config.home_region].update_compartment_and_wait_for_state(
            found_object.id,
            found_object,
            ["ACTIVE"]
        )
        logging.debug("Done.")

        # TODO: check to see if this is actually needed. I don't think so
        logging.debug("Waiting for 2 seconds just to make sure the write finishes")
        import time
        time.sleep( 2 )

        # note that we're incrementing here before deleting. That's because this is about as close to the deletion as
        # I have a hook to do this
        # self.numDeletedCompartments += 1
        numDeletedCompartments += 1
        return

    def findAllInCompartment(self, region, o, this_compartment, **kwargs):
        if numDeletedCompartments >= maxCompartmentsToDelete:
            logging.info(
                "Maximum number of compartments to delete has been reached. Skipping this and all subsequent compartments during this run.")
            return None
        
        # no need to make this api call - self.config has all the data we need
        c=super().findAllInCompartment(region, o, this_compartment, **kwargs)

        # make an array to hold the return
        r = []
        
        # go through the saved compartments...
        for c in self.config.compartment_data:
            if c.compartment_id == this_compartment:
                r.append(c)

        logging.debug("Found {} compartments in compartment {}".format(len(r), this_compartment))
        return r

