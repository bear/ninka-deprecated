
build:
	python setup.py sdist upload
	python setup.py bdist_wheel upload

init:
	pip install -r requirements.txt

test:
	nosetests --verbosity=2 tests 
