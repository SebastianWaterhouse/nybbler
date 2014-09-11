import argparse, sys
import nybbler

def p_std(string):
	if not args.q:
		print string

def p_ver(string):
	if args.v:
		p_std(string)

parser = argparse.ArgumentParser(description='Compress or decompress files.')
parser.add_argument('input', type=str, help='Input File', metavar="input", default=None, nargs="?")
parser.add_argument('output', type=str, help='Output File', metavar="output", default=None, nargs="?")
parser.add_argument('-s', type=str, help='Series File', metavar="series", default="en_US_1.py")
group_output = parser.add_mutually_exclusive_group()
group_output.add_argument('-v', action='store_true', help="Verbose")
group_output.add_argument('-q', action='store_true', help="Quiet")
group_action = parser.add_mutually_exclusive_group(required=True)
group_action.add_argument('-C', action='store_true', help="Compress [Requires input, output]")
group_action.add_argument('-D', action='store_true', help="Decompress [Requires input, output]")
group_action.add_argument('-V', action='store_true', help="Validate series file [Requires series file]")
args = parser.parse_args()

if args.C or args.D:
	p_std("Reading...")
	assert args.input != None and args.output != None, "For -C and -D arguments, you must supply input and output files!"
	p_ver("Reading Series...")
	series=nybbler.load_series(args.s)
	p_ver("Reading File...")
	contents=""
	with open(args.input, 'rb') as f_in:
		for line in f_in:
			contents+=line
	if args.C:
		p_std("Compressing...")
		result=nybbler.compress_string(series, contents)
	if args.D:
		p_std("Decompressing...")
		result=nybbler.inflate_string(series, contents)
	p_std("Writing...")
	with open(args.output, 'wb') as f_out:
		f_out.write(result)
else:
	p_std("Processing...")
	if args.input!=None:
		p_std("\nYou appear to have entered the series file in the input argument. In the future enter it as the -s argument. Continuing assuming input contains the series file you want vaildated.\n")
		args.s=args.input
	try:
		p_ver("Calling...")
		nybbler.load_series(args.s)
		p_std("Series is good")
	except nybbler.SeriesException as e:
		p_std("Error, dump:")
		p_std(str(e))
		p_ver("Raw exception:")
		p_ver(type(e))
		p_ver(e)
		sys.exit(1)

p_ver("Done!")
sys.exit(0)