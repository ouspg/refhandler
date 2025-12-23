while ! pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}; do
    sleep 1
done

echo "Dumping database to /backups"
pg_dump -Fc -U ${POSTGRES_USER} ${POSTGRES_DB} > \
backups/$(date -u +%Y-%m-%d-%H%M).dump

echo "Deleting database dumps older than $BACKUP_RETENTION days"
find /backups -name "*.dump" -mtime $BACKUP_RETENTION -delete