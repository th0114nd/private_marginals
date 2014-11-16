
build:
	cargo build

report:
	latexmk -pvc -pdf doc/private_marginals.tex
