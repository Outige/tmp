-- init & set db
-- DROP DATABASE IF EXISTS d811fiaile1gkm;
-- CREATE DATABASE d811fiaile1gkm;
-- \c d6o4j4vds51re5;

-- init items schema
DROP TABLE IF EXISTS items CASCADE;
CREATE TABLE items (
        id SERIAL NOT NULL, 
        title VARCHAR, 
        description VARCHAR, 
        owner_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(owner_id) REFERENCES users (id)
);

-- init users schema
DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
        id SERIAL NOT NULL,
		email VARCHAR UNIQUE,
        hashed_password VARCHAR, 
        is_active BOOLEAN DEFAULT 't', 
        PRIMARY KEY (id)
);

--users dummy data
-- INSERT INTO users VALUES (1, 'tieg@gmail.com', 'super secret password', 't');
-- INSERT INTO users VALUES (2, 'troy@gmail.com', 'super secreter password', 'f');

--items dummy data
-- INSERT INTO items VALUES (1, 'tiegs pencil', 'here lies tieg pencil', 1);
-- INSERT INTO items VALUES (2, 'tiegs pencil', 'tiegs backup pencil', 1);
-- INSERT INTO items VALUES (3, 'troys bag', 'this is troys bag', 2);