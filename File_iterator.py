from accession_to_details import openFile
import os


def detailMaker(path):
    os.system("mkdir flexbar_output")
    os.chdir("flexbar_output")
    o = open("details.txt", 'w')
    o.write("Accession\tBasic Statistics\tPer base sequence quality\tPer tile sequence quality\tPer sequence quality scores\tPer base sequence content\tPer base N content\tSequence Length Distribution\tSequence Duplication Levels\tOverrepresented sequences\tAdapter Content\tKmer Content\n")
    
    

    for filename in os.listdir(path)[:10]: #take of [:10] to do every file
        if filename.endswith('fastq.gz'):
            temp = filename.replace('.fastq.gz','')
            o.write(openFile(temp, path) + '\n')
        elif filename.endswith('fastqc.zip'):
            temp = filename.replace('_fastqc.zip','')
            o.write(openFile(temp, path) + '\n')
            
    o.close()
    os.system("cd ..")
    
