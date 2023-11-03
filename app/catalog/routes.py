from app.catalog import main
from app import db
from app.catalog.models import Project, Vendor, Transaction
from app.catalog.forms import CreateProjectForm, CreateVendorForm, CreateTransactionForm
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required


@main.route('/')
def display_projects():
    projects = Project.query.all()
    return render_template('home.html', projects=projects)


@main.route('/display/vendors')
def display_vendors():
    vendors = Vendor.query.all()
    return render_template('vendor.html', vendors=vendors)


@main.route('/display/project-expenses/<project_id>')
def display_transactions_for_project(project_id):
    project = Project.query.filter_by(id=project_id).first()
    transactions = Transaction.query.filter_by(project_id=project_id).all()

    return render_template('project-transactions.html', project=project, transactions=transactions)


@main.route('/create/project', methods=['GET', 'POST'])
def create_book():
    form = CreateProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data, site=form.site.data, start_date=form.start_date.data,
                          end_date=form.end_date.data, description=form.description.data)
        db.session.add(project)
        db.session.commit()
        flash('Project added successfully')
        return redirect(url_for('main.display_projects'))
    return render_template('create_project.html', form=form)


@main.route('/create/expense/<int:project_id>', methods=['GET', 'POST'])
def create_expense(project_id):
    form = CreateTransactionForm()
    form.project_id.data = project_id  # Automatically set project_id
    if form.validate_on_submit():
        # Process the form data and save the expense to the database
        transaction = Transaction(amount=form.amount.data, description=form.description.data,
                                  paymentDate=form.paymentDate.data, paymentDetails=form.paymentDetails.data,
                                  project_id=form.project_id.data, vendor_id=form.vendor.data)
        db.session.add(transaction)
        db.session.commit()
        flash('Expense added successfully')
        return redirect(url_for('main.display_transactions_for_project', project_id=project_id))
    return render_template('create_expense.html', form=form, project_id=project_id)


@main.route('/create/vendor', methods=['GET', 'POST'])
def create_vendor():
    form = CreateVendorForm()
    if form.validate_on_submit():
        vendor = Vendor(name=form.name.data, description=form.description.data, address=form.address.data,
                        contactNbr=form.contactNbr.data)
        db.session.add(vendor)
        db.session.commit()
        flash('Vendor added successfully')
        return redirect(url_for('main.display_vendors'))
    return render_template('create_vendor.html', form=form)


