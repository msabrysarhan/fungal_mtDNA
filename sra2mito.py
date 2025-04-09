import argparse
import shutil
import subprocess
import sys
import os
from tqdm import tqdm
from datetime import datetime

def check_tool(tool_name, log_file):
    with open(log_file, 'a') as f:
        tool_path = shutil.which(tool_name)
        if tool_path is None:
            print(f"Step 1: Checking tools... Error: {tool_name} is not found or not executable.")
            f.write(f"Step 1: Checking tools... Error: {tool_name} is not found or not executable.\n")
            sys.exit(1)
        else:
            print(f"Step 1: Checking tools... OK: {tool_name} is present and executable at {tool_path}")
            f.write(f"Step 1: Checking tools... OK: {tool_name} is present and executable at {tool_path}\n")

def download_reads(accession, output_dir, sample_name, threads, log_file):
    fastq1_file = os.path.join(output_dir, f"{sample_name}_1.fastq.gz")
    fastq2_file = os.path.join(output_dir, f"{sample_name}_2.fastq.gz")

    # Check if files already exist
    if os.path.exists(fastq1_file) and os.path.exists(fastq2_file):
        print(f"Step 2: FASTQ files for accession {accession} already exist. Skipping download.")
        with open(log_file, 'a') as f:
            f.write(f"Step 2: FASTQ files for accession {accession} already exist. Skipping download.\n")
        return fastq1_file, fastq2_file

    fasterq_dump_cmd = f"fastq-dl -a {accession} --prefix {sample_name} --outdir {output_dir} --cpus {threads} --force"

    print(f"Step 2: Downloading reads for accession {accession}...")
    with open(log_file, 'a') as f:
        f.write(f"Step 2: Downloading reads for accession {accession}...\n")
        try:
            subprocess.run(fasterq_dump_cmd, shell=True, check=True, stdout=f, stderr=subprocess.STDOUT)
            print(f"Step 2: Downloading reads for accession {accession}... OK")
            f.write(f"Step 2: Downloading reads for accession {accession}... OK\n")
        except subprocess.CalledProcessError as e:
            print(f"Step 2: Downloading reads for accession {accession}... Error: fasterq-dump failed with exit code {e.returncode}")
            f.write(f"Step 2: Downloading reads for accession {accession}... Error: fasterq-dump failed with exit code {e.returncode}\n")
            sys.exit(1)

    return fastq1_file, fastq2_file

def run_fastp(fastq1, fastq2, sample_name, threads, output_dir, log_file):
    trimmed_fastq1 = os.path.join(output_dir, f"{sample_name}_trimmed_1.fastq.gz")
    trimmed_fastq2 = os.path.join(output_dir, f"{sample_name}_trimmed_2.fastq.gz")
    qc_json = os.path.join(output_dir, f"{sample_name}_trimmed.json")
    qc_html = os.path.join(output_dir, f"{sample_name}_trimmed.html")

    fastp_cmd = f"fastp --in1 {fastq1} --in2 {fastq2} --out1 {trimmed_fastq1} --out2 {trimmed_fastq2} --thread {threads} -j {qc_json} -h {qc_html}"

    print(f"Step 3: Running fastp...")
    with open(log_file, 'a') as f:
        f.write(f"Step 3: Running fastp...\n")
        try:
            subprocess.run(fastp_cmd, shell=True, check=True, stdout=f, stderr=subprocess.STDOUT)
            print(f"Step 3: Running fastp... OK")
            f.write(f"Step 3: Running fastp... OK\n")
        except subprocess.CalledProcessError as e:
            print(f"Step 3: Running fastp... Error: fastp failed with exit code {e.returncode}")
            f.write(f"Step 3: Running fastp... Error: fastp failed with exit code {e.returncode}\n")
            sys.exit(1)

    return trimmed_fastq1, trimmed_fastq2

def sample_reads(fastq1, fastq2, sample_name, output_dir, log_file, sample_size=2000000):
    sampled_fastq1 = os.path.join(output_dir, f"{sample_name}_sampled_1.fastq.gz")
    sampled_fastq2 = os.path.join(output_dir, f"{sample_name}_sampled_2.fastq.gz")

    sample_cmd = f"seqtk sample -s100 {fastq1} {sample_size} | gzip > {sampled_fastq1} && seqtk sample -s100 {fastq2} {sample_size} | gzip > {sampled_fastq2}"

    print(f"Step 4: Sampling {sample_size} reads from each FASTQ file...")
    with open(log_file, 'a') as f:
        f.write(f"Step 4: Sampling {sample_size} reads from each FASTQ file...\n")
        try:
            subprocess.run(sample_cmd, shell=True, check=True, stdout=f, stderr=subprocess.STDOUT)
            print(f"Step 4: Sampling {sample_size} reads from each FASTQ file... OK")
            f.write(f"Step 4: Sampling {sample_size} reads from each FASTQ file... OK\n")
        except subprocess.CalledProcessError as e:
            print(f"Step 4: Sampling {sample_size} reads from each FASTQ file... Error: seqtk failed with exit code {e.returncode}")
            f.write(f"Step 4: Sampling {sample_size} reads from each FASTQ file... Error: seqtk failed with exit code {e.returncode}\n")
            sys.exit(1)

    return sampled_fastq1, sampled_fastq2

