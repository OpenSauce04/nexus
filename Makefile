build:
	rm -rf out
	mkdir out
	python -m zipapp --python python3 mouc
	mv mouc.pyz out/mouc