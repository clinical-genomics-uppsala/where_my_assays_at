# where_my_assays_at

### ddPCR database service

Simple django app to handle ddPCR assay design and order. It is using a PostgreSQL database backend.

## Dependencies

- [python3](https://www.python.org/) >= 3.8.5 
- [Django](https://www.djangoproject.com/) >= 3.1.7
- [django_components](https://pypi.org/project/django-components/) >= 0.14
- [django-computed-property](https://django-computed-property.readthedocs.io/en/latest/) >= 0.3.0
- [django-widget-tweaks](https://pypi.org/project/django-widget-tweaks/) >= 1.4.8
- [psycopg2](https://www.psycopg.org/) >= 2.8.6
- [docker](https://www.docker.com/) >= 20.10.2

## Development

First, setup the postgres database server as a docker container. Start by creating a directory `db`
in your local repository's root directory (it will be ignored by `git`). Now start the container like
so:

```
docker run -d \
  --name dev-postgres \
  -e POSTGRES_PASSWORD=notsosecret \
  -v /Path/to/repo/db:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres
```

Next, we need to add the database to hold our data. `Exec` into the postgres container via the `psql`
command:

```
docker exec -i -u postgres dev-postgres psql
```

Once you attached, run the following to create the database, check if you were successful and to quit:

```psql
CREATE DATABASE ddpcr;
\l+
\q
```

Finally, migrate your database structure and start your development server like this:

```
python mysite/manage.py migrate
python mysite/manage.py runserver
```

You can add some mock data via the `psql` interface or the admin web interface at `localhost:8000/admin`.
