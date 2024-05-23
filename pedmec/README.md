# Experimental setup for testing the PedMEC heuristic

Here, we describe the performed steps to setup and execute the experiments for Chapter 2.

Exported conda environments:

`env-pedmec-genetic.yml` - Full package list of used environment

`env-pedmec-genetic-history.yml` - Prompted package list of used environment

## Creating a ground truth phasing

The ground truth phasing is based on a high-quality assembly, available on the following repo: https://github.com/marbl/HG002

In particular, we used the v1.0.1 assembly from October 2023: https://s3-us-west-2.amazonaws.com/human-pangenomics/T2T/HG002/assemblies/hg002v1.0.1.fasta.gz

Next step is to use the tool PAV, available on the following repo: https://github.com/EichlerLab/pav

We followed the given instruction of the tool to create a phased VCF file from the two ground-truth assemblies and the GRCh38 reference genomes from GIAB: https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/release/references/GRCh38/GCA_000001405.15_GRCh38_no_alt_analysis_set.fasta.gz

In the following, we call the phased VCF file `pav_hg002.vcf`.

## Preparing input files for the phasing

For consistent sample naming, we first renamed the VCF files from GIAB that contain variant calls for the two parents HG003 and HG004:

```
bcftools reheader HG003_GRCh38_1_22_v4.2.1_all.vcf.gz -s reheader_HG003.txt > HG003_GRCh38_1_22_v4.2.1_all_reheader.vcf.gz
bcftools reheader HG004_GRCh38_1_22_v4.2.1_all.vcf.gz -s reheader_HG004.txt > HG004_GRCh38_1_22_v4.2.1_all_reheader.vcf.gz
```

The re-header files are uploaded to this repository, while the VCFs can be downloaded via the following links:

`https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/release/AshkenazimTrio/HG003_NA24149_father/NISTv4.2.1/GRCh38/SupplementaryFiles/HG003_GRCh38_1_22_v4.2.1_all.vcf.gz`
`https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/release/AshkenazimTrio/HG004_NA24143_mother/NISTv4.2.1/GRCh38/SupplementaryFiles/HG004_GRCh38_1_22_v4.2.1_all.vcf.gz`

We merge all three VCFs:

`bcftools merge pav_hg002.vcf.gz HG003_GRCh38_1_22_v4.2.1_all_reheader.vcf.gz HG004_GRCh38_1_22_v4.2.1_all_reheader.vcf.gz > pav_hg002_hg003_hg004.vcf`

We unphase the merged VCF and re-genotype all three samples for chromosome 1 using WhatsHap v2.2. The genotyping makes use of pedigree information so that we also needed to re-genotype HG002.

```
whatshap unphase vcf/pav_hg002_hg003_hg004.vcf > vcf/pav_hg002_hg003_hg004_unphased.vcf
whatshap genotype vcf/pav_hg002_hg003_hg004_unphased.vcf bam/HG002_PacBio_GRCh38.bam bam/HG003_PacBio_GRCh38.bam bam/HG004_PacBio_GRCh38.bam -r fa/GCA_000001405.15_GRCh38_no_alt_analysis_set.fasta.gz -o vcf/pav_hg002_hg003_hg004_genotyped.vcf --ped trio.ped --sample HG002 --sample HG003 --sample HG004 --chromosome chr1
```

Finally, we replace the newly genotyped HG002 with the ground truth phasing again because this data should be more reliable:

```
bcftools view pav_hg002_hg003_hg004_genotyped.vcf -s HG003,HG004 > pav_hg002_hg003_hg004_genotyped_withoutHG002.vcf
bgzip < pav_hg002_hg003_hg004_genotyped_withoutHG002.vcf > pav_hg002_hg003_hg004_genotyped_withoutHG002.vcf.gz
bcftools index pav_hg002_hg003_hg004_genotyped_withoutHG002.vcf.gz
bcftools merge pav_hg002.vcf.gz pav_hg002_hg003_hg004_genotyped_withoutHG002.vcf.gz > pav_remerged.vcf
bcftools view pav_remerged.vcf -r chr1 > pav_remerged.chr1.vcf
```

The resulting file `pav_remerged.chr1.vcf` is finally used for the phasing experiments. We also uploaded this file to Zenodo to allow for a reproduction of the phasing results in case any of the data sources above breaks in the future.

## Sequencing data

The PacBio reads for the trio are available here:

https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/AshkenazimTrio/HG002_NA24385_son/PacBio_MtSinai_NIST/PacBio_minimap2_bam/HG002_PacBio_GRCh38.bam

https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/AshkenazimTrio/HG003_NA24149_father/PacBio_MtSinai_NIST/PacBio_minimap2_bam/HG003_PacBio_GRCh38.bam

https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/AshkenazimTrio/HG004_NA24143_mother/PacBio_MtSinai_NIST/PacBio_minimap2_bam/HG004_PacBio_GRCh38.bam

The HiFi reads for the trio are available here:

https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/AshkenazimTrio/HG002_NA24385_son/PacBio_CCS_15kb_20kb_chemistry2/GRCh38/HG002.SequelII.merged_15kb_20kb.pbmm2.GRCh38.haplotag.10x.bam

https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/AshkenazimTrio/HG003_NA24149_father/PacBio_CCS_15kb_20kb_chemistry2/GRCh38/HG003.SequelII.merged_15kb_20kb.pbmm2.GRCh38.haplotag.10x.bam

https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/AshkenazimTrio/HG004_NA24143_mother/PacBio_CCS_15kb_20kb_chemistry2/GRCh38/HG004.SequelII.merged_15kb_20kb.pbmm2.GRCh38.haplotag.10x.bam

## Testing PedMEC heuristic

We summarized all tests in the snakemake pipeline `Snakefile-Pedmec`. Plase adjust the directories in `config.json` to match your file system. The metrics can be found in the `.csv` or `.tsv` files in the `results-thesis-Apr24` directories. It also contains command line logs for the individual WhatsHap calls, from which we extracted the runtime and peak memory consumption.

## Misc

We manually examined the `pav_hg002.vcf` file by removing many fields that are not relevant for phasing. This is not part of the experiments but just reported here in case anyone wants to do this again:

```
rtg vcfsubset -i pav_hg002.vcf -o PureHG002.vcf --remove-info ID --remove-info SVTYPE --remove-info TIG_REGION --remove-format GL --remove-format GQ --remove-info SVLEN --remove-info HOM_REF --remove-info HOM_TIG --remove-ids --remove-info platforms --remove-info platformnames --remove-info dataset --remove-info datasets --remove-info datasetnames --remove-info datasetsnames --remove-info callsets --remove-info callsetnames --remove-info datasetmissingcall --remove-info callable --remove-info filt --remove-info difficultregion --remove-format DP --remove-format ADALL --remove-format AD
```
