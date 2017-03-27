from File_iterator import detailMaker
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("Input_path", help = "path to directory of input files")
args = parser.parse_args()

detailMaker(args.Input_path)

def parser():
    o = open('details.txt','r').readlines()
    f = open('final_cut.txt','w')
    o = o[1:]
    for i in range(len(o)/2):
        temp1 = o[i*2].split('\t')
        temp2 = o[i*2+1].split('\t')
        del temp1[-1]
        del temp1[9]
        del temp1[3]
        del temp2[-1]
        del temp2[9]
        del temp2[3]    
            
        if temp1.count("FAIL") == 0 and temp2.count("FAIL") == 0:
            f.write(temp1[0] + "\n" + temp2[0] + "\n")

parser()
