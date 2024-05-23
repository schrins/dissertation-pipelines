# Scripts for experiments with WhatsHap polyphase genetic

These scripts and pipelines have been used to create the results for Chapter 4.

Exported conda environments:

`env-polyphase-genetic.yml` - Full package list of used environment

`env-polyphase-genetic-history.yml` - Prompted package list of used environment

## Data availability

All files marked with either `(zenodo)`, `(public)` or `(ncbi)`, depending on whether the required data was uploaded on Zenodo, is publicly available or available via an NCBI project. All VCF files have been created from the linked sequencing data. For easier reproduction of the algorithmic results, we provide all processed VCF files via Zenodo (except those for the whole-chromosome results as they are too large).

Link to parental sequencing data: https://www.ncbi.nlm.nih.gov/bioproject/PRJNA718240/

Link to progeny sequencing data: https://www.ncbi.nlm.nih.gov/bioproject/PRJEB48582/

Link to reference genome: https://www.plantbreeding.wur.nl/Solyntus/

## Recreating ground truth region

Requires:
1. .gfa file containing the HiFi assemblies (zenodo)
2. Solyntus reference genome (public)
3. regions of parental VCF files (zenodo)

Run the snakemake pipeline `Snakefile-ASM`.

## Recreating the phasing results

Requires:
1. regions of parental VCF files (zenodo)
2. regions of progeny VCF files (zenodo)
3. ped files, specifying the pedigree relationships (zenodo)
4. regions of downsampled parental VCF files (zenodo)

Run the snakemake pipeline `Snakefile-Genetic`.

## Recreating the whole-chromosome results

Requires:
1. parental VCF files (ncbi)
2. progeny VCF files (ncbi)
3. ped file, specifying the pedigree relationships (zenodo)

Run the snakemake pipeline `Snakefile-Whole`.

