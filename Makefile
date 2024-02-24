init:
	test -n "$(name)"
	rm -rf ./.git
	find ./ -type f -exec perl -pi -e 's/aunar_welfare/$(name)/g' *.* {} \;
	mv ./aunar_welfare ./$(name)

superuser:
	docker exec -it aunar_welfare ./manage.py createsuperuser

shell:
	docker exec -it aunar_welfare ./manage.py shell

makemigrations:
	docker exec -it aunar_welfare ./manage.py makemigrations

migrate:
	docker exec -it aunar_welfare ./manage.py migrate

initialfixture:
	docker exec -it aunar_welfare ./manage.py loaddata initial

testfixture:
	docker exec -it aunar_welfare ./manage.py loaddata test

test:
	docker exec -it aunar_welfare ./manage.py test

statics:
	docker exec -it aunar_welfare ./manage.py collectstatic --noinput

makemessages:
	docker exec -it aunar_welfare django-admin makemessages

compilemessages:
	docker exec -it aunar_welfare django-admin compilemessages
