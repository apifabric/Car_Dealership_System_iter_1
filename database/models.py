# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  December 31, 2024 09:42:59
# Database: sqlite:////tmp/tmp.QLha0kE7ay/Car_Dealership_System_iter_1/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *

Base = SAFRSBaseX



class Brand(Base):  # type: ignore
    """
    description: Represents a car brand with a unique identifier.
    """
    __tablename__ = 'brand'
    _s_collection_name = 'Brand'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    CarList : Mapped[List["Car"]] = relationship(back_populates="brand")



class CarFeature(Base):  # type: ignore
    """
    description: Defines the features that can be associated with different cars.
    """
    __tablename__ = 'car_feature'
    _s_collection_name = 'CarFeature'  # type: ignore

    id = Column(Integer, primary_key=True)
    feature_name = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    CarFeatureAssignmentList : Mapped[List["CarFeatureAssignment"]] = relationship(back_populates="feature")



class Customer(Base):  # type: ignore
    """
    description: Represents a customer with contact details. Tracks the number of test drives requested by the customer.
    """
    __tablename__ = 'customer'
    _s_collection_name = 'Customer'  # type: ignore

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    test_drive_count = Column(Integer)

    # parent relationships (access parent)

    # child relationships (access children)
    SaleList : Mapped[List["Sale"]] = relationship(back_populates="customer")
    TestDriveList : Mapped[List["TestDrive"]] = relationship(back_populates="customer")



class Dealer(Base):  # type: ignore
    """
    description: Represents a dealership location along with its name. Tracks the total inventory count for the dealer.
    """
    __tablename__ = 'dealer'
    _s_collection_name = 'Dealer'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    inventory_count = Column(Integer)

    # parent relationships (access parent)

    # child relationships (access children)
    EmployeeList : Mapped[List["Employee"]] = relationship(back_populates="dealer")
    InventoryList : Mapped[List["Inventory"]] = relationship(back_populates="dealer")



class Car(Base):  # type: ignore
    """
    description: Represents a car in the dealership, including the brand it belongs to and its price. Tracks the number of test drives requested for this car.
    """
    __tablename__ = 'car'
    _s_collection_name = 'Car'  # type: ignore

    id = Column(Integer, primary_key=True)
    model = Column(String)
    brand_id = Column(ForeignKey('brand.id'))
    price = Column(Integer)
    year_of_manufacture = Column(Integer)
    test_drive_count = Column(Integer)

    # parent relationships (access parent)
    brand : Mapped["Brand"] = relationship(back_populates=("CarList"))

    # child relationships (access children)
    CarFeatureAssignmentList : Mapped[List["CarFeatureAssignment"]] = relationship(back_populates="car")
    InventoryList : Mapped[List["Inventory"]] = relationship(back_populates="car")
    MaintenanceList : Mapped[List["Maintenance"]] = relationship(back_populates="car")
    PromotionList : Mapped[List["Promotion"]] = relationship(back_populates="car")
    SaleList : Mapped[List["Sale"]] = relationship(back_populates="car")
    TestDriveList : Mapped[List["TestDrive"]] = relationship(back_populates="car")



class Employee(Base):  # type: ignore
    """
    description: Contains the details of employees working at various dealerships. Tracks the number of services conducted by an employee.
    """
    __tablename__ = 'employee'
    _s_collection_name = 'Employee'  # type: ignore

    id = Column(Integer, primary_key=True)
    dealer_id = Column(ForeignKey('dealer.id'))
    first_name = Column(String)
    last_name = Column(String)
    position = Column(String)
    service_count = Column(Integer)

    # parent relationships (access parent)
    dealer : Mapped["Dealer"] = relationship(back_populates=("EmployeeList"))

    # child relationships (access children)
    MaintenanceList : Mapped[List["Maintenance"]] = relationship(back_populates="employee")



class CarFeatureAssignment(Base):  # type: ignore
    """
    description: Link table between cars and features to assign features to specific cars.
    """
    __tablename__ = 'car_feature_assignment'
    _s_collection_name = 'CarFeatureAssignment'  # type: ignore

    id = Column(Integer, primary_key=True)
    car_id = Column(ForeignKey('car.id'))
    feature_id = Column(ForeignKey('car_feature.id'))

    # parent relationships (access parent)
    car : Mapped["Car"] = relationship(back_populates=("CarFeatureAssignmentList"))
    feature : Mapped["CarFeature"] = relationship(back_populates=("CarFeatureAssignmentList"))

    # child relationships (access children)



class Inventory(Base):  # type: ignore
    """
    description: Tracks the number of a specific car model available at each dealer.
    """
    __tablename__ = 'inventory'
    _s_collection_name = 'Inventory'  # type: ignore

    id = Column(Integer, primary_key=True)
    dealer_id = Column(ForeignKey('dealer.id'))
    car_id = Column(ForeignKey('car.id'))
    quantity = Column(Integer)

    # parent relationships (access parent)
    car : Mapped["Car"] = relationship(back_populates=("InventoryList"))
    dealer : Mapped["Dealer"] = relationship(back_populates=("InventoryList"))

    # child relationships (access children)



class Maintenance(Base):  # type: ignore
    """
    description: Stores information about maintenance and service history of cars. Associates maintenance tasks with employees.
    """
    __tablename__ = 'maintenance'
    _s_collection_name = 'Maintenance'  # type: ignore

    id = Column(Integer, primary_key=True)
    car_id = Column(ForeignKey('car.id'))
    employee_id = Column(ForeignKey('employee.id'))
    last_serviced_date = Column(DateTime)
    service_details = Column(String)

    # parent relationships (access parent)
    car : Mapped["Car"] = relationship(back_populates=("MaintenanceList"))
    employee : Mapped["Employee"] = relationship(back_populates=("MaintenanceList"))

    # child relationships (access children)



class Promotion(Base):  # type: ignore
    """
    description: Lists active promotions on specific cars, including discounts. Tracks how many sales have utilized the promotion.
    """
    __tablename__ = 'promotion'
    _s_collection_name = 'Promotion'  # type: ignore

    id = Column(Integer, primary_key=True)
    car_id = Column(ForeignKey('car.id'))
    description = Column(String)
    discount_percentage = Column(Integer)
    applied_count = Column(Integer)

    # parent relationships (access parent)
    car : Mapped["Car"] = relationship(back_populates=("PromotionList"))

    # child relationships (access children)



class Sale(Base):  # type: ignore
    """
    description: Details the sale transactions involving cars and customers.
    """
    __tablename__ = 'sale'
    _s_collection_name = 'Sale'  # type: ignore

    id = Column(Integer, primary_key=True)
    car_id = Column(ForeignKey('car.id'))
    customer_id = Column(ForeignKey('customer.id'))
    sale_date = Column(DateTime)
    sale_price = Column(Integer)

    # parent relationships (access parent)
    car : Mapped["Car"] = relationship(back_populates=("SaleList"))
    customer : Mapped["Customer"] = relationship(back_populates=("SaleList"))

    # child relationships (access children)



class TestDrive(Base):  # type: ignore
    """
    description: Records customer requests and actual test drive events with dates.
    """
    __tablename__ = 'test_drive'
    _s_collection_name = 'TestDrive'  # type: ignore

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customer.id'))
    car_id = Column(ForeignKey('car.id'))
    date = Column(DateTime)

    # parent relationships (access parent)
    car : Mapped["Car"] = relationship(back_populates=("TestDriveList"))
    customer : Mapped["Customer"] = relationship(back_populates=("TestDriveList"))

    # child relationships (access children)
