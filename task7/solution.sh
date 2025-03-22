# ==========================================================================
# 2. Перевірити правильність конфігурації за допомогою nodetool status
docker exec cassandra-3 nodetool status

# ==========================================================================
# 3. Викоритовуючи  cqlsh, створити три Keyspace з replication factor 1, 2, 3 з SimpleStrategy

docker exec cassandra-1 cqlsh -e "DROP KEYSPACE IF EXISTS factor1;"
docker exec cassandra-1 cqlsh -e "CREATE KEYSPACE factor1 WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};"
docker exec cassandra-1 cqlsh -e "DESCRIBE KEYSPACE factor1;"

docker exec cassandra-1 cqlsh -e "DROP KEYSPACE IF EXISTS factor2;"
docker exec cassandra-1 cqlsh -e "CREATE KEYSPACE factor2 WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 2};"
docker exec cassandra-1 cqlsh -e "DESCRIBE KEYSPACE factor2;"

docker exec cassandra-1 cqlsh -e "DROP KEYSPACE IF EXISTS factor3;"
docker exec cassandra-1 cqlsh -e "CREATE KEYSPACE factor3 WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 3};"
docker exec cassandra-1 cqlsh -e "DESCRIBE KEYSPACE factor3;"


# ==========================================================================
# 4. В кожному з кейспейсів створити прості таблиці 

docker exec cassandra-1 cqlsh -e "USE factor1; CREATE TABLE clouds(name text PRIMARY KEY, rating INT);"
docker exec cassandra-1 cqlsh -e "USE factor1; DESCRIBE TABLE clouds;"

docker exec cassandra-1 cqlsh -e "USE factor2; CREATE TABLE languages(name text PRIMARY KEY, rating INT);"
docker exec cassandra-1 cqlsh -e "USE factor2; DESCRIBE TABLE languages;"

docker exec cassandra-1 cqlsh -e "USE factor3; CREATE TABLE databases(name text PRIMARY KEY, rating INT);"
docker exec cassandra-1 cqlsh -e "USE factor3; DESCRIBE TABLE databases;"


# ==========================================================================
# 5. Спробуйте писати і читати в ці таблиці підключаюсь на різні ноди.
# clouds
docker exec cassandra-1 cqlsh -e "USE factor1; INSERT INTO clouds (name, rating) VALUES ('Google Clouds', 10); SELECT * FROM clouds;"

docker exec cassandra-2 cqlsh -e "USE factor1; INSERT INTO clouds (name, rating) VALUES ('Azure', 8); SELECT * FROM clouds;"

docker exec cassandra-3 cqlsh -e "USE factor1; INSERT INTO clouds (name, rating) VALUES ('AWS', 9); SELECT * FROM clouds;"

# languages
docker exec cassandra-1 cqlsh -e "USE factor2; INSERT INTO languages (name, rating) VALUES ('Scala', 10); SELECT * FROM languages;"

docker exec cassandra-2 cqlsh -e "USE factor2; INSERT INTO languages (name, rating) VALUES ('Python', 8); SELECT * FROM languages;"

docker exec cassandra-3 cqlsh -e "USE factor2; INSERT INTO languages (name, rating) VALUES ('Java', 9); SELECT * FROM languages;"

docker exec cassandra-1 cqlsh -e "USE factor2; INSERT INTO languages (name, rating) VALUES ('C#', 9); SELECT * FROM languages;"

# databases
docker exec cassandra-1 cqlsh -e "USE factor3; INSERT INTO databases (name, rating) VALUES ('PostgreSQL', 10); SELECT * FROM databases;"

docker exec cassandra-2 cqlsh -e "USE factor3; INSERT INTO databases (name, rating) VALUES ('MongoDB', 8); SELECT * FROM databases;"

docker exec cassandra-3 cqlsh -e "USE factor3; INSERT INTO databases (name, rating) VALUES ('Neo4j', 9); SELECT * FROM databases;"

docker exec cassandra-1 cqlsh -e "USE factor3; INSERT INTO databases (name, rating) VALUES ('MySQL', 8); SELECT * FROM databases;"

docker exec cassandra-2 cqlsh -e "USE factor3; INSERT INTO databases (name, rating) VALUES ('SQLite', 5); SELECT * FROM databases;"


# ==========================================================================
# 6. Вставте дані в створені таблиці і подивіться на їх розподіл по вузлах кластера для кожного з кейспесов (команда nodetool status)
docker exec cassandra-1 nodetool status factor1

docker exec cassandra-1 nodetool status factor2

docker exec cassandra-1 nodetool status factor3


# ==========================================================================
# 7. Для якогось запису з кожного з кейспейсу виведіть ноди на яких зберігаються дані
docker exec cassandra-1 nodetool getendpoints factor1 clouds "AWS"

