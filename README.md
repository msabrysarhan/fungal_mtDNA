This script `sra2mito.py` processes SRA accession, performs adapter trimming, sub-sampling, and de novo assembly.

1. **Tool Check**: Ensures required tools are installed and executable.
2. **Read Download**: Downloads FASTQ files using an accession number.
3. **Read Trimming**: Trims reads using `fastp`.
4. **Read Sampling**: Samples a subset of reads using `seqtk`.
5. **Assembly**: Assembles reads using `SPAdes`.

## Requirements

The script requires the following tools to be installed and excutable:

- `fastq-dl`
- `fastp`
- `seqtk`
- `spades.py`
- `bowtie2`


## Usage
To see the usage and options, run:
```bash
python sra2mito.py -h
```

```markdown 
usage: sra2mito.py [-h] [--accession ACCESSION] [--fastq1 FASTQ1]
                   [--fastq2 FASTQ2] [--sample_name SAMPLE_NAME] --output
                   OUTPUT [--threads THREADS]

A pipeline for generating fungal mitochondrial genome sequences from SRA data.

options:
  -h, --help            show this help message and exit
  --accession ACCESSION, -a ACCESSION
                        Accession number
  --fastq1 FASTQ1, -f1 FASTQ1
                        FASTQ file 1
  --fastq2 FASTQ2, -f2 FASTQ2
                        FASTQ file 2
  --sample_name SAMPLE_NAME, -n SAMPLE_NAME
                        Sample name
  --output OUTPUT, -o OUTPUT
                        Output directory
  --threads THREADS, -t THREADS
                        Number of threads
```

The script can be run with either an accession number or pre-existing FASTQ files. Below are examples for both scenarios.

### 1. Using an Accession Number


```bash
python sra2mito.py --accession SRR4063847 --sample_name mlp_98AG31_v1 --output output_directory/ --threads 4
```


- `--accession`: Accession number for downloading reads.
- `--sample_name`: Name of the sample (optional, defaults to the accession number).
- `--output`: Directory to store output files.
- `--threads`: Number of threads to use (default: 1).

### 2. Using Existing FASTQ Files

```bash
python sra2mito.py --fastq1 SRR4063847_1.fastq.gz --fastq2 SRR4063847_2.fastq.gz --sample_name mlp_98AG31_v1 --output output_directory --threads 4
```

- `--fastq1`: Path to the first FASTQ file.
- `--fastq2`: Path to the second FASTQ file.
- `--sample_name`: Name of the sample (optional, defaults to "sample").
- `--output`: Directory to store output files.
- `--threads`: Number of threads to use (default: 1).


## Example Output

After running the script, the output directory will contain:

- Trimmed FASTQ files (`*_trimmed_1.fastq.gz`, `*_trimmed_2.fastq.gz`).
- Sampled FASTQ files (`*_sampled_1.fastq.gz`, `*_sampled_2.fastq.gz`).
- Quality control reports (`*_trimmed.json`, `*_trimmed.html`).
- SPAdes assembly output in a subdirectory (`spades_sample_name`).



