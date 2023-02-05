import os

def get_env_var(env_file):
    env_vars = {}
    with open(env_file) as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            key, value = line.strip().split('=', 1)
            
            env_vars[key] = value # Save to a dict
            
        return env_vars

def update_env_vars(env_file):
    vars = get_env_var(env_file)
    for key, value in vars.items():
        os.environ[key] = value

# Create connection string
def create_conn_string(user, password, host, db_name, engine_type, port=0, oracle_path=""):
    conn_str = user + ":" + password + "@" + host
    if(port != '0'):
        conn_str += ":" + str(port)
    if(engine_type == "mysql"):
        return "mysql://" + conn_str + "/" + db_name + "?charset=utf8mb4"
    elif(engine_type == "mariadb"):
        return "mariadb://" + conn_str + "/" + db_name + "?charset=utf8mb4"
    elif(engine_type == "postgresql"):
        return "postgresql://" + conn_str + "/" + db_name
    elif(engine_type == "mssql"):
        return "mssql+pyodbc://" + conn_str + "/" + db_name

update_env_vars(".env")

class Config(object):
    ENV = os.environ.get("FLASK_ENV")
    FLASK_APP = os.environ.get("FLASK_APP")
    SCHEDULER_API_ENABLED = os.environ.get("SCHEDULER_API_ENABLED")
    SCHEDULER_TIMEZONE = os.environ.get("SCHEDULER_TIMEZONE")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    # SQLALCHEMY_DATABASE_URI = create_conn_string(
    #     os.environ.get("DATABASE_USER"),
    #     os.environ.get("DATABASE_PASSWORD"),
    #     os.environ.get("DATABASE_HOST"),
    #     os.environ.get("DATABASE_NAME"),
    #     os.environ.get("DATABASE_ENGINE"),
    #     os.environ.get("DATABASE_PORT")
    #     )
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flexy.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False