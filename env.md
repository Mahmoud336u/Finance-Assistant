/****  GET STARTED WITH YOUR TIMESCALE SERVICE  ****/

/*
SERVICE INFORMATION:

Service name:  db-14742
Database name: tsdb
Username:      tsdbadmin
Password:      wc7hlq6tqcbbuvhx
Service URL:   postgres://tsdbadmin:wc7hlq6tqcbbuvhx@pd2wimlcf3.likgkpvwch.tsdb.cloud.timescale.com:37778/tsdb?sslmode=require
Port:          37778

~/.pg_service.conf
echo "
[db-14742]
host=pd2wimlcf3.likgkpvwch.tsdb.cloud.timescale.com
port=37778
user=tsdbadmin
password=wc7hlq6tqcbbuvhx
dbname=tsdb
" >> ~/.pg_service.conf
psql -d "service=db-14742"

----------------------------------------------------------------------------

/*
 ╔╗
 
╔╝║
╚╗║

 ║║         CONNECT TO YOUR SERVICE
╔╝╚╦
╗
╚══╩╝


 ​
1. Install psql:
    https://blog.timescale.com/blog/how-to-install-psql-on-mac-ubuntu-debian-windows/

2. From your command line, run:
    psql "postgres://tsdbadmin:wc7hlq6tqcbbuvhx@pd2wimlcf3.likgkpvwch.tsdb.cloud.timescale.com:37778/tsdb?sslmode=require"
*/

----------------------------------------------------------------------------

/*
FOR MORE DOCUMENTATION AND GUIDES, VISIT	>>>--->	HTTPS://DOCS.TIMESCALE.COM/
*/

