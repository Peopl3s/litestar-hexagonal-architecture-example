.DEFAULT_GOAL := help
SHELL := bash

.PHONY : run test check format db-migrate db-upgrade help

# Запускаем проект
run:
	uv run granian --interface asgi travelexhibition/main:app

# Запускаем тесты
test:
	uv run pytest
# Проверяем линтером
check:
	@echo Running project linters...
	uv run ruff check src

# Делаем автоформат
format:
	@echo Running project linters...
	uv run ruff --fix src

# Новая миграция
db-migrate:
	alembic revision --autogenerate -m "New migration"

# Применить миграции
db-upgrade:
	alembic upgrade head

# Список команд
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

ALEMBIC_CONFIG = travelexhibit/alembic.ini

check-alembic:
	@command -v alembic >/dev/null 2>&1 || { echo "Alembic is not installed. Run 'make install'."; exit 1; }

revision: check-alembic
	alembic -c $(ALEMBIC_CONFIG) revision -m '$(msg)' --autogenerate

upgrade: check-alembic
	alembic -c $(ALEMBIC_CONFIG) upgrade head

downgrade: check-alembic
	alembic -c $(ALEMBIC_CONFIG) downgrade -1
