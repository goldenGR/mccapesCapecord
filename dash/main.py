import os

from flask import Flask
import database.supabase

app = Flask(__name__)

from api.login import login_bp
from api.pages import pages_bp
from api.landing_page import landing_bp

app.secret_key = os.getenv("FLASK_SECRET_KEY")

app.register_blueprint(login_bp)
app.register_blueprint(pages_bp)
app.register_blueprint(landing_bp)

if __name__ == "__main__":
    app.run(debug=True)