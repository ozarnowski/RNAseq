from accession_to_details import openFile
import os


def detailMaker(path):
    if "cutadapt_output" not in os.listdir(os.curdir):
        os.system("mkdir cutadapt_output")
    os.chdir("cutadapt_output")
    o = open("details.txt", 'w')
    o.write("Accession\tBasic Statistics\tPer base sequence quality\tPer tile sequence quality\tPer sequence quality scores\tPer base sequence content\tPer base N content\tSequence Length Distribution\tSequence Duplication Levels\tOverrepresented sequences\tAdapter Content\tKmer Content\n")
    
    files = os.listdir(path)
    files.sort()
    files = [x for x in files if x.endswith("fastq.gz")]

    for i in range(len(files)/2): 
        o.write(openFile(files[i*2].replace(".fastq.gz",""), files[i*2+1].replace(".fastq.gz",""),path))
                  
    o.close()
    os.system("cd ..")
    
