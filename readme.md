# Dashboard


# Run with Docker locally

Build and run:

```
docker build . --tag dashboard
docker run -p 8050:8050 --mount type=bind,source=`pwd`/data,destination=/app/data,readonly   --name dashboard    dashboard
```

Clean up:

```
docker container rm dashboard
```

