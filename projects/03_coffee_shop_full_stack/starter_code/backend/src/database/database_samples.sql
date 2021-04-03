-- SQLite
SELECT id, title, recipe
FROM drink;

INSERT INTO drink VALUES
(1,'Pina Colada','[{"name": "Pineapple juice", "color": "#e0f542", "parts": 2}, {"name": "Malibu", "color": "#FFFFF", "parts": 1}]'),
(2,'Coffee','[{"name": "Coffee liquer (medium-fine grind)", "color": "#a88d2c", "parts": 1}, {"name": "Water", "color": "#03adad", "parts": 3}]'),
(3,'Strawb Daquirri','[{"name": "Lime juice", "color": "#027000", "parts": 1}, {"name": "Strawberry juice", "color": "#bf415c", "parts": 2}, {"name": "Vodka", "color": "#FFFFF", "parts": 1}]');

DELETE FROM drink
WHERE id = 4