-- Current schema for plant biz code, update as needed!

CREATE TABLE IF NOT EXISTS statuses (
    statusID INTEGER PRIMARY KEY AUTOINCREMENT,
    status text NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS unitTypes (
    unitID INTEGER PRIMARY KEY AUTOINCREMENT,
    unit TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS expenseCategories (
    categoryID INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT UNIQUE,
    note TEXT
);        

CREATE TABLE IF NOT EXISTS plants (
    plantID INTEGER PRIMARY KEY AUTOINCREMENT,
    genus TEXT,
    species TEXT,
    statusID INTEGER REFERENCES statuses(statusID)
        ON DELETE NO ACTION ON UPDATE CASCADE,
    qty INTEGER NOT NULL,
    wishlist INTEGER NOT NULL CHECK (wishlist IN (0, 1)),
    UNIQUE(genus, species) ON CONFLICT FAIL
);

CREATE TABLE IF NOT EXISTS sales (
    saleID INTEGER PRIMARY KEY AUTOINCREMENT,
    plantID INTEGER REFERENCES plants(plantID)
        ON DELETE NO ACTION ON UPDATE CASCADE,
    qty INTEGER NOT NULL,
    price REAL NOT NULL,
    unitID INTEGER REFERENCES unitTypes(unitID)
        ON DELETE NO ACTION ON UPDATE CASCADE,
    date TEXT,
    note TEXT
);

CREATE TABLE IF NOT EXISTS expenses (
    expenseID INTEGER PRIMARY KEY AUTOINCREMENT,
    categoryID INTEGER REFERENCES expenseCategories(categoryID)
        ON DELETE NO ACTION ON UPDATE CASCADE,
    plantID INTEGER REFERENCES plants(plantID)
        ON DELETE NO ACTION ON UPDATE CASCADE,
    qty INTEGER NOT NULL,
    price REAL NOT NULL,
    date TEXT DEFAULT (datetime('now')),
    note TEXT
);

CREATE TRIGGER IF NOT EXISTS reduce_inventory_after_sale
    AFTER INSERT ON sales
    FOR EACH ROW
    BEGIN
        UPDATE plants
        SET qty = qty - NEW.qty
        WHERE plantID = NEW.plantID;
    END;

CREATE TRIGGER IF NOT EXISTS restore_inventory_on_sale_delete
    AFTER DELETE ON sales
    FOR EACH ROW
    BEGIN
        UPDATE plants
        SET qty = qty + OLD.qty
        WHERE plantID = OLD.plantID;
    END;

CREATE TRIGGER IF NOT EXISTS increase_inventory_after_expense
    AFTER INSERT ON expenses
    FOR EACH ROW
    WHEN NEW.plantID IS NOT NULL
    BEGIN
        UPDATE plants
        SET qty = qty + NEW.qty
        WHERE plantID = NEW.plantID;
    END;