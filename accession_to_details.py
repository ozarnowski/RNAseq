import os

def openFile(accession, path):
    os.system("scp " + path + accession + ".fastq.gz .") #get the file from the path to work with
    os.system("gunzip " + accession + ".fastq.gz") #unzip it for flexbar
    os.system("flexbar -r " + accession + ".fastq --pre-trim-left 13") #run flexbar on it
    os.system("mv flexbar.fastq " + accession + "_flexbar.fastq") #rename the file
    os.system("fastqc " + accession + "_flexbar.fastq.gz --limits limits_edited.txt") #run fastqc on it
    os.system("rm " + accession + "_flexbar_fastqc.html") #remove html
    os.system("rm " + accession + ".fastq.gz") #remove fastq
    os.system("gzip " + accession + "_flexbar.fastq") #zip flexbar output
    os.system("unzip " + accession + "_flexbar_fastqc.zip") #unzip fastqc output
    os.system("rm " + accession + "_flexbar_fastqc.zip") #remove zipped file
    os.chdir(accession + "_flexbar_fastqc") #go into unzipped folder
    f = open("summary.txt", 'r') #find summary text
    s = f.readlines() #read it
    f.close()
    os.chdir("..")
    os.system("rm -r " + accession + "_flexbar_fastqc")#remove unzipped folder
    output = accession
    for line in s:
        output += '\t' + line.split("\t")[0]#create output from summary text
    return output
