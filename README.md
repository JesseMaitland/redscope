# Redscope
### A schema introspection tool for aws Redshift


#### getting started
```bash
pip install redscope
```

#### Create a redscope project
```bash
redscope init
```

#### populate the redshift/redscope/.redscope file
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
