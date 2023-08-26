### Version 3.0.2

## Description

During Active Directory Reviews, it is beneficial to review all of the GPOs.
On a domain controller, the command `Get-GPOReport -All -Domain "domain.com" -Server "ACME-DC1" -ReportType HTML -Path "C:\GPOReport.html"` will export all of the GPOs for `domain.com`. All the individual HTML reports will be combined into a single file; having several HTML files inside a single file causes problems, and cannot be read easily, with a browser. Breakdown GPO separates the individual GPOs into individual HTML files that can be opened in a browser.

A summary of the broken down GPOs will be created.

GPOs will be organized according to their status:
- "Enabled" indicates that both computer and user settings are enabled.
- "Computer" indicates that user settings are disabled and computer settings are enabled.
- "User" indicates that computer settings are disabled and user settings are enabled.
- "Disabled" indicates that computer and user settings are enabled.
- GPOs are "ineffective" if they have a security filter of "None" and are enabled ("enabled", "computer", or "user").

GPOs are prepended with a number to preserve the order they are listed in the original GPOReport.
Using this ordering, it should be possible to calculate winning GPOs.

## Usage
```
Breakdown GPO

        Usage: python3 .\breakdown_gpo.py -i <input> -o <output>

        Options:

        --input, -i, --in               Define the GPOReport to be broken down.
        --output, -o, --out             Define the output directory.
        --default_output, -do, --do     Use the current working directory as the output directory.
        --help, -h                      Print this help menu.
```  
  
## Version Notes

### 3.0.2
#### Introduce Handles Class
Class to maintain file handles.  
Makes the code easier to read (kind of).  
Provides a count of each type of GPO detected.  
Cause why not?  

### 3.0.1
#### Introduce Indices Class
The Indices class packages all the attribute lists into a single object.
The Indices object tracks the number of attributes for each attribute list in the object using decorators.
Because the object tracks the attribute list size, instead of using `len()` before the object was implemented, performance improved.

### 3.0.0
#### Major Refactor
The entire project was rewritten to implement Generators and Comprehensions.
The introduction of these elements:
- Simplies the code
- Reduces memory consumption - although this is likely negligible for most GPOReports
- Eliminates threading - In initial tests, this had no major impact to performance.