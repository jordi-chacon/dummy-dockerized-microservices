all: deps build_and_run

deps:
	sudo pip install fig

build_and_run: duplicate_common
	sudo fig up

duplicate_common:
	echo components/*_service/src/ | xargs -n 1 cp -r components/common

stop:
	sudo fig stop

