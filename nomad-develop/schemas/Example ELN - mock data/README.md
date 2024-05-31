# NOMAD Example Schema
This folder contains an example schema to test functionalities of schema definition. This is the NOMAD-lab tutorial schema with additional definitions, quantities, base_sections and sub_sections.  

## Schema definition
### Sections:
- Chemical
- Sample
- Process
- Instrument


### Quantities:
- Sample
    Name, tags, chemicals, substrate_type, substrate_thickness, and sample_is_from_collaboration.
- Chemical 
    form, cas_numbr and ec_number.
- Process I
    Instrument quantity referencing the Instrument section.
- pvd_evaporation, hotplate_annealing, and plate_reader_setup define specific quantities relevant to those processes.


### Base Sections:
- Chemical inherits from nomad.datamodel.metainfo.eln.Chemical and nomad.datamodel.data.EntryData.
- Instrument inherits from nomad.datamodel.metainfo.eln.Instrument and nomad.datamodel.data.EntryData.
- Process inherits from nomad.datamodel.metainfo.eln.Process.
- Sample inherits from nomad.datamodel.metainfo.eln.Sample and nomad.datamodel.data.EntryData.
- pvd_evaporation, hotplate_annealing, and plate_reader_setup inherit from Process.



### Subsections:
- Sample contains the subsection processes.
- Processes contains the subsections pvd_evaporation, hotplate_annealing, and plate_reader_setup.


### UML
To visualize the relations between different sections, a UML diagram is created. 
![UML](https://git.fhict.nl/coe-htsm/nomad-oasis/-/raw/main/nomad-develop/schemas/Example%20ELN%20-%20mock%20data/UML.png)


Consult the [documentation on the NOMAD Archive and Metainfo](https://nomad-lab.eu/prod/v1/docs/archive.html) to learn more about schemas.
