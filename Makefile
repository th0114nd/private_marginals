
build:
	cargo build

fetch_table:
	ssconvert http://www.irs.gov/pub/irs-soi/13es01fy.xls 13es01fy.csv

report:
	latexmk -pvc -pdf doc/private_marginals.tex
