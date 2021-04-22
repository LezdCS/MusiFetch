# MusiFetch

# [PROJECT ARCHIVED, IT WAS A SCHOOL PROJECT, NOT KEEPING IT UP TO DATE ANYMORE] 
Pour utiliser le programme il faut utiliser [docker](https://www.docker.com/)
```markdown
# Build les images
$ docker-compose build


# lancer les containers
$ docker-compose up

# Accès au shell du container
$ docker-compose exec [id De l'image docker]

## se connecter à la bdd
$ export PGPASSWORD='MusiFetch'; psql -h db -U postgres MusiFetch

## afficher les tables
$ \dt
>
MusiFetch=# \dt
            List of relations
 Schema |     Name     | Type  |  Owner
--------+--------------+-------+----------
 public | fingerprints | table | postgres
 public | music        | table | postgres
(2 rows)


# stopper les containers
$ docker-compose stop

# supprimer les containers
$ docker-compose down
```

