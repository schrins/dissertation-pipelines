from math import ceil
import sys

def merge_monoploid(sample_name):
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
				if sp[i] == "FORMAT":
					format_col = i
					break
			sp[format_col+1] = sample_name
			sys.stdout.write("\t".join(sp[:format_col+2]) + "\n")
			continue

		alleles = []
		line_valid = True
		for i in range(format_col+1, len(sp)):
			s = sp[i] if sp[i][-1] != "\n" else sp[i][:-1]
			if s == "0/0":
				alleles.append("0")
			elif s == "1/1":
				alleles.append("1")
			elif s == "2/2":
				alleles.append("2")
			elif s == "3/3":
				alleles.append("3")
			elif s == "4/4":
				alleles.append("4")
			else:
				line_valid = False

		if line_valid:
			if all([alleles[i] == alleles[0] for i in range(1, len(alleles))]):
				sp[format_col+1] = "/".join(alleles)
			else:
				sp[format_col+1] = "|".join(alleles)
			sys.stdout.write("\t".join(sp[:format_col+2]) + "\n")


def main(argv):
	merge_monoploid(argv[1])

if __name__ == "__main__":
	main(sys.argv)