docker-compose exec web python manage.py dumpdata --natural-foreign -e sessions -e admin -e contenttypes -e auth.Permission > initialdata.json
