# Package-Based Tourism Management System

This project is a **web-based Tourism Management System** designed to streamline travel package bookings and user management for a tourism company. It integrates role-based access control, secure banking transactions, and various user-specific functionalities to provide an efficient and secure platform for customers, administrators, and tour staff.

## Features

### Customer

* Register, login, and manage user profiles.
* Browse, filter, and book travel packages.
* View booking history and manage personal bookings.

### Guest
* Browse available packages without registration.

### Admin
* Manage users (add/remove customers, staff, and tour guides).
* Oversee travel packages, payment transactions, and bookings.
* View financial and booking records.

### Tour Staff & Tour Guides
* Manage packages and sub-packages (Tour Staff).
* View assigned packages and record notes on tourist sites (Tour Guides).

### Banking System
* Deposit, withdraw, and check account balances securely.
* Ensure transaction safety with a transaction-specific password.

### Email Notifications
* Send confirmation emails for successful registration and bookings.
* Notify users about booking updates.

## Technologies Used

* **Backend:** Django, Django Rest Framework (DRF)
* **Database:** MySQL
* **Authentication:** JSON Web Tokens (JWT)
* **Email Service:** Django Email Backend
* **Deployment:** PythonAnywhere

## Applications & Database Tables

### Applications

1. **Users App**: Manages authentication, registration, and profiles.
2. **Packages App**: Handles travel packages and sub-packages.
3. **Bookings App**: Tracks package bookings and history.
4. **Banking App**: Facilitates secure financial transactions.

### Database Tables

* **User**: Stores user details (username, email, role).
* **Package**: Details travel packages (name, price, location).
* **Booking**: Tracks bookings, status, and prices.
* **Bankist**: Manages user balances and transactions.

## API Endpoints Overview

### Authentication

* `api/user/signup/` - Register
* `api/user/signin/` - Login

### Customer-Only

* `api/booking/book/` - Book a package
* `api/bankist/deposit/` - Deposit funds

### Admin-Only

* `api/user/get_users/` - View all users
* `api/package/add_packages/` - Add packages

[Full API endpoint details available in the documentation.](#)

## How to Run the Project

1. Clone the repository:
```bash
git clone [https://github.com/Abel-40/Tourism_Management.git](https://github.com/Abel-40/Tourism_Management.git)
cd Tourism_Management
```
2. Install dependencies using `Pipenv`:
```bash
pipenv install
```
3. Apply migrations:
```bash
python manage.py migrate
```
4. Start the development server:
```bash
python manage.py runserver
```
5. Access the app at `http://127.0.0.1:8000`.

## Project Roadmap
1. Build the foundational features with small iterations.
2. Ensure functionality with thorough testing after each module.
3. Scale and integrate advanced features like secure banking and email notifications.

## Contributing

Contributions are welcome! Please fork this repository, make your changes, and submit a pull request for review.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

Special thanks to the mentors and resources that inspired this project.
```
