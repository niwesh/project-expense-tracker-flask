from app import db  # from the app package __init__
from datetime import datetime


# PROJECT TABLE
class Project(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    site = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __init__(self, name, site, start_date, end_date, description):
        self.name = name
        self.site = site
        self.start_date = start_date
        self.end_date = end_date
        self.description = description

    def __repr__(self):
        return 'The Project is {}'.format(self.name)


# VENDOR TABLE
class Vendor(db.Model):
    __tablename__ = 'vendor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    address = db.Column(db.String(700), nullable=False)
    contactNbr = db.Column(db.String(20), nullable=False)

    def __init__(self, name, description, address, contactNbr):
        self.name = name
        self.description = description
        self.address = address
        self.contactNbr = contactNbr

    def __repr__(self):
        return 'The Vendor is {}'.format(self.name)


# TRANSACTION TABLE
class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    paymentDetails = db.Column(db.String(300), nullable=False)
    paymentDate = db.Column(db.Date, nullable=False)

    # ESTABLISH RELATIONSHIP
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))

    def __init__(self, amount, description, paymentDetails, paymentDate, project_id, vendor_id):
        self.amount = amount
        self.description = description
        self.paymentDate = paymentDate
        self.paymentDetails = paymentDetails
        self.project_id = project_id
        self.vendor_id = vendor_id

    def __repr__(self):
        return '{} by {}'.format(self.amount, self.description)
