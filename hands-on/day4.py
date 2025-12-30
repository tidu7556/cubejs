import streamlit as st

st.title("Mongo Class Day4")
st.text("Run command: streamlit run <script_name>") #TODO: convert to display code

#TODO:
st.text("To start streamlit app:")
st.code("streamlit run <script_name>", language="bash")

#============================
# Expander and Containers
#============================

st.subheader("📦 Expander")
with st.expander("Click to expand"):
    st.write("This is content hidden by default!")
    st.code("print('Hello word')", language="python")

st.divider()

#============================
# Progress and Status
#============================

st.subheader("⏳ Progress and Status")

# progress bar:
progress = st.slider("Progress", 0, 100, 50)
st.progress(progress)

# Spinner
if st.button("Show spinner"):
    with st.spinner("Loading ..."):
        import time
        time.sleep(2)
    st.success("✨ Data Loaded !!!")

st.divider()

#============================
# Metrics (Cards)
#============================

st.subheader("📊 Metrics (dashboard cards)")

# single metric
st.metric(
    label="Temperature",
    value="25 ºC",
    delta="2 ºC"
)

st.markdown("**Temp in cities**")

# multiple metrics:

# Method 1
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="HCM",
        value="25 ºC",
        delta="2 ºC"
    )

with col2:
    st.metric(
        label="HN",
        value="13 ºC",
        delta="-2 ºC"
    )

with col3:
    st.metric(
        label="Hue",
        value="30 ºC",
        delta="5 ºC"
    )

# Method 2:

CITIES = ['TP.HCM', 'HN', 'Hue']
Temps = ["32 ºC", "13 ºC", "25 ºC"]
DELTA = ["3 ºC", "-5 ºC", "2 ºC"]

cols = st.columns(len(CITIES))

for index in range(len(CITIES)):
    with cols[index]:
        st.metric(
            label = CITIES[index],
            value = Temps[index],
            delta = DELTA[index]
        )
st.divider()

#============================
# Sidebar
#============================
st.header("⚙️ Siderbar")

st.sidebar.title("💻 Management")
st.sidebar.text("Put your settings down here")

# Option
sidebar_option = st.sidebar.selectbox(
    "Choose an option",
    ['3 months', '6 months', '1 year']
)

st.write(f"Sidebar option selected: **{sidebar_option}**")

#============================
# Form
#============================
st.subheader("📝 Form")

st.write("Submit your passport")

with st.form("my_form"):
    st.write("Passport Submission")

    name = st.text_input("Name")
    email = st.text_input("Email")
    age = st.number_input("Age", min_value = 0, max_value = 120)
    gender = st.selectbox("Gender", ['F', 'M', 'Other'])

    # Form submit button
    submitted = st.form_submit_button("Submit")

    if submitted:
        st.success("Form submitted successfully!")
        st.write("Your passport info: ")
        st.json({
            "name": name,
            "age": age,
            "email": email,
            "gender": gender
        })