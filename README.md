# Breakdown GPO

#### Version 3.0.0

During Active Directory Reviews, it is beneficial to review all of the GPOs.
On a domain controller, the command `Get-GPOReport -All -Domain "domain.com" -Server "ACME-DC1" -ReportType HTML -Path "C:\GPOReport.html"` will export all of the GPOs for `domain.com`. All the individual HTML reports will be combined into a single file; having several HTML files inside a single file causes problems, and cannot be read easily, with a browser. Breakdown GPO separates the individual GPOs into individual HTML files that can be opened in a browser.

A summary of the broken down GPOs will be created.

GPOs will be organized according to their status:
- "Enabled" indicates that both computer and user settings are enabled.
- "Computer" indicates that user settings are disabled and computer settings are enabled.
- "User" indicates that computer settings are disabled and user settings are enabled.
- "Disabled" incicates that computer and user settings are enabled.
- GPOs are "ineffective" if they have a security filter of "None" and are enabled ("enabled", "computer", or "user").

GPOs are prepended with a number to preserve the order they are listed in the original GPOReport.
Using this ordering, it should be possible to calculate winning GPOs.

#### Version Notes
##### 3.0.0
###### Major Refactor
The entire project was rewritten to implement Generators and Comprehensions.
The introduction of these elements:
- simplies the code
- reduces memory consumption - although this is likely negligible for most GPOReports
- eliminates threading 
In initial tests, this had no major impact to performance.

#### Usage

Breakdown GPO

        Usage: python3 .\breakdown_gpo.py -i <input> -o <output>

        Options:

        --input, -i, --in               Define the GPOReport to be broken down.
        --output, -o, --out             Define the output directory.
        --default_output, -do, --do     Use the current working directory as the output directory.
        --help, -h                      Print this help menu.