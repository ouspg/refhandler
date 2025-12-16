# Postgres

## Backups

The Postgres database container uses the script `/postgres/dump_database.sh`
to backup the database into a dump file in two ways:

1. When the docker stack is started using post_start
2. Every 24h using the deck-chores container (can changed in the compose file under `postgres/labels/deck-chores.dump-database.interval`)

### Backup retention

Database dumps older than `$BACKUP_RETENTION` will be deleted when the script is run (default 30 days, can be changed in the `.env` file).

### Restoring backups

```bash
# Start the docker compose stack
docker compose up

# Open a bash shell inside the postgres container
docker compose exec postgres bash

# Restore a database dump
# --clean allows the dump to be restored on top of an existing database
cd /backups
pg_restore -U $POSTGRES_USER -d $POSTGRES_DB --clean dumpname.dump
```
