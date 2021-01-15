# Redscope
### A schema introspection tool for aws Redshift
Redscope is used to read the raw SQL DDL from your redshift database and save 
the results to `.sql` files in an easy-to-use project tree.

### Why use Redscope?
Keeping track of the database schema is annoying. If DDL files are kept under version control, and a database migration tool
is used as part of your CI, there is a chance that the table definition can be out of date as it changes over time. This tool allows
the current state of the database schema to be read from redshift, and put under version control so changes can be tracked over time.

#### getting started
```bash
pip install redscope
```

#### Create a redscope project
```bash
redscope init
```

#### populate the redshift/redscope/.redscope file
This file is used to tell `redscope` how to connect to redshift. In order to easily support using existing `.env` files in your projects, 
it is necessary to tell `redscope` the name of your environment file, as well as the name of the 
environment variable which contains a standard `psycopg2` connection string.
```ini
[env]
file = name_of_env_file.env

[redshift]
connection = ENV_VARIABLE_WITH_PSYCOPG2_CONNECTION_STRING
```

#### Introspect the database schema
```bash
rescope inspect
```


### Redscope API

*STILL UNDER DEVELOPMENT*

For whatever reason, sometimes it is nice to be able to reference SQL ddl directly from your python code.
This can be accomplished using the `redscope` api.

```python
from pathlib import Path
from dotenv import load_dotenv
from redscope.api import RedshiftSchema

load_dotenv('my-env-file.env')

redshift_schema = RedshiftSchema('MY_DB_CONNECTION_NAME')

# sales_report_table now is a Table DDL object
sales_report_table = redshift_schema.schema('sales').table('report').fetch()

# will print full table ddl including constraints, encoding, and defaults
print(sales_report_table.ddl())

# will print simple ddl with just columns and data types
print(sales_report_table.simple_ddl())


# Accessing a function definition
func_foo = redshift_schema.schema('my_funcs').function('foo').fetch()

# func foo is a Function DDL object
print(func_foo.ddl())



# getting all objects in a schema
reporting_views = redshift_schema.schema('reporting').views().fetch()

for name, ddl in reporting_views.items():
    print(f"the key is the schema qualified view name. {name}")
    print(f"the value is the SQL ddl string.{ddl}")


# Files can also be saved
root_path = Path.cwd()

tables = redshift_schema.schema('sales').tables().fetch()

"""
root_path
    schema
        sales
            tables
                schema.table.sql -- one file per table
"""
for table in tables:
    table.save_file(root_path)

```


