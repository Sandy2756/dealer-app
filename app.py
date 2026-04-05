import streamlit as st
import pandas as pd
import io
import streamlit.components.v1 as components

# Load Dealer Data
data = st.secrets["data"]
df = pd.read_csv(io.StringIO(data))

# Load Stock Data
stock_df = pd.read_csv("https://docs.google.com/spreadsheets/d/1ime3BfD4UIqgJL0X5IcOB8cXI2Avwnia_mztHUzLRX0/export?format=csv")

# Side Bar for Sections Radio Butons
page = st.sidebar.radio(
    "Select Section",
    ["Dealer Order", "Stock Check", "Pricing Check"]
)

if page == "Dealer Order":
    st.title("Dealer Lookup + Order Generator")
    
# Mobile input
    mobile = st.text_input("Enter Mobile Number")
    
# Item inputs
    st.subheader("Add Items")
    
    items = []
    for i in range(8):
        col1, col2 = st.columns(2)
        code = col1.text_input(f"Code {i+1}", key=f"code{i}")
        qty = col2.text_input(f"Qty {i+1}", key=f"qty{i}")
        if code.strip() and qty.strip():
            items.append(f"{code.upper()} - {qty}")
    
# Lookup
    if mobile:
        try:
            mobile = int(mobile)
            result = df[df["Mob_No"] == mobile]

            if not result.empty:
                row = result.iloc[0]

                dealer = row["Dealer"]
                area = row["Area"]
                discount = row["Discount"]
                transport_r = row["Transport_Regular"]
                transport_o = row["Transportation_Others"]

            # Build message
                message = ""

                if items:
                    message += "\n".join(items) + "\n\n"

                message += f"""Dealer: {dealer}
    Area: {area}
    Mob: {mobile}
    Discount: {discount*100:.2f}%
    Transport (Regular): ₹{transport_r}
    Transport (Others): ₹{transport_o}"""

                col1, col2 = st.columns([5,1])

                with col1:
                    st.text_area("Copy Message", message, height=200)

                with col2:
                    components.html(f"""
                    <button onclick="
                
                navigator.clipboard.writeText({repr(message)});
                " style="
                    margin-top: 28px;
                    padding: 8px 12px;
                    font-size: 14px;
                    cursor: pointer;
                ">
                📋 Copy
                </button>
                """, height=60)

            else:
                st.error("Mobile number not found")

        except:
            st.error("Invalid mobile number")

# Check Availability
if page == "Stock Check":
    st.subheader("Check Availability")

    for i in range(10):
        col1, col2 = st.columns([2, 3], vertical_alignment="center")

        code = col1.text_input(
            label=f"Code {i+1}",
            key=f"avail{i}",
            label_visibility="collapsed",
            placeholder=f"Code {i+1}"
        )

        if code:
            result = stock_df[stock_df["Code"] == code.upper()]

            if not result.empty:
                stock = result.iloc[0]["Stock"]
                col2.write(f"{stock} sheets available")
            else:
                col2.write("Not found")
        else:
            col2.write("")  # keeps spacing consistent

# Check Price
# Check Price
if page == "Pricing Check":
    st.subheader("Check Price")

    price_items = []

    for i in range(10):
        col1, col2 = st.columns([2, 3], vertical_alignment="center")

        code = col1.text_input(
            label=f"Code {i+1}",
            key=f"price{i}",
            label_visibility="collapsed",
            placeholder=f"Code {i+1}"
        )

        if code:
            result = stock_df[stock_df["Code"] == code.upper()]

            if not result.empty:
                row = result.iloc[0]
                name = row["Name"]
                price = row["Price"]

                col2.write(f"{name} | ₹{price}/sqft")

                # 👇 THIS IS IMPORTANT (stores for copy)
                price_items.append(f"{code.upper()} - {name} ₹{price}/sqft")

            else:
                col2.write("Not found")
        else:
            col2.write("")

    # =========================
    # COPY SECTION (NEW)
    # =========================

    price_message = ""

    if price_items:
        price_message = "\n".join(price_items)

    col1, col2 = st.columns([5,1])

    with col1:
        st.text_area("Copy Price List", price_message, height=150)

    with col2:
        st.components.v1.html(f"""
        <button onclick="navigator.clipboard.writeText({repr(price_message)})"
        style="
            margin-top: 28px;
            padding: 8px 12px;
            font-size: 14px;
            cursor: pointer;
        ">
        📋 Copy
        </button>
        """, height=60)
