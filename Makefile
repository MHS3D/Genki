.PHONY: all clean

all: main.pdf

main.pdf: docs/gemeinsameDocsFuerHA.tex
	pdflatex -output-directory=docs docs/gemeinsameDocsFuerHA.tex

clean:
	rm -f docs/*.aux docs/*.log docs/*.out docs/*.pdf