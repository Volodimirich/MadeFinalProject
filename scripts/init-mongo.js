db_test = db.getSiblingDB('test')
db_main = db.getSiblingDB('main')

db_test.createUser({
    user: 'user',
    pwd: 'user',
    roles: [
        {
            role: 'root',
            db: 'admin',
        },
    ],
});

db_main.createUser({
    user: 'user',
    pwd: 'user',
    roles: [
        {
            role: 'root',
            db: 'admin',
        },
    ],
});
