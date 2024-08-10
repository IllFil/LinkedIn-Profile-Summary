from flask import Flask, render_template, request, jsonify

from person_summary import look_up_person

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    name = request.form["name"]
    summary_obj, profile_pic_url = look_up_person(name=name)
    summary_dict = summary_obj.to_dict()

    return jsonify({
        "summary": summary_dict["summary"],
        "picture_url": profile_pic_url,
        "facts": summary_dict["facts"],
        "topics_of_interest": summary_dict["topics_of_interest"]
    })


if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)