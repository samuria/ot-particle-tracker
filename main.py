import os
from flask import Flask, render_template, redirect, request, url_for
import utilities

app = Flask(__name__)

app.config["UPLOAD_DIR"] = os.path.abspath(os.curdir) + "/static/uploads"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.files:
            file_name = request.form['fileName']

            file = request.files["file"]
            file.save(os.path.join(app.config["UPLOAD_DIR"], file_name + '.' + utilities.get_file_extension(file.filename)))

            return redirect(request.url)

    return render_template("index.html", file_list=utilities.get_all_uploaded_files())

@app.route("/delete_file/<file_id>")
def delete_file(file_id):
    utilities.delete_file(file_id)
    return render_template("index.html", file_list=utilities.get_all_uploaded_files())

if __name__ == "__main__":
    app.run(debug=True, host="localhost")
