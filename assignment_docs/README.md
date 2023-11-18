# NaomiMowbray_ T2A2

## Helpful links:
[GitHub Repository for Company Flight Log API](https://github.com/captainaomi/NaomiMowbray_T2A2)

[Trello Project Management Board](https://trello.com/b/0uHOqa55/flightlogdb)

## Questions quick links:

[R1 and R2. Identification of problem, and why is it a problem that needs solving?](#r1-and-r2-identification-of-the-problem-you-are-trying-to-solve-by-building-this-particular-app-why-is-it-a-problem-that-needs-solving)

[R3. Choice and drawbacks of database system used](#r3-why-have-you-chosen-this-database-system-what-are-the-drawbacks-compared-to-others)

[R4. Key functionalities and benefits of an ORM](#r4-identify-and-discuss-the-key-functionalities-and-benefits-of-an-orm)

[R5. Endpoint documentation](#r5-document-all-endpoints-for-your-api)

[R6. App ERD](#r6-an-erd-for-your-api)

[R7. Third party services used in app](#r7-detail-any-third-party-services-that-your-app-will-use)

[R8. Project models' relationships with each other](#r8-describe-your-projects-models-in-terms-of-the-relationships-they-have-with-each-other)

[R9. Database relations with regards to ERD](#r9-discuss-the-database-relations-to-be-implemented-in-your-application)

[R10. Project management](#r10-describe-the-way-tasks-are-allocated-and-tracked-in-your-project)

___

<br>

# R1 and R2. Identification of the problem you are trying to solve by building this particular app. Why is it a problem that needs solving?

In Australian general aviation, there is an annual compulsory survey where the owner of each registered aircraft is legally required to provide the number of hours flown and number of landings in that aircraft for that given year. 

As you can imagine, if not tracked throughout the year and kept up to date, this is a hugely tiresome and painstaking job to have to sift back through to correctly provide this required information. 

Bizarrely, I have found in my experience working for three different companies and in general consensus with pilots from other companies, there is a widespread aversion to keeping a tally of landings alongside flight hours! 

With landings in particular, most operators believe that this type of paperwork is a waste of time, and resources can be better spent elsewhere; often just putting it off and off and off until there needs to be a huge audit and comb through every year for the compulsory survey.

Further, there is no program available (that I am aware of), that can easily record and store this data - landings in particular - digitally.

Literally every company I know of (that I’ve worked for, asked directly, or spoken to their pilots about) still tracks flights on paper<sup>*</sup> . We call them running sheets, which include detailed information such as date and time of flight, pilot name, description of the route, flight time, fuel burn, the customer/booking agent, weight and balance confirmation, passenger manifest, and sometimes more: for each individual flight. It is tedious and time consuming, but keeping paper sheets in each aircraft has yet to be revolutionised - and will be something I work on down the track for sure, which will make me rich and the most appreciated pilot/coder in Australia/the world!

Jokes aside, those paper running sheets are how *every company I know* tallies flight time and landings.

And when it comes to the compulsory annual survey, those pieces of paper are then meticulously sifted and cross referenced to count landings and give the correct information to the Department of Infrastructure, Transport, Regional Development, Communication and the Arts (see, even the Australian Government department’s NAME is a headache!). Yes, sometimes this is done monthly, but it’s still not an optimised system by any means.

I believe if there was a way to quickly add flight time and number of landings after completing each flight for a given aircraft, those 30 seconds it takes to enter the information into a database can save literally hours - if not days - of auditing down the track.

And while I could include more information within this database with regards to flights (and one day perhaps even negate running sheets!), for now, its main purpose is for the annual Australian General Aviation Activity Survey.

However, there is one more thing that companies don’t often track: a pilot’s expirations. 

Typically, it’s every individual’s responsibility to remember when their different aviation requirements are due to expire. The most important ones are your medical, biannual check flight for their personal licence, a company check flight (sometimes annual, sometimes biannual), dangerous goods certification, and, in some cases (such as flying into/out of controlled aerodromes), an ASIC (Aviation Security Identification Card).

I thought it made sense that when adding a pilot to the database, you can also add their expirations. This allows a company or pilot to know at a glance what things are expiring next/soon for each pilot, and therefore what tests or checks should be booked in the near future to ensure nothing actually expires that would jeopardise or stop a pilot from flying for any period. It’s not the main focus of this API, but a nice little add on that both helped me understand relationships and functionality a bit better, as well as giving a broader foundation for when I build upon it and become rich and famous one day by selling it to Australian (global?) pilots! 😉

<sup>*</sup> Note: yes, some will enter the information from the running sheets into Excel or some sort of digital database afterward, but the running sheets are still used in the first place and then - if at all - converted.

<br>
<br>

# R3. Why have you chosen this database system. What are the drawbacks compared to others?

Well, I’d be kidding myself if I didn’t start out with the obvious reason for using a PostgreSQL database: it’s the one I’ve learned through Coder Academy! My honest and biggest reason is that I’m at the beginning of my coding journey, and there has been a steep learning curve to get this far. I knew if I tried to implement any other system, I’d probably have a mental/emotional melt down with the mountain of research I’d have to do just to understand and implement a different system to the one I’m only just getting familiar with. 

And while that might not be a super technical answer, it’s an authentic one 😉

My research for the Workbook assignment also helped me learn a lot about PostgreSQL’s pros and cons and why a company/developer might chose that system - beyond simply being familiar with it!

As I said in my RfQ for the Workbook assignment, PostgreSQL (also known as Postgres) is an open source platform that comes with many pros, but there are cons worth noting too.

I mean, Postgres must be pretty good if the claims that America’s Federal Agencies such as the Federal Aviation Administration (FAA), NASA, the Department of Labor and multiple agencies throughout the Department of Defense (DoD) have utilised it<sup>i</sup>, as well as Apple, Netflix and Spotify, right?!

On the other hand, there are claims that Postgres does not come with any warranty, nor is there liability or indemnity protection<sup>ii</sup>, soooo to Postgres or not to Postgres?! 

Well, according to the annual survey completed by Stack Overflow in May 2022 of over 70,000 developers, more than 46% of  the professional developers chose PostgreSQL as the database they've done extensive development work in over the past year, and the one they want to work in across the next year<sup>iii</sup>.

Being free to use and open sourced with a huge community behind it means that support is almost always available by an army of developers around the world, and extensive questions and answers available on the internet too. Chances are, if you word your question right, there’ll be multiple angles, options and opinions on how to approach any challenge you might face - and this has helped me a lot with my app.

However, this large community can also be a source of challenges in its own way. Documentation doesn’t have any uniform standards that it follows, so there might be conflicting information or a lack of consistency in some parts - which, ironically, I’ve also found to be a bit of a struggle with my app 😉

PostgreSQL works with both relational and non relational queries, and its vertical scalability means that any project can start small, while having room to grow extensively without needing to change databases down the track. Although this project is currently utilising a relational database, building with Postgres gives the option to adapt down the track to also incorporate NoSQL features (that is, non relational features), if required. 

In fact, the features and third party tools that are available and easily integrated into Postgres are amazing! It should be noted that the slightly more popular<sup>iii</sup> MySQL does have more third party tools available, but everything I need for my app is available so no need to overcomplicate.

When comparing to MySQL, Postgres is also not as fast, but again, for the intended purpose it is more than capable.

As for security, there are three pillars that Postgres security is built on:
- **Network level security -** sockets and firewalls
- **Transport level security -** secure communication with the database
- **Database level security -** user accounts configuration<sup>iv</sup>
This top to bottom assurance is a massive ‘pro’ for Postgres, and definitely a secure choice for a DBMS.

In line with security, I would be remiss in not mentioning the ability to define who can do what within the database! There is robust functionality for user vs. admin authentication and authorisation, access control, and ability to manage privileges<sup>v</sup>, as well as hashing and encryption capabilities.

The four key properties that guarantee the reliability and integrity of relational databases are collectively known as ACID: atomicity, consistency, isolation, and durability. These collectively ensure data integrity by avoiding validity errors, and luckily for me, Postgres is ACID compliant!

<sup>i</sup><i> US Government Agencies Turn to EnterpriseDB and Postgres to Slash Database Costs by 80%</i>, 23/07/2013, EnterpriseDB, accessed 3rd July 2023, <https://www.enterprisedb.com/news/us-government-agencies-turn-enterprisedb-and-postgres-slash-database-costs-80#:~:text=Federal%20agencies%20using%20Postgres%20include,Department%20of%20Defense%20(DoD)>

<sup>ii</sup>Stuti Dhruv, 15/05/2019, <i>PostgreSQL Advantages and Disadvantages</i>, Aalpha, accessed 3rd July 2023, <https://www.aalpha.net/blog/pros-and-cons-of-using-postgresql-for-application-development/>

<sup>iii</sup><i>2022 Developer Survey</i>, Stack Overflow, accessed 8th July 2023, <https://survey.stackoverflow.co/2022/#most-popular-technologies-database-prof>

<sup>iv</sup>Jane Williams, 05/04/2023, <i>How to Secure PostgreSQL Database – Tips and Tricks</i>, devart, accessed 8th July 2023, <https://blog.devart.com/how-to-secure-postgresql-database.html>

<sup>v</sup>Justin Ellingwood, <i> The benefits of PostgreSQL</i>, Prisma, accessed 8th July 2023, <https://www.prisma.io/dataguide/postgresql/benefits-of-postgresql>

<br>
<br>

# R4. Identify and discuss the key functionalities and benefits of an ORM

Object Relational Mapping (ORM) is a technique used in creating a ‘bridge' between object oriented programming (OOP) languages and relational databases<sup>i</sup> - which is what this Flight Log API is!

I found a great explanation of the difference between OOP and relational databases by Tina Zhou Hui. She explains that OOP’s strength is in combining variables and functions into classes and objects. These can be thought of as ‘real world’ concept: where a car might be the object, wheels are the properties, and driving is the behaviour. On the other hand, relational databases are more focused on relationships between tables through foreign keys. The example here is with a flight where passengers are one entity, another entity is the individual plane seats, and the two are linked by a plane ticket that assigns a particular passenger to a specific seat.<sup>ii</sup>

They’re different paradigms! 

That example truly helped me understand what was going on, and why ORM is soooooo beneficial. It also explains in a more elementary way why there needs to be a bridge between the two!

ORM provides a super convenient way for developers to interact with databases, as ORMs use programming languages such as Python instead of SQL. ORMs are language specific, which means that developers (or me, in this case!) can choose their library based on personal preference and manipulate data without the need for using Structured Query Language (SQL).

### Key Functionality of an ORM
- **Object representation of data** - the biggest one is the ability to represent data as classes and objects, where each table is typically a class and each row within that table is an object.
- **Data Querying** - the ability to perform database queries to retrieve data without the need for SQL (think: the Read in CRUD)
- **Data Manipulation** - the ability to manipulate data through operations without the need for SQL (think: the Create, Update and Delete in CRUD)
- **Data Validation** - before inserting or updating anything, ORMs can validate and sanitise input to ensure integrity across the database
- **Transaction Atomicity ** - operations can be defined as single transactions, ensuring that either all changes are committed or if *any* part of the transaction has an error or fails, then nothing happens at all and the entire transaction is rolled back to its previous state
- **Relationship Management** - ORMs handle the relationships between tables (such as one to one, one to many etc), and help ensure consistency across linked records 


### Key Benefits of an ORM
- **Database Simplicity** - probably the biggest benefit already touched on above is simplicity! Developers can work with familiar languages and object oriented paradigms versus raw SQL
- **Database Agnostic** - good ORMs are agnostic, which means they work even when migrating database management systems<sup>iii</sup>, which gives the flexibility to easily switch (not sure why you’d have to, but hey, at least you can!) without having to rewrite your entire code
- **Productivity** - by interacting with syntax and language that is familiar, a developer doesn’t have to go and try to learn SQL - therefore, they’re more productive, which is always a benefit!
- **Reqduced Vulnerability** - SQL injection attacks are a common security vulnerability in web applications, and ORMs can help reduce these with the defined parameters
- **Code Reusability** - Again, with OOP we can utilise classes, models, schemas and more… This means that we can therefore create functions and logic that can be used repeated throughout the program to keep it DRY (if done well, of course)
- **Testing Ability** - Through the use of programs such as Postman or Insomnia, developers can mock database transactions and test logic without having to rely on a live database - I basically lived on Postman this past week and it was a HUGE benefit 😂

There’s quite clearly some overlap between functionality and benefits, but the theme is the same: ORMs are great!

<sup>i</sup>Ihechikara Vincent Abba, 21/10/2022,<i> What is an ORM – The Meaning of Object Relational Mapping Database Tools
</i>, accessed 30th July 2023, <https://www.freecodecamp.org/news/what-is-an-orm-the-meaning-of-object-relational-mapping-database-tools>

<sup>ii</sup>Tina Zhou Hui, 20/11/2020,<i> Introduction to Object-relational mapping: the what, why, when and how of ORM</i>, dev, accessed 30th July 2023, <https://dev.to/tinazhouhui/introduction-to-object-relational-mapping-the-what-why-when-and-how-of-orm-nb2>

<sup>iii</sup>Mike Huls, 1/11/2022,<i> No Need to Ever Write SQL Again: SQLAlchemy’s ORM for Absolute Beginners
</i>, Towards Data Science, accessed 30th July 2023, <https://towardsdatascience.com/no-need-to-ever-write-sql-again-sqlalchemys-orm-for-absolute-beginners-107be0b3148f>

<br>
<br>

# R5. Document all endpoints for your API

## Pilot Table

![GET method for all pilots](docs/R5/pGET:all_pilots.png)
### REQUIRED DATA INPUT:
`@jwt_required()`

N/A, as it's a GET method

### EXPECTED RESPONSE DATA:
A list of all pilots that have been registered in the database and their corresponding information, or else any applicable error messages (eg. no pilots yet registered, or missing JWT authentication)

<br>
<br>

![GET method for single pilots](docs/R5/pGET:pilot.png)
### REQUIRED DATA INPUT:
`@jwt_required()`

N/A, as it's a GET method - just need the id of the pilot in the route

### EXPECTED RESPONSE DATA:
A single pilot that has been registered in the database and their corresponding information, or else any applicable error messages (eg. not a valid pilot id)

<br>
<br>

![POST method for registering new pilot](docs/R5/pPOST:register.png)
### REQUIRED DATA INPUT:
`@jwt_required()` and `@admin_authorisation`

All fields are required, except the `'id'` (which is the primary key and will be created upon registration of a new pilot), and whether or not this pilot `'is_admin'`, which is set to `False` by default.
``` JSON
{
    "arn": Integer (unique),
    "name": "String" (min length = 4, using only English letters, numbers, dashes or spaces),
    "email": "String" (unique, email format),
    "password": "String" (min length = 6),
    "status": "String" (where the valid statuses are either "active" or "inactive"),
    "is_admin": true or false (default = false)
}
```

### EXPECTED RESPONSE DATA:
An output of the newly registered pilot, serialised without their password:
``` JSON
{
    "arn": 10,
    "email": "doctor@who.com",
    "id": 1,
    "is_admin": false,
    "name": "Doctor Who",
    "status": "active"
}
```
Otherwise, any applicable error messages (eg. the ARN provided is already registered to another pilot in the database)

<br>
<br>

![POST method for pilot login](docs/R5/pPOST:login.png)
### REQUIRED DATA INPUT:
The pilot just needs to enter their email and password to log in:
``` JSON
{
    "email": "doctor@who.com",
    "password": "iLoveMyTardi5"
}
```

### EXPECTED RESPONSE DATA:
The logged in pilot's email, status, whether or not they're an admin, and - most importantly - their token:
``` JSON
{
    "email": "doctor@who.com",
    "is_admin": false,
    "status": "active",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5MDYyNjYyNywianRpIjoiMTE0YThiNWQtYmZhMS00YWZhLTllN2QtMzIwNzIwZDI2MzM5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjIiLCJuYmYiOjE2OTA2MjY2MjcsImV4cCI6MTY5MDcxMzAyN30.t5UZ5HuU_wnJ4WieOcvg9wo0cTd8LcpVr9TzzwObRyo"
}
```
Otherwise, any applicable error messages (eg. an incorrect email or password)

<br>
<br>

![DELETE method for deleting a pilot](docs/R5/pDELETE:pilot.png)
### REQUIRED DATA INPUT:
`@jwt_required()` and `@admin_authorisation`

N/A, as it's a DELETE method, using the id of the pilot to be deleted in the route

### EXPECTED RESPONSE DATA:
Just a confirmation message including the pilot's name:
``` JSON
{
    "Confirmation": "Captain Dalek Supreme has been successfully deleted"
}
```
Otherwise, any applicable error messages (eg. no admin authorisation)

<br>
<br>

![PATCH method for editing or updating a pilot](docs/R5/pPATCH:pilot.png)
### REQUIRED DATA INPUT:
`@jwt_required()` and `@admin_authorisation`

Whatever information the admin would like to update, with the same constraints as in the original POST method (except that nothing is required now, as it's already in the system), using the id of the pilot to be updated in the route:
``` JSON
{
    "name": "David Tennant",
    "is_admin": true
}
```

### EXPECTED RESPONSE DATA:
An output of the updated pilot, serialised without their password:
```JSON
"Noice, you updated your email or password (or both!):",
{
    "arn": 10,
    "email": "doctor@who.com",
    "id": 1,
    "is_admin": true,
    "name": "David Tennant",
    "status": "active",
}
```
Otherwise, any applicable error messages (eg. trying to update their email to one already registered to someone else in their database)

<br>
<br>

![PATCH method for a pilot to edit their email or password](docs/R5/pPATCH:update_login.png)
### REQUIRED DATA INPUT:
`@jwt_required()`

A logged in pilot can update their email or password (or both) by entering them, with the same constraints as in the original POST method:
``` JSON
{
    "email": "tenth@who.com",
    "password": "Ro5eTyler",
}
```

### EXPECTED RESPONSE DATA:
A confirmation message, and the serialised pilot (without their password):
```JSON
"Noice, you updated your email or password (or both!):",
{
    "arn": 10,
    "email": "tenth@who.com",
    "id": 1,
    "is_admin": true,
    "name": "David Tennant",
    "status": "active",
}
```
Otherwise, any applicable error messages (eg. trying to update their email to one already registered to someone else in their database)

<br>
<br>

## Expirations Table

![GET method for all expirations](docs/R5/eGET:all.png)
### REQUIRED DATA INPUT:
`@jwt_required`

N/A, as it's a GET method

### EXPECTED RESPONSE DATA:
A list of all expirations that have been registered in the database with their corresponding dates, or else any applicable error messages (eg. no expirations entered yet)

<br>
<br>

![GET method for an individual pilot's expirations](docs/R5/eGET:pilot.png)
### REQUIRED DATA INPUT:
`@jwt_required`

N/A, as it's a GET method - just need the id of the pilot in the route

### EXPECTED RESPONSE DATA:
The expirations entry for a pilot with the dates their different requirements will be expiring, or else any applicable error messages (eg. not a valid pilot id)

<br>
<br>

![POST method for creating an expirations entry](docs/R5/ePOST:exps.png)
### REQUIRED DATA INPUT:
`@jwt_required()` and `@admin_authorisation`

All fields are required, except the `'id'` (which is the primary key and will be created upon registration of a new expirations entry), and `'asic'`, as not all piots require ASICs.
``` JSON
{
    "medical": "Date",
    "biannual_review": "Date",
    "company_review": "Date",
    "dangerous_goods": "Date",
    "asic": "Date" (can be left out),
}
```

### EXPECTED RESPONSE DATA:
An output of the new expirations entry, with the corresponding pilot's id and name nested:
``` JSON
{
    "biannual_review": "2025-02-14",
    "company_review": "2023-07-30",
    "dangerous_goods": "2023-12-31",
    "id": 1,
    "medical": "2024-03-09",
    "pilot": {
        "id": 1,
        "name": "David Tennant"
    }
}
```
Otherwise, any applicable error messages (eg. the ARN provided is already registered to another pilot in the database)

<br>
<br>

![DELETE method for deleting an expirations entry](docs/R5/eDELETE:exps.png)
### REQUIRED DATA INPUT:
`@jwt_required()` and `@admin_authorisation`

N/A, as it's a DELETE method, using the id of the pilot in the route whose expirations entry the admin wants to delete

### EXPECTED RESPONSE DATA:
Just a confirmation message including the pilot's id:
``` JSON
{
    "Confirmation": "All done; the expirations for Captain Numero 1 were deleted!"
}
```
Otherwise, any applicable error messages (eg. no admin authorisation)

<br>
<br>

![PATCH method for editing or updating a pilot's expirations](docs/R5/ePATCH:exps.png)
### REQUIRED DATA INPUT:
`@jwt_required()` and `@admin_authorisation`

Whatever dates the admin would like to update, with the same constraints as in the original POST method (except that nothing is required now, as it's already in the system), using the id of the pilot in the route whose expirations entry is to be updated:
``` JSON
{
    "asic": "2025-01-11",
    "company_review": "2024-07-30"
}
```

### EXPECTED RESPONSE DATA:
An output of the updated expirations entry, with the corresponding pilot's id and name nested:
``` JSON
{
    "asic": "2025-01-11",
    "biannual_review": "2025-02-14",
    "company_review": "2024-07-30",
    "dangerous_goods": "2023-12-31",
    "id": 1,
    "medical": "2023-10-09",
    "pilot": {
        "id": 1,
        "name": "David Tennant"
    }
}
```
Otherwise, any applicable error messages (eg. an invalid pilot's id in the route)

<br>
<br>

## Aircraft Table

![GET method for all aircraft](docs/R5/aGET:all.png)
### REQUIRED DATA INPUT:
`@jwt_required`

N/A, as it's a GET method

### EXPECTED RESPONSE DATA:
A list of all aircraft that have been registered in the database with their corresponding data, or else any applicable error messages (eg. no aircraft in the system yet)

<br>
<br>

![GET method for a specific aircraft](docs/R5/aGET:aircraft.png)
### REQUIRED DATA INPUT:
`@jwt_required`

N/A, as it's a GET method - just need the id of the aircraft in the route

### EXPECTED RESPONSE DATA:
A specific aircraft and its corresponding information, or else any applicable error messages (eg. not a valid aircraft id)

<br>
<br>

![POST method for creating a new aircraft](docs/R5/aPOST:aircraft.png)
### REQUIRED DATA INPUT:
`@jwt_required()` and `@admin_authorisation`

All fields are required, except the `'id'` (which is the primary key and will be created upon registration of a new pilot):
``` JSON
{
    "callsign": "String" (max length = 10, using only capital English letters, numbers, or dashes),
    "status": "String" (where the valid statuses are either "active" or "inactive"),
}
```

### EXPECTED RESPONSE DATA:
An output of the freshly added aircraft:
``` JSON
{
    "id": 1,
    "callsign": "VH-TARDIS",
    "status": "inactive"
}
```
Otherwise, any applicable error messages (eg. callsign provided is too long)

<br>
<br>

![DELETE method for deleting a pilot](docs/R5/aDELETE:aircraft.png)
### REQUIRED DATA INPUT:
`@jwt_required()` and `@admin_authorisation`

N/A, as it's a DELETE method, using the id of the aircraft to be deleted in the route

### EXPECTED RESPONSE DATA:
Just a confirmation message including the pilot's name:
``` JSON
{
    "Confirmation": "Aircraft WEBSTAR has flown outta the system"
}
```
Otherwise, any applicable error messages (eg. no admin authorisation)

<br>
<br>

![PATCH method for editing or updating an aircraft](docs/R5/aPATCH:aircraft.png)
### REQUIRED DATA INPUT:
`@jwt_required()` and `@admin_authorisation`

Whatever information the admin would like to update, with the same constraints as in the original POST method (except that nothing is required now, as it's already in the system), using the id of the aircraft to be deleted in the route
``` JSON
{
    "status": "active"
}
```

### EXPECTED RESPONSE DATA:
An output of the updated aircraft:
```JSON
{
    "id": 1,
    "callsign": "VH-TARDIS",
    "status": "active"
}
```
Otherwise, any applicable error messages (eg. trying to update their email to one already registered to someone else in their database)

<br>
<br>

## Flights Table

![GET method for all flights](docs/R5/fGET:all.png)
### REQUIRED DATA INPUT:
`@jwt_required`

N/A, as it's a GET method

### EXPECTED RESPONSE DATA:
A list of all flights that have been logged in the database with their corresponding dates, or else any applicable error messages (eg. no flights logged yet)

<br>
<br>

![GET method for all flights for a specific aircraft](docs/R5/fGET:all_aircraft_flights.png)
### REQUIRED DATA INPUT:
`@jwt_required`

N/A, as it's a GET method - just need the correct id of the aircraft in the route

### EXPECTED RESPONSE DATA:
All flight entries for a specified aircraft, or else any applicable error messages (eg. not a valid aircraft id)

<br>
<br>

![GET method for all flights for an individual pilot](docs/R5/fGET:all_pilot_flights.png)
### REQUIRED DATA INPUT:
`@jwt_required`

N/A, as it's a GET method - just need the correct id of the pilot in the route

### EXPECTED RESPONSE DATA:
All flight entries for a specified pilot, or else any applicable error messages (eg. not a valid pilot id)

<br>
<br>

![GET method for a specific flight](docs/R5/fGET:flight.png)
### REQUIRED DATA INPUT:
`@jwt_required`

N/A, as it's a GET method - just need the correct id of the flight in the route

### EXPECTED RESPONSE DATA:
A specific flight entry and its corresponding information, or else any applicable error messages (eg. not a valid flight id)

<br>
<br>

![POST method for logging a new flight](docs/R5/fPOST:flight.png)
### REQUIRED DATA INPUT:
`@jwt_required()`

Only logged in pilots (that is authenticated, and therefore with an `"active"` status) can log flights, and the pilot id will be automatically assigned with the logged in pilot's token.

All fields are required, except the `'id'` (which is the primary key and will be created upon registration of a new flight). 
``` JSON
{
    "aircraft_id": Integer (must be an aircraft with an "active" status),
    "date": "Date",
    "route": "String" (min length = 10, max length = 100, using only English letters, numbers, dashes, spaces or exclamation points because they're fun!),
    "landings": "Integer",
    "flight_time": "Decimal" (decimal places = 2, and a max. flight time of 12.00)
}
```

### EXPECTED RESPONSE DATA:
An output of the freshly logged flight with the corresponding pilot's id and name nested:
``` JSON
{
    "aircraft_id": 1,
    "date": "2005-04-16",
    "flight_time": 1.12,
    "id": 1,
    "landings": 1,
    "pilot": {
        "id": 1,
        "name": "David Tennant",
    },
    "route": "Bad Wolf Bay One Way" 
}
```
Otherwise, any applicable error messages (eg. the aircraft isn't active)

<br>
<br>

![DELETE method for deleting a flight](docs/R5/fDELETE:flight.png)
### REQUIRED DATA INPUT:
`@jwt_required()` and `@admin_authorisation`

N/A, as it's a DELETE method, using the id of the individual flight entry to be deleted in the route

### EXPECTED RESPONSE DATA:
Just a confirmation message that includes the flight id:
``` JSON
{
    "Confirmation": "Flight 2 deleted successfully"
}
```
Otherwise, any applicable error messages (eg. no admin authorisation)

<br>
<br>

![PATCH method for editing or updating a flight](docs/R5/fPATCH:flight.png)
### REQUIRED DATA INPUT:
`@jwt_required()` and `@admin_authorisation`

Whatever information the admin would like to update, with the same constraints as in the original POST method (except that nothing is required now, as it's already in the system), using the id of the flight to be updated in the route:
``` JSON
{
    "flight_time": 1.13,
    "landings": 2,
    "route": "Bad Wolf Bay Return" 
}
```

### EXPECTED RESPONSE DATA:
An output of the updated flight, with the pilot still nested:
```JSON
{
    "aircraft_id": 1,
    "date": "2005-04-16",
    "flight_time": 1.13,
    "id": 1,
    "landings": 2,
    "pilot": {
        "id": 1,
        "name": "David Tennant",
    },
    "route": "Bad Wolf Bay Return" 
}
```

Otherwise, any applicable error messages (eg. trying to update their email to one already registered to someone else in their database)

<br>
<br>

# R6. An ERD for your API

![Company Flight Log ERD](docs/company_flight_log.png)

<br>
<br>

# R7. Detail any third party services that your app will use

## Flask
Flask is my new friend, giving a framework to build a web application quickly (which is relative 😂), and it’s hugely versatile and flexible! It allows for an essentially limitless program that can utilise a heck of a lot of libraries to bring your dream app to life. The available tools and features cover everything from models, decorators, blueprints, controllers, to handling URL requests, HTTP methods, routing, and even styling with a CSS stylesheet or JavaScript functions if your heart/project/client so desires!

## SQLAlchemy
SQLAlchemy is probably THE most significant library that was utilised for this app, when you see how many `db.`s there are throughout the code! It’s the Object Relational Mapping (ORM) library that allows me/developers to interact with the relational database using Python classes, objects and relationships.

## psycopg2
This is the adaptor that enables Python apps to connect to and interact with PostgreSQL databases. It allows developers to execute SQL queries, utilise CRUD functionality (that is, Create, Read, Update, Delete), and essentially manages the database transactions quickly and reliably.

## Marshmallow
This is a handy library for validation and serialisation in Python, which is why it was the backbone of all schema in my app. When used correctly, it’s amazing for data integrity by enforcing constraints (which can be specified by the developer), allowing for custom error messages, and also for converting complete data structures in JSON or other formats for communication between systems.

## Bcrypt
Hashing is virtually impossible to decrypt, and therefore a one-way function. It’s always good practice to hash passwords, which is the process of converting plain texts into a hashed format that, again: can’t be decrypted. The beauty of this is that even in the event of a cyber attach or data breach, anyone with access to the password database won’t be able to do anything with those hashed passwords. 
This is where bcrypt comes into play: it’s considered one of the most secure algorithms in Python for password hashing, and is a nice handy library that I’ve used<sup>i</sup>.

## JWT Extended 
This is a Flask library that is commonly used for authentication and authorisation in apps, and I used it in mine! When a pilot successfully logs in with their correct email and password, a token containing relevant information (such as the user’s role and permissions) will be generated by the server, issued to the pilot and stored for subsequent requests.

## python-dotenv
dotenv is a library that allows developers to manage environment variables such as the database URL and secret key in key-value pairs without ‘exposing them to the outside world’.<sup>ii</sup> The sneaky fullstop at the beginning of the env file makes it hidden on most operating systems, and by adding it to the .gitignore file, it won’t be committed to a git repository either, which ensures sensitive configuration information is kept separate from the codebase and more secure. 

## Postman
A great tool for testing APIs, by allowing the developer to interact with their database. It has functionality to send different HTTP requests for routes, receive input, and return output - sometimes what we’re expecting, and a lot of the time error messages that the developer can then debug! Postman also allows for authentication and tokens, which meant that for this project I could essentially test EVERYTHING from start to finish, purposely enter incorrect information or expired tokens, and ensure that I ended up with either the returned object I wanted or the applicable error messages.

<br>

<sup>i</sup>Atharva Shah, last edited 18/04/2023, <i>Hashing Passwords in Python with BCrypt</i>, tutorialspoint, accessed 8th July 2023, <https://www.tutorialspoint.com/hashing-passwords-in-python-with-bcrypt>

<sup>ii</sup>Emma Donery, 6/9/2021, <i>Python-dotenv (Keep your secrets safe)</i>, Dev Community, accessed 30th July 2023,
 <https://dev.to/emma_donery/python-dotenv-keep-your-secrets-safe-4ocn>

<br>
<br>

# R8. Describe your projects models in terms of the relationships they have with each other

The four tables in my ERD of Pilot, Expirations, Aircraft and Flight are defined and created with four models, found in /src/models, under pilot.py, expirations.py, aircraft.py and flight.py respectively. 

These are further detailed and validated through their schemas, found in /src/schemas with corresponding names.

Lastly, the functionality of each model is determined by the controllers, in /src/controllers, again, with their corresponding named files.

*Note: there's already a lot of repetition below to ensure everything is covered, so for the sake of keeping* some *of it DRY (or at least not soaking wet!):* 
* `db.` is simply a shortcut created in init.py, where `db = SQLAlchemy`
* `back_populates` ensures that relevant information that is updated in one instance of a pilot/expirations/flight/aircraft will automatically be updated in the other

## Pilot Model: *pilot.py*

All pilots in the company must be registered in the database.

The Pilot model:

``` py
class Pilot(db.Model):
    __tablename__ = 'pilot'

    id = db.Column(db.Integer, primary_key=True)
    arn = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    expirations = db.relationship('Expirations', back_populates='pilot')
    flight = db.relationship('Flight', back_populates='pilot')
```

The `'id'` is automatically assigned upon registration of a pilot, with those numbers going up incrementally as more pilots are added to the database.

The fields `'arn'`, `'name'`, `'email'`, `'password'`, `'status'` and `'is_admin'` are all required to register a new pilot, with their datatypes specified in the model as well as further applicable validation in the schema.

'Logging in' requires a pilot to have the status of 'active' and provide their email and password. Upon successful authentication will give a JSON web token (JWT) to use for further functionality, such as updating an email or password, or when logging a flight.

### Pilot (parent) to Expirations (child) relationship
A pilot must exist in the database in order for an expirations entry to be created for them.

This relationship is created with `expirations = db.relationship('Expirations', back_populates='pilot')` in the Pilot model and similarly `pilot = db.relationship('Pilot', back_populates='expirations')` in the Expirations model, as well as assigning the primary key `'id'` as a foreign key `'pilot_id'` in the Expirations model.

### Pilot (parent) to Flight (child) relationship
Pilots must be authenticated (that is, logged in and also therefore with an 'active' status), in order to log any flights they have completed.

This relationship is created with `flight = db.relationship('Flight', back_populates='pilot')` in the Pilot model and similarly `pilot = db.relationship('Pilot', back_populates='flight')` in the Flight model, as well as assigning the primary key `'id'` as a foreign key `'pilot_id'` in the Flight model.

<br>

## Expirations Model: *expirations.py*

All pilots should have an expirations entry (and can only have one). 

The Expirations model:

```py
class Expirations(db.Model):
    __tablename__ = 'expirations'

    id = db.Column(db.Integer, primary_key=True)
    # Include pilot using foreign key
    pilot_id = db.Column(
        db.Integer, db.ForeignKey('pilot.id'), nullable=False, unique=True
        )
    medical = db.Column(db.Date, nullable=False)
    biannual_review = db.Column(db.Date, nullable=False)
    company_review = db.Column(db.Date, nullable=False)
    dangerous_goods = db.Column(db.Date, nullable=False)
    asic = db.Column(db.Date)

    pilot = db.relationship('Pilot', back_populates='expirations')
```

The `'id'` is automatically assigned upon successful entry of a pilot's expirations dates, with those `'id'` numbers going up incrementally as more expirations entries are added to the database for each pilot.

The fields `'medical'`, `'biannual_review'`, `'company_review'` and `'dangerous_goods'` are all required when using the POST method to enter expirations dates, where `'asic'` can be left null if that pilot doesn't have or require one. All datatypes must be valid dates, with the format YYYY-MM-DD being validated in the schema.

### Expirations (child) to Pilot (parent) relationship
As stated above, a pilot must exist in the database in order for an expirations entry to be created for them.

This relationship is created with `pilot = db.relationship('Pilot', back_populates='expirations')` in the Expirations model and similarly `expirations = db.relationship('Expirations', back_populates='pilot')` in the Pilot model, as well as assigning the foreign key `'pilot_id'` in the Expirations model.

For an admin to correctly assign a expirations entry for a specific pilot, they simply have to enter that pilot's `'pilot_id'` in the route.

This is then applied in the function as below:

``` py
def add_expirations(pilot_id):
    ...
    # Check if the pilot_id given in the route is an existing pilot
    stmt = db.select(Pilot).filter_by(id=pilot_id)
    pilot = db.session.scalar(stmt)
    #If there's no pilot that matches the pilot_id, give error
    if not pilot:
        return { 'Error': 'Dang, no pilot with that id was found' }, 404
```
where the pilot is searched for by trying to match the `'pilot_id'` in the route to the primary key `'id'` of a valid pilot, in order for an expirations entry to be made for them.

Now, as the `'pilot_id'` must also be unique in the Expirations table, this ensures that only one pilot can have an expirations entry and if an attempt is made to create a duplicate, it will raise a `UNIQUE_VIOLATION` and stop the process.

For deleting or updating an expirations entry, the admin still needs to add that pilot's `'pilot_id'` in the route.

However, searching for the entry is slightly different as it's already been created in Expirations:

``` py
def function(pilot_id):
    stmt = db.select(Expirations).filter_by(pilot_id=pilot_id)
    pilot_expirations = db.session.scalar(stmt)
```
and then any applicable errors are handled a little further down in try/except blocks.

<br>

## Aircraft Model: *aircraft.py*

All aircraft in the company must be registered in the database.

The Aircraft model:

``` py
class Aircraft(db.Model):
    __tablename__ = 'aircraft'

    id = db.Column(db.Integer, primary_key=True)
    callsign = db.Column(db.String(10), nullable=False, unique=True)
    status = db.Column(db.String, nullable=False)

    flight = db.relationship('Flight', back_populates='aircraft')
```

The `'id'` is automatically assigned upon adding a new aircraft, with those numbers going up incrementally as more pilots are added to the database.

The fields `'callsign'` and `'status'` are both required to add a new aircraft, both as strings, with further applicable validation in the schema.

### Aircraft (parent) to Flight (child) relationship
An aircraft must have an 'active' status in order to fly, and be noted in the Flight log.

This relationship is created with `flight = db.relationship('Flight', back_populates='aircraft')` in the Aircraft model and similarly `aircraft = db.relationship('Aircraft', back_populates='flight')` in the Flight model, as well as assigning the primary key `'id'` as a foreign key `'aircraft_id'` in the Flight model.

<br>

## Flight Model: *flight.py*

All flights are required to be logged, and can only be completed by one pilot in one aircraft. 

The Flight model:

```py
class Flight(db.Model):
    __tablename__ = 'flight'

    id = db.Column(db.Integer, primary_key=True)
    # Include pilot and aircraft using their foreign keys
    pilot_id = db.Column(
        db.Integer, db.ForeignKey('pilot.id'), nullable=False
        )
    aircraft_id = db.Column(
        db.Integer, db.ForeignKey('aircraft.id'), nullable=False
        )
    date = db.Column(db.Date, nullable=False)
    route = db.Column(db.String(100), nullable=False)
    landings = db.Column(db.Integer, nullable=False)
    flight_time = db.Column(db.DECIMAL(4,2), nullable=False)


    pilot = db.relationship('Pilot', back_populates='flight')
    aircraft = db.relationship('Aircraft', back_populates='flight')
```

The `'id'` is automatically assigned upon successfully logging a new flight, with those `'id'` numbers going up incrementally as more flights are logged.

The fields `'date'`, `'route'`, `'landings'` and `'flight_time'` are all required when using the POST method to log a flight, with their datatypes specified in the model as well as further applicable validation in the schema.

### Flight (child) to Pilot (parent) relationship
Flights can only be entered by a pilot who is authenticated (that is, logged in and therefore with an 'active' status).

This relationship is created with `pilot = db.relationship('Pilot', back_populates='flight')` in the Flight model and similarly `flight = db.relationship('Flight', back_populates='pilot')` in the Pilot model, as well as assigning the foreign key `'pilot_id'` in the Flight model.

As stated above, for a pilot to enter a flight, they must be logged in. Their JWT is then assigned to the `'pilot_id'` field, and searched through the registered pilots by querying Pilot objects for the same identity:

``` py
def add_flight():
    # Get the authenticated pilot's identity for the flight,
    # as pilots can only create their own flights
    pilot_id = get_jwt_identity()
    # Fetch the Pilot object corresponding to the pilot_id
    pilot = Pilot.query.get(pilot_id)
    # Just in case it's an invalid login and they still snuck their way in:
    if not pilot:
        return {
            'Error': 'Cheeeeeeky! Not sure how you got here, '
            "as that's an invalid id!"}, 403
```

When an admin is deleting or updating a logged flight, the pilot's id isn't required, as they can only log their own flights (and therefore the pilot cannot be updated).

<br>

### Flight (child) to Aircraft (parent) relationship
Flights obviously have to be flown by an aircraft! 

This relationship is created with `aircraft = db.relationship('Aircraft', back_populates='flight')` in the Flight model and similarly `flight = db.relationship('Flight', back_populates='aircraft')` in the Aircraft model, as well as assigning the foreign key `'aircraft_id'` in the Flight model.

The aircraft must also have an 'active' status. For the POST method, this is checked in the function as below:

``` py
def add_flight():
    ...
    # Ensure aircraft is an integer to search through Aircraft objects
    aircraft_id = int(flight_data.get('aircraft_id'))
    # If the id is an integer, continue through code
    if aircraft_id:
        # Search for corresponding aircraft with that id
        aircraft = Aircraft.query.get(aircraft_id)
        #If there's no aircraft that matches the aircraft, give below error
        if not aircraft:
            return {
                'Error': 'Uh-oh, no aircraft with that id exists'
                }, 404        
        # If aircraft is inactive, it can't be flown so throw error:
        if aircraft.status == 'inactive':
            return {
                'Error':
                "That aircraft didn't take off; it's inactive?"
            }, 406
    #If aircraft is missing or not an integer, give below error
    else: 
        return {
            'Error': 'Uh-oh, you seem to be missing an aircraft id'
            }, 404
    # The aircraft must be valid and active, so try to create a new flight:
    ...
```

It's pretty similar to the Pilot query above, where we check the given `'aircraft_id'` by querying the Aircraft objects for one that matches the `'id'`. 

Once established that it's a valid aircraft, we also need to check the status too, which is a nice easy 'if' statement: `if aircraft.status == 'inactive':`, before moving through the rest of the information given.

<br>
<br>

# R9. Discuss the database relations to be implemented in your application

R9: Discuss the database relations to be implemented in your application

The ERD above in R6 shows the four tables Pilot, Expirations, Aircraft and Flights, and the relationships between them, which are broken into more detail below.

Each table has fields for a primary key and other relevant information, with brackets denoting the applicable data type for each field, whether or not it can be left empty (noted by NOT NULL), and if a field is required to be unique.

Primary keys are then used in other tables as foreign keys to create a relationship between those two tables where/when necessary.

## Pilot Table
`id` is the primary key for the Pilot table, which is an automatically generated integer with the registration of each pilot.

The Pilot table has two different relationships: one to the Expirations table, and one to the Flight table. For both relationships, Pilot table is the ‘parent’, with the primary key becoming a foreign key `pilot_id` when added to the ‘children’ Expirations and Flight tables.

**Pilot to Expirations** is a one to one relationship, as one pilot can only have one expirations entry, and all expirations entries must be linked to one pilot.

**Pilot to Flight** is a one to many relationship, as one pilot will (hopefully!) complete many flights, and each flight is linked to only one pilot.


## Expirations Table
`id` is the primary key for the Expirations table, which is an automatically generated integer with the creation of each expirations entry.

The Expirations table only has one relationship. As above, the Expirations table is the ‘child’ to Pilot table, with that relationship created by the `pilot_id` foreign key of its 'parent' table Pilot. 

**Expirations to Pilot** is a one to one relationship, as one pilot can only have one expirations entry, and an expirations entry cannot be created without a linked pilot.


## Aircraft Table
`id` is the primary key for the Aircraft table, which is an automatically generated integer with the addition of each aircraft into the database.

The Aircraft table has one relationship to the Flight table, where Aircraft table is the ‘parent’, with the primary key becoming a foreign key `aircraft_id` when added to the ‘child’ Flight table.

**Aircraft to Flight** is a one to many relationship, as one aircraft can complete many flights, and each flight is completed by only one aircraft.


## Flight Table
`id` is the primary key for the Flight table, which is an automatically generated integer with each flight that is logged.

The Flight table has two different relationships: one to the Pilot table, and one to the Aircraft table. For both relationships, Flight table is the ‘child’, referencing the foreign keys `pilot_id` and `aircraft_id` for each flight.

**Flight to Pilot** is a many to one relationship, as many flights can be completed but will only ever have only pilot per flight.

**Flight to Aircraft** is also a many to one relationship, as many flights can be completed but will only ever have only aircraft per flight.

<br>
<br>

# R10. Describe the way tasks are allocated and tracked in your project

For all of my assignments, I personally print out and highlight key information, so I can have it spread out on my desk to see it all laid out in front of me - literally. Going through it all with a pen and a highlighter helps give me a better understanding of the requirements before even starting, and includes breaking down questions into key dot points that I might want to focus on throughout the project. 

![Printed rubric](docs/R10/printed_rubric.png)

I expect I’ll do it the same in the workforce too when I step into a real job! 😉

I then copy and paste the questions into a new document, where I write up all my answers. I can use Pages/Microsoft Word better than Obsidian at this stage, so I find I get into a flow state better for writing, researching, editing my answers, and then I can simply move the whole document into VS Code (or Obsidian to format it correctly as a markdown file if required).

With my .doc document, I also have a colour code - similar to what I’ll go through below for my Trello board. Every question starts off orange, then I change it to blue when I’ve began a question or am working on it, and when I’m happy and feel that question is complete, I finally change it to black - ready to copy into Obsidian/Visual Studio Code.

I’m a pretty visual person, and also tend to work through different chunks of questions back and forth - most of them have a little overlap here and there too - so this colour system helps me see what I’ve done, what still needs work, and what I’m yet to begin.

![Word document with questions and colours](docs/R10/word_document_colours.png)

Since joining Coder Academy, I have also started utilising project management tools such as monday.com and Trello boards (depending on which one seems to better fit the project I’m currently working on), to help track and easily update progress.

For this assignment, I felt a Trello board worked perfectly! It was easy to break up the workload into more manageable ‘chunks’/lists, give dot points in each of those lists, with the ability to further expand in notes if I need to, and then colour code them for a super easy snapshot of how everything is progressing.

The lists that I started off with were:
- README - Q’s + RUBRIC: Includes each question with the key requirements
- API - RUBRIC: Includes the different rubric requirements for the actual API code
- API Code: The building blocks for my web server
- API Functionality: Making sure I incorporate a range of CRUD functionality across the database

![Trello board](docs/R10/trello_board.png)

Any extra notes or questions I had would show up as three little lines under the 'task', and then I could click into that to view, such as the example of 'Uses appropriate model methods':

![Trello further notes](docs/R10/trello_more_details.png)

The colours that I use for categorising each task are a bit of a gradient:

![screenshot of colour code](docs/R10/trello_labels_colours.png)

- Orange: *Need to Start* - same colour I use for this document!
- Purple: *Have Started!* - bare bones are in, but needs significant work
- Blue: *Nearly Done :)* - self explanatory 😉
- Green: *Finito! 🥳* - this part has been completed! Celebrate! (and I could have used black to match the .doc file, but it doesn’t feel as celebratory)
- Red: *Eeep, #strugglestreet* - something I’m struggling with or blocked on.

Note: they automatically sort themselves, so the order doesn’t exactly look right in Trello, but I know what it is!

Overall, for me, being both visual and loving personal validation (who doesn’t?!), these colours - both on the .doc file and on the Trello board - help motivate me to keep plugging away, and to be proud of my progress. They help keep me on track; knowing at a glance what areas are lacking, and watching those little Trello bars turn to green or my text here turn to black honestly help spur me on.

Now, I also mentioned that I 'started off' with those lists of tasks above.

As I began to flesh out the app, I realised that it would be a lot easier for me to visualise my progress and track tasks if I broke them further down, so you can see the Trello board I ended up with by [clicking here](https://trello.com/b/0uHOqa55/flightlogdb).

As well as all of the above, I ALSO like to scrawl out notes, thoughts and questions as I go. I've got a journal I keep open on my desk, and I can quickly jot down issues that might arise as I'm debugging something else, or questions that I want to ask in person (thank you Jairo!) etc.

![Handwritten notes](docs/R10/handwritten_notes.png)

I know there seems to be a lot of back and forth, but it makes sense to me, and the three different systems (that is, a Pages document for these questions, a Trello board for tracking progress, and my journal for notes as I go through code) ensures I cover all bases thoroughly.