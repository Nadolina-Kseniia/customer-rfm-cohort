DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    user_id INT PRIMARY KEY,
    signup_date TIMESTAMP
);

CREATE TABLE transactions (
    tx_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    tx_date TIMESTAMP,
    amount INT
);