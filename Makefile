test:
	python3 -m unittest discover
build-package:
	pip install twine wheel
	python3 setup.py sdist bdist_wheel
upload:
	python3 -m twine upload dist/* --verbose