def run_spades(sampled_fastq1, sampled_fastq2, sample_name, output_dir, threads, log_file):
    spades_output_dir = os.path.join(output_dir, f"spades_{sample_name}")

    spades_cmd = f"spades.py --only-assembler -1 {sampled_fastq1} -2 {sampled_fastq2} -o {spades_output_dir} -t {threads} -k 21,33,55,77,89 --gfa11"

    print(f"Step 5: Running SPAdes assembler...")
    with open(log_file, 'a') as f:
        f.write(f"Step 5: Running SPAdes assembler...\n")
        try:
            subprocess.run(spades_cmd, shell=True, check=True, stdout=f, stderr=subprocess.STDOUT)
            print(f"Step 5: Running SPAdes assembler... OK")
            f.write(f"Step 5: Running SPAdes assembler... OK\n")
        except subprocess.CalledProcessError as e:
            print(f"Step 5: Running SPAdes assembler... Error: SPAdes failed with exit code {e.returncode}")
            f.write(f"Step 5: Running SPAdes assembler... Error: SPAdes failed with exit code {e.returncode}\n")
            sys.exit(1)

    return spades_output_dir

def main():
    parser = argparse.ArgumentParser(description="A pipeline for generating fungal mitochondrial genome sequences from SRA data.")

    parser.add_argument("--accession", "-a", help="Accession number")
    parser.add_argument("--fastq1", "-f1", help="FASTQ file 1")
    parser.add_argument("--fastq2", "-f2", help="FASTQ file 2")
    parser.add_argument("--sample_name", "-n", help="Sample name")
    parser.add_argument("--output", "-o", help="Output directory", required=True)
    parser.add_argument("--threads", "-t", help="Number of threads", type=int, default=1)

    args = parser.parse_args()

    # Custom validation for FASTQ files
    if (args.fastq1 and not args.fastq2) or (args.fastq2 and not args.fastq1):
        parser.error("Both --fastq1 and --fastq2 must be provided together")

    if not args.accession and not (args.fastq1 and args.fastq2):
        parser.error("Either --accession or both --fastq1 and --fastq2 must be provided")

    # Create output directory if it doesn't exist
    if not os.path.exists(args.output):
        os.makedirs(args.output)
        print(f"Created output directory: {args.output}")
    else:
        print(f"Output directory {args.output} already exists.")

    # Create log file
    log_file = os.path.join(args.output, f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

    # Check if required tools are present and executable
    tools_to_check = ["fastq-dl", "fastp", "seqtk", "spades.py", "bowtie2"]
    for tool in tools_to_check:
        check_tool(tool, log_file)

    # Handle accession or FASTQ files
    if args.accession:
        if args.fastq1 or args.fastq2:
            print("Error: You cannot provide both an SRA accession number and FASTQ files. Please choose one input method.")
            with open(log_file, 'a') as f:
                f.write("Error: Both accession and FASTQ files cannot be provided.\n")
            sys.exit(1)
        sample_name = args.sample_name if args.sample_name else args.accession
        fastq1, fastq2 = download_reads(args.accession, args.output, sample_name, args.threads, log_file)
    else:
        if not args.fastq1 or not args.fastq2:
            print("Error: Both FASTQ files must be provided.")
            with open(log_file, 'a') as f:
                f.write("Error: Both FASTQ files must be provided.\n")
            sys.exit(1)
        sample_name = args.sample_name if args.sample_name else "sample"
        fastq1, fastq2 = args.fastq1, args.fastq2

        # Check if FASTQ files are in the output directory
        if os.path.dirname(fastq1) == args.output and os.path.dirname(fastq2) == args.output:
            print("Step 2: FASTQ files are already in the output directory. Proceeding to the next step.")
            with open(log_file, 'a') as f:
                f.write("Step 2: FASTQ files are already in the output directory. Proceeding to the next step.\n")
        else:
            print("Step 2: FASTQ files are not in the output directory. Copying files to the output directory...")
            with open(log_file, 'a') as f:
                f.write("Step 2: FASTQ files are not in the output directory. Copying files to the output directory...\n")
            fastq1 = os.path.join(args.output, os.path.basename(fastq1))
            fastq2 = os.path.join(args.output, os.path.basename(fastq2))
            shutil.copy(args.fastq1, fastq1)
            shutil.copy(args.fastq2, fastq2)

    trimmed_fastq1, trimmed_fastq2 = run_fastp(fastq1, fastq2, sample_name, args.threads, args.output, log_file)
    sampled_fastq1, sampled_fastq2 = sample_reads(trimmed_fastq1, trimmed_fastq2, sample_name, args.output, log_file)
    spades_output_dir = run_spades(sampled_fastq1, sampled_fastq2, sample_name, args.output, args.threads, log_file)

    # Access the arguments using args.accession, args.sample_name, etc.
    print("\nArgument values:")
    if args.accession:
        print("Accession:", args.accession)
        print("Sample name:", sample_name)
    else:
        print("FASTQ file 1:", fastq1)
        print("FASTQ file 2:", fastq2)
        print("Sample name:", sample_name)
    print("Output directory:", args.output)
    print("Threads:", args.threads)
    print("Trimmed FASTQ file 1:", trimmed_fastq1)
    print("Trimmed FASTQ file 2:", trimmed_fastq2)
    print("Sampled FASTQ file 1:", sampled_fastq1)
    print("Sampled FASTQ file 2:", sampled_fastq2)
    print("SPAdes output directory:", spades_output_dir)

    

if __name__ == "__main__":
    main()
