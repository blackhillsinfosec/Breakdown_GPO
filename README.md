# breakdown_gpo

#### Version 2.0.w
`
During Active Directory Reviews, it is beneficial to review all of the GPOs.
On a domain controller, the command `Get-GPOReport -All -Domain "domain.com" -Server "ACME-DC1" -ReportType HTML -Path "C:\GPOReport.html"` will export all of the GPOs for `domain.com`. However, it will combine all of the HTML reports into a single file; having several HTML files inside a single file causes problems and cannot be read easily with a browser. This tool breaks down the large file into a collection of individual HTML files that can be opened in a browser.

By default, this script will create an output directory ("gpo_out") in the current working directory.
The script will ask if the output directory needs to be a different name; leave blank for default.

A summary of the broken down GPOs will be created inside the new output directory called "gpo_summary.txt".
GPOs will be organized according to their status: "effective", "computer", "user", "disabled", or "ineffective".
GPOs are considered "ineffective" if they have a security filter of "none".

GPOs that are effective ("effective", "computer", "user") will be prepended with a number to preserve the order they are listed in the original GPOReport.
Using this ordering, it should be possible to calculate winning GPOs.

#### Pre-Reqs
`python3 -m pip install colorama`

#### Version Notes
##### 2.0.0
###### Major Refactor
Separated major code aspects into modules.

###### Distinguish each GPO by status
Determine if the GPO is "Enabled", "Disabled", "Computer", "User", or "Ineffective".

##### 2.0.1
###### UTF-16-LE File Encoding Broke HTML
Converted outputted file encoding to UTF-8, which does not break HTML rendering.

##### 2.0.2
###### Enabled Improvements
The logic originally associated with the Enabled logic was too specific to allow for different GPO versions.
New logic for "fuzzy" comparison.

#### Syntax

###### Specify the GPOReport location on the command_line
`./breakdown_gpo.py ./GPOReport.html`

###### Specify the GPOReport location after execution
`./breakdown_gpo.py`