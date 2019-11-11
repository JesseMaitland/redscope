# Redscope

Redscope is a database migration and introspection tool, designed to help manage your instance of Amazon Redshift.
All migrations are written in plain SQL, in `.sql` files, with no fancy tricks or dependencies on ORM frameworks.

Migration files are timestamp tracked, to eliminate the possibility of a migration key duplication.

### Getting Started

#### Install
Redscope can be installed by using pip.
```
pip install redscope
```

#### New Project
Once Redscope is installed, create a new project.
```
redscope init project
```

This will create the directories where your migrations, ddl, and log files will live.
The `redscope.log` file is used to record every command executed in redscope.
```
database
    ddl
    logs
        redscope.log
    migrations
```
#### Environments
By default, Redscope will look for a `.env` file in the `root` directory of your project, and will load
the connection string in `REDSCOPE_DB_URL` as an environment variable.


#### Init Database
Once a connection string has been provided in a `.env` file, the tables to keep track of applied migrations
must be created. Running the below command will create a schema and table `redscope.migrations`.

```
redscope init db
```

#### Creating Migrations

To create a new migration run the below command, where `name-of-my-migration` is the name you want for your migration. 
This will create a directory in the `migrations` directory which will contain 2 files `up.sql` and `down.sql`

```
redscope new migration --name name-of-my-migration
```

In `up.sql`, place the SQL commands you want to execute against the database to bring the data base `up` to the newest state.
In `down.sql`, place the SQL commands to run, to undo the changes made to the database when the `up.sql` file was executed.

#### Running Migrations

To execute all un-applied migrations

```
redscope migrate up
```

This will apply all the local migration files, against the target database.

To revert the changes

```
redscope migrate down
```


### Custom Environments

In larger projects, perhaps it is possible to have several `.env` files and connections to databases which code in 
your cool project uses to perform some database operation. `redscope` allows using custom `.env` files, and custom environment
variables. Redscope will however expect that this file lives in the root directory of your project.

To load a custom ``.env`` file, but use the default `REDSCOPE_DB_URL` pass the optional `--env-file` parameter.

```
redscope migrate up --env-file dev.env
```

To load the default ``.env`` file, however use a custom environment variable


```
redscope migrate up --env-var MY_OTHER_DB_CONN_STRING
```

To load both a custom file, and custom var

```
redscope migrate up --env-file dev.env --env-var MY_OTHER_DB_CONN_STRING
```

This makes it possible to connect redscope to several databases in a single project.


To load a custom environment, eg `my_cool_file.env` simply pass the file name 

