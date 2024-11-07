# Evan Stark - November 5th 2024 - ITSC-3155-001
# This module will handle the CRUD operations for a sandwich
# recipe table.

# Importing all packages.
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas

# Creating a new recipe entry.
def create(db: Session, recipes):
    db_recipe = models.Recipe(
        sandwich_id=recipes.sandwich_id,
        resource_id=recipes.resource_id,
        amount=recipes.amount
    )

    # Adding the entry to the database.
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

# Reading ALL the recipe entries.
def read_all(db: Session):
    return db.query(models.Recipe).all()

# Reading one recipe given its ID.
def read_one(db: Session, recipe_id):
    return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()

# Updating a specific recipe entry via an ID.
def update(db: Session, recipe_id, recipes):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    # Use new update data to update the row.
    update_data = resources.model_dump(exclusive_unset=True)
    db_recipe.update(update_data, sychronize_session=False)
    # Commit and return
    db.commit()
    return db_recipe

# Deleting a recipe entry from the database.
def delete(db: Session, recipe_id):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    # Delete db_recipe.
    db.delete(db_recipe)
    db.commit()
    # Return a 204 No Content Status Code.
    return Response(status_code=status.HTTP_204_NO_CONTENT)