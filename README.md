# ISPMathematics281
Textbook for the Vector Calc/Differential Equations/Linear Algebra 
Math281 course at Northwestern University

This textbook was originally written in 1992/1993 in AMSTeX
by Leonard Evans.  This version has been retypeset in 2015 in
LaTeX by Jason Siefken.

### Original Source
Since many of the macros from AMSTeX are incompatible with
the newer latex macros, some pre-processing was done to the original
source files with the script contained in `conversionsoftware/convert_old_tex.py`.
Further, all the original diagrams have been converted from ps to pdf.

Modifications of this work should take place in the latex
version located in the `latexsource` directory.  Original
AMSTeX as well as original xfig drawings are located in
the `plaintexsource` directory.

## Compiling
To Compile the text, do

	cd  latexsource
	xelatex evans
	xelatex evans
	makeindex evans
	xelatex evans

and you should have a fully compiled `evans.pdf` document!
