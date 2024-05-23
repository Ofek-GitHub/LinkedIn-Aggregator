from flask import Blueprint
from .controllers import get_jobs

linkedin_jobs_bp = Blueprint("linkedin_jobs_bp", __name__)


@linkedin_jobs_bp.route("/<string:keywords>", methods=["GET"])
def api(keywords):
    return get_jobs(keywords)
