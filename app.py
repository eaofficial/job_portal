from flask import Flask,render_template, url_for ,flash , redirect
from flask import request
import psycopg2
app = Flask(__name__)

#from requests import *
# app = Flask(__name__)  
# app.debug = True          

session = {"logged_in": False, "sek_id": None, "rec_id":None}

@app.route("/")                   
def home():                      
    return render_template("index.html")         
# if __name__ == "__main__":       
#     app.run(debug=True)
    


@app.route("/login", methods=["POST","GET"])
def login():
    
    email = request.form.get("email")
    password = request.form.get("password")
    userType = request.form.get("user")
    print("#####################################################")
    print(email)
    print(password)
    print(userType)
    if(userType=="seeker"):
        getUser = "select seeker_id from seeker where email=(%s) and password=(%s);"
        conn = psycopg2.connect(database = 'job_portal',user = 'postgres',password = "postgres", port = '5432',host = '127.0.0.1')
        cur = conn.cursor()
        cur.execute(getUser, (email, password))
        users = cur.fetchall()
        if(len(users[0] == 0)):
            return redirect(url_for('loginServe'))
        session["logged_in"] = True
        session["sek_id"] = users[0][0]
        session["rec_id"] = None

        return redirect(url_for('dashSek'))

    else:
        getUser = "select id from recruiter where email=(%s) and password=(%s);"
        conn = psycopg2.connect(database = 'job_portal',user = 'postgres',password = "postgres", port = '5432',host = '127.0.0.1')
        cur = conn.cursor()
        cur.execute(getUser, (email, password))
        users = cur.fetchall()
        if(len(users) == 0):
            return redirect(url_for('loginServe'))
        session["logged_in"] = True
        session["sek_id"] = None
        session["rec_id"] = users[0][0]

        return redirect(url_for('dashRec'))


@app.route("/logout")
def logout():
    session["logged_in"]=False
    session["rec_id"] = None
    session["sek_id"] = None

    return redirect(url_for('home'))



@app.route("/signupRec", methods=["POST", "GET"])
def signupRec():
    if(session["logged_in"] == False):
        company_name = request.form.get("company_name")
        mobile = request.form.get("phone")
        email = request.form.get("email")
        password = request.form.get("password")
        print("#####################################################")
        print(email)
        print(password)
        dataStoreQuery = "INSERT INTO recruiter (company_name, mobile, email, password) VALUES (%s,%s,%s,%s) RETURNING id;"

        conn = psycopg2.connect(database = 'job_portal',user = 'postgres',
        password = "postgres", port = '5432',host = '127.0.0.1')
        cur = conn.cursor()
        cur.execute(dataStoreQuery, (company_name, mobile, email, password))
        rec_id = cur.fetchone()[0]
        cur.close()
        conn.commit()
        conn.close()

        session["logged_in"] = True
        session["rec_id"] = rec_id
        session["sek_id"] = None
        session["type"] = "rec"
        return redirect(url_for('dashRec'))
    else: 
        return redirect(url_for('dashRec'))

@app.route("/signupSek", methods=["POST", "GET"])
def signupSek():
    if(session["logged_in"] == False):
        name = request.form.get("name")
        mobile = request.form.get("phone")
        email = request.form.get("email")
        password = request.form.get("password")
        gender = request.form.get("gridRadios")
        
        dataStoreQuery = "INSERT INTO seeker (name, mobile, email, password, gender) VALUES (%s,%s,%s,%s) RETURNING id;"

        conn = psycopg2.connect(database = 'job_portal',user = 'postgres',
        password = "postgres", port = '5432',host = '127.0.0.1')
        cur = conn.cursor()
        cur.execute(dataStoreQuery, (name, mobile, email, password, gender))
        sek_id = cur.fetchone()[0]
        cur.close()
        conn.commit()
        conn.close()

        session["logged_in"] = True
        session["rec_id"] = None
        session["sek_id"] = sek_id
        session["type"] = "rec"
        return redirect(url_for('dashSek'))

