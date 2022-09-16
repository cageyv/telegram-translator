build:
	docker build -t telegram-translator .
run:
	docker run --rm -e BOT_TOKEN telegram-translator
setup:
	./setup.sh && source env/bin/activate
local_run:
	python3 translate.py
