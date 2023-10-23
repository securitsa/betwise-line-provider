create-migrations:
	docker-compose -f docker/docker-compose.yml run line-provider alembic revision --autogenerate -m "$(m)"

migrations-upgrade:
	docker-compose -f docker/docker-compose.yml run line-provider alembic upgrade head

migrations-downgrade:
	docker-compose -f docker/docker-compose.yml run line-provider alembic downgrade -1

up:
	docker-compose -f docker/docker-compose.yml up

up-build:
	docker-compose -f docker/docker-compose.yml up --build

down:
	docker-compose -f docker/docker-compose.yml down

postman-tests:
	docker run --rm --network host -v $$PWD/src/tests/e2e:/etc/newman -t postman/newman:alpine run postman_tests.json \
		--environment environment_local.json \
		--working-dir test_files/

chmod-versions:
	sudo chmod -R a+w src/migrations/versions/

down-remove-volumes:
	docker-compose -f docker/docker-compose.yml down -v
