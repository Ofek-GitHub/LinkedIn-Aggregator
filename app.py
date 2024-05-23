from flask import Flask
from LinkedinJobs.routes import linkedin_jobs_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(linkedin_jobs_bp, url_prefix="/linkedin_jobs")


@app.route("/", methods=["GET"])
def index():
    return "Connected to the server"


if __name__ == "__main__":
    app.run(debug=True)
