.DEFAULT_GOAL := help
SHELL := bash

.PHONY : run test check format db-migrate db-upgrade help

# Запускаем проект
run:
	uv run granian --interface asgi src/app:app

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
