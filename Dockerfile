FROM joplin-base

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["gunicorn", "joplin.wsgi:application", "--pythonpath", "/app/joplin"]
