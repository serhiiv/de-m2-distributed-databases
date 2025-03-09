// Очистка бази даних
MATCH (n) DETACH DELETE n;


// Імпорт переглядів
LOAD CSV WITH HEADERS FROM 'file:///views.csv' AS row
MERGE (i:Item {name: row.Item, price: toFloat(row.price)})
MERGE (c:Customer {name: row.Customer})
MERGE (c)-[:VIEW]->(i);

// Імпорт покупок
LOAD CSV WITH HEADERS FROM 'file:///orders.csv' AS row
MERGE (i:Item {name: row.Item, price: toFloat(row.price)})
MERGE (c:Customer {name: row.Customer})
MERGE (o:Order {number: toInteger(row.Order)})
MERGE (c)-[:MADE]->(o)
MERGE (o)-[:BUY]->(i);


// Видалення переглядів, по яких відбулися покупки
MATCH (c:Customer)-[v:VIEW]->(i:Item)
WHERE exists((c)-[:MADE]->(:Order)-[:BUY]->(i))
DELETE v
RETURN count(v);


// DATA Виберемо випадковий Order
MATCH (o:Order) 
WITH DISTINCT o, rand() as r ORDER BY r LIMIT 1
RETURN o.number as order;


// -​ Знайти Items які входять в конкретний Order
MATCH (o:Order {number: 10361})-[:BUY]->(i:Item)
RETURN i.name, i.price ORDER BY i.name;


// -​ Підрахувати вартість конкретного Order
MATCH (o:Order {number: 10361})-[:BUY]->(i:Item)
RETURN o.number as order, sum(i.price) as total;


// DATA Виберемо випадковий Customer
MATCH (c:Customer)-[:MADE]->(:Order)
MATCH (c:Customer)-[:VIEW]->(:Item)
WITH DISTINCT c, rand() as r ORDER BY r LIMIT 1
RETURN c.name as customer;


// -​ Знайти всі Orders конкретного Customer
MATCH (c:Customer {name: "Euro Shopping Channel"})-[:MADE]-(o:Order)
RETURN o.number as orders 
ORDER BY o.number;


// -​ Знайти всі Items куплені конкретним Customer (через Order)
MATCH (:Customer {name: "Euro Shopping Channel"})-[:MADE]-(:Order)-[:BUY]-(i:Item)
RETURN DISTINCT i.name as items, i.price as price
ORDER BY i.name;


// -​ Знайти кількість Items куплені конкретним Customer (через Order)
MATCH (:Customer {name: "Euro Shopping Channel"})-[:MADE]-(:Order)-[:BUY]-(i:Item)
RETURN count(i) as count;


// -​ Знайти для Customer на яку суму він придбав товарів (через Order)
MATCH (:Customer {name: "Euro Shopping Channel"})-[:MADE]-(:Order)-[:BUY]-(i:Item)
RETURN sum(i.price) as sum;


// -​ Знайті скільки разів кожен товар був придбаний, відсортувати за цим значенням
MATCH (i:Item)<-[:BUY]-(:Order)
RETURN i.name as item, count(i) as count
ORDER BY count(i) DESC;


// -​ Знайти всі Items переглянуті (view) конкретним Customer
MATCH (:Customer {name: "Euro Shopping Channel"})-[:VIEW]->(i:Item)
RETURN i.name as items;


// DATA Виберемо випадковий Item, який був куплений
MATCH (i:Item)<-[:BUY]-(:Order) 
WITH DISTINCT i, rand() as r ORDER BY r LIMIT 1
RETURN i.name as item;


// -​ Знайти інші Items що купувались разом з конкретним Item (тобто всі Items що
// входять до Order-s разом з даними Item)
MATCH (:Item {name: "Classic Cars S10_1949"})<-[:BUY]-(:Order)-[:BUY]->(i:Item)
RETURN DISTINCT i.name as item;


// -​ Знайти Customers які купили даний конкретний Item
MATCH (:Item {name: "Classic Cars S10_1949"})<-[:BUY]-(:Order)<-[:MADE]-(c:Customer)
RETURN DISTINCT c.name as customer;


// -​ Знайти для певного Customer(а) товари, які він переглядав, але не купив
MATCH (c:Customer {name: "Euro Shopping Channel"})-[v:VIEW]->(i:Item)
RETURN DISTINCT i.name as item;
