from File_iterator import detailMaker
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("Input_path", help = "path to directory of input files")
args = parser.parse_args()

detailMaker(args.Input_path)

def parser():
    o = open('details.txt','r')
    f = open('final_cut.txt','w')
    for line in o:
        if not line.startswith("Accession"):
            temp = line.split('\t')
            del temp[-1]
            del temp[9]
            del temp[3]
            
            if temp.count("FAIL")==0:
                f.write(temp[0] + "\n")

parser()
