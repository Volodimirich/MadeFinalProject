db = db.getSiblingDB('main')

db.createUser({
    user: 'user',
    pwd: 'user',
    roles: [
        {
            role: 'root',
            db: 'admin',
        },
    ],
});
