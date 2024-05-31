# NOMAD Oasis research for the RobotLab

This folder contains the research to three requirements that are researched for the RobotLab. 
A requirement is researched and tested accordingly on NOMAD Oasis. 

## Data access
The RobotLab project involves multiple stakeholders with diverse data access needs, necessitating well-defined access policies. Stakeholder interviews and literature reviews identified key criteria for data access, including support for dynamic user roles, collaboration rights, ease of specification, efficient storage, and automation. Existing access control policies (DAC, MAC, RBAC) were evaluated but found lacking for the project's specific requirements. An enhanced access matrix model was proposed, offering improved administration and efficiency in access control, particularly suited for the collaborative environment of RobotLab. This model was implemented and tested using the NOMAD system, which confirmed the feasibility of enforcing these enhanced policies, although the current whitelist mechanism still falls short in meeting specific data access management needs.

## Traceability
Ensuring traceability of experimental data in the RobotLab project is crucial for reproducibility and data integrity. NOMAD’s schema system, based on UML, defines the structure of data entries, allowing detailed metadata capture and hierarchical relationships between sections. A use case involving fluorescence measurement was designed to test NOMAD’s traceability capabilities. The schema developed for this use case included detailed sections and subsections, ensuring consistent data representation and equipment traceability. The implementation demonstrated that NOMAD can effectively manage traceability, aligning with the FAIR principles, thereby enhancing data reproducibility and integrity.

## Various and Voluminous
The RobotLab project deals with a wide range of file formats and large volumes of experimental data. NOMAD’s data management system supports various data formats and ensures FAIR data principles through its bottom-up approach and use of parsers. The system’s upload capacity allows handling large data volumes, evidenced by the successful upload and management of extensive experimental data, such as videos from fluorescence measurements. 
