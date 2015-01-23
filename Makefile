all: deps build_and_run

deps:
	sudo pip install fig

build_and_run: duplicate_common replace_env_in_fig
	sudo fig up

duplicate_common:
	echo components/*_service/src/ | xargs -n 1 cp -r components/common

replace_env_in_fig: env clean_fig
	mv fig.yml fig.yml.bup
	bash -ac '. ./env; envsubst < fig.yml.bup > fig.yml'

clean_fig:
	-mv fig.yml.bup fig.yml

stop:
	sudo fig stop

