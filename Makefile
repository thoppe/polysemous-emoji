all:
	echo "pass"

build:
	python train.py
	python polysem.py

plot:
	python src_plots/plot_diffs.py
