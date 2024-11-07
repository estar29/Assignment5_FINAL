# Evan Stark - November 5th 2024 - ITSC-3155-001
# This module will handle the CRUD operations of a database displaying
# specific details of an order.

# Import all necessary modules
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas

# Creating a new order details entry.
def create(db: Session, order_details):
    db_order_details = models.OrderDetail(
        order_id=order_details.order_id,
        sandwich_id=order_details.sandwich_id,
        amount=order_details.amount,
        sandwich=order_details.sandwich,
        order=order_details.order
    )

    # Adding the new entry and returning.
    db.add(db_order_details)
    db.commit()
    db.refresh(db_order_details)
    return db_order_details

# Retrieve ALL order detail entries for reading.
def read_all(db: Session):
    return db.query(models.OrderDetail).all()

# Reading the order detail row given its ID.
def read_one(db: Session, order_details_id):
    return db.query(models.OrderDetail).filter(models.OrderDetail.id == order_details_id).first()

# Updating the information for a given order detail row.
def update(db: Session, order_details_id, order_details):
    db_order_details = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_details_id).first()

    # Pausing to update the data, then committing and returning.
    update_data = order_details.model_dump(exclusive_unset=True)
    db_order_details.update(update_data, synchronize_session=False)
    db.commit()
    return db_order_details

# Deleting an order_details entry.
def delete(db: Session, order_details_id, order_details):
    delete_order = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_details_id).first()
    # Delete, then update/return database.
    db.delete(delete_order)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)