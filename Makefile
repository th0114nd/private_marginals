run:
	python src/all.py accu \
	--db="data/ex.tab" \
	--query="{1:1, 3:0}"
#	python src/main.py priv \
#				       --epsilon=1 \
#					   --delta=0.2 \
#					   --db="data/DATA.DB" \
#				       --query_dist="0.5 0.5"

fetch_table:
	ssconvert http://www.irs.gov/pub/irs-soi/13es01fy.xls 13es01fy.csv

