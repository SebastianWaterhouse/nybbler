import argparse, sys
import nybbler

def p_std(string):
	if not args.q:
		print string

def p_ver(string):
	if args.v:
		p_std(string)

parser = argparse.ArgumentParser(description='Compress or decompress files.')
parser.add_argument('input', type=str, help='Input File', metavar="input")
parser.add_argument('output', type=str, help='Output File', metavar="output")
parser.add_argument('-s', type=str, help='Series File', metavar="series", default="en_US_1.py")
group_output = parser.add_mutually_exclusive_group()
group_output.add_argument('-v', action='store_true', help="Verbose")
group_output.add_argument('-q', action='store_true', help="Quiet")
group_action = parser.add_mutually_exclusive_group(required=True)
group_action.add_argument('-c', action='store_true', help="Compress")
group_action.add_argument('-d', action='store_true', help="Decompress")
args = parser.parse_args()

p_std("Reading...")
p_ver("Reading Series...")
series=nybbler.load_series(args.s)
p_ver("Reading File...")
contents=""
with open(args.input, 'rb') as f_in:
	for line in f_in:
		contents+=line
if args.c:
	p_std("Compressing...")
	result=nybbler.compress_string(series, contents)
if args.d:
	p_std("Decompressing...")
	result=nybbler.inflate_string(series, contents)
p_std("Writing...")
with open(args.output, 'wb') as f_out:
	f_out.write(result)
p_ver("Done!")