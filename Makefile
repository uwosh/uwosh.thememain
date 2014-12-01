PYTHON=/Users/kim/Plone/Python-2.4/bin/python

all:
	cat Makefile
	@echo ""
	@echo "Don't forget to change the version number in setup.py, in profiles/default/metadata.xml, and in version.txt"

clean:
	rm -rf build dist

egg:
	$(PYTHON) setup.py bdist_egg

dist4:
	/usr/local/bin/python2.6 setup.py sdist bdist_egg upload -r ourbasket
