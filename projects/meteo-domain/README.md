# Domain


## Systems Overview

- MeteoStation : Measurements acquisition center 
- MeteoAgency: Exploits meteo predictions and visualizations

- DataStore: System designed to store measurements
- ModelStore: System designed to store prevision models

- PrevisionService: Provides meteo previsions
- VisualisationService: Provides meteo visualisations


## Glossary

- Measurement: Telemetry composed of a measure and an acquisition time
- Sensor: Metadata describing a source of measurements (at least a location and a name)
- DataFile: Batch of telemetries provided by a set of sensors (grid aligned)
