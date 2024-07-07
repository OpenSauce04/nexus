build:
	rm -rf out
	mkdir out
	python -m zipapp --python "/usr/bin/env python3" nexus
	mv nexus.pyz out/nexus
	chmod +x out/nexus

install: build
	su -c 'cp out/nexus /usr/local/bin/nexus'