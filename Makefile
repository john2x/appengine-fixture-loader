version=1.9.15

# Override VENV if not defined
VENV?=.env

# Consciously avoiding "all" target because we may want to use it for building
# the actual product rather than a sane testing environment
venv: virtualenv libraries

directories:
	mkdir -p $(CURDIR)/build $(CURDIR)/cache

appenginesdk: directories
	wget -c https://storage.googleapis.com/appengine-sdks/featured/google_appengine_$(version).zip -O $(CURDIR)/cache/google_appengine_$(version).zip
	unzip -q -o $(CURDIR)/cache/google_appengine_$(version).zip -d $(CURDIR)/build

requirements:
	$(CURDIR)/$(VENV)/bin/pip install --download-cache $(CURDIR)/cache -r $(CURDIR)/resources/requirements.txt

libraries: requirements appenginesdk
	mv -v $(CURDIR)/build/google_appengine $(CURDIR)/$(VENV)/lib
	ln -sv $(CURDIR)/$(VENV)/lib/google_appengine/*.py $(CURDIR)/$(VENV)/bin/
	cp $(CURDIR)/resources/autogenerated $(CURDIR)/$(VENV)/lib/python2.7/site-packages/src.pth
	echo "$(CURDIR)/src/" >> $(CURDIR)/$(VENV)/lib/python2.7/site-packages/src.pth
	cp $(CURDIR)/resources/autogenerated $(CURDIR)/$(VENV)/lib/python2.7/site-packages/gae.pth
	echo "$(CURDIR)/$(VENV)/lib/google_appengine/" >> $(CURDIR)/$(VENV)/lib/python2.7/site-packages/gae.pth
	echo "import dev_appserver; dev_appserver.fix_sys_path()" >> $(CURDIR)/$(VENV)/lib/python2.7/site-packages/gae.pth

virtualenv:
	virtualenv $(CURDIR)/$(VENV)

# A useful target for PEP-8'ing your source tree
pep8:
	find $(CURDIR)/src/ -name *.py -exec pep8 {} \;
	find $(CURDIR)/tests/ -name *.py -exec pep8 {} \;

# The same for pyflakes
pyflakes:
	find $(CURDIR)/src/ -name *.py -exec pyflakes {} \;
	find $(CURDIR)/tests/ -name *.py -exec pyflakes {} \;

clean_dirs:
	rm -rf $(CURDIR)/build/*

clean_cache:
	rm -rf $(CURDIR)/cache/*

# Also avoiding the "clean" target for the reasons described at the "venv" target
# Deletes the virtualenv
clean_venv: clean_dirs
	rm -rf $(CURDIR)/$(VENV)

test: venv
	.env/bin/nosetests