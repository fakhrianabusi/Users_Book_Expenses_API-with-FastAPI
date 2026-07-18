# python -m venv .venv   /to install venv
# .venv\Scripts\activate  /to activate venv
# uvicorn main:app --reload /to run server
# extension: Mypy Type Checker + ruff

# CRUD
# Create - POST
# Read - GET
# Update - PUT
# Delete - DELETE
# query parameters & path parameters


from fastapi import FastAPI
from router.expenses import router as expenses_router
from router.users import router as users_router
from router.books import router as books_router

app = FastAPI()


app.include_router(expenses_router)
app.include_router(users_router)
app.include_router(books_router)


@app.get("/")
def root():
    return {"status": "running", "message": "Welcome to the Books API"}
