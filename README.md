```markdown

# FASTQ Processing Pipeline

This script automates the processing of FASTQ files for genomic data analysis. It performs the following steps:

1. **Tool Check**: Ensures required tools are installed and executable.
2. **Read Download**: Downloads FASTQ files using an accession number.
3. **Read Trimming**: Trims reads using `fastp`.
4. **Read Sampling**: Samples a subset of reads using `seqtk`.
5. **Assembly**: Assembles reads using `SPAdes`.

## Requirements

The script requires the following tools to be installed and accessible in your `PATH`:

- `fastq-dl`
- `fastp`
- `seqtk`
- `spades.py`
- `bowtie2`


## Usage

The script can be run with either an accession number or pre-existing FASTQ files. Below are examples for both scenarios.

### 1. Using an Accession Number


```bash
python script.py --accession SRR123456 --sample_name sample1 --output /path/to/output --threads 4
```


- `--accession`: Accession number for downloading reads.
- `--sample_name`: Name of the sample (optional, defaults to the accession number).
- `--output`: Directory to store output files.
- `--threads`: Number of threads to use (default: 1).

### 2. Using Existing FASTQ Files

```bash
python script.py --fastq1 /path/to/sample1_1.fastq.gz --fastq2 /path/to/sample1_2.fastq.gz --sample_name sample1 --output /path/to/output --threads 4
```

- `--fastq1`: Path to the first FASTQ file.
- `--fastq2`: Path to the second FASTQ file.
- `--sample_name`: Name of the sample (optional, defaults to "unknown_sample").
- `--output`: Directory to store output files.
- `--threads`: Number of threads to use (default: 1).


## Example Output

After running the script, the output directory will contain:

- Trimmed FASTQ files (`*_trimmed_1.fastq.gz`, `*_trimmed_2.fastq.gz`).
- Sampled FASTQ files (`*_sampled_1.fastq.gz`, `*_sampled_2.fastq.gz`).
- Quality control reports (`*_trimmed.json`, `*_trimmed.html`).
- SPAdes assembly output in a subdirectory (`spades_sample_name`).


```
