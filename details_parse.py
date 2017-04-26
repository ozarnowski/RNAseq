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
    p = open('below_threshhold.txt','w')
    f = open('final_cut.txt', 'w')
    z = o[0]
    p.write(z)
    o = o[1:]
    
    for i in range(len(o)/2):
        temp1 = o[i*2].split('\t')
        temp1x = o[i*2]
        temp2 = o[i*2+1].split('\t')
        temp2x = o[i*2+1]
        
        f.write(temp1[0] + '\n' + temp2[0] + '\n')    
            
        if temp1.count("FAIL") != 0 or temp2.count("FAIL") != 0:
            p.write(temp1x + "\n" + temp2x + "\n")
    f.close()

def runAnalysis(fastqList):
    fastqList = map(str.strip, fastqList)
    for i in range(len(fastqList)/2):
        os.system("STAR --runThreadN 6 --genomeDir " + args.Genome_path + "/star_indices --readFilesIn "
        + fastqList[i*2] + "_cutadapt.fastq.gz " + fastqList[i*2+1] + "_cutadapt.fastq.gz --readFilesCommand"
        + " zcat --outSAMtype BAM Unsorted")
        os.system("rm Log.progress.out")
        os.system("rm Log.out")
        os.system("rm SJ.out.tab")
        os.system("mv Aligned.out.bam " + fastqList[i*2][:-2] + ".bam")
        print ("Samtools is sorting " + fastqList[i*2][:-2] + " ...")
        os.system("samtools sort " + fastqList[i*2][:-2] + ".bam -o " + fastqList[i*2][:-2] + ".sorted.bam")
        print ("Samtools is indexing " + fastqList[i*2][:-2] + " ...")
        os.system("samtools index " + fastqList[i*2][:-2] + ".sorted.bam " + fastqList[i*2][:-2] + ".sorted.bam.bai")
        os.system("rm " + fastqList[i*2][:-2] + ".bam")
        print ("Calculating FPKM values for "  + fastqList[i*2][:-2] + " ...")
        os.system("python /usr/local/bin/anaconda2/bin/FPKM_count.py -i" + fastqList[i*2][:-2] + ".sorted.bam -o " + fastqList[i*2][:-2] + " -r " + args.Genome_path + "/annotation/gencode.v24.annotation.nochr.bed")
    os.system("rm Log.final.out")

def geneExpressionData(fastqList):
    fastqList = map(str.strip, fastqList)
    for i in range(len(fastqList)/2):
        os.system("python /usr/local/bin/anaconda2/bin/RPKM_saturation.py -i bam_files/" + fastqList[i*2][:-2] + ".sorted.bam -o " + fastqList[i*2][:-2] + " -r " + args.Genome_path + "/annotation/gencode.v24.annotation.nochr.bed")
        os.system("python /usr/local/bin/anaconda2/bin/junction_saturation.py -i bam_files/" + fastqList[i*2][:-2] + ".sorted.bam -o " + fastqList[i*2][:-2] + " -r " + args.Genome_path + "/annotation/gencode.v24.annotation.nochr.bed")
        os.system("python /usr/local/bin/anaconda2/bin/read_distribution.py -i bam_files/" + fastqList[i*2][:-2] + ".sorted.bam -r " + args.Genome_path + "/annotation/gencode.v24.annotation.nochr.bed > " + fastqList[i*2][:-2] + ".read_distribution")
        os.system("python /usr/local/bin/anaconda2/bin/infer_experiment.py -i bam_files/" + fastqList[i*2][:-2] + ".sorted.bam -r " + args.Genome_path + "/annotation/gencode.v24.annotation.nochr.bed > " + fastqList[i*2][:-2] + ".infer_experiment")
        os.system("python /usr/local/bin/anaconda2/bin/junction_annotation.py -i bam_files/" + fastqList[i*2][:-2] + ".sorted.bam -o " + fastqList[i*2][:-2] + " -r " + args.Genome_path + "/annotation/gencode.v24.annotation.nochr.bed")
    os.system("python /usr/local/bin/anaconda2/bin/geneBody_coverage.py -i bam_files/ -o all -r " + args.Genome_path + "/annotation/gencode.v24.annotation.nochr.bed")

def main():
    parser()
    f = open("final_cut.txt",'r')
    f = f.readlines()
    if "fastq_files" not in os.listdir(os.curdir):
        os.system("mkdir fastq_files")
    if "bam_files" not in os.listdir(os.curdir):
        os.system("mkdir bam_files")
    if "gene_expression_files" not in os.listdir(os.curdir):
        os.system("mkdir gene_expression_files")
    runAnalysis(f)
    os.system("mv *.sorted.* bam_files/")
    os.system("mv *.FPKM.xls gene_expression_files/")
    os.system("mv *.fastq.gz fastq_files/")
    geneExpressionData(f)
    os.system("mv *.eRPKM.xls gene_expression_files/")
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
