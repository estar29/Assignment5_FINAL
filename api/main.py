# Evan Stark - November 2nd 2024 - ITSC-3155-001
# This is the main module of the project.
# It holds all the API paths and endpoints to modify all the sandwich databases.

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from .models import models, schemas
from .controllers import orders, recipes, resources, sandwiches, order_details
from .dependencies.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/orders/", response_model=schemas.Order, tags=["Orders"])
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return orders.create(db=db, order=order)


@app.get("/orders/", response_model=list[schemas.Order], tags=["Orders"])
def read_orders(db: Session = Depends(get_db)):
    return orders.read_all(db)


@app.get("/orders/{order_id}", response_model=schemas.Order, tags=["Orders"])
def read_one_order(order_id: int, db: Session = Depends(get_db)):
    order = orders.read_one(db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="User not found")
    return order


@app.put("/orders/{order_id}", response_model=schemas.Order, tags=["Orders"])
def update_one_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    order_db = orders.read_one(db, order_id=order_id)
    if order_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    return orders.update(db=db, order=order, order_id=order_id)


@app.delete("/orders/{order_id}", tags=["Orders"])
def delete_one_order(order_id: int, db: Session = Depends(get_db)):
    order = orders.read_one(db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="User not found")
    return orders.delete(db=db, order_id=order_id)


# Posting new sandwich data.
@app.post("/sandwiches/", response_model=schemas.Sandwich, tags=["Sandwiches"])
def create_sandwich(sandwich: schemas.Sandwich, db: Session = Depends(get_db)):
    return sandwiches.create(db=db, sandwich=sandwich)


# Reading ALL rows in sandwich data.
@app.get("/sandwiches/", response_model=list[schemas.Sandwich], tags=["Sandwiches"])
def read_all_sandwiches(db: Session = Depends(get_db)):
    return sandwiches.read_all(db)


# Reading ONLY one row of sandwich data.
@app.get("/sandwiches/{sandwich_id}", response_model=schemas.Sandwich, tags=["Sandwiches"])
def read_one_sandwich(db: Session = Depends(get_db)):
    sandwich = sandwiches.read_one(db, sandwich_id=id)

    # Checking to see if the sandwich exists in the db.
    if sandwich is None:
        return HTTPException(status_code=404, detail="Sandwich not found!")
    else:
        return sandwich


# Updating the info of one sandwich.
@app.put("/sandwiches/{sandwich_id}", response_model=schemas.Sandwich, tags=["Sandwiches"])
def update_one_sandwich(sandwich_id : id, sandwich: schemas.SandwichUpdate, db: Session = Depends(get_db)):
    sandwich_db = sandwiches.read_one(db, sandwich_id=sandwich_id)
    # Check if the id of a sandwich exists.
    if sandwich_db is None:
        raise HTTPException(status_code=404, detail="Sandwich not found!")
    else:
        return sandwiches.update(db=db, sandwich=sandwich, sandwich_id=sandwich_id)


# Deleting a specific sandwich.
@app.delete("/sandwiches/{sandwich_id}", response_model=schemas.Sandwich, tags=["Sandwiches"])
def delete_one_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    sandwich = sandwiches.read_one(db, sandwich_id=sandwich_id)
    if sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found!")
    else:
        return sandwiches.delete(db=db, sandwich=sandwich, sandwich_id=sandwich_id)


# Creating a new resource entry.
@app.post("/resources/", response_model=schemas.Resource, tags=["Resources"])
def create_resource(resource: schemas.Resource, db: Session = Depends(get_db)):
    return resources.create(db=db, resource=resource)

# Reading ALL rows of resource information.
@app.get("/resources/", response_model=schemas.Resource, tags=["Resources"])
def read_all_resources(db: Session = Depends(get_db)):
    return resources.read_all(db)

# Reading just a single resource row.
@app.get("/resources/{resource_id}", response_model=schemas.Resource, tags=["Resources"])
def read_one_resource(resource_id: int, db: Session = Depends(get_db)):
        resource = resources.read_one(db, resource_id=resource_id)
        # Checking to see if the resource exists.
        if resource is None:
            raise HTTPException(status_code=404, detail="Resource row not found!")
        else:
            return resource

