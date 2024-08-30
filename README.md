# quick_sand
The purpose of this tool is to generate significant noise within an endpoint detection and response (EDR) solution, potentially overwhelming its monitoring capabilities.

This tool is primarily intended for educational and testing purposes, to demonstrate how API hammering techniques can be used to evade or bypass EDR detection in controlled environments like sandboxes or isolated virtual machines (VMs).

Prerequisites

Python 3.x is required to run this tool.
This tool is intended for use on Windows systems, as it utilizes Windows-specific APIs.

Dependencies

The following libraries are required to run the tool:

types: Included with Python by default. It provides C compatible data types and allows calling functions in DLLs or shared libraries.

No external packages need to be installed for this tool.

Run the tool using Python:

            python quick_sand.py

Once the tool starts, it will begin generating noise by making various Windows API calls in multiple threads. It will continue running until manually stopped.
