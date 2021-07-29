#! /bin/sh
#$ -S /bin/sh
#$ -cwd

export PATH=#Input your conda pass:${PATH}
bwa_PATH=#Input your bwa pass
samtools_PATH=#Input your samtools pass

#fastq.qz pass
alignment_txt=xxx/xxx/xxx/xxx.txt
#Reference fasta pass
reference_fasta=xxxx/xxx/xxx/.fasta
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#used upu
used_cpu=8
#-----------------------------------------------------------------------------------------------------------------------------------------------------------

dir_name=`echo ${alignment_txt}|sed -e "s/.*\\///"`
dir_name=`echo ${dir_name}|sed -e "s/\.txt//"`
mkdir ${dir_name}
cd ${dir_name}

ln -s ${reference_fasta}
if [ -e ${reference_fasta}.pac ]; then
  echo "File exists."
else
  bwa index -p ${reference_fasta} -a bwtsw ${reference_fasta}
fi
python /lustre7/home/lustre3/takagi-hiroki/multi_align_fragaria/output_txt.py ${alignment_txt} ${reference_fasta}

echo "make sai"
cat bwa_aln_sai.txt|xargs -P${used_cpu} -I % sh -c %

echo "make sam"
cat sai_to_sam.txt|xargs -P${used_cpu} -I % sh -c %
rm *sai

echo "make pre.bam"
cat sam_to_prebam.txt|xargs -P${used_cpu} -I % sh -c %
rm *sam

echo "make marge.bam"
cat prebam_to_mergebam.txt|xargs -P${used_cpu} -I % sh -c %
rm *pre.bam

echo "make sort.bam"
cat mergebam_to_sortbam.txt|xargs -P${used_cpu} -I % sh -c %

echo "make bai"
cat sortbam_to_bai.txt|xargs -P${used_cpu} -I % sh -c %

mkdir sort_bam_bai_pass
mv *.sort.bam sort_bam_bai_pass
mv *.bai sort_bam_bai_pass

rm *marge.bam
