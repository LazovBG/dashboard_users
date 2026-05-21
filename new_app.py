import streamlit as st
import requests
import sqlite3
import bcrypt

# ===== DATABASE =====
def init_db():
  conn = sqlite3.connect("lazov_tools.db")
  cursor = conn.cursor()
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE NOT NULL,
      password TEXT NOT NULL,
      email TEXT 
    )
  """)

  cursor.execute("""
      CREATE TABLE IF NOT EXISTS tasks (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          user_id INTEGER NOT NULL,
          title TEXT NOT NULL,
          done INTEGER DEFAULT 0
      )
  """)

  conn.commit()
  conn.close()

def register_user(username, password, email):
  # хешира паролата и записва потребителя
  conn = sqlite3.connect("lazov_tools.db")
  cursor = conn.cursor()
  hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
  cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, hashed_password, email))
  conn.commit()
  conn.close()

def login_user(username, password):
  # проверява дали потребителят съществува и паролата е вярна
  conn = sqlite3.connect("lazov_tools.db")
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
  user = cursor.fetchone()
  conn.close()
  if user and bcrypt.checkpw(password.encode("utf-8"), user[2]):
    return user
  return False



# UI частта
st.title("🗂️ Lazov Tools")

if not st.session_state.user_id:
  #st.header("Вход или регистрация")
  tab1, tab2 = st.tabs(["Вход", "Регистрация"])

  with tab1:
    st.header("Вход")
    pass


  with tab2:
    st.header("Регистрация")
    pass
