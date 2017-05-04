![alt text](https://github.com/ozarnowski/RNAseq/blob/master/RSePi_logo_final.png "RSePi")

# Overview

RNAseqPipeline is a command line tool that serves as a pipeline which processes RNA sequences via the use of various applications including quality control metrics.

## Software Requirements: 
+ Linux
+ Python 2.7.13
+ R

### All of the following programs must be installed and in your PATH:
+ Cutadapt 1.13
+ FastQC 0.11.5
+ STAR 2.5
+ Samtools 1.3.1
+ RSeQC 1.1.8
+ And all their dependencies.

## Scripts
+ accession_to_details.py
  + Runs cutadapt on a pair of files: trims first 13 bases.
  + Runs FastQC on the pair, and obtain summary consisting of PASS/WARN/FAIL values for different parameters for each fastq file.
  + This summary will be compiled into a table.
+ File_iterator.py
  + Compiles the summary data generated in accession_to_details.py.
+ details_parse.py
  + First uses File_iterator.py to trim sequences and to generate a summary table.
  + Makes a list of the input files that do not meet the quality threshold.
  + Run STAR, which aligns the fastq reads to a genome to generate BAM files.
  + Sort BAM files with Samtools.
  + Calculate FPKM values with RSeQC.
  + Obtains the following information from each file using RSeQC:
    + FPKM counts
    + RPKM saturation
    + Junction saturation
    + Read distribution
    + Infer experiment
    + Junction annotation

# Input data

## FastQ files

+ They must be paired end.
+ They must be in the following format: name_1.fastq.gz and name_2.fastq.gz to identify pairs (note: they should also be compressed using gzip).
+ All fastQ files must be in a single directory.

## Genome directory

### File structure (for troubleshooting purposes):
+ Genome name, contains:
  + annotation, contains:
    + .bed file
    + .gtf file
  + sequence, contains:
    + genomeName.all.fa
    + all .dna.chromosome.10.fa.gz files
  + star_indices (contents generated by STAR), contains:
    + chrLength.txt
    + chrName.txt
    + exonGeTrInfo.tab
    + geneInfo.tab
    + genomeParameters.txt
    + SAindex
    + sjdbList.fromGTF.out.tab
    + transcriptInfo.tab
    + chrNameLength.txt
    + chrStart.txt
    + exonInfo.tab
    + Genome
    + SA
    + sjdbInfo.txt
    + sjdbList.out.tab
  
  
### How to build [if NOT on Wheelerlab2]:

`mkdir -p genomeName/sequence`

`cd genomeName/sequence/`

`[download fasta files of genome into this directory. *]`

`gunzip -c Genus_species.genomeName.dna.chromosome.* > genomeName.all.fa`

`cd ../../`

`mkdir -p genomeName/annotation`

`cd genomeName/annotation/`

`[download corresponding versions of gtf and bed into this directory. * *]`

`cat filename.bed sed 's/^chr//' > filename.nochr.bed`

`rm filename.bed`

`cd ../../`

`mkdir -p GRCh38/star_indices`

`STAR --runThreadN 4 --runMode genomeGenerate --genomeDir genomeName/star_indices_overhang100/ --genomeFastaFiles GRCh38/sequence/genomeName.all.fa --sjdbGTFfile genomeName/annotation/filename.gtf --sjdbOverhang 100`

+ `*` fasta files can be found at ftp.ensembl.org/pub/release-88/fasta/ ; only download dna.chromosome.n.fa.gz files.
+ `* *` corresponding bed and gtf files can be found at genome.ucsc.edu/cgi-bin/hgTables?command=start

### How to build [if on Wheelerlab2 and you want to use the human genome build 38]:

Don't. It's already built at /home/azakkar/GRCh38 (can be used as input as path to genome directory. Check usage).

# Usage 

`python /path/to/details_parse.py -i path/to/FASTQ/directory/ -g /path/to/genomeDir`

+ Optional Input (-c)
  + add `-c True` to run geneBody_coverage.py (default = False)
  
### To run in background:

`nohup python /path/to/details_parse.py -i path/to/FASTQ/directory/ -g /path/to/genomeDir&`

+ A sample fastq folder with three paired fastq files is available at:
  + https://github.com/ozarnowski/RNAseq/tree/master/sample_files

+ The genome index can be constructed using STAR (Input Data), however, the path to a pipeline-ready index is as follows:
  + /home/azakkar/GRCh38/
  
## Output files

+ All output files contained in RNAseq_pipeline_output.
+ below_threshold.txt contains information on files deemed to have poor quality.
+ fastq_files contains the trimmed fastq files from the input directory.
+ bam_files contains the alignment data for every fastq file based on the desired genome.
+ gene_expression_files contains outputs of:
  + FPKM counts
  + RPKM saturation
  + Junction saturation
  + Read distribution
  + Infer experiment
  + Junction annotation
  + Gene body coverage

