import os
import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()

class EmailSender:
    """Sends emails to flexforge100@gmail.com."""

    def __init__(self):      
        password = os.getenv("GMAIL_PASSWORD")
        if password is None:
            raise Exception("Missing GMAIL_PASSWORD in .env")
        self.password = password
        self.template = self.get_template()
        

    def send_order(self, products: list[dict], first_name: str, email: str, address: str):
        """Sends an email to flexforge100@gmail.com with the ordered products and person's contact info."""
        # TODO: Include address in the email somewhere.
        msg = EmailMessage()
        total_cost = f"${self.get_total_cost(products):.2f}"
        msg.set_content(self.template.format(name=first_name,cart=self.get_cart_string(products), total_cost=total_cost))

        msg["Subject"] = "Check out your recent order from FlexForge!"
        msg["From"] = "flexforge100@gmail.com"
        msg["To"] = email
        msg["Cc"] = "flexforge100@gmail.com"

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login("flexforge100@gmail.com", password=self.password)
        server.send_message(msg)
        server.quit()

    def get_template(self) -> str:
        with open("email_info.txt") as file:
            text = file.read()
        return text
    
    def get_total_cost(self, products: list[dict]) -> float:
        total = 0
        for product in products:
            total = total + product["price"]
        return total
    
    def get_cart_string(self, products: list[dict]) -> str:
        cart_string = ""
        for product in products:
            product_string = f"- {product["name"]} ({product["size"]}, ${product["price"]:.2f})\n"
            cart_string = cart_string + product_string
        return cart_string


if __name__ == "__main__":
    products = [
        {
            "name": "Flexi-Rex",
            "image_path": "images/flexi_rex.jpg",
            "info": "The Flexi Rex is a 3D-printed, poseable dinosaur model designed to move and bend without needing any assembly. Its body is made of connected segments that print in one piece, allowing it to wiggle, twist, and flex smoothly. The design usually features a friendly T-rex shape with rounded details, making it fun to hold, fidget with, or display. Flexi Rex models are popular because they’re quick to print, satisfyingly flexible, and show off what 3D printers can do with articulated designs.",
            "price": 10.00,
            "size":"medium"
        },
        {
            "name": "Flexi-Rex",
            "image_path": "images/flexi_rex.jpg",
            "info": "The Flexi Rex is a 3D-printed, poseable dinosaur model designed to move and bend without needing any assembly. Its body is made of connected segments that print in one piece, allowing it to wiggle, twist, and flex smoothly. The design usually features a friendly T-rex shape with rounded details, making it fun to hold, fidget with, or display. Flexi Rex models are popular because they’re quick to print, satisfyingly flexible, and show off what 3D printers can do with articulated designs.",
            "price": 25.50,
            "size":"big"
        },
    ]
    contact_info = {
        "first_name": "Rees",
        "last_name": "Johnson",
        "email": "reesrjohnson@gmail.com",
        "address": "3615 S Wicklow Place",
    }

    sender = EmailSender()
    sender.send_order(products, contact_info)