@app.route("/dashRec", methods = ["GET", "POST"])
def dashRec():
    if(session["logged_in"]==True):
        rec_id = session["rec_id"]
        fetchQuery = "SELECT * from jobs where recruiter_id = %s"
        conn = psycopg2.connect(database = 'job_portal',user = 'postgres',password = "postgres", port = '5432',host = '127.0.0.1')
        cur = conn.cursor()
        cur.execute(fetchQuery, (rec_id,))
        jobArray = cur.fetchall()
        print("#####################################")
        print(jobArray)
        cur.close()
        conn.commit()
        conn.close()

        return render_template('dashboard_r.html', jobArray = jobArray)

    else:
        return redirect(url_for('loginServe'))
        

@app.route("/dashSek", methods = ["GET"])
def dashSek():
    conn = psycopg2.connect(database = 'job_portal',user = 'postgres',password = "postgres", port = '5432',host = '127.0.0.1')
    cur = conn.cursor()
    if(session["logged_in"]==True):
        sek_id = session["sek_id"]
        fetchNotJobs = "SELECT job_id from applications where seeker_id = (%s);"
        cur.execute(fetchNotJobs, (sek_id,))
        notJobs = cur.fetchall()
        
        notJobs = [[1],[2],[3]]
        tempJobs = tuple()
        for j in notJobs:
            k = j[0]
            tempJobs + (k,)
        fetchJobs = "select job_id from jobs where job_id NOT IN %s;"
        cur.execute(fetchJobs,(tempJobs,))

        jobArray = cur.fetchall()

        return render_template('dashboard_s.html', jobArray)

@app.route("/jobpost", methods = ["POST", "GET"])
def jobpost():
    if(session["logged_in"]==True and session["rec_id"]):
        
        title= request.form.get("title")
        company = request.form.get("company")
        description = request.form.get("description")
        rec_id = session["rec_id"]
        print("#############################################")
        print(title)
        print(description)
        dataStoreQuery = "INSERT INTO jobs (title, company_name, description, recruiter_id) VALUES (%s,%s,%s,%s);"
        conn = psycopg2.connect(database = 'job_portal',user = 'postgres', password = "postgres", port = '5432',host = '127.0.0.1')
        cur = conn.cursor()
        cur.execute(dataStoreQuery, (title, company, description, rec_id))
        cur.close()
        conn.commit()
        conn.close()
        return redirect(url_for('dashRec'))
    else:
        return redirect(url_for('loginServe'))

@app.route("/job/<id>", methods = ["GET"])
def job(id):
    fetchSeekerId = "select seeker_id from applications where job_id = (%s);"
    conn = psycopg2.connect(database = 'job_portal',user = 'postgres',password = "postgres", port = '5432',host = '127.0.0.1')
    cur = conn.cursor()
    cur.execute(fetchSeekerId, (id,))

    seekerArr = cur.fetchall()
    fetchInfo = "select * from seeker where seeker_id = (%s)"
    seekers = []
    for sek in seekerArr:
        cur.execute(fetchInfo, (sek[0],))
        temp = cur.fetchall()[0]
        seekers.append(temp)
    

    cur.close()
    conn.commit()
    conn.close()

    return render_template('applications.html', seekers)


@app.route("/apply", methods = ["POST"])
def apply(job_id):
    conn = psycopg2.connect(database = 'job_portal',user = 'postgres',password = "postgres", port = '5432',host = '127.0.0.1')
    cur = conn.cursor()
    if(session["logged_in"] and session["sek_id"]):
        sek_id = session["sek_id"]
        dataStoreQuery = "INSERT INTO applications (seeker_id, job_id) VALUES (%s,%s);"
        cur.execute(dataStoreQuery, (sek_id, job_id))
        cur.close()
        conn.commit()
        conn.close()
        return redirect(url_for('dashSek'))

    else:
        return redirect(url_for('login'))

@app.route("/signupRecServe")
def signupRecServe():
    return render_template('recruiter_signup.html')

@app.route("/signupSekServe")
def signupSekServe():
    return render_template('seeker_signup.html')

@app.route("/loginServe")
def loginServe():
    return render_template('login.html')

@app.route("/jobPostServe")
def jobPostServe():
    return render_template('post_job.html')





if __name__=='__main__':
    app.run(debug=True)