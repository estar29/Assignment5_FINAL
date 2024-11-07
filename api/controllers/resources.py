# Evan Stark - November 4th 2024 - ITSC-3155-001
# This module will handle methods relating storing sandwich resources.

# Importing all packages.
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas

# Creating a new row/resource.
def create(db: Session, resources):
    db_resource = models.Resource(
        item=resources.item,
        amount=resources.amount
    )
    # Add the data to the database.
    db.add(db_resource)
    db.commit()
    db.refresh()
    return db_resource

# Reading ALL rows of resource information.
def read_all(db: Session):
    return db.query(models.Resource).all()

# Reading only a SPECIFIED resource given by its ID.
def read_one(db: Session, resource_id):
    return db.query(models.Resource).filter(models.Resource.id == resource_id).first()

# Updating a selected resource row.
def update(db: Session, resource_id, resources):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    # Take in the new update data and replace old row.
    update_data = resources.model_dump(exclusive_unset=True)
    db_resource.update(update_data, synchronize_session=False)
    # Commit changes and return.
    db.commit()
    return db_resource

# Deleting a resource row given its ID.
def delete(db: Session, resource_id):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    # Delete the row, update database, and return 204 code.
    db.delete(db_resource)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)