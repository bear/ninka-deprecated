
init:
	pip install -r requirements.txt

test:
	nosetests --verbosity=2 tests 

upload: check
	python setup.py sdist upload
	python setup.py bdist_wheel upload

clean:
	python setup.py clean

dist: check
	python setup.py sdist

check:
	check-manifest
	python setup.py check
