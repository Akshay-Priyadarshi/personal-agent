CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS expense_categories (
    id TEXT PRIMARY KEY DEFAULT uuid_generate_v1()::TEXT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS expenses (
    id TEXT PRIMARY KEY DEFAULT uuid_generate_v1()::TEXT,
    description TEXT NOT NULL,
    amount NUMERIC NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    category_id TEXT NOT NULL
);

ALTER TABLE expenses ADD FOREIGN KEY (category_id) REFERENCES expense_categories(id);
