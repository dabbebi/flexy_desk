from app import app, db, ma, init_database, register_blueprints
from config import Config
from flask import send_from_directory

# config object
config_obj = Config()

# Configure app from object
app.config.from_object(config_obj)

# Serve the front end application
@app.route("/flexy-desk/<path:path>")
def serve_frontend(path):
    if('static' in path):
        return send_from_directory("frontend",  str(path)[str(path).index('static'):]), 200
    elif('/' not in  str(path) and '.' in str(path)):
        return send_from_directory("frontend",  path), 200
    else:
        return send_from_directory("frontend", 'index.html'), 200

# Register backend blueprints
register_blueprints(app)

# init database
init_database(app, db, ma
                , True
                )

# Run Server
if __name__ == '__main__':
    # Turn on debug mode
    app.debug=True

    # run app
    app.run(host="0.0.0.0")


#################################### Development environment ###############################################
# To run app on development mode use this command : python -m flask run # or use this : python .\server.py #
############################################################################################################

#################################### Production environment ################################################
# To run this app execute this command      : flask --app app run                                          #
# To run it as an Externally Visible Server : flask run --host=0.0.0.0                                     #
# To specify the port number use --port     : flask run --host=0.0.0.0 --port=2200                         #
############################################################################################################