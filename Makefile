build:
	rm -rf out
	mkdir out
	python -m zipapp --python "/usr/bin/env python3" mouc
	mv mouc.pyz out/mouc
	chmod +x out/mouc

install: build
	su -c 'cp out/mouc /usr/local/bin/mouc'