# MusiFetch
Pour utiliser le programme il faut utiliser [docker](https://www.docker.com/)
```markdown
# Créer et initier les containers
$ docker-compose build
$ docker-compose up -d

# lancer les containers
$ docker-compose run python /bin/bash


# se connecter à la bdd
$ psql -h db -U postgres MusiFetch
>MDP PAR DEFAUT : MusiFetch

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
