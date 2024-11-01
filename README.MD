# README for ociextirpate

extirpate
: ex·tir·pate
: to completely erase or eradicate

## What it is and does

The OCI Extirpater is a command line tool that deletes everything within a compartment in every subscribed OCI region.

## How it does it

The tool uses the OCI SDK to

1. find every compartment underneath the specified root
2. find every object within that compartment
3. delete the object

The code for each object type is actually quite small (see ociclients/template.py).

In short that code declares:

* the class in the OCI SDK to be used
* (optionally) the "composite class" to be used
* the name (both singular and plural) for human-readable logging
* the method in the class used to list and delete the object
* (optionally) specific formatters to generate a "one-liner" for the object

A class may also override some of the stuff in OCIClient.py in cases where the client class works differently than
typical.

## Quick Start

**NOTE:** OCIExtirpate supports a number of command line options including allowing you to limit
the resource types and regions it explores and cleans.
Running ociextirpate.py without any command line options will show you command line help.

### Running from your laptop

1. Set up the OCI CLI following the [instructions in the public documentation](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm)
1. copy the code to your machine
   * if you have registered your ssh key in GitHub:
     * run "git clone ssh://github.com/therealcmj/ociextirpater.git"
   * if you have **NOT** registered you ssh key in GitHub:
       * run `git clone https://github.com/therealcmj/ociextirpater.git`
1. cd into "ociextirpater"
1. run "./ociextirpate.py -c ocid1.compartment.oc1..XXXX"
   * replacing ocid1.compartment.oc1..XXXX with the compartment you want to clean

### Running in Cloud Shell

Since iterating over all child compartments, regions, and resources types is a slow process **and** Cloud Shell has
a relatively short timeout before disconnecting it is generally preferable to run extirpater from your laptop or
from a compute instance.

But if you **want** to run it from Cloud Shell that is supported:

1. open Cloud Shell
1. run `git clone https://github.com/therealcmj/ociextirpater.git`
   * You need to use https rather than ssh since you likely won't have an ssh key for your Cloud Shell registered in GitHub
1. cd into "ociextirpater"
1. run "./ociextirpate.py -c ocid1.compartment.oc1..XXXX -dt"
   * replacing ocid1.compartment.oc1..XXXX with the compartment you want to clean

### Running as a Function

1. Set up a development environment based on the [Functions documentation](https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionsquickstartguidestop.htm).
1. On Function Application *APP_NAME* or the underlying *ociextirpater* function, enter the following *Configurations*

   * **EXTFN_COMPARTMENT** for the compartment to extirpate
   * (optional) **EXTIRPATER_PREFIX** if you want to use a different prefix than the default of **EXTFN**
   * (optional) **EXTFN_REGIONS** a comma seperated list, for region(s) to extirpate *(default all subscribed regions)*
   * (optional) **EXTFN_OBJECTS** for objects to extirpate
   * (optional) **EXTFN_FORCE** to force deletion
   * (optional) **EXTFN_DEBUG** to activate debug mode
   * (optional) **EXTFN_SKIP_DELETE_COMPARTMENT** to skip deleting compartments

1. Run `fn deploy --app {APP_NAME}`
1. Run `fn invoke {APP_NAME} ociextirpater`

Use [Resources Scheduler](https://docs.oracle.com/en-us/iaas/Content/resource-scheduler/home.htm), [OCI Events](https://docs.oracle.com/en-us/iaas/Content/Events/home.htm), or another method to automate invokation.

## More info

Check out my blog post at
<https://www.ateam-oracle.com/post/cleanup-an-oci-compartment>

## Inspiration

This was inspired by Richard Garsthagen's work on [OCI Super Delete](https://github.com/AnykeyNL/OCI-SuperDelete). In
fact, I even stole (most of) the command line arguments from his script. Making this *almost* a drop in replacement.

I wanted to try my hand at something similar but that was less "code" and more "declarative". Mostly because I thought
it would be nice to be able to add new object types to be deleted by simply declaring them rather than needing to write
a bunch of code.

In the end I'm not sure my approach was better or worse (OCIClient.py is practically unreadable) but it was a good
learning experience!

## What's next

* adding more objects
* trying to use the [Search service](https://docs.oracle.com/en-us/iaas/Content/Search/home.htm) instead of iterating over every object type
