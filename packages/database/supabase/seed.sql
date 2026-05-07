insert into public.equities (ticker, name, exchange, commodity_focus) values
  ('COALINDIA', 'Coal India Ltd', 'NSE', 'Coal'),
  ('NMDC', 'NMDC Ltd', 'NSE', 'Iron Ore'),
  ('HINDALCO', 'Hindalco Industries Ltd', 'NSE', 'Aluminium'),
  ('VEDL', 'Vedanta Ltd', 'NSE', 'Base Metals'),
  ('JSWSTEEL', 'JSW Steel Ltd', 'NSE', 'Steel'),
  ('TATASTEEL', 'Tata Steel Ltd', 'NSE', 'Steel'),
  ('HINDZINC', 'Hindustan Zinc Ltd', 'NSE', 'Zinc'),
  ('HINDCOPPER', 'Hindustan Copper Ltd', 'NSE', 'Copper')
on conflict (ticker) do nothing;
