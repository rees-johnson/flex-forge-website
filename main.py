import streamlit as st
import json
from pathlib import Path
from st_keyup import st_keyup
from utils import get_image, validate_email, send_order

st.set_page_config(
    page_title="FlexForge",
    page_icon="images/flexforge.jpg",
    layout="wide"
)

images_dir = Path("images")
products_dir = Path("products") 

def add_product_to_cart(name: str, size: str, price: float):
    st.session_state.cart.append({"name": name, "size": size, "price": price})

def remove_products_from_cart(names: list, pretty_cart: list):
    for name in names:
        i = pretty_cart.index(name)
        pretty_cart.pop(i)
        st.session_state.cart.pop(i)

def next_page():
    st.session_state.current_page = st.session_state.current_page + 1

def previous_page():
    st.session_state.current_page = st.session_state.current_page - 1

def display_product_info(container: st.container, product_idx: int):
    name = st.session_state.products[product_idx]["name"]
    with container:
        st.write(st.session_state.products[product_idx]["info"])
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button(
                label="Buy big ($10.00)",
                on_click=add_product_to_cart,
                kwargs={"name": name, "size": "big", "price": 10.0},
            )
        with col2:
            st.button(
                label="Buy medium ($7.00)",
                on_click=add_product_to_cart,
                kwargs={"name": name, "size": "medium", "price": 7.0},
            )
        with col3:
            st.button(
                label="Buy small ($3.00)",
                on_click=add_product_to_cart,
                kwargs={"name": name, "size": "small", "price": 3.0},
            )

if __name__ == "__main__":
    # Set initial session state values
    if "product_on_display" not in st.session_state:
        st.session_state.product_on_display = None
    if "cart" not in st.session_state:
        st.session_state.cart = []
    if "products" not in st.session_state:
        st.session_state.products = []
        for fpath in products_dir.iterdir():
            with open(fpath) as f:
                contents = json.load(f)
                st.session_state.products.append(contents)

    if "current_page" not in st.session_state:
        st.session_state.current_page = 0
    
    with st.sidebar:
        st.image("images/flexforge.jpg",width=250)
        #st.image("images/kick_off_sale.png", width=250)

    main_column, checkout_column = st.columns([0.8, 0.2], gap="large")
    with checkout_column:
        if len(st.session_state.cart) == 0:
            st.image("images/checkout.jpg",width=75)
        else:
            st.image("images/ucheckout.jpg",width=75)
        with st.popover("Checkout"):
            dollar_amt = 0
            for item in st.session_state.cart:
                dollar_amt = dollar_amt + item["price"]
            st.write(f"Buy {len(st.session_state.cart)} item(s) for ${dollar_amt:.2f}?")
            yes_col, edit_col = st.columns([0.4, 0.6])
            with yes_col:
                with st.popover("Yes"):
                    first_name = st_keyup("First Name", key="firstname")
                    last_name = st_keyup("Last Name", key="lastname")
                    email = st_keyup("Email", key="email")
                    email_is_valid = validate_email(email) or (not email)
                    if not email_is_valid:
                        st.text("Invalid email!")
                    address = st_keyup("Address", key="address")
                    # TODO: Look into address validation (maybe use Google Maps API?)

                    all_ready = all((first_name, last_name, email, email_is_valid, address))

                    #TODO: clear all the text feilds in the after you submit it
                    st.button(
                        label="submit order?",
                        on_click=send_order,
                        kwargs={ 
                            "first_name":first_name,
                            "products":st.session_state.cart,
                            "address":address,
                            "email":email
                        },
                        disabled=(not all_ready),
                    )

            with edit_col:
                with st.popover("Edit cart"):
                    pretty_cart = []
                    for item in st.session_state.cart:
                        pretty_string = f"{item['size']} {item['name']} (${item['price']})"
                        pretty_cart.append(pretty_string)
                    selection = st.pills("Select items to remove from cart", pretty_cart, selection_mode="multi")
                    
                    st.button(
                        label=f"Remove {len(selection)} item(s)?",
                        on_click=remove_products_from_cart,
                        kwargs={"names": selection, "pretty_cart": pretty_cart},
                        disabled=len(selection) == 0,
                    )
        
    with main_column:

        st.markdown("## Welcome To FlexForge")
        
        products_container = st.container(height=500, width=900)
        with products_container:

            product = st.session_state.products[st.session_state.current_page]
            col1, col2 = st.columns([0.4, 0.6])
            with col1:
                get_image(product["image_path"], width=300)
            with col2:
                product_info_container = st.container()
                display_product_info(product_info_container, st.session_state.current_page)

        prev_col, number_col, next_col = st.columns(3)
        with prev_col:
            st.button(
                label="<-",
                on_click= previous_page,
                disabled = st.session_state.current_page == 0
            )
        num_products = len(st.session_state.products)
        with number_col:
            st.write(f"{st.session_state.current_page + 1} / {num_products}") 
           
        with next_col:
            st.button(
                label="->",
                on_click= next_page,
                disabled= st.session_state.current_page == num_products - 1
            )
        st.markdown('<div class="footer">© 2026 FlexForge Industries</div>', unsafe_allow_html=True)
