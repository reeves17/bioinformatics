dataDir=<data directory>
outDir=<out directory>
pythonScript=<path to fastq_percent_extraction.py>
percent=<percent to be extracted>

# create directory if it does not yet exist
mkdir -p "$outDir"

master="fastq_percent_extraction_master.sh"
printf "#"'!'/bin/bash"\n" >$master
index=0

shopt -s nullglob

for read1 in $dataDir/*_1.{fq,fastq,fq.gz,fastq.gz}; do
  echo "Processing "$read1
  suffix=${read1##*_1}
  sample=${read1%_1$suffix}
  sample=${sample##*/}
  read2=${read1%_1$suffix}
  read2=$read2"_2"$suffix
  sampleshort=${sample%%*/}
  ((++index))
  sh_worker="run"$index"_"$sampleshort".sh"
  printf "qsub "$sh_worker"\n" >>$master
  printf "#"'!'/bin/bash"\n" >$sh_worker
  printf "#PBS -N "$percent"percent_"$sampleshort"\n" >>$sh_worker
  printf "#PBS -q batch\n" >>$sh_worker
  printf "#PBS -l nodes=1:ppn=1:AMD\n" >>$sh_worker
  printf "#PBS -l walltime=4:00:00\n" >>$sh_worker
  printf "cd "$outDir"\n" >>$sh_worker
  printf "module load python/3.4.3\n" >>$sh_worker
  printf "python3 "$pythonScript" "$percent" "$read1" "$read2" "$outDir >>$sh_worker
done
