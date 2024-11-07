# Evan Stark - November 2nd 2024, ITSC-3155-001
# This module will handle all CRUD operations for the sandwich database table.

# Importing all packages.
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas

# Creating new sandwich data.
def create (db: Session, sandwiches):
    db_sandwich = models.Sandwich(
        sandwich_name=sandwiches.sandwich_name,
        price=sandwiches.price
    )
    # Add to the database.
    db.add(db_sandwich)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich

# Reading all rows of sandwich info.
def read_all(db: Session):
    return db.query(models.Sandwich).all()

# Reading the sandwich info of the specified id.
def read_one(db: Session, id):
    return db.query(models.Sandwich).filter(models.Sandwich.id == id).first()

# Updating a sandwich's information.
def update(db: Session, id, sandwiches):
    # Retrieve which sandwich should be updated.
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == id).first()
    # Extract the update data and add it to the database.
    updated_data = sandwiches.model_dump(exclusive_unset=True)
    db_sandwich.update(updated_data, synchronized_session=False)
    # Commit the changes and return.
    db.commit()
    return db_sandwich.first()

# Deleting a sandwich off of the database.
def delete(db: Session, id):
    # From the passed id, determine which sandwich should be deleted.
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == id).first()
    # Delete the data, commit changes.
    db.delete(db_sandwich)
    db.commit()
    # Send out HTTPS Code 204 to assert that no content is found at that id.
    return Response(status_code = status.HTTP_204_NO_CONTENT)


