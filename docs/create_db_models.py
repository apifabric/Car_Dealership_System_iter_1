# using resolved_model self.resolved_model FIXME
# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from datetime import date   
from datetime import datetime
from typing import List


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py


from sqlalchemy.dialects.sqlite import *

class Car(Base):
    """description: Represents a car in the dealership, including the brand it belongs to and its price. Tracks the number of test drives requested for this car."""
    __tablename__ = 'car'
    id = Column(Integer, primary_key=True, autoincrement=True)
    model = Column(String)
    brand_id = Column(Integer, ForeignKey('brand.id'))
    price = Column(Integer)
    year_of_manufacture = Column(Integer)
    test_drive_count = Column(Integer)

class Brand(Base):
    """description: Represents a car brand with a unique identifier."""
    __tablename__ = 'brand'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

class Customer(Base):
    """description: Represents a customer with contact details. Tracks the number of test drives requested by the customer."""
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    test_drive_count = Column(Integer)

class Sale(Base):
    """description: Details the sale transactions involving cars and customers."""
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True, autoincrement=True)
    car_id = Column(Integer, ForeignKey('car.id'))
    customer_id = Column(Integer, ForeignKey('customer.id'))
    sale_date = Column(DateTime)
    sale_price = Column(Integer)

class Dealer(Base):
    """description: Represents a dealership location along with its name. Tracks the total inventory count for the dealer."""
    __tablename__ = 'dealer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    location = Column(String)
    inventory_count = Column(Integer)

class Inventory(Base):
    """description: Tracks the number of a specific car model available at each dealer."""
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    dealer_id = Column(Integer, ForeignKey('dealer.id'))
    car_id = Column(Integer, ForeignKey('car.id'))
    quantity = Column(Integer)

class Employee(Base):
    """description: Contains the details of employees working at various dealerships. Tracks the number of services conducted by an employee."""
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True, autoincrement=True)
    dealer_id = Column(Integer, ForeignKey('dealer.id'))
    first_name = Column(String)
    last_name = Column(String)
    position = Column(String)
    service_count = Column(Integer)

class TestDrive(Base):
    """description: Records customer requests and actual test drive events with dates."""
    __tablename__ = 'test_drive'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    car_id = Column(Integer, ForeignKey('car.id'))
    date = Column(DateTime)

class Promotion(Base):
    """description: Lists active promotions on specific cars, including discounts. Tracks how many sales have utilized the promotion."""
    __tablename__ = 'promotion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    car_id = Column(Integer, ForeignKey('car.id'))
    description = Column(String)
    discount_percentage = Column(Integer)
    applied_count = Column(Integer)

class Maintenance(Base):
    """description: Stores information about maintenance and service history of cars. Associates maintenance tasks with employees."""
    __tablename__ = 'maintenance'
    id = Column(Integer, primary_key=True, autoincrement=True)
    car_id = Column(Integer, ForeignKey('car.id'))
    employee_id = Column(Integer, ForeignKey('employee.id'))
    last_serviced_date = Column(DateTime)
    service_details = Column(String)

class CarFeature(Base):
    """description: Defines the features that can be associated with different cars."""
    __tablename__ = 'car_feature'
    id = Column(Integer, primary_key=True, autoincrement=True)
    feature_name = Column(String)

class CarFeatureAssignment(Base):
    """description: Link table between cars and features to assign features to specific cars."""
    __tablename__ = 'car_feature_assignment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    car_id = Column(Integer, ForeignKey('car.id'))
    feature_id = Column(Integer, ForeignKey('car_feature.id'))


# end of model classes


