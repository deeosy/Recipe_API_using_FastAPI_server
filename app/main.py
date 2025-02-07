from fastapi import FastAPI, APIRouter, Depends, Query, HTTPException
from typing import List, Literal, Optional, Any
from datetime import datetime

from app.schemas import RecipeSearchResults, Recipe, RecipeCreate
from app.recipe_data import RECIPES


app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

api_router = APIRouter()


@api_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, World!"}


# Updated with error handling
# https://fastapi.tiangolo.com/tutorial/handling-errors/
@api_router.get("/recipe/{recipe_id}", status_code=200, response_model=Recipe)
def fetch_recipe(*, recipe_id: int) -> Any:
    """
    Fetch a single recipe by ID
    """

    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Recipe with ID {recipe_id} not found"
        )

    return result[0]


@api_router.get("/search/", status_code=200, response_model=RecipeSearchResults)
def search_recipes(
    *,
    keyword: Optional[str] = Query(None, min_length=3, examples="chicken"),
    max_results: Optional[int] = 10,
) -> dict:
    """
    Search for recipes based on label keyword
    """
    if not keyword:
        # we use Python list slicing to limit results
        # based on the max_results query parameter
        return {"results": RECIPES[:max_results]}

    results = filter(lambda recipe: keyword.lower() in recipe["label"].lower(), RECIPES)
    return {"results": list(results)[:max_results]}


@api_router.post("/recipe/", status_code=201, response_model=Recipe)
def create_recipe(*, recipe_in: RecipeCreate) -> dict:
    """
    Create a new recipe (in memory only)
    """
    new_entry_id = len(RECIPES) + 1
    recipe_entry = Recipe(
        id=new_entry_id,
        label=recipe_in.label,
        source=recipe_in.source,
        url=recipe_in.url,
    )
    RECIPES.append(recipe_entry.dict())

    return recipe_entry


@api_router.get("/recipes/sorted_by_labels", response_model=List[str])
def get_sorted_labels() -> List[str]:
    """
    Get all recipe labels sorted alphabetically.
    """
    labels = [recipe["label"] for recipe in RECIPES]
    sorted_labels = sorted(labels)
    return sorted_labels


@api_router.get("/recipes/sorted_by_dates", status_code=200, response_model=List[str])
def get_sorted_dates() -> List[str]:
    """
    Retrieve a sorted list of recipe dates.
    """
    return sorted([recipe["date"] for recipe in RECIPES])


@api_router.post("/recipes/sorted_by_user_option", status_code=200, response_model=List[str])
def get_sorted_recipes(sort_recipes_by: Literal["date", "alphabetical"] = Query("date")) -> List[str]:
    """
    List of recipes, sorted either by date or alphabetically. 
    """
    if sort_recipes_by == "date":
        return sorted([recipe["date"] for recipe in RECIPES])
    elif sort_recipes_by == "alphabetical":
        return sorted([recipe["label"] for recipe in RECIPES])

    return []

@api_router.post("/recipes/search_based_on_authentication", status_code=200, response_model=List[dict])
def get_recipes_based_on_authentication(user_id: int = None) -> List[dict]:
    """
    Retrieve a list of accessible recipes for a given user.
    Includes all public recipes and private recipes owned by the user.
    """
    return [recipe for recipe in RECIPES if recipe["public"] or (user_id is not None and recipe["owner_id"] == user_id)]



app.include_router(api_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
