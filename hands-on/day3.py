# installs streamlit:
# pip install streamlit
# uv add streamlit


# === install lib ===
import streamlit as st
from datetime import datetime, date
import random
# if you don't have this lib, install it
# pip install pandas
# uv add pandas
import pandas as pd

# ===================
# streamlit basic text and title
# ===================

st.title("Welcome to our finance-tracker app")
st.header("This is header")
st.subheader("This is subheader")
st.text("This is simple text")
st.markdown("**This is bold text**")
st.markdown("*This is italic text*")

st.divider() # add horizontal line

# ===============
# Display data
# ===============

st.header("This is section to display data")

# Display dictionary
st.subheader("Display dictionary")

category = {
    "type": "Income",
    "category": "Shopping",
    "amount": "5$"
}
st.write(category)

# Display list
st.subheader("Display list")

collections = ['categories', 'users', 'budgets']
st.write(collections)

# Display Dataframe
st.subheader("Display dataframe")

data = []
for i in range(10):
    item = {
        "id": i+1,
        "sex": random.choice(['F', 'M']),
        "age": random.randint(3, 50)
    }
    data.append(item)

df = pd.DataFrame(data)

st.markdown("**Interactive table**")
st.dataframe(df) # interactive table

st.markdown("**Static table**")
st.table(df) # static table

# =========
# User widget input
# ============

# Text input
st.subheader("Text input")
name = st.text_input("What's your name", placeholder = "Enter your name")
if name:
    st.write(f"Hello {name}")

# Number input:
st.subheader("Number Input")
number = st.number_input("How old are you?", placeholder = "Enter a positive number")
if number:
    st.write(f"You are {number} years old")

# Slider
st.subheader("Slider Input")
my_slide = st.slider("Select a current temperature", min_value = -10, max_value = 50, value = 20)
st.write(f"Current temperature is {my_slide} Celsius")

# option
option = st.selectbox("Choose your Domain?", ["Education", "Technology", "Marketing"])
if option:
    st.write(f"Your option: {option}")

st.divider()

# ======
# Break playground: App CALCULATION
# ======

st.subheader("====My Calculation app===")
number_1 = st.number_input("Input your first number")
number_2 = st.number_input("Input your second number")
operation = st.selectbox("Choose your operation?", ["+", "-", "x", ":"])

# calculating:
if operation == "+":
    result = number_1 + number_2
elif operation == "-":
    result = number_1 - number_2
elif operation == "x":
    result = number_1 * number_2
elif operation == ":" and number_2 != 0:
    result = number_1/number_2
else:
    result = "Invalid operation"

st.write(f"Result of {number_1} {operation} {number_2} = {result}")

# ======= 
# Buttons and Actions
# ======

st.header("Button and Action")

# divide page into three columns
col1, col2, col3  = st.columns(3)

with col1:
    if st.button("Click Me"):
        st.success("You clicked!")
        st.balloons() # funny effect

with col2:
    if st.button("Show failed"):
        st.error("Message error !")
    
with col3:
    if st.button("Show warning"):
        st.warning("Message warning !")

st.divider()