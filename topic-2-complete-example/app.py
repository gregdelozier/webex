from flask import Flask, render_template, request, redirect, url_for
import database

database.setup_database("pets")

app = Flask(__name__)


def error_page(message, status=400):
    return message, status, {"Content-Type": "text/plain; charset=utf-8"}


@app.route("/", methods=["GET"])
@app.route("/list", methods=["GET"])
def get_list():
    pets = database.get_pets()
    return render_template("list.html", pets=pets)


@app.route("/create", methods=["GET"])
def get_create():
    return render_template("create.html")


@app.route("/create", methods=["POST"])
def post_create():
    data = dict(request.form)
    try:
        database.create_pet(data)
        return redirect(url_for("get_list"))
    except (ValueError, database.ConstraintError) as e:
        return error_page(f"Error: {e}", 400)
    except Exception as e:
        return error_page(f"Unexpected error creating pet: {e}", 500)


@app.route("/reset", methods=["GET"])
def get_reset():
    try:
        database.reset()
        return redirect(url_for("get_list"))
    except Exception as e:
        return error_page(f"Unexpected error resetting pets: {e}", 500)


@app.route("/delete/<id>", methods=["GET"])
def get_delete(id):
    try:
        database.delete_pet(id)
        return redirect(url_for("get_list"))
    except ValueError as e:
        return error_page(f"Error: {e}", 400)
    except database.NotFoundError as e:
        return error_page(f"Error: {e}", 404)
    except Exception as e:
        return error_page(f"Unexpected error deleting pet: {e}", 500)


@app.route("/update/<id>", methods=["GET"])
def get_update(id):
    try:
        data = database.get_pet(id)
        if data is None:
            return error_page("Error: pet not found.", 404)
        return render_template("update.html", data=data)
    except ValueError as e:
        return error_page(f"Error: {e}", 400)
    except Exception as e:
        return error_page(f"Unexpected error loading pet: {e}", 500)


@app.route("/update/<id>", methods=["POST"])
def post_update(id):
    data = dict(request.form)
    try:
        database.update_pet(id, data)
        return redirect(url_for("get_list"))
    except (ValueError, database.ConstraintError) as e:
        return error_page(f"Error: {e}", 400)
    except database.NotFoundError as e:
        return error_page(f"Error: {e}", 404)
    except Exception as e:
        return error_page(f"Unexpected error updating pet: {e}", 500)


@app.route("/health", methods=["GET"])
def health():
    try:
        database.get_pets()
        return error_page("ok", 200)
    except Exception as e:
        return error_page(f"Error checking health: {e}", 500)


if __name__ == "__main__":
    app.run(debug=True)
