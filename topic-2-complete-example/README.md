# Topic 2: Complete Example

This topic is a small end-to-end Flask app. It uses server-side templates for the pages, a simple data layer in `database.py`, and Mongita as a lightweight document database.

The app manages a list of pets. You can list them, create them, update them, delete them, and reset the database back to a known sample set.

## What This Topic Covers

- Flask routes for Create, Read, Update, and Delete (CRUD) operations
- Jinja templates for forms and table-based pages
- basic document-database operations in a separate data layer
- simple validation and constraint checks in Python
- redirect-based request flow after create, update, delete, and reset actions

## Files

- `app.py` contains the Flask app and route handlers.
- `database.py` contains the data access code and validation rules.
- `templates/list.html` shows the pet table.
- `templates/create.html` shows the create form.
- `templates/update.html` shows the update form.
- `requirements.txt` lists the Python packages needed for the app.
- `install.sh` installs the dependencies.
- `start.sh` starts the app.

## Install

```bash
./install.sh
```

## Run

```bash
./start.sh
```

Then open the app in a browser. The main page is:

```text
http://127.0.0.1:5000/
```

If you want to reload the sample data, visit:

```text
http://127.0.0.1:5000/reset
```

## Routes

The app uses these routes:

- `/` and `/list` show the full pet list.
- `/create` with `GET` shows the create form.
- `/create` with `POST` creates a new pet and redirects back to the list.
- `/update/<id>` with `GET` shows the update form for one pet.
- `/update/<id>` with `POST` updates that pet and redirects back to the list.
- `/delete/<id>` deletes one pet and redirects back to the list.
- `/reset` clears the collection and reloads the sample data.
- `/health` runs a simple health check.

## How The Pieces Fit Together

The flow is straightforward.

The browser sends a request to a Flask route in `app.py`. That route calls a function in `database.py` when it needs to read or change data. The route then either renders a template or redirects to another route.

For example, the list page works like this:

1. The browser requests `/list`.
2. `app.py` calls `database.get_pets()`.
3. The data layer reads from the `pets` collection and returns plain Python dictionaries.
4. Flask passes that data into `templates/list.html`.
5. The template renders the HTML table.

The create and update flows work the same way, except the data starts in an HTML form, moves through `request.form`, and then gets validated in the data layer before it is saved.

## The Templates

This app uses server-side templates instead of client-side rendering.

- `list.html` renders a Bootstrap table with one row per pet.
- `create.html` renders a form for a new pet.
- `update.html` renders a form with the current values already filled in.

The templates use Jinja syntax such as `{{ pet['name'] }}` to insert values into the HTML.

This matters because it shows the basic template pattern clearly: Python gathers the data, Flask passes it to the template, and the template turns that data into HTML.

## The Data Layer

`database.py` keeps the database logic out of the route handlers.

This example uses Mongita, which is a Python implementation of the Mongo-style document database experience. That makes it easy to teach the nature of Mongo operations without requiring a separate database server during class.

Because the database access is isolated in `database.py`, this example could be pointed at a real Mongo database later. That change would be in the client setup, so it connects to something like Mongo Atlas or a locally installed MongoDB server instead of using `MongitaClientDisk`. The other CRUD operations in the data layer are already compatible with that approach.

That file is responsible for:

- opening the database connection
- selecting the `pets` collection
- converting Mongo `ObjectId` values to strings for use in URLs and templates
- converting string IDs back into `ObjectId` values for lookups
- validating pet data before inserts and updates
- enforcing a simple uniqueness rule
- seeding the database with sample records

The main data-layer functions are:

- `setup_database()` prepares the collection on startup.
- `get_pets()` returns all pets.
- `get_pet(id)` returns one pet.
- `create_pet(data)` inserts a new pet.
- `update_pet(id, data)` updates an existing pet.
- `delete_pet(id)` removes a pet.
- `reset()` clears the collection and inserts the sample data.

## Validation And Constraints

The data layer enforces a few rules:

- `name` is required.
- `type` is required.
- `owner` is required.
- `age` is converted to an integer when possible.
- if `age` cannot be converted, it becomes `0`
- the pet ID in update and delete operations must be a valid `ObjectId`
- the pet must exist before it can be updated or deleted
- the combination of `name` and `owner` must be unique

That last rule means one owner cannot have two pets with the same name in this example.

## Sample Data

The `/reset` route calls `database.reset()` and loads this sample set:

- Dorothy, dog, age 9, owner Greg
- Heidi, dog, age 15, owner David
- Sandy, cat, age 2, owner Janet
- Suzy, dog, age 2, owner Greg
- Squeakers, hamster, age 1, owner Christopher

This makes the app easier to demo during class because you can always get back to a known state.

## What To Notice In This Example

This topic is meant to show the full request cycle in a compact app:

- routes handle web requests
- templates render HTML responses
- the data layer handles persistence and validation
- redirects keep the user on the normal CRUD flow

That is the main point of the example. It is small enough to follow without much trouble, but complete enough to show how the pieces work together.
