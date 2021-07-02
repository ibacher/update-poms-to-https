update-poms-to-https
====================

This repos is some relatively straight-forward scripts that we used to upgrade OpenMRS Maven projects to use https in the URL for repositories instead of http. This change is necessary because Maven 3.8.1 requires repositories to use https by default.

This project uses [poetry](https://python-poetry.org/) to provide a reproducible build environment.

The scripts should be run in this order:

1. `poetry run python checkout_repos.py`
2. `poetry run python update_poms.py`
3. `poetry run python commit_updated_poms.py`

Checkout Repos
==============

This script tries to find all repositories in the "openmrs" GitHub organisation that have a "pom.xml" file and creates a shallow clone of them locally. This script takes one optional argument, namely a GitHub Personal Access Token with access to read repositories on your behalf. Because of the number of repositories in the openmrs organisation and the limits GitHub puts on anonymous API access, this token is basically required to actually run the script.

Update POMs
===========

This script finds all repository URLs in a POM.xml file and changes any http links to https. At the same time, it also updates any references to `mavenrepo.openmrs.org` to use the shortened URL without mention of Nexus instead of the longer URL. This latter change is purely cosmetic. Because the POM file is actually parsed using the Python [ElementTree library](https://docs.python.org/3/library/xml.etree.elementtree.html), the outputted POM will not always be identical to the input POM. In particular, this updating process will add the `<?xml version="1.0" encoding="UTF-8"?>` header and remove any comments that occur before the header (all other comments should be preserved).

Commit Updated POMs
===================

This last script scans through the local clones of the OMRS repos for those that have a modified POM, commit the modifications with an explanatory message and pushes the changes to upstream.
