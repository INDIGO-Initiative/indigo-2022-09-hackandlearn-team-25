# Dashboard


## Run with Docker locally

Build and run:

```
docker build . --tag dashboard
docker run -p 8050:8050 --mount type=bind,source=`pwd`/data,destination=/app/data,readonly   --name dashboard    dashboard
```

Clean up:

```
docker container rm dashboard
```

## Deploy with Dokku

Set up volume & app, configure:

```
dokku apps:create golabteam26
dokku git:set golabteam26 deploy-branch main
dokku storage:ensure-directory golabteam26
dokku storage:mount golabteam26 /var/lib/dokku/data/storage/golabteam26:/app/data
dokku proxy:ports-add golabteam26 http:80:8050
```

Copy data file to server from laptop:

```
scp data/research-projects-database.sqlite  root@dokku-live-2.dokku.opendataservices.uk0.bigv.io:/var/lib/dokku/data/storage/golabteam26
```

To deploy:

```
dokku git:sync --build   golabteam26   https://github.com/INDIGO-Initiative/indigo-2022-09-hackandlearn-team-26.git
```

To clean up:

```
dokku apps:destroy golabteam26
rm -rf /var/lib/dokku/data/storage/golabteam26
```
