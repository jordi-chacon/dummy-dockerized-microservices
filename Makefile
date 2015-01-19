all: deps build_and_run

deps:
	sudo pip install fig

build_and_run:
	sudo fig up

stop:
	sudo fig stop

