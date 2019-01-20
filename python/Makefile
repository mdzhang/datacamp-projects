PWD = $(shell pwd)

# NB: You can also download the datacamp project, which will include a 8.2MB names.csv.zip
baby_names:
	# wget https://www.ssa.gov/oact/babynames/names.zip
	# unzip names.zip -d ./baby_names_unzipped
	python manage.py baby_names ${PWD}/datasets/baby_names_unzipped ${PWD}/datasets/baby_names.csv

# TODO: Based on download project data, this doesn't seem to be the data Datacamp is using
#       but neither does the site data they link out to ¯\_(ツ)_/¯
lifetables:
	# View more at: https://www.ssa.gov/oact/HistEst/PerLifeTables/2017/PerLifeTables2017.html
	# wget https://www.ssa.gov/oact/HistEst/PerLifeTables/2017/PerLifeTables_M_Hist_TR2017.csv -P ./datasets/
	# wget https://www.ssa.gov/oact/HistEst/PerLifeTables/2017/PerLifeTables_F_Hist_TR2017.csv -P ./datasets/
	python manage.py lifetables ${PWD}/datasets/PerLifeTables_M_Hist_TR2017.csv ${PWD}/datasets/PerLifeTables_F_Hist_TR2017.csv ${PWD}/datasets/lifetables.csv


