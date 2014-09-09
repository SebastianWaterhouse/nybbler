import string, importlib

"""
Call compress_string or compress_file to compress.
Call inflate_string or inflate_file to decompress.
A common series is inculded, en_US_1

~Louis Goessling
""" 

class InvalidSeriesException(Exception):
    pass
class InflateFailureException(Exception):
    pass
class SeriesLoadException(Exception):
	pass

def validate_series(series):
	already=[] #Set up list to aggregate indexed characters
	for row in series:
		for char in row:
			if not (char in string.printable or char.startswith("^^>") or char in ["^^ascii"]):
				raise InvalidSeriesException("Invalid character '"+char+"'") #Character code is invalid
			if char in already:
				raise InvalidSeriesException("Character '"+char+"' already found") #Character has already been found
			already.append(char)
			if char.startswith("^^>"):
				try:
					if not int(char.replace("^^>",""))<len(series):
						raise InvalidSeriesException("Escape '"+char+"' refers to an invalid row")
				except ValueError:
					raise InvalidSeriesException("'"+char+"' is not a valid shift")
		if not len(row)==16:
			raise InvalidSeriesException("Row "+str(series.index(row))+" too long")
	return True

def load_series(filename):
	try:
		module=importlib.import_module(filename)
	except BaseException as e:
		raise SeriesLoadException(e)
	validate_series(module.series)
	return module.series

def raw_bin(byte):
	return bin(byte).replace("0b","")

def expand(a, l):
	return ("0"*(l-len(a)))+a

def split_byte(byte):
	output=[]
	byte_bin=expand(raw_bin(byte),8)
	output.append(int(byte_bin[:4],2))
	output.append(int(byte_bin[4:],2))
	return output

def _compress_character(series, char):
	for row in series:
		if char in row:
			if series.index(row)!=0:
				ret=_compress_character(series,"^^>"+str(series.index(row)))
				ret.append(row.index(char))
				return ret
			else:
				return [row.index(char)]
	ascii_escape=_compress_character(series,"^^ascii")
	ascii_escape.extend(split_byte(ord(char)))
	return ascii_escape

def compress_characters(series, chars):
	ret=[]
	for char in chars:
		ret.extend(_compress_character(series, char))
	return ret

def _pack_two_nybbles(nybbles):
	nybble_1=expand(raw_bin(nybbles[0]),4)
	nybble_2=expand(raw_bin(nybbles[1]),4)
	return chr(int(nybble_1+nybble_2,2))

def pack_nybbles(nybbles, null_nybble):
	last_nybble=-1
	packed=""
	for nybble in nybbles:
		if last_nybble==-1:
			last_nybble=nybble
		else:
			packed+=_pack_two_nybbles([last_nybble,nybble])
			last_nybble=-1
	if last_nybble!=-1:
		packed+=_pack_two_nybbles([last_nybble,null_nybble])
	return packed

def compress_string(series, string):
	"""Compress whole string using series, returning whole compressed string"""
	return pack_nybbles(compress_characters(series, string),
	 _compress_character(series, "^^ascii")[0])

def compress_file(series, file_in):
	"""Compress whole file, returning its entirety"""
	contents=""
	for line in file_in.readlines():
		contents+=line
	return compress_string(series, contents)

def _inflate_character(series, row, nybble):
	try:
		return series[row][nybble]
	except IndexError:
		raise InflateFailureException("Invaid Nybble while decompressing")

def inflate_characters(series, nybbles):
	ret=""
	escape=0
	ascii_build=""
	for nybble in nybbles:
		inflated=_inflate_character(series, escape, nybble)
		if escape!=-1:
			if inflated.startswith("^^>"):
				escape=int(inflated.replace("^^>",""))
			elif inflated=="^^ascii":
				escape=-1
			else:
				ret+=inflated
				escape=0
		else:
			ascii_build+=expand(raw_bin(nybble),4)
			if len(ascii_build)==8:
				ret+=chr(int(ascii_build,2))
				escape=0
				ascii_build=""
	return ret

def _unpack_character(char):
	nybbles=[]
	char_bin=expand(raw_bin(ord(char)),8)
	nybbles.append(int(char_bin[:4],2))
	nybbles.append(int(char_bin[4:],2))
	return nybbles

def unpack_characters(chars):
	nybbles=[]
	for char in chars:
		nybbles.extend(_unpack_character(char))
	return nybbles

def inflate_string(series, string):
	"""Inflate 'string' using 'series,' return inflated string in its entirety"""
	return inflate_characters(series, unpack_characters(string))

def inflate_file(series, file_in):
	"""Inflate the contents of the file, returning them in their entirety"""
	contents=""
	for line in file_in.readlines():
		contents+=line
	return decompress_string(series, contents)