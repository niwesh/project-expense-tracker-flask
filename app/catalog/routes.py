from app.catalog import main
from app import db
from app.catalog.models import Project, Vendor, Transaction, Firm
from app.catalog.forms import CreateProjectForm, CreateVendorForm, CreateTransactionForm, CreateFirmForm
from flask import render_template, request, redirect, url_for, flash, jsonify


@main.route('/')
def display_projects():
    projects = Project.query.all()
    firms = Firm.query.all()
    return render_template('home.html', projects=projects, firms=firms)


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
def create_project():
    firm_id = request.args.get('firm_id')  # Get the firm_id from the query parameters
    firm = Firm.query.get(firm_id)
    firm_name = firm.name
    form = CreateProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data, site=form.site.data, start_date=form.start_date.data,
                          end_date=form.end_date.data, description=form.description.data,
                          firm_id=firm_id)  # Set firm_id here
        db.session.add(project)
        db.session.commit()
        flash('Project added successfully')
        return redirect(url_for('main.display_projects'))
    return render_template('create_project.html', form=form, firm_id=firm_id,
                           firm_name=firm_name)  # Pass firm_id to the template


@main.route('/create/expense/<int:project_id>', methods=['GET', 'POST'])
def create_expense(project_id):
    form = CreateTransactionForm()
    form.project_id.data = project_id  # Automatically set project_id

    project = Project.query.get(project_id)
    firm = Firm.query.get(project.firm_id)

    firm_name = firm.name
    project_name = project.name

    if form.validate_on_submit():
        # Process the form data and save the expense to the database
        transaction = Transaction(
            amount=form.amount.data,
            description=form.description.data,
            paymentDate=form.paymentDate.data,
            paymentDetails=form.paymentDetails.data,
            project_id=form.project_id.data,
            vendor_id=form.vendor.data,
            firm_id=firm.id
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Expense added successfully')
        return redirect(url_for('main.display_transactions_for_project', project_id=project_id))

    return render_template('create_expense.html', form=form, project_name=project_name, firm_name=firm_name,
                           project_id=project_id, firm_id=firm.id)


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


@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@main.route('/display/transactions', methods=['GET', 'POST'])
def display_transactions():
    firms = Firm.query.all()
    projects = Project.query.all()

    selected_firm_id = None
    selected_project_id = None
    selected_firm_name = ""
    selected_project_name = ""
    selected_date = None

    # Handle form submission
    if request.method == 'POST':
        selected_firm_id = request.form.get('firm')
        selected_project_id = request.form.get('project')

        # Filter transactions by selected firm and project
        transactions_query = Transaction.query
        if selected_firm_id:
            transactions_query = transactions_query.filter_by(firm_id=selected_firm_id)
        if selected_project_id:
            transactions_query = transactions_query.filter_by(project_id=selected_project_id)

        # Fetch and display transactions
        transactions = transactions_query.all()

        selected_firm_name = Firm.query.get(selected_firm_id).name if selected_firm_id else ""
        selected_project_name = Project.query.get(selected_project_id).name if selected_project_id else ""

        total_amount = sum(transaction.amount for transaction in transactions)

        return render_template('transactions.html', firms=firms, projects=projects, transactions=transactions,
                               total_amount=total_amount, selected_firm_id=selected_firm_id,
                               selected_project_id=selected_project_id,
                               selected_firm_name=selected_firm_name, selected_project_name=selected_project_name)

    # Display all transactions by default
    transactions = Transaction.query.all()
    total_amount = sum(transaction.amount for transaction in transactions)
    return render_template('transactions.html', firms=firms, projects=projects, transactions=transactions,
                           total_amount=total_amount, selected_firm_id=selected_firm_id,
                           selected_project_id=selected_project_id,
                           selected_firm_name=selected_firm_name, selected_project_name=selected_project_name)


@main.route('/get_projects_for_firm', methods=['POST'])
def get_projects_for_firm():
    firm_id = request.form.get('firm_id')
    projects = Project.query.filter_by(firm_id=firm_id).all()

    project_options = ""
    for project in projects:
        project_options += f'<option value="{project.id}">{project.name}</option>'

    return project_options


@main.route('/create/firm', methods=['GET', 'POST'])
def create_firm():
    form = CreateFirmForm()

    if form.validate_on_submit():
        firm = Firm(
            name=form.name.data,
            address=form.address.data,
            description=form.description.data,
            gst_no=form.gst_no.data
        )

        db.session.add(firm)
        db.session.commit()

        flash('Firm added successfully', 'success')
        return redirect(url_for('main.display_firms'))

    return render_template('create_firm.html', form=form)


@main.route('/display/firms')
def display_firms():
    firms = Firm.query.all()
    return render_template('firm.html', firms=firms)
