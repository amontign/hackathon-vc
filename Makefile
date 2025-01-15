all: build up

up:
	docker-compose -f docker-compose.yml up -d

down:
	docker-compose -f docker-compose.yml down

stop:
	docker-compose -f docker-compose.yml stop

start:
	docker-compose -f docker-compose.yml start

build:
	docker-compose -f docker-compose.yml build

clean:
	@docker stop $$(docker ps -qa) || true
	@docker rm $$(docker ps -qa) || true
	@docker rmi -f $$(docker images -qa) || true
	@docker volume rm $$(docker volume ls -q) || true
	@docker network rm $$(docker network ls -q) || true

re: clean up

prune: clean
	@docker system prune -a --volumes -f

.PHONY: all up down stop start build ng mdb wp clean re prune
