import os

def openFile(accession,accession2,path):
    os.system("scp " + path + accession + ".fastq.gz .") #get the file from the path to work with
    os.system("scp " + path + accession2 + ".fastq.gz .") 
    os.system("gunzip " + accession + ".fastq.gz") #unzip it for flexbar
    os.system("gunzip " + accession2 + ".fastq.gz")
    os.system("flexbar -r " + accession + ".fastq -p" + accession2 + ".fastq --pre-trim-left 13") #run flexbar on it
    os.system("mv flexbar_1.fastq " + accession + "_flexbar.fastq") #rename the file
    os.system("mv flexbar_2.fastq " + accession2 + "_flexbar.fastq")
    os.system("fastqc " + accession + "_flexbar.fastq") #run fastqc on it
    os.system("fastqc " + accession2 + "_flexbar.fastq")
    os.system("rm " + accession + "_flexbar_fastqc.html") #remove html
    os.system("rm " + accession2 + "_flexbar_fastqc.html")
    os.system("rm " + accession + ".fastq") #remove fastq
    os.system("rm " + accession2 + ".fastq")
    os.system("gzip " + accession + "_flexbar.fastq") #zip flexbar output
    os.system("gzip " + accession2 + "_flexbar.fastq")
    os.system("unzip " + accession + "_flexbar_fastqc.zip") #unzip fastqc output
    os.system("unzip " + accession2 + "_flexbar_fastqc.zip")
    os.system("rm " + accession + "_flexbar_fastqc.zip") #remove zipped file
    os.system("rm " + accession2 + "_flexbar_fastqc.zip")
    return getSummary(accession) + getSummary(accession2)

def getSummary(accession):
    os.chdir(accession + "_flexbar_fastqc") #go into unzipped folder
    f = open("summary.txt", 'r') #find summary text
    s = f.readlines() #read it
    f.close()
    os.chdir("..")
    os.system("rm -r " + accession + "_flexbar_fastqc")#remove unzipped folder
    output = accession
    for line in s:
        output += '\t' + line.split("\t")[0]#create output from summary text
    return output + '\n'
