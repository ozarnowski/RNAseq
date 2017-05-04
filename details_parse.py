from File_iterator import detailMaker
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("Input_path", help = "path to directory of input files") #Creates parameter for required path to directory of input files
parser.add_argument("Genome_path", help = "path to genome directory") #Creates parameter for required path to genome directory
args = parser.parse_args()

detailMaker(args.Input_path) #runs function from File_iterator.py that runs cutadapt, fastQC and generates a details file

def parser(): #goes through fastQC diagnostics file (details.txt) and makes a file of the inputs below threshhold
    o = open('details.txt','r').readlines()
    p = open('below_threshhold.txt','w')
    f = open('final_cut.txt', 'w')
    z = o[0]
    p.write(z)
    o = o[1:]
    
    for i in range(len(o)/2): #parses lines from details.txt into list
        temp1 = o[i*2].split('\t')
        temp1x = o[i*2]
        temp2 = o[i*2+1].split('\t')
        temp2x = o[i*2+1]
        
        f.write(temp1[0] + '\n' + temp2[0] + '\n')    
            
        if temp1.count("FAIL") != 0 or temp2.count("FAIL") != 0: #if either of the paired end files have a FAIL in any diagnostics test, put all of the diagnostic info into below_threshhold.txt
            p.write(temp1x + "\n" + temp2x + "\n")
    f.close()

def runAnalysis(fastqList):#runs STAR to align genome, runs samtools to sort STAR output, calculates FPKM values for each file
    fastqList = map(str.strip, fastqList)
    for i in range(len(fastqList)/2): #iterates through each file
        os.system("STAR --runThreadN 6 --genomeDir " + args.Genome_path + "/star_indices --readFilesIn "
        + fastqList[i*2] + "_cutadapt.fastq.gz " + fastqList[i*2+1] + "_cutadapt.fastq.gz --readFilesCommand"
        + " zcat --outSAMtype BAM Unsorted") #STAR command
        os.system("rm Log.progress.out")#removing files we don't use
        os.system("rm Log.out")
        os.system("rm SJ.out.tab")
        os.system("mv Aligned.out.bam " + fastqList[i*2][:-2] + ".bam")#renaming files
        print ("Samtools is sorting " + fastqList[i*2][:-2] + " ...")
        os.system("samtools sort " + fastqList[i*2][:-2] + ".bam -o " + fastqList[i*2][:-2] + ".sorted.bam")#samtools sorts by coordinate
        print ("Samtools is indexing " + fastqList[i*2][:-2] + " ...")
        os.system("samtools index " + fastqList[i*2][:-2] + ".sorted.bam " + fastqList[i*2][:-2] + ".sorted.bam.bai") #samtools makes a bai file
        os.system("rm " + fastqList[i*2][:-2] + ".bam")
        print ("Calculating FPKM values for "  + fastqList[i*2][:-2] + " ...")
        os.system("python /usr/local/bin/anaconda2/bin/FPKM_count.py -i" + fastqList[i*2][:-2] + ".sorted.bam -o " + fastqList[i*2][:-2] + " -r " + args.Genome_path + "/annotation/gencode.v24.annotation.nochr.bed")#Runs FPKM_count.py on each file 
    os.system("rm Log.final.out")#removing unneccesary file

def geneExpressionData(fastqList): #runs various RSeQC scripts on Samtools sorted STAR output
    fastqList = map(str.strip, fastqList)
    for i in range(len(fastqList)/2): #iterates through files and runs each script on each one
        os.system("python /usr/local/bin/anaconda2/bin/RPKM_saturation.py -i bam_files/" + fastqList[i*2][:-2] + ".sorted.bam -o " + fastqList[i*2][:-2] + " -r " + args.Genome_path + "/annotation/gencode.v24.annotation.nochr.bed")#runs RPKM_saturation.py
        os.system("python /usr/local/bin/anaconda2/bin/junction_saturation.py -i bam_files/" + fastqList[i*2][:-2] + ".sorted.bam -o " + fastqList[i*2][:-2] + " -r " + args.Genome_path + "/annotation/gencode.v24.annotation.nochr.bed")#runs junction_saturation.py
        os.system("python /usr/local/bin/anaconda2/bin/read_distribution.py -i bam_files/" + fastqList[i*2][:-2] + ".sorted.bam -r " + args.Genome_path + "/annotation/gencode.v24.annotation.nochr.bed > " + fastqList[i*2][:-2] + ".read_distribution")#runs read_distribution.py
        os.system("python /usr/local/bin/anaconda2/bin/infer_experiment.py -i bam_files/" + fastqList[i*2][:-2] + ".sorted.bam -r " + args.Genome_path + "/annotation/gencode.v24.annotation.nochr.bed > " + fastqList[i*2][:-2] + ".infer_experiment")#runs infer_experiment.py and puts output into a text file
        os.system("python /usr/local/bin/anaconda2/bin/junction_annotation.py -i bam_files/" + fastqList[i*2][:-2] + ".sorted.bam -o " + fastqList[i*2][:-2] + " -r " + args.Genome_path + "/annotation/gencode.v24.annotation.nochr.bed")#runs junction_annotation.py
    os.system("python /usr/local/bin/anaconda2/bin/geneBody_coverage.py -i bam_files/ -o all -r " + args.Genome_path + "/annotation/gencode.v24.annotation.nochr.bed")#runs gene body coverage on ALL files outside of the for loop

def main():
    parser()
    f = open("final_cut.txt",'r')
    f = f.readlines()
    if "fastq_files" not in os.listdir(os.curdir): #makes directory for fastq files if it doesnt exist
        os.system("mkdir fastq_files")
    if "bam_files" not in os.listdir(os.curdir): #makes directory for bam files if it doesnt exist 
        os.system("mkdir bam_files")
    if "gene_expression_files" not in os.listdir(os.curdir):#makes directory for gene expression files if it doesn't already exist
        os.system("mkdir gene_expression_files")
    runAnalysis(f) #see above for function details
    os.system("mv *.sorted.* bam_files/") #moves files into designated folders
    os.system("mv *.FPKM.xls gene_expression_files/")
    os.system("mv *.fastq.gz fastq_files/")
    geneExpressionData(f)#see above for function details
    os.system("mv *.eRPKM.xls gene_expression_files/") #moves files into designated folders and deletes unnecessary files
    os.system("mv *.junctionSaturation_plot.* gene_expression_files/")
    os.system("mv *.rawCount.xls gene_expression_files/")
    os.system("mv *.saturation.* gene_expression_files/")
    os.system("mv all.geneBodyCoverage.* gene_expression_files/")
    os.system("mv *.read_distribution gene_expression_files/")
    os.system("mv *.infer_experiment gene_expression_files/")
    os.system("mv *.junction* gene_expression_files/")
    os.system("mv *.splice* gene_expression_files/")
    os.system("rm final_cut.txt")
    os.system("rm log.txt")
    os.system("rm details.txt")

main()
