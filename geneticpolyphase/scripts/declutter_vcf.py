from math import ceil
import sys

def declutter(path, outpath, remove_info=True, keep_format=["PS","GT","AD"]):
	info_col = 0
	format_col = 0
	with open(path, "r") as f, open(outpath, "w") as o:
		for line in f.read().splitlines():
			if len(line) < 2:
				o.write(line+"\n")
				continue
				
			if line[0:2] == "##":
				if len(line) >= 7 and line[0:7] == "##INFO=":
					pass
				else:
					o.write(line+"\n")
				continue
				
			sp = line.split("\t")
			if line[0] == "#":
				for i in range(len(sp)):
					if sp[i] == "INFO":
						info_col = i
					if sp[i] == "FORMAT":
						format_col = i
				o.write(line+"\n")
				continue
				
			sp[info_col] = "."
			
			sp2 = sp[format_col].split(":")
			kept = []
			for i in range(len(sp2)):
				if sp2[i] in keep_format:
					kept.append(i)
					
			sp[format_col] = ":".join([sp2[i] for i in kept])
			
			for col in range(format_col+1, len(sp)):
				sp2 = sp[col].split(":")
				sp[col] = ":".join([sp2[i] for i in kept])
				
			if not sp[-1].endswith("\n"):
				sp[-1] = sp[-1] + "\n"
				
			o.write("\t".join(sp))


def main(argv):
	declutter(argv[1], argv[2])

if __name__ == "__main__":
	main(sys.argv)