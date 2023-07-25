# README for ociextirpate

extirpate
: ex·tir·pate
: to completely erase or eradicate

## What it is and does

The OCI Extirpater is a command line tool that deletes everything within a compartment in every OCI region.

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

## More info

Check out my blog post at 
https://www.ateam-oracle.com/post/cleanup-an-oci-compartment

## Inspiration

This was inspired by Richard Garsthagen's work on [OCI Super Delete](https://github.com/AnykeyNL/OCI-SuperDelete). In
fact, I even stole (most of) the command line arguments from his script. Making this almost a drop in replacement.

I wanted to try my hand at something similar but that was less "code" and more "declarative". Mostly because I thought
it would be nice to be able to add new object types to be deleted by simply declaring them rather than needing to write
a bunch of code.

In the end I'm not sure my approach was better or worse (OCIClient.py is practically unreadable) but it was a good
learning experience!

## What's next

* adding more objects
* trying to use the [Search service](https://docs.oracle.com/en-us/iaas/Content/Search/home.htm) instead of iterating over every object type
