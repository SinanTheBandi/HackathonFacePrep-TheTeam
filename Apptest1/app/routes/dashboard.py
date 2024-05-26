from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
def index():
    room_summary = "5 rooms available today"
    return render_template('dashboard.html', room_summary=room_summary)
