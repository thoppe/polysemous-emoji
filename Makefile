all:
	echo "pass"

build:
	python train.py
	python find_low_entropy_words.py
	python polysem.py

plot:
	python src_plots/plot_diffs.py
	python src_plots/repeated_letter_plot.py
	python src_plots/spatial_test.py
