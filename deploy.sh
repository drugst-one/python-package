# build dist
python setup.py sdist

# test on test pypi
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/drugstone-0.3.2.tar.gz

# upload to pypi
python3 -m twine upload dist/drugstone-0.3.2.tar.gz