docker exec cassandra-1 nodetool getendpoints factor2 languages "Java"

docker exec cassandra-1 nodetool getendpoints factor3 databases "MySQL"


# ==========================================================================
# 8. Відключити одну з нод. Для кожного з кейспейсів перевірити з якими рівнями consistency можемо читати та писати
docker network disconnect cassandra-net cassandra-3

docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"


# для Keyspace з replication factor 1 - CONSISTENCY ONE
docker exec cassandra-1 cqlsh -e "CONSISTENCY ONE; USE factor1; INSERT INTO clouds (name, rating) VALUES ('Oracle', 9);"
docker exec cassandra-1 cqlsh -e "CONSISTENCY ONE; USE factor1; SELECT * FROM clouds;"

# для Keyspace з replication factor 2 - CONSISTENCY ONE/TWO
# TWO
docker exec cassandra-1 cqlsh -e "CONSISTENCY TWO; USE factor2; INSERT INTO languages (name, rating) VALUES ('C#', 9);"
docker exec cassandra-1 cqlsh -e "CONSISTENCY TWO; USE factor2; SELECT * FROM languages;"

# ONE
docker exec cassandra-1 cqlsh -e "CONSISTENCY ONE; USE factor2; INSERT INTO languages (name, rating) VALUES ('Java Script', 7);"
docker exec cassandra-1 cqlsh -e "CONSISTENCY ONE; USE factor2; SELECT * FROM languages;"

# для Keyspace з replication factor 3 - CONSISTENCY ONE/TWO/THREE
# THREE
docker exec cassandra-1 cqlsh -e "CONSISTENCY THREE; USE factor3; INSERT INTO databases (name, rating) VALUES ('Snowflake', 7);"
docker exec cassandra-1 cqlsh -e "CONSISTENCY THREE; USE factor3; SELECT * FROM databases;"

# TWO
docker exec cassandra-1 cqlsh -e "CONSISTENCY TWO; USE factor3; INSERT INTO databases (name, rating) VALUES ('Databricks', 9);"
docker exec cassandra-1 cqlsh -e "CONSISTENCY TWO; USE factor3; SELECT * FROM databases;"

# ONE
docker exec cassandra-1 cqlsh -e "CONSISTENCY ONE; USE factor3; INSERT INTO databases (name, rating) VALUES ('Redis', 7);"
docker exec cassandra-1 cqlsh -e "CONSISTENCY ONE; USE factor3; SELECT * FROM databases;"


docker network connect cassandra-net cassandra-3

docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"


# ==========================================================================
# 9. Зробить так щоб три ноди працювали, але не бачили одна одну по мережі (заблокуйте чи відключити зв'язок між ними)
docker network disconnect cassandra-net cassandra-1

docker network disconnect cassandra-net cassandra-2

docker network disconnect cassandra-net cassandra-3

docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"


# ==========================================================================
# 10. Для кейспейсу з replication factor 3 задайте рівень consistency рівним 1. Виконайте по черзі запис значення з однаковим primary key, але різними іншими значенням окремо на кожну з нод (тобто створіть конфлікт)

docker exec cassandra-1 cqlsh -e "CONSISTENCY ONE; USE factor3; INSERT INTO databases (name, rating) VALUES ('Apache Cassandra', 1);"
docker exec cassandra-1 cqlsh -e "CONSISTENCY ONE; USE factor3; SELECT * FROM databases;"

docker exec cassandra-2 cqlsh -e "CONSISTENCY ONE; USE factor3; INSERT INTO databases (name, rating) VALUES ('Apache Cassandra', 2);"
docker exec cassandra-2 cqlsh -e "CONSISTENCY ONE; USE factor3; SELECT * FROM databases;"

docker exec cassandra-3 cqlsh -e "CONSISTENCY ONE; USE factor3; INSERT INTO databases (name, rating) VALUES ('Apache Cassandra', 3);"
docker exec cassandra-3 cqlsh -e "CONSISTENCY ONE; USE factor3; SELECT * FROM databases;"



# ==========================================================================
# 11. Відновіть зв'язок між нодами, і перевірте що вони знову об'єдналися у кластер. Визначте яким чином була вирішений конфлікт даних та яке значення було прийнято кластером та за яким принципом
docker network connect cassandra-net cassandra-1

docker network connect cassandra-net cassandra-2

docker network connect cassandra-net cassandra-3

docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"

sleep 10

docker exec cassandra-1 cqlsh -e "USE factor3; SELECT * FROM databases;"

docker exec cassandra-2 cqlsh -e "USE factor3; SELECT * FROM databases;"

docker exec cassandra-3 cqlsh -e "USE factor3; SELECT * FROM databases;"
