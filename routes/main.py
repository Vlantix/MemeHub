from flask import Blueprint, render_template
import traceback

landing_bp = Blueprint('landing', __name__)

@landing_bp.route("/")
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        print("ERROR:", e)
        print(traceback.format_exc())
        return str(e), 500