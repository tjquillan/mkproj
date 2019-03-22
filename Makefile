format:
	black mkproj
	isort -y

distribute:
	rm -r ./dist
	python setup.py sdist bdist_wheel
	twine check dist/*

test-upload: distribute
	twine upload --skip-existing --repository-url https://test.pypi.org/legacy/ dist/*

upload: distribute
	twine upload dist/*