try:
    
    
    # ALS/GenAI: Create an SQLite database
    import os
    mgr_db_loc = True
    if mgr_db_loc:
        print(f'creating in manager: sqlite:///system/genai/temp/create_db_models.sqlite')
        engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    else:
        current_file_path = os.path.dirname(__file__)
        print(f'creating at current_file_path: {current_file_path}')
        engine = create_engine(f'sqlite:///{current_file_path}/create_db_models.sqlite')
    Base.metadata.create_all(engine)
    
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # ALS/GenAI: Prepare for sample data
    
    
    session.commit()
    car1 = Car(id=1, model="Model S", brand_id=1, price=80000, year_of_manufacture=2021, test_drive_count=1)
    car2 = Car(id=2, model="Model 3", brand_id=1, price=40000, year_of_manufacture=2020, test_drive_count=1)
    car3 = Car(id=3, model="Mustang", brand_id=2, price=55000, year_of_manufacture=2022, test_drive_count=1)
    car4 = Car(id=4, model="Civic", brand_id=3, price=25000, year_of_manufacture=2019, test_drive_count=1)
    brand1 = Brand(id=1, name="Tesla")
    brand2 = Brand(id=2, name="Ford")
    brand3 = Brand(id=3, name="Honda")
    brand4 = Brand(id=4, name="Toyota")
    customer1 = Customer(id=1, first_name="Alice", last_name="Smith", email="alice@example.com", test_drive_count=1)
    customer2 = Customer(id=2, first_name="Bob", last_name="Johnson", email="bob@example.com", test_drive_count=1)
    customer3 = Customer(id=3, first_name="Charlie", last_name="Brown", email="charlie@example.com", test_drive_count=1)
    customer4 = Customer(id=4, first_name="Diana", last_name="Evans", email="diana@example.com", test_drive_count=1)
    sale1 = Sale(id=1, car_id=1, customer_id=1, sale_date=date(2022, 5, 20), sale_price=80000)
    sale2 = Sale(id=2, car_id=2, customer_id=2, sale_date=date(2022, 7, 15), sale_price=38000)
    sale3 = Sale(id=3, car_id=3, customer_id=3, sale_date=date(2022, 8, 30), sale_price=55000)
    sale4 = Sale(id=4, car_id=4, customer_id=4, sale_date=date(2022, 12, 5), sale_price=24000)
    dealer1 = Dealer(id=1, name="Auto World", location="New York", inventory_count=15)
    dealer2 = Dealer(id=2, name="Speed Motors", location="Los Angeles", inventory_count=20)
    dealer3 = Dealer(id=3, name="Fast Drive", location="Chicago", inventory_count=17)
    dealer4 = Dealer(id=4, name="Luxury Cars", location="Houston", inventory_count=19)
    inventory1 = Inventory(id=1, dealer_id=1, car_id=1, quantity=5)
    inventory2 = Inventory(id=2, dealer_id=2, car_id=2, quantity=10)
    inventory3 = Inventory(id=3, dealer_id=3, car_id=3, quantity=3)
    inventory4 = Inventory(id=4, dealer_id=4, car_id=4, quantity=7)
    employee1 = Employee(id=1, dealer_id=1, first_name="Paul", last_name="Davis", position="Sales Manager", service_count=3)
    employee2 = Employee(id=2, dealer_id=2, first_name="Laura", last_name="Miller", position="Technician", service_count=2)
    employee3 = Employee(id=3, dealer_id=3, first_name="Kevin", last_name="Cook", position="Accountant", service_count=4)
    employee4 = Employee(id=4, dealer_id=4, first_name="Sarah", last_name="Johnson", position="Receptionist", service_count=1)
    test_drive1 = TestDrive(id=1, customer_id=1, car_id=1, date=date(2022, 4, 10))
    test_drive2 = TestDrive(id=2, customer_id=2, car_id=2, date=date(2022, 6, 12))
    test_drive3 = TestDrive(id=3, customer_id=3, car_id=3, date=date(2022, 7, 18))
    test_drive4 = TestDrive(id=4, customer_id=4, car_id=4, date=date(2022, 9, 25))
    promotion1 = Promotion(id=1, car_id=1, description="Winter Sale", discount_percentage=10, applied_count=1)
    promotion2 = Promotion(id=2, car_id=2, description="Summer Clearance", discount_percentage=15, applied_count=1)
    promotion3 = Promotion(id=3, car_id=3, description="New Year Offer", discount_percentage=5, applied_count=1)
    promotion4 = Promotion(id=4, car_id=4, description="Anniversary Special", discount_percentage=20, applied_count=1)
    maintenance1 = Maintenance(id=1, car_id=1, employee_id=1, last_serviced_date=date(2022, 3, 10), service_details="Oil Change")
    maintenance2 = Maintenance(id=2, car_id=2, employee_id=2, last_serviced_date=date(2022, 5, 5), service_details="Brake Check")
    maintenance3 = Maintenance(id=3, car_id=3, employee_id=3, last_serviced_date=date(2022, 6, 22), service_details="Tire Rotation")
    maintenance4 = Maintenance(id=4, car_id=4, employee_id=4, last_serviced_date=date(2022, 8, 14), service_details="Battery Replacement")
    car_feature1 = CarFeature(id=1, feature_name="Sunroof")
    car_feature2 = CarFeature(id=2, feature_name="Leather Seats")
    car_feature3 = CarFeature(id=3, feature_name="Bluetooth")
    car_feature4 = CarFeature(id=4, feature_name="Backup Camera")
    car_feature_assignment1 = CarFeatureAssignment(id=1, car_id=1, feature_id=1)
    car_feature_assignment2 = CarFeatureAssignment(id=2, car_id=2, feature_id=2)
    car_feature_assignment3 = CarFeatureAssignment(id=3, car_id=3, feature_id=3)
    car_feature_assignment4 = CarFeatureAssignment(id=4, car_id=4, feature_id=4)
    
    
    
    session.add_all([car1, car2, car3, car4, brand1, brand2, brand3, brand4, customer1, customer2, customer3, customer4, sale1, sale2, sale3, sale4, dealer1, dealer2, dealer3, dealer4, inventory1, inventory2, inventory3, inventory4, employee1, employee2, employee3, employee4, test_drive1, test_drive2, test_drive3, test_drive4, promotion1, promotion2, promotion3, promotion4, maintenance1, maintenance2, maintenance3, maintenance4, car_feature1, car_feature2, car_feature3, car_feature4, car_feature_assignment1, car_feature_assignment2, car_feature_assignment3, car_feature_assignment4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
