import json
import os
import time

from flask import Flask, render_template, redirect, request, Response
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

    return render_template("index.html", file_list=utilities.get_all_uploaded_files(),
                           properties=va.get_tracking_properties())


@app.route("/select_file/<file_name>", methods=['POST'])
def select_file(file_name):
    va.set_video(file_name)
    return "true"


@app.route("/<int:frame_id>/simple.png", methods=['GET'])
def get_frame(frame_id):
    figure = va.create_figure(frame_id)
    return figure


@app.route("/delete_file/<file_id>")
def delete_file(file_id):
    utilities.delete_file(file_id)
    return render_template("index.html", file_list=utilities.get_all_uploaded_files())


@app.route('/save_properties', methods=['POST'])
def save_properties():
    data = json.loads(request.data)

    va.set_tracking_properties(data.get('mpp'), data.get('fd'))

    return va.get_tracking_properties()


@app.route('/get_csv', methods=['GET'])
def get_csv():
    return Response(
        va.export_csv(),
        mimetype="text/csv",
        headers={"Content-disposition":
                     "attachment; filename=myplot.csv"})



if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host="localhost")
