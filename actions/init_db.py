import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

# Создание таблицы users
c.execute('''
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  phone_number TEXT UNIQUE,
  name TEXT,
  lastname TEXT,
  gender TEXT,
  age INTEGER,
  region TEXT,
  photo_url TEXT,
  location_lat FLOAT,
  location_lon FLOAT,
  role TEXT DEFAULT 'user'
)
''')

# Создание таблицы user_interests
c.execute('''
CREATE TABLE IF NOT EXISTS user_interests (
  user_id INTEGER,
  interest TEXT,
  FOREIGN KEY (user_id) REFERENCES users(id)
)
''')

# Создание таблицы events
c.execute('''
CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT,
  date TEXT,
  time TEXT,
  location TEXT,
  description TEXT,
  photo_url TEXT,
  creator_id INTEGER,
  FOREIGN KEY (creator_id) REFERENCES users(id)
)
''')

# Создание таблицы event_interests
c.execute('''
CREATE TABLE IF NOT EXISTS event_interests (
  event_id INTEGER,
  interest TEXT,
  FOREIGN KEY (event_id) REFERENCES events(id)
)
''')

# Создание таблицы friendships
c.execute('''
CREATE TABLE IF NOT EXISTS friendships (
  user_id INTEGER,
  friend_id INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, friend_id),
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (friend_id) REFERENCES users(id)
)
''')

# Создание таблицы event_participants
c.execute('''
CREATE TABLE IF NOT EXISTS event_participants (
  event_id INTEGER,
  user_id INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (event_id, user_id),
  FOREIGN KEY (event_id) REFERENCES events(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
)
''')

# Создание таблицы event_invitations
c.execute('''
CREATE TABLE IF NOT EXISTS event_invitations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id INTEGER,
  user_id INTEGER,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (event_id) REFERENCES events(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
)
''')

# Создание таблицы regions
c.execute('''
CREATE TABLE IF NOT EXISTS regions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE
)
''')

# Создание таблицы interests
c.execute('''
CREATE TABLE IF NOT EXISTS interests (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE
)
''')

conn.commit()
conn.close()

