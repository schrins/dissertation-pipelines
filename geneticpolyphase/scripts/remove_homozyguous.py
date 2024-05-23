import sys

def remove_homozyguous(sample_name):
	format_col = None
	sample_col = None
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
				if sp[i].strip() == "FORMAT":
					format_col = i
				if sp[i].strip() == sample_name:
					sample_col = i
			sys.stdout.write(line)
			continue

		gt_col = -1
		sp2 = sp[format_col].split(":")
		for i in range(len(sp2)):
			if sp2[i] == "GT":
				gt_col = i
				break
				
		line_valid = gt_col >= 0
				
		s = sp[sample_col] if sp[sample_col][-1] != "\n" else sp[sample_col][:-1]
		sp3 = s.split(":")[gt_col].split("/")
		if len(sp3) >= 2 and all([sp3[i] == sp3[0] for i in range(1, len(sp3))]):
			line_valid = False

		if line_valid:
			sys.stdout.write(line)


def main(argv):
	remove_homozyguous(argv[1])

if __name__ == "__main__":
	main(sys.argv)