-- create_clients_table.sql
CREATE TABLE IF NOT EXISTS clients (
                                       id SERIAL PRIMARY KEY,
                                       url VARCHAR(255) NOT NULL
    );
