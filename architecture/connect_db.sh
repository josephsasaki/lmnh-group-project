source .env
export PGPASSWORD=$DB_PASSWORD
sqlcmd -S $DB_ENDPOINT -U $DB_USERNAME -P $DB_PASSWORD -d $DB_NAME -C
