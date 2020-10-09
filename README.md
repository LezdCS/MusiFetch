# MusiFetch
Pour utiliser le programme il faut utiliser [docker](https://www.docker.com/)
```markdown
# Créer et initier les containers
$ docker-compose build
$ docker-compose up -d

# lancer le shell WSL
$ docker-compose run python /bin/bash

# se connecter à la bdd
$ psql -h db -U postgres MusiFetch
>MDP PAR DEFAUT : MusiFetch
MusiFetch=# \dt
            List of relations
 Schema |     Name     | Type  |  Owner
--------+--------------+-------+----------
 public | fingerprints | table | postgres
 public | music        | table | postgres
(2 rows)



# afficher les tables
$ \dt

# shutdown les containers
$ docker-compose down
```
