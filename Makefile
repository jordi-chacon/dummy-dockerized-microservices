all: deps build_and_run

deps:
	sudo pip install fig

build_and_run: duplicate_common
	sudo fig up

duplicate_common:
	cp -r components/common components/*_service/src/

stop:
	sudo fig stop

