# How we interact with PostgreSQL

Key insight: There is one server, and everything else is just a remote control for it. When you install Postgres, it set up a background service that starts running and just sits there waiting for connections listening on port 5432. It is not something we interact with diectly, it has no window or UI. This is the actual owner of our data and all the database and everything in it lives inside files that this server process manages on disk.

- pgAdmin is just a client. pgAdmin doesn't store the database, rather it is a GUI that opens a connection to the Postgres server and sends SQL commands over that connection and displays whatever the server sends back.

- Our Python/VS code is also just a client.
```
engine = create_engine('postgresql+psycopg://postgres:postgres@localhost:5432/satutorialdatabase', echo=True)
```
This line is similar to what pgAdmin does - opening a network connection to the same server, at the same address  localhost:5432 and connects to the Postgres server directly.


# How PostgreSQL differs from SQLite

- SQLite: the database is a single .db file that sits in your project folder. There is no server, no login no network - your python code just opens that file directly. No remote/network access so a different computer on the internet of even another computer on the same WIFI network cannot connect to your SQLite file.

- Postgres: the database lives inside a running server process, completely separate from any single application or folder. Then multiple different programs (pgAdmin, python app, another app, another laptop if configured for remote access) can all connect to that one database server at the same time over the network.

- This is the reason why Postgres is built for real multi-user production apps, and SQLite generally isn't. Postgres running as an actual server is designed for many clients possible on different machines, all talking to a central database at once. Postgres can handle many concurrent connections such as if multiple users hit our API simultaneously from their browsers.