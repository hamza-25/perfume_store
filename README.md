# Perfume Emporium

## Description
Perfume Emporium aims to redefine the fragrance shopping experience by providing a comprehensive online platform where users can explore a vast collection of perfumes, create personalized accounts, and seamlessly place orders. The project seeks to merge convenience with luxury, offering customers a virtual haven for indulging in their olfactory desires.

## Features
- **Browse Perfumes:** Users can explore a vast collection of perfumes without the need to log in.
- **User Authentication:** Users can register and log in to the web app to access additional features.
- **Order Management:** Authenticated users can place orders, add addresses, cancel orders, and confirm delivery.
- **Profile Management:** Authenticated users can edit their profiles, including personal information and preferences.
- **Admin Control Panel (CPanel):** Admin users have access to a control panel where they can:
  - **Manage Categories:** Add, edit, and delete product categories.
  - **Manage Products:** Add, edit, and delete products within categories.
  - **View Orders:** Access a list of orders placed by all users.
  - **User Management:** View a list of users and take actions such as banning suspicious users.

## Technologies Used
- **Frontend:**
  - HTML
  - CSS
  - Bootstrap
  - JavaScript
  - jQuery
  
- **Backend:**
  - Python with Flask framework
  
- **Database:**
  - MySQL

## Installation
1. Clone the project repository:
2. Activate the virtual environment (if it exists):
   ```bash
   source per_venv/bin/activate
3. If the virtual environment doesn't exist, create one and install the required packages:
   ```bash
   python3 -m venv per_venv
   source per_venv/bin/activate
3. Ensure that the following packages are installed:
   ```bash
   pip list
alembic==1.13.1

blinker==1.7.0

click==8.1.7

dnspython==2.6.1

email-validator==2.1.0.post1

Flask==3.0.1

Flask-Cors==4.0.0

Flask-Login==0.6.3

Flask-Migrate==4.0.5

Flask-SQLAlchemy==3.1.1

greenlet==3.0.3

idna==3.6

itsdangerous==2.1.2

Jinja2==3.1.3

Mako==1.3.2

MarkupSafe==2.1.4

mysql-connector-python==8.3.0

PyMySQL==1.1.0

SQLAlchemy==2.0.25

typing-extensions==4.9.0

Werkzeug==3.0.1

WTForms==3.1.2

4. Run MySQL and create a database named perfume_db.
5. Update the database information in db_info.py with your database name, username, and password.
6. Open a terminal and start the Python interactive shell
   ```bash
   python3
   >>> from app import *
   >>> db.create_all()
   >>> exit
7. Finally, run the app:
   ```bash
   python3 app.py
## Usage
- After running the application, note the local IP address provided in the terminal, e.g., http://127.0.0.1:5000.
- Copy the IP address and paste it into your web browser's address bar.
- You'll be directed to the homepage of the Perfume Emporium web app.
- **If you're a regular user, you can:
  - **Browse the collection of perfumes.
  - **Add items to your cart.
  - **Proceed to checkout.
  - **View and manage your orders.
  - **Edit your profile information.
- **If you want to access the admin features:
  - **Register as a normal user.
  - **Access MySQL and run the following commands:
   ```bash
   USE perfume_db;
   UPDATE users SET is_admin=1 WHERE email='youremail@email.com';
 - **Log in with the email address used for registration.**
 - **You'll now have access to the admin control panel, where you can manage categories, products, orders, and users.**
## Contact
 - Email: me677499@gmail.com
 - LinkedIn: https://www.linkedin.com/in/hamza-ichaoui-2b2561244/

Feel free to reach out via email or connect with me on LinkedIn for any inquiries, feedback, or support related to Perfume Emporium.
