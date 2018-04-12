docker-compose exec web sh -c "python manage.py dumpdata --natural-foreign -e sessions -e admin -e contenttypes -e auth.Permission > carceropolis/carceropolis/fixtures/initialdata.json"
