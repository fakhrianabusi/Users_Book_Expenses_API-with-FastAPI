# Users, Books & Expenses API with FastAPI

> Built during the **AI in Web Development** training program. Full CRUD API using an in-memory data store, Pydantic schemas for validation, and auto-generated Swagger docs.

This repository contains the code from the first session of the **AI in Web Development** training. It introduces the basic ideas of FastAPI by building a small API for expenses.

## 1. Environment Setup on Windows

This section uses **Windows Command Prompt**. It does not use PowerShell or Git Bash.

You can use Command Prompt in either of these ways:

### Option 1: Open Command Prompt in Windows

1. Press the **Windows** key or open the **Start** menu.
2. Type `Command Prompt` or `cmd`.
3. Select **Command Prompt**.

### Option 2: Use the Terminal in VS Code

1. Open the project folder in VS Code.
2. Press `Ctrl+J` to open the panel at the bottom of VS Code.
3. Select the **Terminal** tab in that panel.
4. Select the arrow next to the **+** button in the terminal area.
5. Select **Command Prompt** to create a Command Prompt terminal.

If you want every new VS Code terminal to use Command Prompt, open the same arrow menu, select **Select Default Profile**, choose **Command Prompt**, and then create a new terminal. Changing the default does not change a terminal that is already open.

> **Important:** Check the terminal name before entering the commands in this tutorial. It should say **Command Prompt**, not PowerShell or Git Bash.

`Ctrl+J` opens or hides VS Code's bottom panel. You can also create an integrated terminal by selecting **Terminal > New Terminal** from the VS Code menu.

### Install Python

Python now uses the **Python Install Manager** on Windows. The manager installs and updates Python versions for us.

