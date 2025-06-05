-- Disable FK checks for safe deletion
PRAGMA foreign_keys = OFF;

-- Clear dependent tables first to avoid FK errors
DELETE FROM expenses;
DELETE FROM sales;

-- Then clear base tables
DELETE FROM plants;
DELETE FROM statuses;
DELETE FROM unitTypes;
DELETE FROM expenseCategories;

-- Reset autoincrement counters (optional)
DELETE FROM sqlite_sequence WHERE name IN (
    'plants',
    'sales',
    'expenses',
    'statuses',
    'unitTypes',
    'expenseCategories'
);

-- Re-enable foreign key enforcement
PRAGMA foreign_keys = ON;