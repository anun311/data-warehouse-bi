## Step to run
1. Run Codespace on Github
2. in Terminal:
   
   2.1 cd 01-data-modeling-i
   
   2.2 docker compose up (to run file: docker-compose.yml)
   
   2.3 click on port 8080, that forward port form docker to run Adminer via PostgresSQL
   
```
cd 01-data-modeling-i
docker compose up
```
   
3. run create-table.py (to drop and create table)
```
python create-table.py
```
4. run etl.py (to drop and create table)
```
python etl.py
```
