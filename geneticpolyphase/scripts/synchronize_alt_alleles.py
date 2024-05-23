from math import ceil
import sys

def syn_alts(reference_vcf):
	ref_col = None
	alt_col = None
	
	# create mapping from sequence to allele for each position in reference vcf
	seq_to_idx = dict()
	idx_to_seq = dict()
	with open(reference_vcf, "r") as f:
		for line in f.read().splitlines():
			if len(line) < 2 or line[0:2] == "##":
				continue
				
			sp = line.split("\t")
			if line[0] == "#":
				for i in range(len(sp)):
					if sp[i] == "REF":
						ref_col = i
						continue
					if sp[i] == "ALT":
						alt_col = i
						continue
				continue

			pos = int(sp[1])
			pos_list = [sp[ref_col]]
			pos_dict = dict()
			pos_dict[sp[ref_col]] = 0
			for i, alt in enumerate(sp[alt_col].split(",")):
				pos_list.append(alt)
				pos_dict[alt] = i+1
			idx_to_seq[pos] = pos_list
			seq_to_idx[pos] = pos_dict
				
	# rename alleles in input vcf
	ref_col = None
	alt_col = None
	format_col = None
	for line in sys.stdin:
		if len(line) < 2:
			sys.stdout.write(line)
			continue

		if line[:2] == "##":
			sys.stdout.write(line)
			continue

		sp = line.split("\t")
		if line[0] == "#":
			for i in range(len(sp)):
				if sp[i] == "REF":
					ref_col = i
					continue
				if sp[i] == "ALT":
					alt_col = i
					continue
				if sp[i] == "FORMAT":
					format_col = i
					continue
			sys.stdout.write(line)
			continue

		pos = int(sp[1])
		if pos not in seq_to_idx:
			sys.stdout.write(line)
			continue
		
		# create name map
		alleles = [sp[ref_col]] + sp[alt_col].split(",")
		assert len(alleles) >= 2
		
		new_alleles = 0
		require_rewrite = False
		name_map = dict() # maps old name to new name
		for i, allele in enumerate(alleles):
			if allele not in seq_to_idx[pos]:
				seq_to_idx[pos][allele] = len(seq_to_idx[pos])
				idx_to_seq[pos].append(allele)
			name_map[i] = seq_to_idx[pos][allele]
			if name_map[i] != i:
				require_rewrite = True
				
		if not require_rewrite:
			sys.stdout.write(line)
			continue
		
		# rewrite alleles
		line_out = "\t".join(sp[:ref_col]) + "\t"
		line_out += idx_to_seq[pos][0] + "\t"
		if alt_col - ref_col > 1:
			line_out += "\t".join(sp[ref_col+1:alt_col]) + "\t"
		line_out += ",".join([idx_to_seq[pos][i] for i in range(1, len(idx_to_seq[pos]))]) + "\t"
		line_out += "\t".join(sp[alt_col+1:format_col+1]) + "\t"
		
		# update genotypes/phasings
		gt_col = -1
		sp2 = sp[format_col].split(":")
		for i in range(len(sp2)):
			if sp2[i] == "GT":
				gt_col = i
				break

		if gt_col < 0:
			sys.stdout.write(line_out + "\t".join(sp[formal_col+1:]))
			continue
			
		for sampleseq in sp[format_col+1:]:
			sp2 = sampleseq.split(":")
			gt = sp2[gt_col]
			sep = "/" if "/" in gt else "|"
			p = gt.split(sep)
			sp2[gt_col] = sep.join([str(name_map[int(a)]) for a in p])
			line_out += ":".join(sp2) + "\t"

		sys.stdout.write(line_out + "\n")


def main(argv):
	syn_alts(argv[1])

if __name__ == "__main__":
	main(sys.argv)