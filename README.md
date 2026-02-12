# documentIncORM
Testing:
I used a venv for this project so that it could be easily tested and graded.

To Run:
Create database named documentinc using PostgreSQL \
use submitted sql file to initiallize tables


```
cd <location of choice>
git clone https://github.com/James-Wiley/documentIncORM.git
cd documentIncORM
```
Create .env with:
```
DB_USER=<db username>
DB_PASSWORD=<db password>
DB_NAME=documentinc
DB_HOST=localhost
DB_PORT=5432
```
(may not be exact values, but this worked for me)
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

To Stop venv:
```
deactivate
```