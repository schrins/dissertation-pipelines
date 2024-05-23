# Pipelines and instructions for experiments in dissertation

This repository contains a collection of workflow pipelines, which I used to create the experimental results for my dissertation. Although I created a DOI for the state of submission, this repository might be updated afterwards to fix discovered bugs, simplify usage and add things I initially forgot.

## Structure

The repository is divided into three subfolders, each of which correspond to one algorithm being evaluated in my dissertation. All subfolders mainly consist of snakemake pipelines that summarize all performed steps.

## Data

Each subfolder uses different datasets from varying sources. The readme file in each subfolder should provide information on where to find the data. Some of the required files are uploaded on Zenodo under the DOI '10.5281/zenodo.11264527'. All reference to Zenodo in the other readme files refer to this Zenodo upload.

It does not contain all data, as the used sequencing data would be too large. However, it contains many intermediate files that I or my collaborators created while we worked on the different projects. These intermediate files are, in principle, reconstructible from publicly available data but I uploaded them separately for two reasons: (i) It simplifies the reproduction of algorithmic results because the data generation steps requires some effort and might yield different results in the future due to different tools or tool versions. (ii) The original data sources might become unavailable.

## Software

The main software of this dissertation is WhatsHap (https://github.com/whatshap/whatshap). I used it in different versions for each of the experiments:
1. For the PedMEC heuristic, I used a custom version (see below) that is uploaded as an archive on Zenodo as well
2. For WhatsHap Polyphase, I used release 2.2 for the new algorithm and release 1.0 the old algorithm. Using cluster refinement on the new algorithm requires the custom version.
3. For Whatshap Polyphase Genetic, I use the custom version again.

The custom version refers to following commit: https://github.com/whatshap/whatshap/commit/77133e665616346f66606c6dbdae407c97af6c29

The commit is branched off version 2.2, with version 2.3 rebased in. The changes will likely be merged back with the release of 2.4, except for the cluster refinement; this feature was removed with the transition to version 2.0 and only re-inserted for experimental use. There is not intention to permanently add in again.