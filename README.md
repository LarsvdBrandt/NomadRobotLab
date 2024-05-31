# NOMAD Oasis Customization Repository 

This repository serves as a central hub for all the code changes and custom components, made to the NOMAD Oasis framework to tailor it perfectly for the RobotLab project. 
By combining these customized elements, we've created a data management environment specifically designed for RobotLab project. Feel free to explore the code to understand the modifications.

This repository is structured to keep everything organized and easy to understand.

## docker-compose:
This folder contains instructions for building and running your entire RobotLab environment in a single step. The Docker Compose setup allows you to effortlessly spin up all the necessary containers with just a single command. No more juggling configurations or worrying about dependencies.

## nomad-develop/nomad-source:
This folder holds all the modifications, made to the core NOMAD code. Here's where you'll find the specific changes that make NOMAD meet data access requirements for the RobotLab project. 

## nomad-develop/schemas:
Data needs structure, and schemas provide that structure. This folder contains custom schemas, created for the RobotLab project. These schemas define the format and organization of the data received from the experiments, ensuring that NOMAD can process it accurately and efficiently.


## nomad-develop/scripts:
Scripts created as proof of concept to handle data access. This script runs as a separate service. It communicates met the NOMAD API, and adds meta data to uploads. This method is not secure, as users can communicate with the API directly and avoid communication with the script overall, this would skip the access check.
This scrips was created as proof of concept, but is now added to the NOMAD-source code.

