import easygui, nybbler, os

title="Nybbler GUI"

def main():
	series=None
	while series==None:
		series=easygui.fileopenbox("Select a series file", title, './en_US_1.py', [["*.py", "*.nybser", "Series File"]])

	action=None
	while action==None:
		action=easygui.boolbox("Select an Action", title, ("Compress", "Decompress"))

	f_in=None
	while f_in==None:
		f_in=easygui.fileopenbox("Select an input file", title, '*')

	f_out=None
	while f_out==None:
		f_out=easygui.filesavebox("Select a output file", title, '*')

	if action: #Decompress
		os.system("python nybblecli.py -qs "+series+" -d "+f_in+" "+f_out)
	else: #Compress
		os.system("python nybblecli.py -qs "+series+" -c "+f_in+" "+f_out)

	repeat=None
	while repeat==None:
		repeat=easygui.boolbox("Again?", title, ("Yes", "No"))

	if repeat: main()

main()