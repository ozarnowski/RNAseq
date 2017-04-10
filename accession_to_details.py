import os

def openFile(accession,accession2,path):
    os.system("scp " + path + accession + ".fastq.gz .") #get the file from the path to work with
    os.system("scp " + path + accession2 + ".fastq.gz .") 
    os.system("cutadapt -u 13 -o " + accession + "_cutadapt.fastq.gz " + accession + ".fastq.gz ") #run cutadapt on it
    os.system("cutadapt -u 13 -o " + accession2 + "_cutadapt.fastq.gz " + accession2 + ".fastq.gz")
    os.system("fastqc " + accession + "_cutadapt.fastq.gz") #run fastqc on it
    os.system("fastqc " + accession2 + "_cutadapt.fastq.gz")
    os.system("rm " + accession + "_cutadapt_fastqc.html") #remove html
    os.system("rm " + accession2 + "_cutadapt_fastqc.html")
    os.system("rm " + accession + ".fastq.gz") #remove fastq
    os.system("rm " + accession2 + ".fastq.gz")
    os.system("unzip " + accession + "_cutadapt_fastqc.zip") #unzip fastqc output
    os.system("unzip " + accession2 + "_cutadapt_fastqc.zip")
    os.system("rm " + accession + "_cutadapt_fastqc.zip") #remove zipped file
    os.system("rm " + accession2 + "_cutadapt_fastqc.zip")
    return getSummary(accession) + getSummary(accession2)

def getSummary(accession):
    os.chdir(accession + "_cutadapt_fastqc") #go into unzipped folder
    f = open("summary.txt", 'r') #find summary text
    s = f.readlines() #read it
    f.close()
    os.chdir("..")
    os.system("rm -r " + accession + "_cutadapt_fastqc")#remove unzipped folder
    output = accession
    for line in s:
        output += '\t' + line.split("\t")[0]#create output from summary text
    listy = output.split('\t')
    del listy[-1]
    del listy[9]
    del listy[3]
    newout = ''
    for x in listy:
        newout += x + '\t'    
    return newout + '\n'
