from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import current_user
from DeadMatter.reports.forms import report_server_form, report_page_form
from DeadMatter.models import Servers
from DeadMatter.reports.utils import send_server_report_email, send_page_report_email


reports = Blueprint('reports', __name__)


@reports.route('/server/<server_name>/report', methods=['GET', "POST"])
def report_server(server_name):
    form = report_server_form()
    if current_user.is_authenticated:
        form.email.data = current_user.email
    if form.validate_on_submit():
        send_server_report_email(form)
        flash(f"Your report has been send!", 'success')
        return redirect(url_for('main.index'))

    return render_template('report/report_page.html', form=form)


@reports.route('/report', methods=['GET', "POST"])
def report():
    form = report_page_form()
    if current_user.is_authenticated:
        form.email.data = current_user.email
    if form.validate_on_submit():
        send_page_report_email(form)
        flash(f"Your report has been send!", 'success')
        return redirect(url_for('main.index'))

    return render_template('report/report_page.html', form=form)
