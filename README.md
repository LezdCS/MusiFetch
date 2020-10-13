# MusiFetch
Pour utiliser le programme il faut utiliser [docker](https://www.docker.com/)
```markdown
# Créer et initier les containers
$ docker-compose build
$ docker-compose up -d

# lancer le container python
$ docker-compose run python /bin/bash

# lancer le programme
$ cd src
$ python fingerprints_generator.py find:create

# se connecter à la bdd
$ export PGPASSWORD='MusiFetch'; psql -h db -U postgres MusiFetch

# afficher les tables
$ \dt
>
MusiFetch=# \dt
            List of relations
 Schema |     Name     | Type  |  Owner
--------+--------------+-------+----------
 public | fingerprints | table | postgres
 public | music        | table | postgres
(2 rows)


# tout éteindre
$ docker-compose down
```
