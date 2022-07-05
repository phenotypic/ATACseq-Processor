# ATACseq-Processor

This script is used to process raw ATAC-seq files ready for analysis. Processed files can be viewed in the [IGV Genome browser](https://software.broadinstitute.org/software/igv/) to visualise chromatin accessibility.

## Prerequisites

You must have `python3` installed. You will need to install any other outstanding requirements:

| Command | Installation |
| --- | --- |
| `fastqc`, `bowtie2`, `samtools`, `bioawk`, `bedtools` | Install via [brew](https://brew.sh) by running `brew install fastqc bowtie2 samtools bioawk bedtools` |
| `macs2` | Install by running `pip3 install macs2` |
| `bedClip` | Install from the same directory by running `curl http://hgdownload.cse.ucsc.edu/admin/exe/macOSX.x86_64/bedClip --output bedClip && chmod +x bedClip` |
| `bedClip` | Install from the same directory by running `curl http://hgdownload.cse.ucsc.edu/admin/exe/macOSX.x86_64/bedGraphToBigWig --output bedGraphToBigWig && chmod +x bedGraphToBigWig` |

## Usage

Download with:
```
git clone https://github.com/phenotypic/ATACseq-Processor.git
```

Before running, you must ensure that your reference genome is located in the the same directory as the script, and that your raw ATAC-seq files are located in the `ATAC_paired` subdirectory. For example:

```
ATACseq-Processor
│   ├── ATAC_paired
│   │   ├── 30fish-0hpa_S1_L001_R1_00_1.fastq.gz
│   │   ├── 30fish-0hpa_S1_L001_R1_00_2.fastq.gz
│   │   └── 30fish-0hpa_S1_L001_R1_00_3.fastq.gz
│   ├── Danio_rerio.GRCz11.dna.toplevel.fa.gz
│   ├── LICENSE
│   ├── README.md
│   └── processor.py
```
Start `processor.py` by running:
```
python3 processor.py
```

After running the script, you will have to wait a while as the tasks performed by the script are computationally intensive.

Once the script has finished running, open the `NAME.clipped.sorted.bw` in the [IGV Genome browser](https://software.broadinstitute.org/software/igv/) to view chromatin accessibility:

![igv_snapshot_ATAC](https://user-images.githubusercontent.com/33377034/177248346-749c0c7e-9ac9-4dda-b508-0835dcc5959e.png)

You can delete all other files created by the script
