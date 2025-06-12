import streamlit as st
from inventory import Inventory, Product

# Initialize inventory
inv = Inventory()

st.title("📦 Smart Inventory Management")

# Sidebar menu
menu = st.sidebar.selectbox("Choose Action", ["Add Product", "Update Stock", "View All Products", "Low Stock Products"])

# 1. Add Product
if menu == "Add Product":
    st.subheader("➕ Add New Product")

    sku = st.text_input("SKU")
    name = st.text_input("Product Name")
    category = st.text_input("Category")
    price = st.number_input("Price", min_value=0.0)
    stock = st.number_input("Stock Quantity", min_value=0)

    if st.button("Add Product"):
        if sku and name and category:
            try:
                product = Product(sku, name, category, price, stock)
                inv.add_product(product)
                st.success("Product added successfully.")
            except ValueError as e:
                st.error(str(e))
        else:
            st.warning("Please fill all required fields.")

# 2. Update Stock
elif menu == "Update Stock":
    st.subheader("🔁 Update Stock")

    sku = st.text_input("Enter SKU to update")
    amount = st.number_input("Amount to Add (can be negative)", step=1)

    if st.button("Update Stock"):
        try:
            inv.update_stock(sku, amount)
            st.success("Stock updated successfully.")
        except ValueError as e:
            st.error(str(e))

# 3. View All Products
elif menu == "View All Products":
    st.subheader("📋 All Products")

    products = inv.get_all()
    if products:
        for product in products:
            st.markdown(f"""
                - **SKU**: {product.sku}
                - **Name**: {product.name}
                - **Category**: {product.category}
                - **Price**: ${product.price}
                - **Stock**: {product.stock}
                - **Added**: {product.created_at}
                ---
            """)
    else:
        st.info("No products in inventory.")

# 4. Low Stock Products
elif menu == "Low Stock Products":
    st.subheader("⚠️ Low Stock Products (<= 5)")
    low_stock = inv.get_low_stock()

    if low_stock:
        for product in low_stock:
            st.markdown(f"🔻 **{product.name}** (SKU: {product.sku}) — Stock: {product.stock}")
    else:
        st.success("All products are sufficiently stocked.")
