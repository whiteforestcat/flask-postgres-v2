from sqlalchemy import create_engine, text

import os
from dotenv import load_dotenv

load_dotenv()

db_connection_string = os.environ.get("DATABASE_URL")

engine = create_engine(db_connection_string)

###############################################################
# Rest of the code remains unchanged
###############################################################

# with engine.connect() as conn:
#     result = conn.execute(text("SELECT * FROM jobs"))
#     result_all = result.all()
#     # xxx.all() to print all the associated rows
#     # need to store result.all() into a variable cos result.all() can only be called once
#     result_dicts = (
#         []
#     )  # result.all() is an sqlalchemy data structure, need to convert into normal dict
#     for row in result_all:
#         result_dicts.append(row._mapping)
#     print(result_dicts[0])
#     print(result_dicts[1])
#     print(result_dicts)


def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs"))
        result_all = result.all()
        # xxx.all() to print all the associated rows
        # need to store result.all() into a variable cos result.all() can only be called once
        db_jobs = []
        # result.all() is an sqlalchemy data structure, need to convert into normal dict
        for row in result_all:
            db_jobs.append(dict(row._asdict()))
        # print(type(db_jobs))
        # print(db_jobs)
        return db_jobs


def load_single_job(id):
    with engine.connect() as conn:
        # use this format if you require params
        query = text("SELECT * FROM jobs WHERE id = :val")
        result = conn.execute(query.bindparams(val=id))
        rows = result.all()
        if len(rows) == 0:
            return (
                None  # returns false so that this false value can create Error 404 page
            )
        else:
            # return dict(rows[0])
            db_jobs = []
            print("number of rows in query", len(rows))
            for row in rows:
                db_jobs.append(row._mapping)
            # print(db_jobs)
            # print(db_jobs[0])
            return db_jobs[0]


def add_application_to_db(job_id, application):
    with engine.connect() as conn:
        query = text(
            "INSERT INTO applications (job_id, full_name, email, linkedin, education) VALUES (:job_id, :full_name, :email, :linked_in, :education)"
        )
        # remember that the first variables are the column names in table and second variables are the values you want to put in
        # in this case, these values here are the values of the form key-value pair (ie name-input_value pairs)
        result = conn.execute(
            query.bindparams(
                job_id=job_id,
                full_name=application.get("full_name"),
                email=application.get("email"),
                linked_in=application.get("linked_in"),
                education=application.get("education"),
            )
        )
        # up to this point, data is sent to DB, no need return json
        
