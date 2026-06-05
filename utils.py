import re
import streamlit as st
from PIL import Image, ImageOps
from email_helper import EmailSender

def validate_email(email: str):
    # A common regex pattern for basic email validation
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    # Use re.fullmatch() to ensure the entire string matches the pattern
    if re.fullmatch(pattern, email):
        return True
    else:
        return False

@st.cache_data
def load_image(filepath: str) -> Image.Image:
    image = Image.open(filepath)
    image = ImageOps.exif_transpose(image)
    return image

def get_image(filepath: str, width: int = 300):
    """Load the image at the given filepath, rotate it correctly, and return a st.image widget."""
    image = load_image(filepath)
    return st.image(image, width=width)

def send_order(first_name,products,address,email):
    EmailSender().send_order(products, first_name=first_name, email=email, address=address)
    print("sent")
    # TODO: Reset the app (empty the cart, clear the text fields, etc.)