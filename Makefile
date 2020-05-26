make_migr:
	docker-compose run --rm web sh -c "python manage.py makemigrations"

migr:
	docker-compose run --rm web sh -c "python manage.py migrate"

ssh_w:
	docker-compose exec web sh

m_shell:
	docker-compose run --rm web sh -c "python manage.py shell"

run_tests:
	docker-compose run --rm web sh -c "pytest"

