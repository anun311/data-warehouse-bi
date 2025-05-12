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
   
3. run create-table.py (to drop and create table with structured databased)
```
python create-table.py
```
4. run etl.py (to drop and create table)
```
python etl.py
```
## Data Structured

Relationship

![image](https://github.com/user-attachments/assets/11631f95-53df-41c7-9a72-f92d01c4d50e)

ER Diagram

![image](https://github.com/user-attachments/assets/d2f24c51-db46-49db-8331-5b5a9a5b7d9b)
