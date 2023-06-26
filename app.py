from flask import (
    Flask,  # flask is library name, Flask is class in flask library
    render_template,
    jsonify,  # to return json in endpoints
    request,  # enables us to use params in url after "?"
)
from database import (
    load_jobs_from_db,  # importing engine from database.py file
    load_single_job,
    add_application_to_db,
)

app = Flask(__name__)
# print(__name__)

# # dummy data
# dummy_jobs = [
#     {"id": 1, "title": "Data Analyst", "location": "Singapore", "salary": 4000},
#     {"id": 2, "title": "Backend Engineer", "location": "Singapore", "salary": 4000},
#     {"id": 3, "title": "Frontend Engineer", "location": "Singapore", "salary": 4000},
#     {"id": 3, "title": "Full Stack Engineer", "location": "Singapore"},
# ]


# # remember that @ is decorator
# @app.route("/")
# def hello_world():
#     return render_template(
#         "home.html",
#         jobs=dummy_jobs,
#         name="Amir"
#         # dummy_jobs is now accessible in home.html
#     )  # flask looks for html file in specifically a templates folder


# remember that @ is decorator
@app.get("/")
def hello_world():
    db_jobs = load_jobs_from_db()  # storing return result of function into variable
    return render_template(
        "home.html",
        jobs=db_jobs,
        name="Amir"
        # dummy_jobs is now accessible in home.html
    )  # flask looks for html file in specifically a templates folder


# by default, ("/static/xxx.png") route will show you the image


@app.get("/api/jobs")
def list_jobs():
    jobs = load_jobs_from_db()
    print(type(jobs))
    return jsonify(jobs)
    # return render_template("rawdata.html", jobs=jobs)
    
@app.post("/api/apply")
def apply_job():
    data = request.get_json()
    job_id = data.get("job_id")
    application = data.get("application")
    add_application_to_db(job_id, application)
    return "application submitted"



@app.get("/job/<id>")
def show_job(id):
    job = load_single_job(id)
    if not job:  # in controller, here will be None data type. meaning if (!job) is JS
        return "Job Not found", 404
    return render_template("jobpage.html", job=job)


@app.post("/job/<id>/apply")
def apply_to_job(id):
    # data = request.args # information stored in url can be accesssed via request.args, need to leave out methods if want to store info in url
    data = request.form  # to access data when using methods
    job = load_single_job(id)
    # return jsonify(data)
    # this returns form in json format
    # where keys are the name attribute of input HTML element and values are the user input values of the input box
    # can store this data in DB, see below
    add_application_to_db(id, data)
    # return render_template("application_submit.html", application=data, job=job)
    return "application submitted"

# render_template is the html page that is called when endpoint is called

if __name__ == "__main__":
    app.run(debug=True)

# following up, use mailjet to send admin email when job application is submitted
# for captcha, use hcaptcha