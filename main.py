import os

from flask import Flask, render_template, redirect, request
from flask_jsglue import JSGlue

import utilities
from core import VideoAnalyser

app = Flask(__name__)
jsglue = JSGlue(app)

app.config["UPLOAD_DIR"] = os.path.abspath(os.curdir) + "/static/uploads"

va = VideoAnalyser.VideoAnalyser()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.files:
            file_name = request.form['fileName']

            file = request.files["file"]
            file.save(
                os.path.join(app.config["UPLOAD_DIR"], file_name + '.' + utilities.get_file_extension(file.filename)))

            return redirect(request.url)

    return render_template("index.html", file_list=utilities.get_all_uploaded_files())


@app.route("/<int:frame_id>/simple.png", methods=['GET'])
def get_frame(frame_id):
    frame = va.create_figure(frame_id)
    # response.headers['Content-Type'] = 'image/png'
    return frame


@app.route("/delete_file/<file_id>")
def delete_file(file_id):
    utilities.delete_file(file_id)
    return render_template("index.html", file_list=utilities.get_all_uploaded_files())


if __name__ == "__main__":
    app.run(debug=True, host="localhost")
