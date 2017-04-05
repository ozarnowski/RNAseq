# RNAseqPipeline
RNAseqPipeline is a command line tool that serves as a pipeline which processes RNA sequences via the use of various applications including quality control metrics.

## Software Requirements: 
Linux or MAC OS
Python 2.7 

## Scripts
+ details_parse.py
  + [info on details_parse.py]
+ File_iterator.py
  + [info on File_iterator.py]
+ accession_to_details.py
  + [info on accession_to_details.py]

## Usage 

`python /path/to/details_parse.py path/to/FASTQ/directory/ /path/to/genomeIndex/`

### To run in background:

`nohup python /path/to/details_parse.py path/to/FASTQ/directory/ /path/to/genomeIndex/&`

+ A sample fastq folder with three paired fastq files is available at:
  + https://github.com/ozarnowski/RNAseq/tree/master/sample_files

+ The genome index can be constructed using STAR, however, the path to a pipeline-ready index is as follows:
  + /home/azakkar/GRCh38/star_indices/
