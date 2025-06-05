DELETE FROM statuses;
INSERT INTO statuses (status) VALUES 
  ('Available'),
  ('Sold Out'),
  ('Propagating');

DELETE FROM unitTypes;
INSERT INTO unitTypes (unit) VALUES 
  ('per pot'),
  ('per cutting'),
  ('per plant');

DELETE FROM expenseCategories;
INSERT INTO expenseCategories (category, note) VALUES 
  ('Soil', 'Soil mixes and substrates'),
  ('Pots', 'Containers of all sizes'),
  ('Fertilizer', 'Fertilizers and nutrients'),
  ('Supplies', 'Other horticultural supplies');

-- === Plants ===

DELETE FROM plants;
INSERT INTO plants (genus, species, statusID, qty, wishlist) VALUES
('Begonia', 'lichenora', 1, 4, 0),
('Begonia', 'limprichtii', 1, 2, 0),
('Begonia', 'baik', 1, 5, 0),
('Begonia', 'melanobullata', 2, 0, 1),
('Caladium', 'palaciaoanum', 1, 3, 0),
('Elaphoglossum', 'peltatum', 3, 1, 1),
('Phinaea', 'multiflora', 1, 2, 0),
('Selaginella', 'willdenowii', 1, 6, 0),
('Begonia', 'pearcei', 2, 0, 1);

-- === Sales ===

DELETE FROM sales;
INSERT INTO sales (plantID, qty, price, unitID, date, note) VALUES
(1, 1, 12.00, 1, '2024-11-15', 'Sold online'),
(3, 2, 10.00, 2, '2024-12-01', 'Farmer''s market'),
(5, 1, 15.00, 1, '2025-01-10', 'Repeat customer'),
(7, 1, 8.50, 1, '2025-02-18', 'In-person sale');

-- === Expenses ===

DELETE FROM expenses;
INSERT INTO expenses (categoryID, plantID, qty, price, date, note) VALUES
(1, 1, 1, 5.00, '2024-10-01', 'Soil mix for propagation'),
(2, 1, 3, 2.50, '2024-10-03', '3" nursery pots'),
(4, NULL, 1, 18.00, '2024-10-05', 'Humidity dome'),
(3, NULL, 1, 12.00, '2024-10-06', 'General fertilizer'),
(2, 3, 2, 5.00, '2024-11-20', 'Repotted for sale'),
(1, 5, 1, 4.75, '2024-12-01', 'Aroid soil'),
(4, NULL, 1, 9.00, '2025-01-01', 'Labels and tags');