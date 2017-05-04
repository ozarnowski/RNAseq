from accession_to_details import openFile
import os


def detailMaker(path):#this function creates the details.txt file housing all FastQC diagnostics information for later use
    if "RNAseq_pipeline_output" not in os.listdir(os.curdir): #make a directory if not already there
        os.system("mkdir RNAseq_pipeline_output")
    os.chdir("RNAseq_pipeline_output")
    o = open("details.txt", 'w') 
    o.write("Accession    Basic Statistics    Per base sequence quality    Per sequence quality scores    Per base sequence content    Per sequence GC content    Per base N content    Sequence Length Distribution    Overrepresented sequences    Adapter Content\n")#write the header for the details.txt file
    
    files = os.listdir(path)
    files.sort()
    files = [x for x in files if x.endswith("fastq.gz")]  #generates a list of all fastq files

    for i in range(len(files)/2): 
        o.write(openFile(files[i*2].replace(".fastq.gz",""), files[i*2+1].replace(".fastq.gz",""),path))#adds summary row created by openFile (in accession_to_details.py) to the details.txt file
                  
    o.close()
    os.system("cd ..")
    
