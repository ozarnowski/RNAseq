from File_iterator import detailMaker
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("Input_path", help = "path to directory of input files")
parser.add_argument("Genome_path", help = "path to genome directory")
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
    f.close()

def runSTAR(fastqList):
    fastqList = map(str.strip, fastqList)
    for i in range((len(fastqList)/2)):
        os.system("STAR --runThreadN 6 --genomeDir " + args.Genome_path + " --readFilesIn "
        + fastqList[i*2] + "_cutadapt.fastq.gz " + fastqList[i*2+1] + "_cutadapt.fastq.gz --readFilesCommand"
        + " zcat --outSAMtype BAM SortedByCoordinate")
        os.system("rm Log.progress.out")
        os.system("rm Log.out")
        os.system("rm SJ.out.tab")
        os.system("mv Aligned.sortedByCoord.out.bam " + fastqList[i*2][:-2] + ".bam")
    #os.system("STAR --runThreadN 6 --genomeDir /home/azakkar/GRCh38/star_indices --genomeLoad Remove")
    #os.system("rm Aligned.out.sam")
    #os.system("rm Log.progress.out")
    #os.system("rm Log.out")
    #os.system("rm -r _STARtmp")
    os.system("rm Log.final.out")

def main():
    parser()
    f = open("final_cut.txt",'r')
    f = f.readlines()
    runSTAR(f)


main()
