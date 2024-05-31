# NOMAD Oasis Customization Repository 

## nomad-source:
This folder holds all the modifications, made to the core NOMAD code. Here's where you'll find the specific changes that make NOMAD meet data access requirements for the RobotLab project. 

## schemas:
Data needs structure, and schemas provide that structure. This folder contains custom schemas, created for the RobotLab project. These schemas define the format and organization of the data received from the experiments, ensuring that NOMAD can process it accurately and efficiently.

## scripts:
Scripts created as proof of concept to handle data access. This script runs as a separate service. It communicates met the NOMAD API, and adds meta data to uploads. This method is not secure, as users can communicate with the API directly and avoid communication with the script overall, this would skip the access check. 
This scrips was created as proof of concept, but is now added to the NOMAD-source code. 

