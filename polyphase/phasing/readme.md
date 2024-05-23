# Scripts for experiments with WhatsHap polyphase

These scripts and pipelines have been used to create the results for Chapter 3.

## Used data

The polyploid human data is generated in a separate step (see other `data-generation`-subfolder of `polyphse`).
The procedure for the simulated S. tuberosum data was created by Shaw and Yu (https://doi.org/10.1089/cmb.2021.0436). We provide the generated PacBio reads for ploidies 3 to 6 and the corresponding VCF files on Zenodo.
The HiFi data for the Altus cultivar is also provided on Zenodo. In the `polyphase-genetic` folder, more details are given where this data stems from and how it can be retrieved. We only tested some small selected regions as benchmark.

## Running the pipeline

All phasing results can be created by running the provided snakemake pipeline. Since HPoP creates temporary files with hardcoded names, it cannot be run in parallel. (TODO: use shadow rules for this in the future)

`snakemake all --snakefile Snakemake-evaluation --cores 64 --resources hpop=1 --use-conda`

For the runtime benchmarks, there is a reduced set of configurations that should only be run with a small number of cores to minimize their competition for shared resources. We used two cores on a 64-core machine for this purpose:

`snakemake benchmark --snakefile Snakemake-evaluation --cores 2 --resources hpop=1 --use-conda`

Please note that this pipeline requires conda to run properly because it contains two different versions of WhatsHap, for which separate environments are needed.
