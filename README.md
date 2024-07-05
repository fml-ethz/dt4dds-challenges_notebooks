# 🧬🏆 dt4dds-challenges_notebooks

- [Overview](#overview)
- [Software Requirements](#software-requirements)
- [Installation Guide](#installation-guide)
- [Data Sources](#data-sources)
- [Codec Sources](#codec-sources)

# Overview
This repository contains the data analysis, in the form of Jupyter Notebooks and data files, for the error characterization and figures in the following publication:

> Gimpel, A.L., Stark, W.J., Heckel, R., Grass R.N. Challenges for error-correction coding in DNA data storage: photolithographic synthesis and DNA decay. bioRxiv 2024.07.04.602085 (2024). https://doi.org/10.1101/2024.07.04.602085

The program `dt4dds-challenges`, providing a digital benchmark for current challenges in DNA data storage, is found in the [dt4dds-challenges repository](https://github.com/fml-ethz/dt4dds-challenges).

# Software requirements
The data analysis has been tested and performed on Windows 10 using Python 3.12. The following Python packages are required: 
```
dt4dds
pandas
numpy
statsmodels
plotly
scipy
```

Moreover, the error-correction codes used for the benchmarking in `50_Simulation`, need to be installed from their respective sources. For this, installation scripts are provided in [`./50_Simulation/simulator/codecs`](/50_Simulation/simulator/codecs/). See also the Section on [Codec Sources](#codec-sources).


# Installation guide
To clone this repository from Github, use
```bash
git clone https://github.com/fml-ethz/dt4dds-challenges_notebooks
cd dt4dds-challenges_notebooks
```


# Data sources
Some of the analysis in this repository is based on sequencing data from other publications. Download and processing scripts are provided in the respective folders to download and post-process the sequencing data as required by the analysis scripts. This is only required if re-running the full pipeline starting from the sequencing data is desired. The intermediate files for data analysis are already provided with this repository.


## /data_experimental/Aging_Meiser
> Meiser, L.C., Gimpel, A.L., Deshpande, T. et al. Information decay and enzymatic information recovery for DNA data storage. Commun Biol 5, 1117 (2022). https://doi.org/10.1038/s42003-022-04062-9

The data is publicly available in this [figshare repository](https://figshare.com/articles/dataset/Sequencing_data/21070684).


## /data_experimental/Aging_Song
> Song, L., Geng, F., Gong, ZY. et al. Robust data storage in DNA by de Bruijn graph-based de novo strand assembly. Nat Commun 13, 5361 (2022). https://doi.org/10.1038/s41467-022-33046-w

The data is publicly available in the figshare repositories [1](https://figshare.com/articles/online_resource/Error-prone_PCR_1st_round/16727122/2), [2](https://figshare.com/articles/online_resource/Error-prone_PCR_3st_and_4st_rounds/17193128/1), and [3](https://figshare.com/articles/online_resource/Error-prone_PCR_5st_and_6st_rounds/18515045/1).


## /data_experimental/Photolithographic_Antkowiak
> Antkowiak, P.L., Lietard, J., Darestani, M.Z. et al. Low cost DNA data storage using photolithographic synthesis and advanced information reconstruction and error correction. Nat Commun 11, 5345 (2020). https://doi.org/10.1038/s41467-020-19148-3

The data is publicly available in this [figshare repository](https://figshare.com/collections/Low_Cost_DNA_Data_Storage_Using_Photolithographic_Synthesis_and_Advanced_Information_Reconstruction_and_Error_Correction/5128901/1). The data for File 3 was requested from the authors.


## /data_experimental/Photolithographic_Lietard
> Jory Lietard, Adrien Leger, Yaniv Erlich, Norah Sadowski, Winston Timp, Mark M Somoza, Chemical and photochemical error rates in light-directed synthesis of complex DNA libraries, Nucleic Acids Research, Volume 49, Issue 12, 9 July 2021, Pages 6687–6701, https://doi.org/10.1093/nar/gkab505

The data is publicly available in the European Nucleotides Archive (ENA) under project number [PRJEB43002](https://www.ebi.ac.uk/ena/browser/view/PRJEB43002). The data for the high-density synthesis was requested from the authors.


## /30_Photolithographic/run36.npy
> Chen, YJ., Takahashi, C.N., Organick, L. et al. Quantifying molecular bias in DNA data storage. Nat Commun 11, 3264 (2020). https://doi.org/10.1038/s41467-020-16958-3

The dataset `run36.npy` was used for the comparison of the pool homogeneity after synthesis. The data is publicly available in this [GitHub repository](https://github.com/uwmisl/storage-biasing-ncomms20).



# Codec sources
The error-correction codes tested in the benchmarking of the two challenges were developed by and re-used from other publications. Installation scripts are provided in the respective folders to perform installation as required by the analysis scripts. Installation is only required to re-run the decoding pipeline. The intermediate files for data analysis are already provided with this repository. 


## /50_Simulation/simulator/codecs/DBGPS
> Song, L., Geng, F., Gong, ZY. et al. Robust data storage in DNA by de Bruijn graph-based de novo strand assembly. Nat Commun 13, 5361 (2022). https://doi.org/10.1038/s41467-022-33046-w

The codec is publicly available in this [GitHub repository](https://github.com/Scilence2022/DBGPS_Python). The encoding and decoding scripts were slightly altered to support automation by the simulation pipeline.


## /50_Simulation/simulator/codecs/dna_rs_coding
> Antkowiak, P.L., Lietard, J., Darestani, M.Z. et al. Low cost DNA data storage using photolithographic synthesis and advanced information reconstruction and error correction. Nat Commun 11, 5345 (2020). https://doi.org/10.1038/s41467-020-19148-3

The codec is publicly available in these GitHub repositories: [reinhardh/dna_rs_coding](https://github.com/reinhardh/dna_rs_coding) and [MLI-lab/noisy_dna_data_storage](https://github.com/MLI-lab/noisy_dna_data_storage). A fork with a parallelized decoding step was created and used to accelerate the benchmarking, see [this GitHub repository](https://github.com/agimpel/dna_rs_coding).


## /50_Simulation/simulator/codecs/dnafountain
> Yaniv Erlich, Dina Zielinski, DNA Fountain enables a robust and efficient storage architecture.Science 355, 950-954 (2017). DOI:10.1126/science.aaj2038

The codec is publicly available in this [GitHub repository](https://github.com/TeamErlich/dna-fountain). A fork porting the original code from Python 2 to Python 3 by Yihang Du, Wenrong Wu and Justin Brody (Franklin & Marshall College, PA, USA) was used, see [this GitHub repository](https://github.com/jdbrody/dna-fountain).