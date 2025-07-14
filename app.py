import streamlit as st
import pandas as pd
import os

CSV_FILE = 'inventory.csv'

def load_inventory():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=['id', 'name', 'category', 'quantity', 'price'])

def save_inventory(df):
    df.to_csv(CSV_FILE, index=False)

def add_item(df):
    st.subheader("Add New Item")
    id = st.text_input("Enter ID")
    name = st.text_input("Enter Name")
    category = st.text_input("Enter Category")
    quantity = st.number_input("Enter Quantity", min_value=0)
    price = st.number_input("Enter Price", min_value=00.0, format="%.2f")

    if st.button("Add Item"):
        if id and name:
            new_row = pd.DataFrame([[id, name, category, quantity, price]],
                                   columns=['id', 'name', 'category', 'quantity', 'price'])
            df = pd.concat([df, new_row], ignore_index=True)
            save_inventory(df)
            st.success("Item added successfully!")
        else:
            st.warning("ID and Name are required.")
    return df

def update_item(df):
    st.subheader(" Update Item")
    if df.empty:
        st.info("No items available to update.")
        return df

    item_ids = df['id'].tolist()
    selected_id = st.selectbox("Select ID to update", item_ids)

    if selected_id:
        item = df[df['id'] == selected_id].iloc[0]
        name = st.text_input("Name", item['name'])
        category = st.text_input("Category", item['category'])
        quantity = st.number_input("Quantity", value=int(item['quantity']), min_value=0)
        price = st.number_input("Price", value=float(item['price']), min_value=0.0, format="%.2f")

        if st.button("Update Item"):
            df.loc[df['id'] == selected_id, ['name', 'category', 'quantity', 'price']] = [name, category, quantity, price]
            save_inventory(df)
            st.success("Item updated successfully!")
    return df


def delete_item(df):
    st.subheader("Delete Item")
    item_ids = df['id'].tolist()
    selected_id = st.selectbox("Select ID to delete", item_ids)

    if st.button("Delete"):
        df = df[df['id'] != selected_id]
        save_inventory(df)
        st.success("Item deleted.")
    return df

def search_item(df):
    st.subheader(" Search Inventory")
    term = st.text_input("Enter keyword (name/category)")
    if term:
        result = df[df.apply(lambda row: term.lower() in row.astype(str).str.lower().values, axis=1)]
        st.dataframe(result)

def main():
    st.title("Basic Inventory Management System")
    st.markdown("Manage items like clothing, groceries, tools, etc.")

    df = load_inventory()

    # NO leading/trailing spaces here!
    menu = ["View Inventory", "Add Item", "Update Item", "Delete Item", "Search"]
    choice = st.sidebar.radio("Select Action", menu)

    if choice == "View Inventory":
        st.subheader("All Inventory Items")
        st.dataframe(df)

    elif choice == "Add Item":
        df = add_item(df)

    elif choice == "Update Item":
        df = update_item(df)

    elif choice == "Delete Item":
        df = delete_item(df)

    elif choice == "Search":
        search_item(df)
if __name__ == "__main__":
    main()

