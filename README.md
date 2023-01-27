# breakdown_gpo
#### Version 1.2.1

During Active Directory Reviews, it is beneficial to review all of the GPOs.
On a domain controller, the command `Get-GPOReport -All -Domain "domain.com" -Server "ACME-DC1" -ReportType HTML -Path "C:\GPOReport.html"` will export all of the GPOs for `domain.com`. However, it will combine all of the HTML reports into a single file; having several HTML files inside a single file causes problems and cannot be read easily with a browser. This tool breaks down the large file into a collection of individual HTML files that can be opened in a browser.

By default, this script will create an output directory ("gpo_out") in the current working directory.
The script will ask if the output directory needs to be a different name; leave blank for default.

A summary of the broken down GPOs will be created inside the new output directory called "0_gpo_summary.txt".
GPOs that are not linked in the domain will be combined into a directory named "0_unlinked_gpos" inside the new output directory.

GPOs that are linked will be prepended with a number to preserve the order they are listed in the original GPOReport.
Using this ordering, it should be possible to calculate winning GPOs.

#### Version Notes
##### 1.2.0
###### Introduced threading to the read and parse process to make it faster.
Four threads are used for multi-threading. This setting is not changeable in this version.

###### Introduced ability to use nested directories as an output destination.

##### 1.2.1
###### Correct Encoding types for generated HTML files.
This is to fix encoding issues that may be created by special Unicode characters that do not belong in a normal file.

###### Add Exception strings to except blocks.
Generate better error output.

#### Syntax

###### Specify the GPOReport location on the command_line
`./breakdown_gpo.py ./GPOReport.html`

###### Specify the GPOReport location after execution
`./breakdown_gpo.py`