# My Shop

Pc Shop is an e-commerce platform built with Django, allowing users to browse products, add them to a cart, and manage their account. The project includes features like user authentication, product management, and a shopping cart.

## Features

- **Product Listing**: View a list of products with their details.
- **Product Detail**: See detailed information about individual products.
- **Shopping Cart**: Add products to the cart, view cart details, and remove items from the cart.
- **User Authentication**: Register, log in, and manage user accounts.
- **Dashboard**: Access user-specific information and actions.

## Requirements

- Python 3.x
- Django 4.x
- Pillow (for image handling)

## Installation & usage

1. **Clone the Repository**
 git clone https://github.com/Dobauron/PC_SHOP.git
 cd pc_shop

2. Install Dependencies
  pip install -r requirements.txt

3. Apply Migrations
  python manage.py migrate

4.Create superuser
  python manage.py createsuperuser

5.Run the Development Server
  pytohn manage.py runserver
