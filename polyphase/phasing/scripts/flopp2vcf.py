import sys

def hpopToVcfConverter(phasing_path, vcf_input_path, vcf_output_path):

    with open(phasing_path, 'r') as phasing_file, open(vcf_input_path, 'r') as vcf_input, open(vcf_output_path, 'w') as vcf_output:
        format_index = -1
        vcf_pos = -1
        vcf_row = vcf_input.readline()
        statistic_phased_vars = 0
        statistic_one_missing = 0
        statistic_more_missing = 0
        ploidy = None
        block_id = 0
        hpop_row = phasing_file.readline()
        
        while hpop_row:
            # Advance in hpop file until first phasing line is reached
            while hpop_row.startswith("*"):
                hpop_row = phasing_file.readline()
            while hpop_row.startswith("BLOCK:"):
                block_id += 1
                hpop_row = phasing_file.readline()
            # Parse vcf row. If end of file reached, set row to -1.
            raw_pos = hpop_row.split("\t")[0].split(":")
            if len(raw_pos) == 2 and raw_pos[1].isdigit():
                variant_pos = int(raw_pos[1])
            else:
                variant_pos = -1

            #print("Searching for row {}".format(variant_pos))

            while vcf_row and vcf_pos <= variant_pos:
                if vcf_row[0] == '#':
                    # Header lines are just copied to output vcf
                    while vcf_row and vcf_row[0] == "#":
                        rowtabs = vcf_row.split("\t")
                        if vcf_row[1] != "#":
                            format_index = rowtabs.index("FORMAT")
                        vcf_output.write(vcf_row)
                        vcf_row = vcf_input.readline()
                    vcf_pos = int(vcf_row.split("\t")[1])
                    continue
                    
                if vcf_pos < variant_pos:
                    #print("Skipping position {} in VCF.".format(vcf_pos))
                    
                    next_output = "".join([tab+"\t" for tab in rowtabs[0:-1]])
                    next_output += (rowtabs[-1].replace("|", "/"))
                    vcf_output.write(next_output)
                elif vcf_pos == variant_pos:
                    #print("Phasing position {} in VCF.".format(vcf_pos))
                    # Copy vcf row, except the phasing information
                    rowtabs = vcf_row.split("\t")

                    # Detect ploidy if not done yet
                    if not ploidy:
                        phasing = hpop_row.split("\n")[0].split("\t")[1:]
                        for i, token in enumerate(phasing):
                            if not token.isdigit() and token != "-1":
                                ploidy = i
                                break
                        else:
                            ploidy = len(phasing)
                        #print("Ploidy = {}".format(ploidy))

                    # Add phasing to vcf
                    phasing = hpop_row.split("\n")[0].split("\t")[1:ploidy + 1]
                    phased_genotype = 0
                    missing_entries = 0
                    for p in phasing:
                        if p.isdigit() and int(p) >= 0:
                            phased_genotype += int(p)
                        else:
                            missing_entries += 1
                    phasing_old = [p for p in phasing]
                    
                    phased = False
                    # Look at missing entries
                    if missing_entries == 0:
                        # Phasing complete for current position
                        statistic_phased_vars += 1
                        phased = True
                    
                    else:
                        # Too many haplotypes missing. Omit position
                        #print("Missing: "+str(phasing_old)+" -> n/a : "+rowtabs[-1].replace("|", "/"))
                        statistic_more_missing += 1
                        phased = False
                        
                    # write correct entry
                    if phased:
                        next_output = "\t".join([tab for tab in rowtabs[0:format_index]])
                        format_tokens = rowtabs[format_index].split(":")
                        if "PS" in format_tokens:
                            ps_index = format_tokens.index("PS")
                            next_output += "\t" + rowtabs[format_index] + "\t"
                        else:
                            ps_index = len(format_tokens)
                            next_output += "\t" + rowtabs[format_index] + ":PS\t"
                        
                        phasing_tokens = rowtabs[format_index + 1].split(":")
                        phasing_tokens[-1] = phasing_tokens[-1][0:-1]
                        if all([p == phasing[0] for p in phasing[1:]]):
                            next_output += "/".join(phasing)
                        else:
                            next_output += "|".join(phasing)
                        if len(phasing_tokens[1:ps_index]) > 0:
                            next_output += ":"
                        next_output += ":".join(phasing_tokens[1:ps_index])
                        next_output += ":" + str(block_id)
                        if ps_index < len(phasing_tokens) - 1:
                            next_output += ":" + ":".join(phasing_tokens[ps_index + 1:])
                        next_output += "\n"
                    else:
                        next_output = "".join([tab + "\t" for tab in rowtabs[0:-1]])
                        next_output += (rowtabs[-1].replace("|", "/"))

                    vcf_output.write(next_output)
                vcf_row = vcf_input.readline()
                if vcf_row:
                    rowsplit = vcf_row.split("\t")
                    if len(rowsplit) >= 2:
                        vcf_pos = int(vcf_row.split("\t")[1])
                    else:
                        vcf_pos = -1
                else:
                    vcf_pos = -1
                #print("Next position: {} in VCF.".format(vcf_pos))
            hpop_row = phasing_file.readline()
                
    total = statistic_phased_vars + statistic_one_missing + statistic_more_missing
    print("Parsed "+str(block_id)+" blocks with a total of "+str(total)+" variants, from which "+str(statistic_phased_vars)+" are completely phased, "+str(statistic_one_missing)+" could be infered from genotype information and "+str(statistic_more_missing)+" are unphased.")

def main(argv):
    if (len(argv) != 4):
        print("Required call format:")
        print("python flopp2vcf.py <flopp-file> <input-vcf> <output-vcf>")
    else:
        hpopToVcfConverter(argv[1], argv[2], argv[3])
    
if __name__ == '__main__':
    main(sys.argv)