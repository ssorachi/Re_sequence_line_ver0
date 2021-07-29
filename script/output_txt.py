#!/usr/bin/env python
# coding: UTF-8
# In[11]:

import sys
import re

args = sys.argv
alignment_txt = args[1]
reference_fasta = args[2]
#----------------------------------------------------------------------------------------------------------------------------------------
alignment_txt = alignment_txt
reference_fasta = reference_fasta
#----------------------------------------------------------------------------------------------------------------------------------------
a = open(alignment_txt,'r')

e = open('bwa_aln_sai.txt',mode='w')
f = open('sai_to_sam.txt',mode='w')
g = open('sam_to_prebam.txt',mode='w')
h = open('mergebam_to_sortbam.txt',mode='w')
i = open('sortbam_to_bai.txt',mode='w')
j = open('prebam_to_mergebam.txt',mode='w')

count = 0
sample_name = 'hogehoge'

while True:
    line_1 = a.readline()
    if line_1:
        list_1 = line_1.split()
        if sample_name == list_1[0]:
            count = count + 1
        else:
            all_bam=''
            if count>0:
                for item in range(count):
                    numeric_number=item+1
                    all_bam=all_bam+' '+sample_name+'_'+str(numeric_number)+'pre.bam'

                j.write('samtools merge -f '+sample_name+'_'+'marge.bam'+all_bam+'\n')
                h.write('samtools sort -@ 4 '+sample_name+'_'+'marge.bam '+'-o '+sample_name+'.sort.bam'+'\n')
                i.write('samtools index '+sample_name+'.sort.bam'+'\n')

            count = 1
            sample_name = list_1[0]
        first_read=list_1[1]
        first_read_name=re.sub('\S+/','',first_read)
        second_read=list_1[2]
        second_read_name=re.sub('\S+/','',second_read)

        e.write('bwa aln '+reference_fasta+' '+list_1[1]+'>'+first_read_name+'.sai'+'\n')
        e.write('bwa aln '+reference_fasta+' '+list_1[2]+'>'+second_read_name+'.sai'+'\n')
        f.write('bwa sampe '+reference_fasta+' '+first_read_name+'.sai '+second_read_name+'.sai '+list_1[1]+' '+list_1[2]+'>'+list_1[0]+'_'+str(count)+'.sam'+'\n')
        g.write('samtools view -Sb -@ 4 '+list_1[0]+'_'+str(count)+'.sam'+' > '+list_1[0]+'_'+str(count)+'pre.bam'+'\n')

    else:
        break

all_bam=''
if count>0:
    for item in range(count):
        numeric_number=item+1
        all_bam=all_bam+' '+sample_name+'_'+str(numeric_number)+'pre.bam'
    j.write('samtools merge -f '+sample_name+'_'+'marge.bam'+all_bam+'\n')
    h.write('samtools sort -@ 4 '+sample_name+'_'+'marge.bam '+'-o '+sample_name+'.sort.bam'+'\n')
    i.write('samtools index '+sample_name+'.sort.bam'+'\n')

a.close()
