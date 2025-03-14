// The function to use as the prompt.
prompt = function () { return `\n\n${db.getName()} > `; };

// The current database to use.
use("task3");

// delete all collections
db.items.drop();
db.orders.drop();

// The current collection to use.   
db.createCollection("items");

// Insert some sample data.
db.items.insertMany([
    { "_id": 1, "category": "Phone", "model": "Galaxy S6", "producer": "Samsung", "price": 500 },
    { "_id": 2, "category": "Phone", "model": "iPhone 6", "producer": "Apple", "price": 600 },
    { "_id": 3, "category": "Phone", "model": "Lumia 950", "producer": "Microsoft", "price": 400 },
    { "_id": 4, "category": "Tablet", "model": "iPad Air 2", "producer": "Apple", "price": 500 },
    { "_id": 5, "category": "Tablet", "model": "Galaxy Tab S2", "producer": "Samsung", "price": 400 },
    { "_id": 6, "category": "Tablet", "model": "Surface Pro 4", "producer": "Microsoft", "price": 600 },
    { "_id": 7, "category": "Laptop", "model": "MacBook Pro", "producer": "Apple", "price": 1200 },
    { "_id": 8, "category": "Laptop", "model": "ThinkPad X1 Carbon", "producer": "Lenovo", "price": 1130 },
    { "_id": 9, "category": "PowerBank", "model": "iPower W14", "producer": "Apple", "price": 140 }
]);

// Напишіть запит, який виводіть усі товари (відображення у JSON)
db.items.find({});

// Підрахуйте скільки є різних категорій товарів
db.items.distinct('category').length;

// Виведіть список всіх виробників товарів без повторів
db.items.distinct('producer');

// Оновить певні товари, змінивши існуючі значення і додайте нові властивості (характеристики) усім товарам за певним критерієм
// Наприклад, зменшити ціну на 5% та додайте поле discount зі значенням 5%
db.items.updateMany({ "producer": "Microsoft" }, { "$mul": { "price": 0.95 }, "$set": { "discount": 0.05 } });

// Знайдіть товари у яких є (присутнє поле) певні властивості
db.items.find({ "discount": { "$exists": true } });

// Товари ви додаєте в замовлення - orders, яке містити вартість, ім'я замовника, і адресу доставки.
// Товари (items) в замовленні (order) повинні бути представлені у вигляді references, а замовник (customer) у вигляді embed
// Створіть колекцію orders з різними наборами items, але так щоб один з товарів був у декількох замовленнях
db.createCollection("orders");
db.orders.insertMany([{
    "order_number": 20151401,
    "date": new Date("2015-04-14"),
    "total_sum": 2300,
    "customer": {
        "name": "Andrii",
        "surname": "Rodinov",
        "phones": [380679876543, 380501234567],
        "address": "PTI, Peremohy 37, Kyiv, UA"
    },
    "payment": {
        "card_owner": "Andrii Rodionov",
        "cardId": 1234567812345678
    },
    "items_id": [2, 4, 7]
},
{
    "order_number": 20151501,
    "date": new Date("2015-04-15"),
    "total_sum": 1500,
    "customer": {
        "name": "Ivan",
        "surname": "Ivanov",
        "phones": [380672534567],
        "address": "Peremohy 13, Kyiv, UA"
    },
    "payment": {
        "card_owner": "Ivan Ivanov",
        "cardId": 1234567856781234
    },
    "items_id": [4, 5, 6]
},
{
    "order_number": 20151502,
    "date": new Date("2015-04-15"),
    "total_sum": 1130,
    "customer": {
        "name": "Ivan",
        "surname": "Ivanov",
        "phones": [380672534567],
        "address": "Peremohy 13, Kyiv, UA"
    },
    "payment": {
        "card_owner": "Ivan Ivanov",
        "cardId": 1234567856781234
    },
    "items_id": [8]
}
]);


// Виведіть всі замовлення
db.orders.find({});

// Знайдіть всі замовлення з певним товаром (товарами) (шукати можна по ObjectId)
db.orders.find({ "items_id": 4 });

// Додайте в усі замовлення з певним товаром ще один товар і збільште існуючу вартість замовлення на деяке значення Х
db.orders.updateMany({ "items_id": 4 }, { "$push": { "items_id": 8 }, "$inc": { "total_sum": 140 } });
db.orders.find({ "items_id": 4 });

// Виведіть тільки інформацію про кастомера і номери кредитної карт, для замовлень вартість яких перевищує певну суму
db.orders.find({ "total_sum": { "$gt": 1600 } }, { "_id": 0, "customer": 1, "payment.cardId": 1 });

// У замовлені підставити замість ObjectId("***") назви товарів
db.createView("orders_view", "orders", [
    {
        "$lookup": {
            "from": "items",
            "localField": "items_id",
            "foreignField": "_id",
            "as": "items"
        }
    }
]);

// Знайдіть замовлення зроблені одним замовником, і виведіть тільки інформацію про кастомера та товари
db.orders_view.find({ "customer.name": "Ivan" }, { "_id": 0, "customer": 1, "items": 1 });



// Створіть Сapped collection яка б містила 5 останніх відгуків на наш інтернет-магазин. Структуру запису визначіть самостійно.
db.createCollection("reviews", { "capped": true, "size": 1024, "max": 5 });
db.reviews.insertMany([
    { "name": "Ivan Ivanov", "text": "Good service 1" },
    { "name": "Petro Petrov", "text": "Baaaaaaaaaaaaaaaad service" },
    { "name": "Andrii Andriev", "text": "Good service 3" },
    { "name": "Sergii Sergiev", "text": "Good service 4" },
    { "name": "Vasyl Vasyliev", "text": "Good service 5" },
    { "name": "Ivan Ivanov", "text": "Good service 6" }
]);
db.reviews.find({}, { "_id": 0 });

// Перевірте що при досягненні обмеження старі відгуки будуть затиратись
db.reviews.insertOne({ "name": "Petro Petrov", "text": "The last message" });
db.reviews.find({}, { "_id": 0 });
