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

db.createUser({
    user: "mongodb_exporter",
    pwd: "s3cr3tpassw0rd",
    roles: [
        { role: "clusterMonitor", db: "admin" },
        { role: "read", db: "local" }
    ]
})
