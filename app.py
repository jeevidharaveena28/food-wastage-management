import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt


st.title("Local Food Wastage Management System")
st.write("Welcome to the Food Wastage Management Dashboard")


try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="270422",
        database="food_wastage"
    )

    st.success("Database Connected Successfully!")

except Exception as e:
    st.error(f"Connection Error: {e}")
    st.stop()

providers_count = pd.read_sql(
    "SELECT COUNT(*) AS cnt FROM providers", conn
)

receivers_count = pd.read_sql(
    "SELECT COUNT(*) AS cnt FROM receivers", conn
)

food_count = pd.read_sql(
    "SELECT COUNT(*) AS cnt FROM food_listings", conn
)

claims_count = pd.read_sql(
    "SELECT COUNT(*) AS cnt FROM claims", conn
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Providers", providers_count["cnt"][0])
col2.metric("Receivers", receivers_count["cnt"][0])
col3.metric("Food Listings", food_count["cnt"][0])
col4.metric("Claims", claims_count["cnt"][0])

menu = st.sidebar.selectbox(
    "Select Option",
    [
        "Dashboard",
        "Providers",
        "Receivers",
        "Food Listings",
        "Claims",
        "Provider Contacts",
        "SQL Queries"
    ]
)

if menu == "Dashboard":
    st.write("Dashboard")

elif menu == "Providers":
    df = pd.read_sql("SELECT * FROM providers", conn)
    st.dataframe(df)

elif menu == "Receivers":
    df = pd.read_sql("SELECT * FROM receivers", conn)
    st.dataframe(df)

elif menu == "Food Listings":

    df = pd.read_sql("SELECT * FROM food_listings", conn)

    
    city = st.selectbox(
        "Select City",
        ["All"] + list(df["Location"].unique()),
        key="city_filter"
    )

    provider = st.selectbox(
        "Select Provider Type",
        ["All"] + list(df["Provider_Type"].unique()),
         key="provider_filter"

    )

    
    food_type = st.selectbox(
        "Select Food Type",
        ["All"] + list(df["Food_Type"].unique()),
        key="food_type_filter"
    )

    
    meal_type = st.selectbox(
        "Select Meal Type",
        ["All"] + list(df["Meal_Type"].unique()), 
        key="meal_type_filter"
    )

    
    if city != "All":
        df = df[df["Location"] == city]

    if provider != "All":
        df = df[df["Provider_Type"] == provider]

    if food_type != "All":
        df = df[df["Food_Type"] == food_type]

    if meal_type != "All":
        df = df[df["Meal_Type"] == meal_type]

    st.dataframe(df)

elif menu == "Claims":

    df = pd.read_sql(
        "SELECT * FROM claims",
        conn
    )

    st.subheader("Claims")
    st.dataframe(df)

elif menu == "Provider Contacts":

    provider_df = pd.read_sql(
        "SELECT Provider_ID, Name, Contact, City FROM providers",
        conn
    )
     
    st.subheader("Provider Contact Details")
    st.dataframe(provider_df)

elif menu == "SQL Queries":

    st.subheader("SQL Query Results")

    query_option = st.selectbox(
        "Choose Query",
        [
            "Providers by City",
            "Receivers by City",
            "Food Type Count",
            "Meal Type Count",
            "Claim Status Count",
            "Top Food Donors",
            "Total Food Quantity",
            "Providers by Type",
            "Food Listings by City",
            "Available Food by Meal Type",
            "Available Food by Food Type",
            "Top Cities by Food Quantity",
            "Total Claims",
            "Completed Claims",
            "Pending Claims"
        ]
    )

    if query_option == "Providers by City":

        result = pd.read_sql("""
        SELECT City,
               COUNT(*) AS Total_Providers
        FROM providers
        GROUP BY City
        """, conn)

        st.dataframe(result)

    elif query_option == "Receivers by City":

        result = pd.read_sql("""
        SELECT City,
               COUNT(*) AS Total_Receivers
        FROM receivers
        GROUP BY City
        """, conn)

        st.dataframe(result)

    elif query_option == "Food Type Count":

        result = pd.read_sql("""
        SELECT Food_Type,
               COUNT(*) AS Total
        FROM food_listings
        GROUP BY Food_Type
        """, conn)

        st.dataframe(result)    

    elif query_option == "Meal Type Count":

        result = pd.read_sql("""
        SELECT Meal_Type,
           COUNT(*) AS Total
        FROM food_listings
        GROUP BY Meal_Type
        """, conn)

        st.dataframe(result)

    elif query_option == "Claim Status Count":

        result = pd.read_sql("""
        SELECT Status,
           COUNT(*) AS Total
        FROM claims
        GROUP BY Status
        """, conn)

        st.dataframe(result)

    elif query_option == "Top Food Donors":

        result = pd.read_sql("""
        SELECT Provider_ID,
           SUM(Quantity) AS Total_Donated
        FROM food_listings
        GROUP BY Provider_ID
        ORDER BY Total_Donated DESC
        LIMIT 10
        """, conn)

        st.dataframe(result)

    elif query_option == "Total Food Quantity":

         result = pd.read_sql("""
         SELECT SUM(Quantity) AS Total_Food
         FROM food_listings
         """, conn)

         st.dataframe(result)

    elif query_option == "Providers by Type":

        result = pd.read_sql("""
        SELECT Provider_Type,
           COUNT(*) AS Total
        FROM food_listings
        GROUP BY Provider_Type
        """, conn)

        st.dataframe(result)

    elif query_option == "Food Listings by City":

        result = pd.read_sql("""
        SELECT Location,
           COUNT(*) AS Total_Listings
        FROM food_listings
        GROUP BY Location
        ORDER BY Total_Listings DESC
        """, conn)

        st.dataframe(result)

    elif query_option == "Available Food by Meal Type":

        result = pd.read_sql("""
        SELECT Meal_Type,
           SUM(Quantity) AS Total_Quantity
        FROM food_listings
        GROUP BY Meal_Type
        """, conn)

        st.dataframe(result)

    elif query_option == "Available Food by Food Type":

        result = pd.read_sql("""
        SELECT Food_Type,
           SUM(Quantity) AS Total_Quantity
        FROM food_listings
        GROUP BY Food_Type
        """, conn)

        st.dataframe(result)

    elif query_option == "Top Cities by Food Quantity":

        result = pd.read_sql("""
        SELECT Location,
           SUM(Quantity) AS Total_Quantity
        FROM food_listings
        GROUP BY Location
        ORDER BY Total_Quantity DESC
        LIMIT 10
        """, conn)

        st.dataframe(result)

    elif query_option == "Total Claims":

        result = pd.read_sql("""
        SELECT COUNT(*) AS Total_Claims
        FROM claims
        """, conn)

        st.dataframe(result)

    elif query_option == "Completed Claims":

        result = pd.read_sql("""
        SELECT COUNT(*) AS Completed_Claims
        FROM claims
        WHERE Status = 'Completed'
        """, conn)

        st.dataframe(result)

    elif query_option == "Pending Claims":

        result = pd.read_sql("""
        SELECT COUNT(*) AS Pending_Claims
        FROM claims
        WHERE Status = 'Pending'
        """, conn)

        st.dataframe(result)

if menu == "Dashboard":

    st.subheader("Food Type Distribution")

    food_chart = pd.read_sql("""
    SELECT Food_Type, COUNT(*) AS Total
    FROM food_listings
    GROUP BY Food_Type
    """, conn)

    st.bar_chart(food_chart.set_index("Food_Type"))

    st.subheader("Top Cities by Food Listings")

    city_chart = pd.read_sql("""
    SELECT Location, COUNT(*) AS Total
    FROM food_listings
    GROUP BY Location
    ORDER BY Total DESC
    LIMIT 10
    """, conn)

    st.bar_chart(city_chart.set_index("Location"))

    st.subheader("Claim Status Distribution")

    claim_chart = pd.read_sql("""
    SELECT Status, COUNT(*) AS Total
    FROM claims
    GROUP BY Status
    """, conn)

    st.bar_chart(claim_chart.set_index("Status"))

    st.subheader("Food Contribution by Provider Type")

    provider_chart = pd.read_sql("""
    SELECT Provider_Type,
    SUM(Quantity) AS Total_Quantity
    FROM food_listings
    GROUP BY Provider_Type
    """, conn)

    st.bar_chart(provider_chart.set_index("Provider_Type"))

    st.subheader("Food Type Share")

    food_share = pd.read_sql("""
    SELECT Food_Type,
    COUNT(*) AS Total
    FROM food_listings
    GROUP BY Food_Type
    """, conn)

    fig, ax = plt.subplots()

    ax.pie(
        food_share["Total"],
        labels=food_share["Food_Type"],
        autopct="%1.1f%%"
    )

    st.pyplot(fig)

# -----------------------------
# PROVIDERS
# -----------------------------
elif menu == "Providers":

    df = pd.read_sql(
        "SELECT * FROM providers",
        conn
    )

    st.subheader("Providers")
    st.dataframe(df)

# -----------------------------
# RECEIVERS
# -----------------------------
elif menu == "Receivers":

    df = pd.read_sql(
        "SELECT * FROM receivers",
        conn
    )

    st.subheader("Receivers")
    st.dataframe(df)

# -----------------------------
# FOOD LISTINGS
# -----------------------------
elif menu == "Food Listings":

    df = pd.read_sql(
        "SELECT * FROM food_listings",
        conn
    )

    df.columns = df.columns.str.strip()

    st.subheader("Food Listings")

    # City Filter
    city = st.selectbox(
        "Select City",
        ["All"] + list(df["Location"].unique())
    )

    # Food Type Filter
    food_type = st.selectbox(
        "Select Food Type",
        ["All"] + list(df["Food_Type"].unique())
    )

    # Meal Type Filter
    meal_type = st.selectbox(
        "Select Meal Type",
        ["All"] + list(df["Meal_Type"].unique())
    )

    # Apply Filters
    if city != "All":
        df = df[df["Location"] == city]

    if food_type != "All":
        df = df[df["Food_Type"] == food_type]

    if meal_type != "All":
        df = df[df["Meal_Type"] == meal_type]

    st.dataframe(df)

# -----------------------------
# CLAIMS
# -----------------------------
elif menu == "Claims":

    df = pd.read_sql(
        "SELECT * FROM claims",
        conn
    )

    st.subheader("Claims")
    st.dataframe(df)

# -----------------------------
# PROVIDER CONTACTS
# -----------------------------
elif menu == "Provider Contacts":

    provider_df = pd.read_sql(
        """
        SELECT Provider_ID,
               Name,
               Contact,
               City
        FROM providers
        """,
        conn
    )

    st.subheader("Provider Contact Details")

    provider_name = st.selectbox(
        "Select Provider",
        provider_df["Name"]
    )

    details = provider_df[
        provider_df["Name"] == provider_name
    ]

    st.dataframe(details)

# -----------------------------
# CLOSE CONNECTION
# -----------------------------
conn.close()



