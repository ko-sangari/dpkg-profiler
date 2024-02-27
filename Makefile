
coffee:
	@printf 'Be Happy Even if Things Aren’t Perfect Now. 🎉🎉🎉\n'
	@printf 'Enjoy your coffee! ☕\n'

dev:
	@docker compose -f docker-compose.yaml up --build

run:
	@docker compose -f docker-compose.yaml up --build -d

down:
	@docker compose -f ./docker-compose.yaml down --remove-orphans

shell:
	@docker exec -it dpkg_profiler_fastapi bash

packages:
	@docker exec -it dpkg_profiler_fastapi poetry run python /home/app/src/utils/parser.py

tests:
	@docker exec -it dpkg_profiler_fastapi poetry run pytest

coverage:
	@docker exec -it dpkg_profiler_fastapi poetry run coverage run -m pytest
	@docker exec -it dpkg_profiler_fastapi poetry run coverage report

mypy:
	@docker exec -it dpkg_profiler_fastapi poetry run mypy --config-file mypy.ini --explicit-package-bases .

.PHONY: coffee dev run down shell packages tests coverage mypy
