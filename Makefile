all:
	echo "pass"

build:
	python train.py
	python polysem.py
