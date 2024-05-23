import sys



if __name__ == '__main__':
	
	gfafile = sys.argv[1]
	fastafile = sys.argv[2]

	with open(fastafile, 'w') as fasta:	
		with open(gfafile) as gfa:
			for i,line in enumerate(gfa):
				if (line[0] == 'S'):
					
					name = line.strip().split('\t')[1]
#					if (name == "utg000187l"):					
					seq = line.strip().split('\t')[2]
					fasta.write('>'+name+'\n')
					fasta.write(seq+'\n')
					
