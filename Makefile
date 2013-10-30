draft: *.tex
	pdflatex main-draft.tex

complete:
	pdflatex main.tex
	bibtex main
	pdflatex main.tex
	pdflatex main.tex

simple:
	pdflatex main.tex
