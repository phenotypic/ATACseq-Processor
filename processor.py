import subprocess
import pathlib

if not pathlib.Path('ATAC_paired').is_dir():
    print('\nERROR: Please ensure that the ATAC files are in the ATAC_paired subdirectory')
    quit()

print('\nRunning quality control...')
pathlib.Path('Quality_ATAC').mkdir(parents=True, exist_ok=True)
subprocess.run(['fastqc', '-o', 'Quality_ATAC', 'ATAC_paired/*.gz'])
print('Quality control finished. View in Quality_ATAC folder')

referenceGenome = input('\nInput name of reference genome file in this directory (e.g. Danio_rerio.GRCz11.dna.toplevel.fa.gz): ')
speciesShorthand = input('Enter species shorthand (e.g. Dr.GRCz11): ')

print('\nBuilding bowtie2 Genome Index...')
pathlib.Path('bwt_index').mkdir(parents=True, exist_ok=True)
subprocess.run(['bowtie2-build', referenceGenome, 'bwt_index/' + speciesShorthand])
print('Finished building bowtie2 Genome Index...')

threads = subprocess.run(['sysctl', '-n', 'hw.logicalcpu'], stdout=subprocess.PIPE)

bowtieCom = ['bowtie2', '--threads', threads, '-x', 'bwt_index/' + speciesShorthand, '-q']
for i in range(1, 4):
    text = input('\nInput name of ATAC input file ' + str(i) + ' (e.g. 30fish-0hpa_S1_L001_R1_00_' + str(i) + '.fastq.gz), or press return to skip: ')
    if not text:
        break
    bowtieCom.extend(('-' + str(i), 'ATAC_paired/' + text))
bowtieCom.extend(('-S', 'bwt_out/' + speciesShorthand + '.sam'))

print('\nPerforming alignment using bowtie2...')
subprocess.run(bowtieCom)
print('Finished performing alignment...')

print('\nConverting SAM to BAM and sorting...')
pathlib.Path('bam').mkdir(parents=True, exist_ok=True)
subprocess.run(['samtools', 'view', '--threads', threads, '-bS', 'bwt_out/' + speciesShorthand + '.sam', '|', 'samtools', 'sort', '--threads', threads, '-', '>', 'bam/' + speciesShorthand + '.sorted.bam'])
print('Finished conversion and sorting...')

print('\nIndexing the BAM file and removing Mt/Chloroplast reads...')
subprocess.run(['samtools', 'index', 'bam/' + speciesShorthand + '.sorted.bam'])
subprocess.run(['samtools', 'idxstats', 'bam/' + speciesShorthand + '.sorted.bam', '|', 'cut', '-f1', '|', 'grep', '-v', 'Mt', '|', 'grep', '-v', 'Pt', '|', 'grep', '-v', 'MT', '|', 'xargs', 'samtools', 'view', '--threads', threads, '-b', 'bam/' + speciesShorthand + '.sorted.bam', '>', 'bam/' + speciesShorthand + '.sorted.noorg.bam'])
print('Finished indexing and removing unwanted alignments...')

print('\nStarting PEAK calling...')
pathlib.Path('peak').mkdir(parents=True, exist_ok=True)
subprocess.run(['macs2', 'callpeak', '-t', 'bam/' + speciesShorthand + '.sorted.noorg.bam', '-q', '0.05', '--broad', '-f', 'BAMPE', '-n', speciesShorthand, '-B', '--trackline', '--outdir', 'peak', '&>peak/' + speciesShorthand + '.peak.log'])
print('Finished indexing and removing unwanted alignments...')

print('\nMaking chromosome sizes file...')
subprocess.run(['bioawk', '-c', 'fastx', '\'{print', '$name,', 'length($seq)}\'', referenceGenome, '>', speciesShorthand + '.sizes'])
print('Finished making sizes file...')

print('\nClipping bed graph files to correct coordinates...')
subprocess.run(['bedtools', 'slop', '-i', 'peak/' + speciesShorthand + '.bdg', '-g', speciesShorthand + '.sizes', '-b', '0', '|', 'bedClip', 'stdin', speciesShorthand + '.sizes', speciesShorthand + '.clipped.bdg'])
print('Finished clipping bed graph files...')

print('\nSorting clipped files...')
subprocess.run(['sort', '-k1,1', '-k2,2n', speciesShorthand + '.clipped.bdg', '>', speciesShorthand + '.clipped.sorted.bdg'])
print('Finished clipping bed graph files...')

print('\nConverting to bigwig...')
subprocess.run(['bedGraphToBigWig', speciesShorthand + '.clipped.sorted.bdg', speciesShorthand + '.sizes', speciesShorthand + '.clipped.sorted.bw'])
print('Finished converting to bigwig')

print('\nYou can import the bigwig file (' + speciesShorthand + '.clipped.sorted.bw' + ') into the IGV Genome browser')
print('All other files can be deleted')
