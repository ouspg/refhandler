while ! pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}; do
    sleep 1
done

echo "Dumping database to /backups"
pg_dump -c -U ${POSTGRES_USER} ${POSTGRES_DB} > \
backups/postgres_$(date -u +%Y-%m-%d-%H%M).sql