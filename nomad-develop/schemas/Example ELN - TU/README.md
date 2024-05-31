# Fluorescence measurement Schema
This folder contains the fluorescence measurement schema definition. 

# #Schema definition
Sections:
•	Experiment
•	Chemical
•	Sample
•	Process
•	Instrument

### Quantities:
- Experiment
    Name, Experiment Description, Experiment Visual and Sample
- Sample
    Name, tags and chemicals.
- Chemical
    Form and fluorescence.
- Process 
    Instrument quantity referencing the Instrument section.
- Pipetting 
    Size_of_pippet, number_of_wells, heated_to_temperature, time_shaken
- Fluorescence_measurement
    Plotted quantities 


### Base Sections:
- Experiment inherits from nomad.datamodel.data.EntryData.
- Chemical inherits from nomad.datamodel.metainfo.eln.Chemical and nomad.datamodel.data.EntryData.
- Instrument inherits from nomad.datamodel.metainfo.eln.Instrument and nomad.datamodel.data.EntryData.
- Process inherits from nomad.datamodel.metainfo.eln.Process.
- Sample inherits from nomad.datamodel.metainfo.eln.Sample and nomad.datamodel.data.EntryData.
- Pipetting and fluorescence_measurement inherit from Process.


### Subsections:
- Sample contains the subsection processes.
- Processes contains the subsections pipetting and fluorescence measurement

### UML
To visualize the relations between different sections, a UML diagram is created. The diagram clearly illustrates the hierarchical structure of the sections Experiment, Chemical, Instrument, Process, and Sample, along with their associated properties (quantities) and inheritance (base sections). 
The Sample section contains a processes subsection, which further breaks down into detailed process sections Fluorescence_measurement and pipetting. Both these processes contain the sub-section process, referring to the defined process with its reference to the instrument. 
Each of these sections and subsections is defined with their relevant quantities, types, and their corresponding annotations, showcasing a well-organized and comprehensive schema design. This visual aid helps to better understand the complex relationships and data flow within the schema.
![UML](https://git.fhict.nl/coe-htsm/nomad-oasis/-/raw/main/nomad-develop/schemas/Example%20ELN%20-%20TU/UML.png)


