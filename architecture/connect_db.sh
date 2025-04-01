source .env
export PGPASSWORD=$DB_PASSWORD
sqlcmd -S c16-trenet-rds.c57vkec7dkkx.eu-west-2.rds.amazonaws.com -U $DB_USERNAME -P $DB_PASSWORD -C
