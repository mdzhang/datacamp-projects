PWD = $(shell pwd)

# NB: You can also download the datacamp project, which will include a 8.2MB names.csv.zip
baby_names:
	# wget https://www.ssa.gov/oact/babynames/names.zip
	# unzip names.zip -d ./baby_names_unzipped
	python manage.py baby_names ${PWD}/datasets/baby_names_unzipped ${PWD}/datasets/baby_names.csv