# Updating a given resource.
@app.put("/resources/{resource_id}", response_model=schemas.Resource, tags=["Resources"])
def update_one_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = resources.read_one(db, resource_id=resource_id)
    # Check for that resources row's existence.
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource row not found!")
    # If resource does exist, run the update function.
    else:
        return resources.update(db=db, resource=resource, resource_id=resource_id)

# Deleting a given resource.
@app.delete("/resources/{resource_id}", response_model=schemas.Resource, tags=["Resources"])
def delete_one_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = resources.read_one(db, resource_id=resource_id)
    # Check to see if the row exists.
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource row not found!")
    else:
        return resources.delete(db=db, resource=resource, resource_id=resource_id)


# Creating a new recipe.
@app.post ("/resource/", response_model=schemas.Resource, tags=["Recipes"])
def create_recipe(recipe: schemas.Recipe, db: Session = Depends(get_db)):
    return recipes.create(db=db, recipe=recipe)

# Returning all recipes.
@app.get("/resource/", response_model=schemas.Recipe, tags=["Recipes"])
def read_all_recipes(db: Session = Depends(get_db)):
    return recipes.read_all(db)


# Returning only one recipe from the database.
@app.get("/recipe/{recipe_id}", response_model=schemas.Recipe, tags=["Recipes"])
def read_one_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = recipes.read_one(db, recipe_id=recipe_id)
    # Checking to see if the recipe exists and throwing 404 if not found.
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found!")
    else:
        return recipe

# Updating a recipe.
@app.put("/recipe/{recipe_id}", response_model=schemas.Recipe, tags=["Recipes"])
def update_one_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = recipes.read_one(db, recipe_id=recipe_id)
    # Checking to see if that entry exists.
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found!")
    else:
        return recipes.update(db=db, recipe=recipe, recipe_id=recipe_id)


# Deleting a recipe entry from the table.
@app.delete("/recipe/{recipe_id}", response_model=schemas.Recipe, tags=["Recipes"])
def delete_one_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = recipes.read_one(db, recipe_id=recipe_id)
    # Check to see if the recipe entry exists.
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found!")
    else:
        return recipes.delete(db=db, recipe=recipe, recipe_id=recipe_id)


# Creating a new order details entry.
@app.post("/order_detail/", response_model=schemas.OrderDetail, tags=["OrderDetails"])
def create_order_detail(order_detail: schemas.OrderDetail, db: Session = Depends(get_db)):
    return order_details.create(db=db, order_detail=order_detail)


# Returning ALL order detail rows.
@app.get("/order_detail/", response_model=schemas.OrderDetail, tags=["OrderDetails"])
def read_all_order_details(db: Session = Depends(get_db)):
    return order_details.read_all(db)


# Returning ONE order detail given an id.
@app.get("/order_detail/{order_detail_id}", response_model=schemas.OrderDetail, tags=["OrderDetails"])
def read_one_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    order_detail = order_details.read_one(db, order_detail_id=order_detail_id)

    # Check for the entry's existence, then either throw a 404 or return.
    if order_detail is None:
        raise HTTPException(status_code=404, detail="Order details not found!")
    else:
        return order_detail


# Updating a specified order detail.
@app.put("/order_detail/{order_detail_id}", response_model=schemas.OrderDetail, tags=["OrderDetails"])
def update_one_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    order_detail = order_details.read_one(db, order_detail_id=order_detail_id)

    # Check for existence, then throw exception or return update method.
    if order_detail is None:
        raise HTTPException(status_code=404, detail="Order details not found!")
    else:
        return order_details.update(db=db, order_detail=order_detail, order_detail_id=order_detail_id)


# Deleting an order details row.
@app.delete("/order_detail/{order_detail_id}", response_model=schemas.OrderDetail, tags=["OrderDetails"])
def delete_one_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    order_detail = order_details.read_one(db, order_detail_id=order_detail_id)

    # Check, then throw exception or return.
    if order_detail is None:
        raise HTTPException(status_code=404, detail="Order details not found!")
    else:
        return order_details.delete(db=db, order_detail=order_detail, order_detail_id=order_detail_id)