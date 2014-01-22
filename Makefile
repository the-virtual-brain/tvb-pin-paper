complete:
	pdflatex main.tex
	bibtex main
	pdflatex main.tex
	pdflatex main.tex

simple:
	pdflatex main.tex

watchdog:
	watchmedo shell-command -c "make simple" -p "*.tex;*.bib;images/*"

