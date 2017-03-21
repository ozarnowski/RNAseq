from accession_to_details import openFile
import argparse
import os

parser = argparse.ArgumentParser() 
parser.add_argument("Input_path", help = "path to directory of input files")
args = parser.parse_args()


def detailMaker():
    o = open("details.txt", 'w')
    o.write("Accession\tBasic Statistics\tPer base sequence quality\tPer tile sequence quality\tPer sequence quality scores\tPer base sequence content\tPer base N content\tSequence Length Distribution\tSequence Duplication Levels\tOverrepresented sequences\tAdapter Content\tKmer Content\n")
    
    
<<<<<<< HEAD
    for filename in os.listdir(args.Input_path)[:5]: #take of [:10] to do every file
=======
    for filename in os.listdir(args.Input_path):#[:10]: take of [:10] to do every file
>>>>>>> d131117195f5704f8fc2f92197b3ab76db817d3b
        if filename.endswith('fastq.gz'):
            temp = filename.replace('.fastq.gz','')
            o.write(openFile(temp, args.Input_path) + '\n')
        elif filename.endswith('fastqc.zip'):
            temp = filename.replace('_fastqc.zip','')
            o.write(openFile(temp, args.Input_path) + '\n')
            
    o.close()
    
detailMaker()
