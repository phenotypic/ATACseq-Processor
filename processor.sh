#!/bin/bash

threads="$(sysctl -n hw.logicalcpu)"
reference="$(find . -name '*toplevel*' | cut -c 3-)"
species="$(echo ${reference} | awk -F '.' '{print $2}')"
dirlist=(ATAC_paired/*.fastq.gz)

printf "\nReference genome detected: ${reference}"
printf "\nSpecies shorhand: ${species}"
printf "\nATAC file 1: ${dirlist[0]}"
printf "\nATAC file 2: ${dirlist[1]}"
printf "\nNumber of threads available: ${threads}"

rm -rf Quality_ATAC bwt_out bam peak ${species}.clipped.bdg ${species}.sizes ${species}.clipped.sorted.bdg

printf "\n\n(1/10) Starting quality control\n\n"
mkdir -p Quality_ATAC
fastqc -o Quality_ATAC ATAC_paired/*.gz

if [ ! -d bwt_index ]; then
  printf "\n(2/10) Building genome index"
  mkdir -p bwt_index
  bowtie2-build ${reference} bwt_index/${species}
else
  printf "\n(2/10) Using pre-existing genome index"
fi

printf "\n\n(3/10) Starting alignment\n\n"
mkdir -p bwt_out
bowtie2 --threads ${threads} -x bwt_index/${species} -q -1 ${dirlist[0]} -2 ${dirlist[1]} -S bwt_out/${species}.sam

printf "\n(4/10) Converting SAM to BAM and sorting\n\n"
mkdir -p bam
samtools view --threads ${threads} -bS bwt_out/${species}.sam | samtools sort --threads ${threads} - > bam/${species}.sorted.bam

printf "\n(5/10) Indexing BAM file and removing Mt/Chloroplast reads"
samtools index bam/${species}.sorted.bam
samtools idxstats bam/${species}.sorted.bam | cut -f1 | grep -v Mt | grep -v Pt | grep -v MT | xargs samtools view --threads ${threads} -b bam/${species}.sorted.bam > bam/${species}.sorted.noorg.bam

printf "\n\n(6/10) Started PEAK calling"
mkdir -p peak
macs3 callpeak -t bam/${species}.sorted.noorg.bam -q 0.05 --broad -f BAMPE -n ${species} -B --trackline --outdir peak &>peak/${species}.peak.log

printf "\n\n(7/10) Started making chromasome sizes file"
bioawk -c fastx '{print $name, length($seq)}' Mus_musculus.${species}.dna.toplevel.fa.gz > ${species}.sizes

printf "\n\n(8/10) Clipping bed graph files to correct coordinates"
bedtools slop -i peak/${species}_treat_pileup.bdg -g ${species}.sizes -b 0 | ./bedClip stdin ${species}.sizes ${species}.clipped.bdg

printf "\n\n(9/10) Sorting clipped files"
sort -k1,1 -k2,2n ${species}.clipped.bdg > ${species}.clipped.sorted.bdg

printf "\n\n(10/10) Converting to bigwig"
./bedGraphToBigWig ${species}.clipped.sorted.bdg ${species}.sizes ${species}.clipped.sorted.bw

printf "\n\nFinished"
printf "\nYou can import the bigwig file (${species}.clipped.sorted.bw) into the IGV Genome Browser"
printf "\nAll other files can be deleted\n"
