import os

def openFile(accession, path):
    os.system("scp " + path +  accession + ".fastq.gz .")
    os.system("fastqc " + accession + ".fastq.gz")
    os.system("rm " + accession + "_fastqc.html")
    os.system("rm " + accession + ".fastq.gz")
    os.system("unzip " + accession + "_fastqc.zip")
    os.system("rm " + accession + "_fastqc.zip")
    os.chdir(accession + "_fastqc")
    f = open("summary.txt", 'r')
    s = f.readlines()
    f.close()
    os.chdir("..")
    os.system("rm -r " + accession + "_fastqc")
    output = accession
    for line in s:
        output += '\t' + line.split("\t")[0]
    return output