1. Go to [python.org/downloads](https://www.python.org/downloads/).
2. Download the **Python Install Manager** for Windows.
3. Open the downloaded installer and select **Install**.
4. When the manager finishes, keep the option to install **CPython** selected and continue. CPython is the normal version of Python used in this tutorial.
5. A console window will open to finish the setup. When it asks for confirmation, type `Y` and press **Enter**. If it shows another confirmation question, type `Y` and press **Enter** again.
6. Wait until the CPython installation and configuration are complete. Do not close the console while it is working.

After it is installed and configured, the `python`, `py`, and `pymanager` commands should be available automatically.

If the console does not open or CPython is not installed, open **Command Prompt** and run:

```cmd
py install
```

More details are available in the official [Python documentation for Windows](https://docs.python.org/3/using/windows.html#python-install-manager).

Open **Command Prompt** and check that Python is installed:

```cmd
python --version
```

The command should display the installed Python version.

### Open the Project Folder

In Command Prompt, move to the folder that contains this project. For example:

```cmd
cd C:\path\to\tutorial
```

Replace `C:\path\to\tutorial` with the real location of the project on your computer.

### Create a Virtual Environment

A virtual environment keeps the packages for this project separate from other Python projects.

Create a virtual environment named `.venv`:

```cmd
python -m venv .venv
```

### Activate the Virtual Environment

Activate it from Command Prompt:

```cmd
.venv\Scripts\activate
```

After activation, `(.venv)` should appear at the beginning of the Command Prompt line.

Each time you open a new Command Prompt window to work on this project, move to the project folder and activate the virtual environment again.

### Install the Required Package

This tutorial only requires FastAPI with its standard dependencies:

```cmd
pip install "fastapi[standard]"
```

Keep the virtual environment active while running the application.

## 2. Initializing the FastAPI App

The FastAPI application is created in `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()
```

`FastAPI()` creates our API application. We store it in a variable named `app`.

To run the application, use:

```cmd
uvicorn main:app --reload
```

The API will usually be available at:

```text
http://127.0.0.1:8000
```

## 3. Adding Our First Endpoint: Hello World!

An endpoint is a URL that the API listens to.

Our first endpoint is:

```python
@app.get("/")
def hello_world():
    return {"Hello": "World"}
```

Open `http://127.0.0.1:8000/` in a browser. The API returns:

```json
{
  "Hello": "World"
}
```

`@app.get("/")` tells FastAPI to run this function when it receives a `GET`
request for `/`.

## 4. Inspecting the Documentation

FastAPI creates interactive API documentation automatically.

After running the application, open:

```text
http://127.0.0.1:8000/docs
```

The documentation shows all available endpoints. You can open an endpoint,
click **Try it out**, enter some data, and send a request.


## 5. Adding a Dummy In-Memory Database of Expenses

The file `database.py` contains a Python list named `expenses`:

```python
expenses = [
    {
        "id": 101,
        "label": "Bread",
        "item_price": 3,
        "currency": "NIS",
        "amount": 1,
    },
    ...
]
```

This list acts like a very simple database. It is useful for learning, but it
is not a real database. All changes are lost when the application stops or
restarts.

## 6. Very Simple CRUD

CRUD means the four basic actions we usually perform on data:

- **Create**: add new data.
- **Read**: get existing data.
- **Update**: change existing data.
- **Delete**: remove data.

This project uses the following HTTP methods:

- `GET` reads expenses.
- `POST` creates an expense.
- `PATCH` updates part of an expense.
- `DELETE` removes an expense.

The expense endpoints are defined in `router/expenses.py`. The router is added
to the FastAPI application in `main.py`.

## 7. `GET /expenses`

This endpoint returns all expenses:

```text
GET /expenses
```

It also accepts an optional `min_price` query parameter:

```text
GET /expenses?min_price=4
```

When `min_price` is provided, the endpoint returns expenses whose item price is
greater than that value.

## 8. `GET /expenses/{id}`

This endpoint returns one expense using its ID:

```text
GET /expenses/101
```

Here, `101` is a path parameter. If the expense does not exist, the API returns
a `404 Not Found` error.

## 9. `POST /expenses`

This endpoint creates a new expense:

```text
POST /expenses
```

Send the expense data as JSON:

```json
{
  "label": "Apples",
  "expense_date": "2026-07-18",
  "item_price": 4.5,
  "currency": "NIS",
  "amount": 2,
  "unit": "KG",
  "category": "food"
}
```

FastAPI uses the `ExpenseCreate` Pydantic model to check the request data. The
application creates an ID and adds the new expense to the in-memory list.

## 10. `PATCH /expenses/{id}`

This endpoint updates some fields of an existing expense:

```text
PATCH /expenses/101
```

You only need to send the fields that should change:

```json
{
  "item_price": 4,
  "amount": 2
}
```

FastAPI uses the `ExpenseUpdate` model. All fields in this model are optional,
so a `PATCH` request can update only part of the expense.

## 11. `DELETE /expenses/{id}`

This endpoint removes an expense using its ID:

```text
DELETE /expenses/101
```

The application finds the expense in the list and deletes it. Because the data is stored only in memory, the original dummy data returns when the application restarts.

## 12. Why We Use Pydantic Models

Pydantic models describe the shape of our data. FastAPI uses them for both request bodies and responses.

### Pydantic for a Request Body

The `ExpenseCreate` model describes the data needed to create an expense:

```python
class ExpenseCreate(BaseModel):
    label: str = Field(min_length=5)
    expense_date: str
    item_price: float
    currency: str
    amount: int
    unit: str
    category: str
```

We use it in the `POST /expenses` endpoint:

```python
@router.post("/expenses")
def expenses_create(expense: ExpenseCreate):
    ...
```

This gives us several benefits:

- FastAPI checks that all required fields are included.
- It checks that each value has the expected type.
- It checks extra rules, such as the minimum length of `label`.
- It returns a clear error response when the request data is invalid.
- It adds the request body structure to the automatic API documentation.
- We can use the validated data inside our function as `expense`.

The `ExpenseUpdate` model makes every field optional. This is useful for a `PATCH` request because the client only sends the fields it wants to change.

### Pydantic for a Response

Pydantic can also control which fields the API sends back to the client. The users endpoint uses this public response model:

```python
class UserPublic(BaseModel):
    id: int
    username: str
```

It is added to the endpoint with `response_model`:

```python
@router.get("/users/{id}", response_model=UserPublic)
def users_details(id: int):
    ...
```

The user stored in our dummy database also has a `password` field:

```python
{
    "id": 1,
    "username": "ahmad",
    "password": "123456"
}
```

However, the API response only contains the fields defined in `UserPublic`:

```json
{
  "id": 1,
  "username": "ahmad"
}
```

The password is hidden from the response. This is important because sensitive information should never be exposed to API users. A response model also checks the response data, keeps responses consistent, and documents the response shape in `/docs`.

In a real application, passwords must also be hashed and stored securely. A response model helps prevent them from being returned, but it does not replace secure password storage.
