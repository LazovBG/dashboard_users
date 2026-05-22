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

if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None

# UI частта
init_db()
st.title("🗂️ Lazov Tools")

if not st.session_state.user_id:
  #st.header("Вход или регистрация")
  tab1, tab2 = st.tabs(["Вход", "Регистрация"])

  with tab1:
    st.header("Вход")
    username = st.text_input("Име на потребителя:")
    password = st.text_input("Парола:", type="password")
    if st.button("Вход"):
      user = login_user(username, password)  
      if user:
        st.success(f"Welcome, {user[1]}!")
        st.session_state.user_id = user[0]
        st.session_state.username = user[1]
        st.rerun()
      else:
        st.error("Invalid username or password")
  
   

  with tab2:
    st.header("Регистрация")
    username = st.text_input("Име на потребителя:", key="reg_username")
    password = st.text_input("Парола:", type="password", key="reg_password")
    email = st.text_input("Електронна поща:")
    if st.button("Регистрация"):
      register_user(username, password, email)
      st.success("Регистрацията е успешна!")
else:
  
  
  col1, col2 = st.columns([4, 1])
  col1.header(f"Добре дошъл, {st.session_state.username} 👋")
  col1.button("Изход") # бутонът за изход вдясно
  if col2.button("Изход"):
    st.session_state.user_id = None
    st.session_state.username = None
    st.rerun()
