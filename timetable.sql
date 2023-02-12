CREATE TABLE note (
    id INTEGER PRIMARY KEY
    ,content TEXT
    ,created DATETIME
);

CREATE TABLE event (
    id INTEGER PRIMARY KEY
    ,title TEXT
    ,category_id INT
    ,start DATETIME
    ,end DATETIME
    ,created DATETIME
    ,updated DATETIME
);
