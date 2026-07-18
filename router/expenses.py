from fastapi import HTTPException, Path, Query, status, APIRouter
from pydantic import BaseModel, Field

from database import expenses


class ExpenseCreate(BaseModel):
    label: str = Field(min_length=5)
    expense_date: str
    item_price: float
    currency: str
    amount: int
    unit: str
    category: str


class ExpenseUpdate(BaseModel):
    label: str | None = Field(default=None, min_length=5)
    expense_date: str | None = None
    item_price: float | None = None
    currency: str | None = None
    amount: int | None = None
    unit: str | None = None
    category: str | None = None


# app = FastAPI()
router = APIRouter(tags=["Expenses"])


@router.get("/expenses")
def expenses_list(
    # min_price: float | None = None,
    min_price: float | None = Query(default=None, gt=0),
):
    if min_price is None:
        return expenses
    results = []
    for expense in expenses:
        if expense["item_price"] > min_price:
            results.append(expense)
    return results


@router.get("/expenses/{id}")
def expenses_detail(id: int = Path(gt=0, le=99999)):
    for expense in expenses:
        if expense["id"] == id:
            return expense

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Expense with id {id} not found!"
    )


@router.post("/expenses")
def expenses_create(expense: ExpenseCreate):
    # max_id = -1
    # for expense in expenses:
    #     if expense["id"] > max_id:
    #         max_id = expense["id"]
    # max_id = max_id + 1
    max_id = max(expense["id"] for expense in expenses) + 1  # type: ignore

    # OPTION 1
    db_expense = expense.model_dump()
    db_expense["id"] = max_id
    expenses.append(db_expense)

    # OPTION 2
    # db_expense = {
    #     "id": max_id,
    #     **expense.model_dump()
    # }

    # OPTION 3 (NO pydantic)
    # item = {
    #     "id": max_id,
    #     "label": expense.label,
    #     "expense_date": expense.expense_date,
    #     "currency": expense.currency,
    #     "unit": expense.unit,
    #     "category": expense.category,
    #     "item_price": expense.item_price,
    #     "amount": expense.amount,
    # }
    # expenses.append(item)

    # return item


@router.patch("/expenses/{id}")
def expenses_update(id: int, expense: ExpenseUpdate):
    for item in expenses:
        if item["id"] == id:
            item.update(expense.model_dump(exclude_none=True))
            return expense

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Expense with id {id} not found!"
    )


@router.delete("/expenses/{id}")
def expenses_delete(id: int):
    for index, item in enumerate(expenses):
        if item["id"] == id:
            del expenses[index]
