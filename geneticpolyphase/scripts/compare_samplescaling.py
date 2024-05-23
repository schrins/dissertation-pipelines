from os import listdir
from os.path import isfile, join
from collections import defaultdict
import sys
import re

def create_csv(tsv_folder, target, chromosome, complexity):
    print(chromosome)

    metrics_list = ['all_assessed_pairs', 'all_switch_rate', 'all_switchflip_rate', 'blockwise_hamming_rate', 'blockwise_diff_genotypes_rate']
    metrics = set(metrics_list)
    data = defaultdict(dict)
    
    filenames = [f for f in listdir(tsv_folder) if isfile(join(tsv_folder, f))]
    reg = re.compile(fr'\A{chromosome}\.genetic\.altus\.c{complexity}\.\S+\.sub(\d+)\-(\d+)\.new14\.tsv')
    
    # extract metric information from all tsvs in folder
    for f in filenames:
        print(f)
        match = reg.search(f)
        if not match is None:
            print(f)
            subsize = match.group(1)
            iteration = match.group(2)
            if subsize not in data:
                data[subsize] = dict()
                for metric in metrics_list:
                    data[subsize][metric] = []
            
            with open(tsv_folder+f, 'r') as h:
                lines = h.read().splitlines()
                headers = lines[0].split('\t')
                values = lines[1].split('\t')
                for (prop, value) in zip(headers, values):
                    if prop in metrics:
                        data[subsize][prop].append(float(value))
                
    # aggegrate data
    print(data)
    data_avg = defaultdict(list)
    for subsize in data:
        for metric in metrics_list:
            data_avg[int(subsize)].append(str(sum(data[subsize][metric]) / len(data[subsize][metric])))
            
    # write to csv
    sep = ','
    with open(target, 'w') as h:
        h.write('sample_size{}{}\n'.format(sep, sep.join(metrics_list)))
        for subsize in sorted([int(s) for s in data]):
            h.write('{}{}{}\n'.format(subsize, sep, sep.join(data_avg[subsize])))
    
def main(argv):
    create_csv(argv[1], argv[2], argv[3], argv[4])

if __name__ == "__main__":
    main(sys.argv)
