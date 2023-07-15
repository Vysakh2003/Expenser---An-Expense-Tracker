# Expenser---An-Expense-Tracker

The Expense Tracker website is designed to help users manage their expenses effectively. It provides features such as user registration, sign-in, adding expenses, removing expenses, and displaying expense details.

Here's a brief overview of the main components and functionalities of the Expense Tracker website:

    User Registration and Sign-In:
        Users can create an account by registering with their email and password.
        Existing users can sign in using their credentials to access their account.

    Dashboard:
        After signing in, users are presented with a dashboard where they can view their expense records and perform various actions.

    Add Expense:
        Users can add a new expense by entering the amount, note, and date of the expense.
        The entered data is stored in the MongoDB database, associated with the user's account.

    Remove Expense:
        Users can remove a specific expense from their records.
        When selecting an expense for removal, the corresponding record is deleted from the MongoDB database.

    Display Expenses:
        The website provides a display of the user's expense records.
        Users can view their expenses along with the associated amount, note, and date.
        The displayed expenses can be sorted or filtered based on various criteria, such as date range or amount.

    Front-end Technologies:
        The front-end of the website is built using HTML, CSS, JavaScript, and Bootstrap.
        Django templates are used for rendering dynamic content in the Flask application.

    Back-end Technologies:
        Flask is used as the web framework to handle requests, routes, and interactions with the MongoDB database.
        MongoDB is utilized as the database to store and retrieve expense records.
        PyMongo is used as the Python driver to connect and interact with the MongoDB database.

Overall, the Expense Tracker website provides a user-friendly interface for managing and tracking expenses. It allows users to add, remove, and view their expense records conveniently, facilitating better financial management.
