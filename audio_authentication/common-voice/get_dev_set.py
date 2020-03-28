import csv
from shutil import copyfile

i = 0
max_files = 1000
with open('dev.tsv', 'r') as devFile:
    reader = csv.DictReader(devFile, delimiter='\t')
    for line in reader:
        copyfile('./clips/' + line['path'], './dev-clips/' + line['path'])

        if i > max_files:
            break

        i += 1
