# Topic 1: Flask Intro

This is a small Flask starter app. The point is to show the basic shape of a Flask project before the later topics get more ambitious.

The app does two simple things:

- It serves a home page at `/`.
- It serves a greeting at `/hello` and `/hello/<name>`.

Both routes render the same template and pass in a message, so this topic gives you a first look at routing plus template rendering without much extra machinery in the way.

## Files

- `app.py` contains the Flask app and routes.
- `templates/index.html` is the template used by both routes.
- `requirements.txt` lists the Python dependency.
- `install.sh` installs the dependency.
- `start.sh` starts the app.

## Install

```bash
./install.sh
```

## Run

```bash
./start.sh
```

## Routes

- `/` renders the template with a simple note.
- `/hello` renders the template with `Hello, World!`
- `/hello/<name>` renders the template with `Hello, <name>!`

The `hello` view handles both route patterns:

```python
@app.route("/hello/<name>")
@app.route("/hello")
def hello(name="World"):
```

When the request is `/hello`, Flask calls the function without a `name` value from the URL, so the default argument `name="World"` is used.

When the request is `/hello/Dorothy`, Flask pulls `Dorothy` from the URL and passes it into the same function as the `name` argument.

That gives you one view function that supports both versions of the route without writing the logic twice.

## What We Covered

This topic keeps the first step small. It shows how Flask routes work, how a template gets rendered, and how data moves from Python into HTML.
