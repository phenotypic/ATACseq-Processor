# ATACseq-Processor

This script is used to process raw ATAC-seq files ready for analysis. Processed files can be opened in the [IGV Genome browser](https://software.broadinstitute.org/software/igv/) to visualise chromatin accessibility.



## Prerequisites

| Command | Installation |
| --- | --- |
| `fastqc`, `bowtie2`, `samtools`, `bioawk`, `bedtools` | Install via [brew](https://brew.sh) by running `brew install fastqc bowtie2 samtools bioawk bedtools` |
| `macs3` | Install by running `pip3 install macs3` |
| `bedClip` | Install from the same directory by running `curl http://hgdownload.cse.ucsc.edu/admin/exe/macOSX.x86_64/bedClip --output bedClip && chmod +x bedClip` |
| `bedGraphToBigWig` | Install from the same directory by running `curl http://hgdownload.cse.ucsc.edu/admin/exe/macOSX.x86_64/bedGraphToBigWig --output bedGraphToBigWig && chmod +x bedGraphToBigWig` |

## Usage

Download with:
```
git clone https://github.com/phenotypic/ATACseq-Processor.git
```

Before running, you must ensure that the reference genome and executable files are located in the the same directory as the script, and that the two ATAC-seq files are located in the `ATAC_paired` subdirectory. See below:

```
ATACseq-Processor
│   ├── ATAC_paired
│   │   ├── 30fish-0hpa_S1_L001_R1_00_1.fastq.gz
│   │   └── 30fish-0hpa_S1_L001_R1_00_2.fastq.gz
│   ├── Danio_rerio.GRCz11.dna.toplevel.fa.gz
│   ├── bedClip
│   ├── bedGraphToBigWig
│   └── processor.sh
```

Start `processor.sh` from the `ATACseq-Processor` directory by running:
```
bash processor.sh
```

The first thing the script does is generate a quality control report for the two files in the `ATAC_paired` subdirectory and output it to the `Quality_ATAC` folder. You can view the reports in a web browser. Use [this](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/3%20Analysis%20Modules/) guide to interpret the results.

Once the script has finished running, open the `SPECIES.clipped.sorted.bw` file in the [IGV Genome browser](https://software.broadinstitute.org/software/igv/) and load a reference genome to view chromatin accessibility:

![igv_snapshot_ATAC](https://user-images.githubusercontent.com/33377034/177248346-749c0c7e-9ac9-4dda-b508-0835dcc5959e.png)

## Notes

- The pipeline used in this script is adapted from [this](https://bioinformaticsworkbook.org/dataAnalysis/ATAC-seq/ATAC_tutorial.html) excellent tutorial
- The script should automatically detect the reference genome and ATAC-seq files, as long as they are located in the correct directories. The script will also automatically detect the species shorthand name and the number of CPU cores available
- Building the genome index (step 2) is likely to take a long time as the process is computationally intensive
- Once the script has run and you have saved the `SPECIES.clipped.sorted.bw` file, you are welcome to delete all of the other files generated as they are no longer needed
