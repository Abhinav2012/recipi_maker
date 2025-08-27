import streamlit as st
import pandas as pd
import os

FILE_PATH = "grocery_list/grocery_list.csv"

# Load grocery list
def load_data():
    if os.path.exists(FILE_PATH):
        return pd.read_csv(FILE_PATH)
    else:
        return pd.DataFrame(columns=["Item", "Quantity", "Metric"])

# Save grocery list
def save_data(df):
    df.to_csv(FILE_PATH, index=False)

# Streamlit app
st.set_page_config(page_title="Grocery List Manager", layout="centered")
st.title("🛒 Grocery List Manager")

df = load_data()

# Display current list
st.subheader("📋 Current Grocery List")
st.dataframe(df, use_container_width=True)

# Add an item
st.subheader("➕ Add Item")
item = st.text_input("Item name")
quantity = st.number_input("Quantity", min_value=1, value=1, step=1)
metric = st.selectbox("Metric", ["kg", "g", "ltr", "ml", "pcs", "dozen", "other"])

if st.button("Add to list"):
    if item.strip():
        new_row = pd.DataFrame([[item.strip(), quantity, metric]], columns=["Item", "Quantity", "Metric"])
        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df)
        st.success(f"Added '{item}' to the list.")
        st.rerun()

# Remove an item
st.subheader("➖ Remove Item")
remove_item = st.selectbox("Select item to remove", df["Item"].unique() if not df.empty else ["No items available"])

if st.button("Remove selected item"):
    if remove_item in df["Item"].values:
        df = df[df["Item"] != remove_item]
        save_data(df)
        st.success(f"Removed '{remove_item}' from the list.")
        st.rerun()
