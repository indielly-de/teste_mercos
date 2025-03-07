build:
	docker-compose up -d --build

stop:
	docker-compose stop

run:
	docker-compose start

format:
	isort src && black src

kill:
	docker-compose down
	docker system prune --volumes -f
	docker rmi teste_mercos_api

setup:
	cp local.env .env

test:
	pytest tests/