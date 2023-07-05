Welcome to the Linkage&Overlap tool!

This program accepts gene list(text/file), and searches the database according to the search method chosen and saves the results in .csv file in chosen folder.
These are the search method options:
	-Linkage – Checking which genes surround a specific gene (5 genes in each direction – upstream and downstream) on both strands.
	-Overlapping genes –Checking if the gene of interest overlaps another gene in the opposite DNA strand.

Requirements - 
	- All related files must be in the same folder.
	- Required libraries: pandas, numpy, tkinter, openpyxl, os, and threading. 
	Some of them are already installed by default when you install Python, but if needed - can be installed by 'pip install'.
	
How to run -
	- Gene input - enter gene list either by file or text. Example files are genes.txt  and genes.xlsx.
	- Search method - choose one or both.
	- Output - choose location to save the output file and its name.
	-RUN!

This code was checked by a fellow studeng Reut Yemini (reut.yemini@weizmann.ac.il)