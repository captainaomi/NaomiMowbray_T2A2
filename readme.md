# Company Flight Log API

## Keep track of all aircraft landings, flight time, and pilot expirations for your company!

You'll need to ensure that you have Python 3 and PostgreSQL installed, as well as either a clone of this repository (or you can download the ZIP file).

### Setup and Installation: 
- Open your CLI or terminal and enter: `psql`
- Then, create your new database by typing: `CREATE DATABASE flight_log_db;`
- Next, you'll need to create a new user: `CREATE USER captain WITH PASSWORD '123abc';`
- Grant all the permissions: `GRANT ALL PRIVILEGES ON DATABASE flight_log_db TO captain;`
- You're ready to connect! Enter: `\c flight_log_db;`

I suggest an IDE for this next part, but feel free to use terminal if you feel comfortable to do so!

- Rename the *.env.sample* file to *.env*, and set your database URL and secret key using the format explained in the file comments.
- You now need to create a new virtual environment. Do this by opening a new terminal window and entering: `python3 -m venv .venv && source .venv/bin/activate`
- Install the requirements: `pip3 install -r requirements.txt`

To begin with, you'll need to create and seed tables. This gives your app the framework by creating mock pilots, expirations, aircraft, and flights. 

In doing so, you'll start off with a user who is an admin, and you can then edit, update or delete from there. 

- To create initial tables, enter: `flask db create`
- To seed initial data entries, enter: `flask db seed`

Please feel free to play around with Postman or Insomnia or a similar program to become familiar with the functions, input requirements and expected output. 

- In your terminal, please enter: `flask run`
- You can access the server on Postman/Insomnia/similar at `localhost:8080/_____` 

We suggest you begin with a simple login request, by using the POST method at `localhost:8080/pilot/login` and entering your seeded admin email and password:

``` json
{
        "email": "doctorwho@captain.com",
        "password": "123abc"
}
```

Once comfortable with the system, we strongly suggest you drop the tables, edit the cli_controller with relevant information and then go for gold from there.

- You can drop tables by entering: `flask db drop`

Note: you will have to enter `flask db create` again to start fresh with some snazzy new empty tables to fill.

Like I said, you're ready to go for gold!

## Best of luck, blue skies and tail winds to you!