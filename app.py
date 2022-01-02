from flask import Flask,render_template,request,redirect,session
from DBConnection import Db
import random
import datetime

app = Flask(__name__)
app.secret_key="h"

path="C:\\Users\\PARVAN\\PycharmProjects\\hospitallog\\static\\photos\\"

@app.route('/')
def login():
    return render_template("home/page-login.html")

@app.route('/logout')
def logout():
    session['ln'] = ""
    return redirect("/")

@app.route('/register_link')
def register_link():
    return render_template("register_link.html")

@app.route('/loginpost',methods=['post'])
def loginpost():
    u=request.form['textfield']
    p=request.form['textfield2']
    db=Db()
    qry=db.selectOne("select * from login where username='"+u+"'and password='"+p+"'")
    if qry is not None:
        type=qry['usertype']
        id=qry['login_id']
        if type=="admin":
            session['login_id']=id
            session['ln']="pn"
            return redirect("/admin")
        elif type=="collector":
            session['login_id'] = id
            session['ln']="pn"
            return redirect("/collector")
        elif type=="hospital":
            session['login_id'] = id
            session['ln']="pn"
            return redirect("/hospital")
        elif type=="ashaworker":
            session['login_id'] = id
            session['ln']="pn"
            return redirect("/ashaworker")
        elif type=="patient":
            session['login_id'] = id
            session['ln']="pn"
            return redirect("/patient")
        else:
            return '<script>alert("invalid user");window.location="/"</script>'
    else:
        return '<script>alert("username or password incorrect");window.location="/"</script>'

###################################################################### [ADMIN] ##############################################################################################################################################

@app.route('/admin')
def adminform():
    if session['ln']=="pn":
       return render_template("admin/admin_header.html")
    else:
        return redirect("/")

@app.route('/collector')
def collectorform():
    if session['ln']=="pn":
        db = Db()
        qry = db.selectOne("select * from collector where collector_id='" + str(session['login_id']) + "'")
        session['c_name'] = qry['name']
        session['c_photo'] = qry['photo']
        c_photo = qry['photo']
        c_name = qry['name']
        return render_template("collector/collector_header.html",c_name=c_name,c_photo=c_photo)
    else:
        return redirect("/")

@app.route('/hospital')
def hospitalform():
    if session['ln']=="pn":
        db = Db()
        qry = db.selectOne("select * from hospital where hospital_id='" + str(session['login_id']) + "'")
        session['hos_name'] = qry['h_name']
        session['hos_photo'] = qry['h_photo']
        hos_photo = qry['h_photo']
        hos_name = qry['h_name']
        return render_template("hospital/hospital_header.html",hos_name=hos_name,hos_photo=hos_photo)
    else:
        return redirect("/")

@app.route('/ashaworker')
def ashaworkerform():
    if session['ln']=="pn":
        db = Db()
        qry = db.selectOne("select * from ashaworker where ashaworker_id='" + str(session['login_id']) + "'")
        session['a_name'] = qry['name']
        session['a_photo'] = qry['photo']
        a_photo = qry['photo']
        a_name = qry['name']
        return render_template("asha worker/asha_worker_header.html",a_name=a_name, a_photo=a_photo)
    else:
        return redirect("/")

@app.route('/patient')
def patientform():
    if session['ln']=="pn":
        db=Db()
        qry=db.selectOne("select * from patient where patient_id='"+str(session['login_id'])+"'")
        session['p_name']=qry['name']
        session['p_photo']=qry['photo']
        p_photo=qry['photo']
        p_name=qry['name']
        return render_template("patient/patient_header.html",p_name=p_name,p_photo=p_photo)
    else:
        return redirect("/")

########################################################### COLLECTOR MANAGEMENT #######################################
@app.route('/addcollector')
def addcoltr():
    if session['ln'] == "pn":
        return render_template("admin/add_collector.html")
    else:
        return redirect("/")

@app.route('/add_collectorpost',methods=['post'])
def addclctform():
    if session['ln'] == "pn":
        name = request.form['textfield']
        gender = request.form['RadioGroup1']
        dob = request.form['textfield2']
        place = request.form['textfield3']
        post = request.form['textfield4']
        pincode = request.form['textfield5']
        district = request.form['select']
        workingdistrict = request.form['select2']
        phoneno = request.form['textfield6']
        email= request.form['textfield7']
        photo = request.files['fileField']
        qualification = request.form.getlist('CheckboxGroup1')
        q=",".join(qualification)
        pwd=random.randint(000000,999999)
        date=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
        photo.save(path+date+".jpg")
        p="/static/photos/"+date+".jpg"
        db=Db()
        qry=db.insert("insert into login values('','"+email+"','"+str(pwd)+"','collector')")
        qry1=db.insert("insert into collector values('"+str(qry)+"','"+name+"','"+gender+"','"+dob+"','"+place+"','"+post+"','"+pincode+"','"+district+"','"+workingdistrict+"','"+phoneno+"','"+email+"','"+p+"','"+q+"')")
        return '<script>alert("Inserted Successfully");window.location="/addcollector"</script>'
    else:
        return redirect("/")

@app.route('/view_collector')
def view_collector():
    if session['ln'] == "pn":
        db=Db()
        qry=db.select("select * from collector")
        return render_template("admin/view_collector.html",data=qry)
    else:
        return redirect("/")

@app.route('/delete_collector/<dlt>')
def delete_collector(dlt):
    if session['ln'] == "pn":
        db=Db()
        qry=db.delete("delete from collector where collector_id='"+str(dlt)+"'")
        return view_collector()
    else:
        return redirect("/")

@app.route('/edit_collector/<edt>')
def edit_collector(edt):
    if session['ln'] == "pn":
        db=Db()
        qry=db.selectOne("select * from collector where collector_id='"+str(edt)+"'")
        q=qry['qualification']
        qr=q.split(",")
        return render_template("admin/edit_collector.html",data=qry,q=qr)
    else:
        return redirect("/")

@app.route('/edit_collectorpost/<i>',methods=['post'])
def edit_collectorpost(i):
    if session['ln'] == "pn":
        db=Db()
        name=request.form['textfield']
        gender=request.form['RadioGroup1']
        dob=request.form['textfield2']
        place=request.form['textfield3']
        post=request.form['textfield4']
        pincode=request.form['textfield5']
        district=request.form['select']
        workingdistrict=request.form['select2']
        phoneno= request.form['textfield6']
        email=request.form['textfield7']
        photo=request.files['fileField']
        qualification=request.form.getlist('CheckboxGroup1')
        q=",".join(qualification)
        if request.files is not None:
            if photo.filename!="":
                date=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
                photo.save(path+date+".jpg")
                p="/static/photos/"+date+".jpg"
                qry=db.update("update collector set name='"+name+"',gender='"+gender+"',date_of_birth='"+dob+"',place='"+place+"',post='"+post+"',pincode='"+pincode+"',district='"+district+"',working_district='"+workingdistrict+"',phone_no='"+phoneno+"',email_id='"+email+"',photo='"+p+"',qualification='"+q+"'where collector_id='"+str(i)+"'")
            else:
                qry=db.update("update collector set name='"+name+"',gender='"+gender+"',date_of_birth='"+dob+"',place='"+place+"',post='"+post+"',pincode='"+pincode+"',district='"+district+"',working_district='"+workingdistrict+"',phone_no='"+phoneno+"',email_id='"+email+"',qualification='"+q+"'where collector_id='"+str(i)+"'")
        else:
            qry= db.update("update collector set name='"+name+"',gender='"+gender+"',date_of_birth='"+dob+"',place='"+place+"',post='"+post+"',pincode='"+pincode+"',district='"+district+"',working_district='"+workingdistrict+"',phone_no='"+phoneno+"',email_id='"+email+"',qualification='"+q+"'where collector_id='"+str(i)+"'")
        qry1=db.update("update login set username='"+email+"'where login_id='"+str(i)+"'")
        return '<script>alert("Updated Successfully");window.location="/view_collector"</script>'
    else:
        return redirect("/")


########################################################### VIEW COMPLAINTS & SEND REPLAY ##############################

@app.route('/view_complaint')
def view_complaint():
    if session['ln'] == "pn":
        db=Db()
        qry=db.select("SELECT * FROM `complaint`,`patient` WHERE complaint.patient_id=patient.patient_id")
        return render_template("admin/view_complaint.html",data=qry)
    else:
        return redirect("/")

@app.route('/send_reply/<l>')
def send_reply(l):
    if session['ln'] == "pn":
        db=Db()
        return render_template("admin/send_reply.html",r=l)
    else:
        return redirect("/")


@app.route('/send_reply_post/<w>',methods=['post'])
def send_reply_post(w):
    if session['ln'] == "pn":
        db = Db()
        reply=request.form['textarea']
        db.update("update complaint set reply='"+reply+"', reply_date=curdate()where complaint_id='"+str(w)+"'")
        return '<script>alert("Reply Send Successfully");window.location="/view_complaint"</script>'
    else:
        return redirect("/")

########################################################### VIEW DISEASE ###############################################

@app.route('/hospital_view_disease')
def hospital_view_disease():
    if session['ln'] == "pn":
        db=Db()
        qry=db.select("SELECT * FROM `disease`,`hospital` WHERE disease.hospital_id=hospital.hospital_id")
        return render_template("admin/view_disease.html",data=qry)
    else:
        return redirect("/")

########################################################### VIEW HOSPITALS #############################################
@app.route('/view_hospital')
def view_hospital():
    if session['ln'] == "pn":
        db=Db()
        qry=db.select("select * from hospital")
        return render_template("admin/view_hospital.html",data=qry)
    else:
        return redirect("/")


########################################################### VIEW DOCTOR ################################################

@app.route('/hospital_view_doctor')
def hospital_view_doctor():
    if session['ln'] == "pn":
        db=Db()
        qry = db.select("SELECT * FROM `doctor`,`hospital` WHERE doctor.hospital_id=hospital.hospital_id")
        return render_template("admin/view_doctor.html", data=qry)
    else:
        return redirect("/")

########################################################### VIEW REVIEWS ###############################################

@app.route('/view_review')
def view_review():
    if session['ln'] == "pn":
        db=Db()
        qry = db.select("SELECT * FROM `review`,`patient`,`hospital` WHERE review.patient_id=patient.patient_id and review.hospital_id=hospital.hospital_id")
        return render_template("admin/view_review.html", data=qry)
    else:
        return redirect("/")

################################################################################ [COLLECTOR] ##############################################################################################################################################

######################################## VIEW PROFILE ##################################################################
@app.route('/view_profile')
def view_profile():
    if session['ln'] == "pn":
        db=Db()
        c_name = session['c_name']
        c_photo = session['c_photo']
        qry=db.selectOne("select * from collector where collector_id='"+str(session['login_id'])+"'")
        return render_template("collector/view_profile.html",data=qry,c_name = c_name, c_photo = c_photo)
    else:
        return redirect("/")
######################################## ASHA WORKER MANAGEMENT ########################################################

@app.route('/add_asha_worker')
def addashaworkerform():
    if session['ln'] == "pn":
        db = Db()
        c_name = session['c_name']
        c_photo = session['c_photo']
        return render_template("collector/add_asha_worker.html",c_name = c_name, c_photo = c_photo)
    else:
        return redirect("/")

@app.route('/add_ashaworkerpost',methods=['post'])
def add_ashaworkerpost():
    if session['ln'] == "pn":
        name=request.form['textfield']
        gender=request.form['RadioGroup1']
        dob=request.form['textfield2']
        place=request.form['textfield3']
        post=request.form['textfield4']
        pincode=request.form['textfield5']
        district=request.form['select']
        qualification=request.form['textfield6']
        phoneno=request.form['textfield7']
        email=request.form['textfield8']
        photo=request.files['fileField']
        pwd=random.randint(0000,9999)
        date=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
        photo.save(path+date+".jpg")
        p="/static/photos/"+date+".jpg"
        db=Db()
        qry=db.insert("insert into login values('','"+email+"','"+str(pwd)+"','ashaworker')")
        qry1=db.insert("insert into ashaworker values('"+str(qry)+"','"+name+"','"+gender+"','"+dob+"','"+place+"','"+post+"','"+pincode+"','"+district+"','"+qualification+"','"+phoneno+"','"+email+"','"+p+"')")
        return '<script>alert("Inserted Successfully");window.location="/view_profile"</script>'
    else:
        return redirect("/")


@app.route('/view_asha_worker')
def view_ashaworker():
    if session['ln'] == "pn":
        db=Db()
        c_name = session['c_name']
        c_photo = session['c_photo']
        q=db.selectOne("select * from collector where collector_id='"+str(session['login_id'])+"'")
        d=q['working_district']
        qry=db.select("select * from ashaworker where district='"+d+"'")
        return render_template("collector/view_asha_worker.html",data=qry,c_name = c_name, c_photo = c_photo)
    else:
        return redirect("/")


@app.route('/delete_ashawoker/<dlt>')
def delete_ashawoker(dlt):
    if session['ln'] == "pn":
        db=Db()
        qry=db.delete("delete from ashaworker where ashaworker_id='"+str(dlt)+"'")
        return view_ashaworker()
    else:
        return redirect("/")


@app.route('/edit_ashaworker/<edt>')
def edit_ashaworker(edt):
    if session['ln'] == "pn":
        db=Db()
        c_name = session['c_name']
        c_photo = session['c_photo']
        qry = db.selectOne("select * from ashaworker where ashaworker_id='"+str(edt)+"'")
        return render_template("collector/edit_asha_worker.html",data=qry,c_name = c_name, c_photo = c_photo)
    else:
        return redirect("/")

@app.route('/edit_ashaworkerpost/<f>',methods=['post'])
def edit_ashaworkerpostform(f):
    if session['ln'] == "pn":
        db=Db()
        name = request.form['textfield']
        gender = request.form['RadioGroup1']
        dob = request.form['textfield2']
        place = request.form['textfield3']
        post = request.form['textfield4']
        pincode = request.form['textfield5']
        district = request.form['select']
        qualification = request.form['textfield6']
        phoneno = request.form['textfield7']
        email = request.form['textfield8']
        photo = request.files['fileField']
        if request.files is not None:
            if photo.filename!="":
                date=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
                photo.save(path+date+".jpg")
                p="/static/photos/"+date+".jpg"
                qry = db.update("update ashaworker set name='"+name+"',gender='"+gender+"',date_of_birth='"+dob+"',place='"+place+"',post='"+post+"',pincode='"+pincode+"',district='"+district+"',qualification='"+qualification+"',phone_no='"+phoneno+"',email_id='"+email+"',photo='"+p+"' where ashaworker_id='"+str(f)+"'")
            else:
                qry = db.update("update ashaworker set name='"+name+"',gender='"+gender+"',date_of_birth='"+dob+"',place='"+place+"',post='"+post+"',pincode='"+pincode+"',district='"+district+"',qualification='"+qualification+"',phone_no='"+phoneno+"',email_id='"+email+"' where ashaworker_id='"+str(f)+"'")
        else:
            qry = db.update("update ashaworker set name='"+name+"',gender='"+gender+"',date_of_birth='"+dob+"',place='"+place+"',post='"+post+"',pincode='"+pincode+"',district='"+district+"',qualification='"+qualification+"',phone_no='"+phoneno+"',email_id='"+email+"' where ashaworker_id='"+str(f)+"'")
        qry1 = db.update("update login set username='"+email+"'where login_id='"+str(f)+"'")
        return'<script>alert("Updated Successfully");window.location="/view_asha_worker"</script>'
    else:
        return redirect("/")

############################################### ALLOCATE WORK TO ASHA WORKER ###########################################


@app.route('/allocate_ashaworker')
def allocate_ashaworker():
    if session['ln'] == "pn":
        db=Db()
        c_name = session['c_name']
        c_photo = session['c_photo']
        q = db.selectOne("select * from collector where collector_id='" + str(session['login_id']) + "'")
        d = q['working_district']
        qry=db.select("select * from ashaworker where district='"+d+"'")
        qry1=db.select("select * from work,ashaworker where work.ashaworker_id=ashaworker.ashaworker_id and ashaworker.district='"+d+"'")
        if len(qry1)>0:
            return render_template("collector/allocate_workto_asha_worker.html", data=qry,d=qry1,c_name = c_name, c_photo = c_photo)
        else:
            return render_template("collector/allocate_workto_asha_worker.html",data=qry,c_name = c_name, c_photo = c_photo)
    else:
        return redirect("/")

@app.route('/allocate_work_post',methods=['post'])
def allocate_work_post():
    if session['ln'] == "pn":
        db=Db()
        ashaworker = request.form['select']
        panchayat = request.form['textfield']
        District = request.form['select2']
        qry=db.insert("insert into work values('','"+str(ashaworker)+"','"+panchayat+"','"+District+"')")
        return '<script>alert("Inserted Successfully");window.location="/allocate_ashaworker"</script>'
    else:
        return redirect("/")


@app.route('/delete_woker/<dlt>')
def delete_woker(dlt):
    if session['ln'] == "pn":
        db=Db()
        qry=db.delete("delete from work where work_id='"+str(dlt)+"'")
        return allocate_ashaworker()
    else:
        return redirect("/")


################################################# VIEW LOCATIONWOSE PATIENT STATUS #####################################

@app.route('/collector_view_patients')
def collector_view_patients():
    if session['ln'] == "pn":
        db=Db()
        c_name = session['c_name']
        c_photo = session['c_photo']
        qry=db.select("SELECT * FROM `quarantine`,`patient` WHERE quarantine.patient_id=patient.patient_id")
        return render_template("collector/view_locationwise_patient_status.html",data=qry,c_name = c_name, c_photo = c_photo)
    else:
        return redirect("/")

@app.route('/search_patient_status',methods=['post'])
def search_patient_status():
    if session['ln'] == "pn":
        db=Db()
        c_name = session['c_name']
        c_photo = session['c_photo']
        s=request.form['textfield2']
        qry=db.select("SELECT * FROM `quarantine`,`patient` WHERE quarantine.patient_id=patient.patient_id and patient.district like '%"+s+"%'")
        return render_template("collector/view_locationwise_patient_status.html",data=qry,c_name = c_name, c_photo = c_photo)
    else:
        return redirect("/")

################################################ VIEW HOSPITAL REVIEW ##################################################

@app.route('/view_hospital_reviews')
def view_hospital_review():
    if session['ln'] == "pn":
        db=Db()
        c_name = session['c_name']
        c_photo = session['c_photo']
        qry = db.select("SELECT * FROM `review`,`patient`,`hospital` Where review.patient_id=patient.patient_id and review.hospital_id=hospital.hospital_id")
        return render_template("collector/view_hospital_reviews.html", data=qry,c_name = c_name, c_photo = c_photo)
    else:
        return redirect("/")



################################################################################ [HOSPITAL] ##############################################################################################################################################

############################################### REGISTRATION ###########################################################

@app.route('/add_hospital',methods=['post','get'])
def add_hospital():
    db=Db()
    return render_template("hospital/hsnewregistr.html")

@app.route('/add_hospital_post',methods=['post'])
def add_hospital_post():
    db=Db()
    name=request.form['textfield']
    place=request.form['textfield2']
    post=request.form['textfield3']
    pincode=request.form['textfield4']
    district=request.form['select']
    phoneno=request.form['textfield5']
    email=request.form['textfield6']
    photo=request.files['fileField']
    licenceno=request.form['textfield7']
    newpassword=request.form['textfield8']
    confirmpassword=request.form['textfield9']
    if newpassword==confirmpassword:
        date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
        photo.save(path + date + ".jpg")
        p = "/static/photos/" + date + ".jpg"
        qry = db.insert("insert into login values('','" + email + "','" + str(newpassword) + "','hospital')")
        qry1 = db.insert("insert into hospital values('" + str(qry) + "','" + name + "','" + place + "','" + post + "','" + pincode + "','" + district + "','" + phoneno + "','" + email + "','" + p + "','"+licenceno+"')")
        return '<script>alert("Inserted Successfully");window.location="/"</script>'
    else:
        return '<script>alert("Password mismatch");window.location="/add_hospital"</script>'


#################################################### DOCTOR MANAGEMENT #################################################

@app.route('/add_doctor')
def add_doctor():
    if session['ln'] == "pn":
        db=Db()
        hos_name = session['hos_name']
        hos_photo = session['hos_photo']
        return render_template("hospital/add_doctor.html",hos_name = hos_name,hos_photo = hos_photo)
    else:
        return redirect("/")


@app.route('/add_doctor_post',methods=['post'])
def add_doctor_post():
    if session['ln'] == "pn":
        db=Db()
        name = request.form['textfield']
        gender = request.form['RadioGroup1']
        dob = request.form['textfield2']
        specialisation = request.form['textfield3']
        experience = request.form['textfield4']
        qualification = request.form['textfield5']
        place = request.form['textfield6']
        post = request.form['textfield7']
        pincode = request.form['textfield8']
        district = request.form['select']
        email = request.form['textfield9']
        phoneno = request.form['textfield10']
        photo = request.files['fileField']
        scheduletime = request.form['textfield11']
        date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
        photo.save(path + date + ".jpg")
        p = "/static/photos/" + date + ".jpg"
        qry=db.insert("insert into doctor values('','"+name+"','"+gender+"','"+dob+"','"+specialisation+"','"+experience+"','"+qualification+"','"+place+"','"+post+"','"+pincode+"','"+district+"','"+email+"','"+phoneno+"','"+p+"','"+str(session['login_id'])+"','"+scheduletime+"')")
        return '<script>alert("Inserted Successfully");window.location="/add_doctor"</script>'
    else:
        return redirect("/")


@app.route('/view_doctor')
def view_doctor():
    if session['ln'] == "pn":
        db=Db()
        qry=db.select("select * from doctor where hospital_id='"+str(session['login_id'])+"'")
        hos_name = session['hos_name']
        hos_photo = session['hos_photo']
        return render_template("hospital/view_doctor.html",data=qry,hos_name = hos_name,hos_photo = hos_photo)
    else:
        return redirect("/")

@app.route('/delete_doctor/<dlt>')
def delete_doctor(dlt):
    if session['ln'] == "pn":
        db=Db()
        qry=db.delete("delete from doctor where doctor_id='"+str(dlt)+"'")
        return view_doctor()
    else:
        return redirect("/")

@app.route('/edit_doctor/<edt>')
def edit_doctor(edt):
    if session['ln'] == "pn":
        db=Db()
        qry=db.selectOne("select * from doctor where doctor_id='"+str(edt)+"'")
        hos_name = session['hos_name']
        hos_photo = session['hos_photo']
        return render_template("hospital/edit_doctor.html",data=qry,hos_name = hos_name,hos_photo = hos_photo)
    else:
        return redirect("/")


@app.route('/edit_doctor_post/<i>',methods=['post'])
def edit_doctor_post(i):
    if session['ln'] == "pn":
        db=Db()
        name = request.form['textfield']
        gender = request.form['RadioGroup1']
        dob = request.form['textfield2']
        specialisation = request.form['textfield3']
        experience = request.form['textfield4']
        qualification = request.form['textfield5']
        place = request.form['textfield6']
        post = request.form['textfield7']
        pincode = request.form['textfield8']
        district = request.form['select']
        email = request.form['textfield9']
        phoneno = request.form['textfield10']
        photo = request.files['fileField']
        scheduletime = request.form['textfield11']
        if request.files is not None:
            if photo.filename!="":
                date=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
                photo.save(path+date+".jpg")
                p="/static/photos/"+date+".jpg"
                qry=db.update("update doctor set d_name='"+name+"',d_gender='"+gender+"',d_date_of_birth='"+dob+"',d_specialisation='"+specialisation+"',d_experience='"+experience+"',d_qualification='"+qualification+"',d_place='"+place+"',d_post='"+post+"',d_pincode='"+pincode+"',d_district='"+district+"',d_email_id='"+email+"',d_phone_no='"+phoneno+"',d_profile_photo='"+p+"',d_schedule_time='"+scheduletime+"'where doctor_id='"+str(i)+"'")
            else:
                qry=db.update("update doctor set d_name='"+name+"',d_gender='"+gender+"',d_date_of_birth='"+dob+"',d_specialisation='"+specialisation+"',d_experience='"+experience+"',d_qualification='"+qualification+"',d_place='"+place+"',d_post='"+post+"',d_pincode='"+pincode+"',d_district='"+district+"',d_email_id='"+email+"',d_phone_no='"+phoneno+"',d_schedule_time='"+scheduletime+"'where doctor_id='"+str(i)+"'")
        else:
            qry=db.update("update doctor set d_name='"+name+ "',d_gender='"+gender+ "',d_date_of_birth='"+dob+"',d_specialisation='"+specialisation+"',d_experience='"+experience+"',d_qualification='"+qualification+"',d_place='"+place+"',d_post='"+post+"',d_pincode='"+pincode+"',d_district='"+district+"',d_email_id='"+email+"',d_phone_no='"+phoneno+"',d_schedule_time='"+scheduletime+"'where doctor_id='"+str(i)+"'")
        qry1=db.update("update login set username='"+email+"'where login_id='"+str(i)+"'")
        return '<script>alert("Updated Successfully");window.location="/view_doctor"</script>'
    else:
        return redirect("/")

#################################################### DISEASE MANAGEMENT ################################################

@app.route('/add_disease')
def add_disease():
    if session['ln'] == "pn":
        db = Db()
        hos_name = session['hos_name']
        hos_photo = session['hos_photo']
        return render_template("hospital/add_disease.html",hos_name = hos_name,hos_photo = hos_photo)
    else:
        return redirect("/")

@app.route('/add_disease_post',methods=['post'])
def add_disease_post():
    if session['ln'] == "pn":
        db=Db()
        disease = request.form['textfield']
        symptoms = request.form['textarea']
        qry=db.insert("insert into disease values('','"+disease+"','"+symptoms+"',curdate(),'"+str(session['login_id'])+"')")
        return '<script>alert("Inserted Successfully");window.location="/add_disease"</script>'
    else:
        return redirect("/")


@app.route('/view_disease')
def view_disease():
    if session['ln'] == "pn":
        db=Db()
        qry=db.select("select * from disease where hospital_id='"+str(session['login_id'])+"'")
        hos_name = session['hos_name']
        hos_photo = session['hos_photo']
        return render_template("hospital/view_disease.html",data=qry,hos_name = hos_name,hos_photo = hos_photo)
    else:
        return redirect("/")

@app.route('/delete_disease/<dlt>')
def delete_disease(dlt):
    if session['ln'] == "pn":
        db=Db()
        qry=db.delete("delete from disease where disease_id='"+str(dlt)+"'")
        return view_disease()
    else:
        return redirect("/")

@app.route('/edit_disease/<edt>')
def edit_disease(edt):
    if session['ln'] == "pn":
        db=Db()
        qry=db.selectOne("select * from disease where disease_id='"+str(edt)+"'")
        hos_name = session['hos_name']
        hos_photo = session['hos_photo']
        return render_template("hospital/edit_disease.html",data=qry,hos_name = hos_name,hos_photo = hos_photo)
    else:
        return redirect("/")

@app.route('/edit_disease_post/<i>',methods=['post'])
def edit_disease_post(i):
    if session['ln'] == "pn":
        db=Db()
        disease = request.form['textfield']
        symptoms = request.form['textfield2']
        qry = db.update("update disease set disease='"+disease+"',symptoms='"+symptoms+"'where disease_id='"+str(i)+"'")
        return '<script>alert("Inserted Successfully");window.location="/view_disease"</script>'
    else:
        return redirect("/")

#################################################### VIEW PATIENTS #####################################################

@app.route('/hospital_view_patients')
def hospital_view_patients():
    if session['ln'] == "pn":
        db=Db()
        qry=db.select("SELECT * FROM `patient`,`patiententry`,`doctor` WHERE patient.patient_id=patiententry.patient_id AND doctor.doctor_id=patiententry.doctor_id AND doctor.hospital_id='"+str(session['login_id'])+"'")
        hos_name = session['hos_name']
        hos_photo = session['hos_photo']
        return render_template("hospital/view_patients.html",data=qry,hos_name = hos_name,hos_photo = hos_photo)
    else:
        return redirect("/")

#################################################### MANAGE PATIENT ENTRY ##############################################

@app.route('/patient_entry')
def patient_entry():
    if session['ln'] == "pn":
        db=Db()
        hos_name = session['hos_name']
        hos_photo = session['hos_photo']
        qry=db.select("SELECT * FROM `patiententry`,`patient`,`doctor` WHERE `patiententry`.patient_id=`patient`.patient_id AND `patiententry`.doctor_id=`doctor`.doctor_id AND `doctor`.hospital_id='"+str(session['login_id'])+"'")
        return render_template("hospital/view_patient_entry.html",data=qry,hos_name = hos_name,hos_photo = hos_photo)
    else:
        return redirect("/")

@app.route('/approve_phr_entry/<id>')
def approve_phr_entry(id):
    if session['ln'] == "pn":
        db=Db()
        qry=db.update("update patiententry set status='approve' where patient_entry_id='"+str(id)+"'")
        return '<script>alert("Approved Successfully");window.location="/patient_entry/'+id+'"</script>'
    else:
        return redirect("/")


@app.route('/reject_phr_entry/<id>')
def reject_phr_entry(id):
    if session['ln'] == "pn":
        db=Db()
        qry=db.update("update patiententry set status='reject' where patient_entry_id='"+str(id)+"'")
        return '<script>alert("Rejected");window.location="/patient_entry/'+id+'"</script>'
    else:
        return redirect("/")

#################################################### VIEW REVIEWS ######################################################

@app.route('/h_view_review')
def h_view_review():
    if session['ln'] == "pn":
        db=Db()
        hos_name = session['hos_name']
        hos_photo = session['hos_photo']
        qry = db.select("SELECT * FROM `review`,`patient`,`hospital` Where review.patient_id=patient.patient_id and review.hospital_id=hospital.hospital_id and hospital.hospital_id='"+str(session['login_id'])+"'")
        return render_template("hospital/view_review.html",data=qry,hos_name = hos_name,hos_photo = hos_photo)
    else:
        return redirect("/")
#################################################### UPLOAD PHR ########################################################

@app.route('/upload_phr/<id>')
def upload_phr(id):
    if session['ln'] == "pn":
        db = Db()
        hos_name = session['hos_name']
        hos_photo = session['hos_photo']
        return render_template("hospital/upload_phr.html",id=id,hos_name = hos_name,hos_photo = hos_photo)
    else:
        return redirect("/")

@app.route('/upload_phr_post/<id>',methods=['post'])
def upload_phr_post(id):
    if session['ln'] == "pn":
        db=Db()
        health_status=request.form['textfield']
        report=request.files['fileField']
        date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
        report.save(path + date + ".pdf")
        f = "/static/photos/" + date + ".pdf"
        qry=db.insert("insert into phr values('','"+str(id)+"','"+health_status+"','"+str(f)+"',curdate())")
        return '<script>alert("Uploaded Successfully");window.location="/upload_phr/'+id+'"</script>'
    else:
        return redirect("/")

@app.route('/view_phr/<id>')
def view_phr(id):
    if session['ln'] == "pn":
        db=Db()
        hos_name = session['hos_name']
        hos_photo = session['hos_photo']
        qry=db.select("select * from phr where patient_entry_id='"+str(id)+"'")
        return render_template("hospital/view_phr.html",data=qry,hos_name = hos_name,hos_photo = hos_photo)
    else:
        return redirect("/")

@app.route('/delete_phr/<dlt>')
def delete_phr(dlt):
    if session['ln'] == "pn":
        db=Db()
        qry=db.delete("delete from phr where phr_id='"+str(dlt)+"'")
        return view_phr()
    else:
        return redirect("/")

@app.route('/edit_phr/<edt>')
def edit_phr(edt):
    if session['ln'] == "pn":
        db=Db()
        hos_name = session['hos_name']
        hos_photo = session['hos_photo']
        qry=db.selectOne("select * from phr where phr_id='"+str(edt)+"'")
        return render_template("hospital/edit_phr.html",data=qry,hos_name = hos_name,hos_photo = hos_photo)
    else:
        return redirect("/")


@app.route('/edit_phr_post/<i>',methods=['post'])
def edit_phr_post(i):
    if session['ln'] == "pn":
        db=Db()
        health_status = request.form['textfield2']
        report = request.files['fileField']
        if request.files is not None:
            if report.filename!="":
               date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
               report.save(path + date + ".pdf")
               f = "/static/photos/" + date + ".pdf"
               qry = db.update("update phr set health_status='"+health_status+"',report='"+str(f)+"',date=curdate() where phr_id='"+str(i)+"'")
            else:
                qry = db.update("update phr set health_status='"+health_status+"',date=curdate() where phr_id='"+str(i)+"'")
        else:
            qry = db.update("update phr set health_status='"+health_status+"',date=curdate() where phr_id='"+str(i)+"'")

        return '<script>alert("Updated Successfully");window.location="/edit_phr/'+i+'"</script>'
    else:
        return redirect("/")


################################################################################ [ ASHA WORKER ] ##############################################################################################################################################


#################################################### VIEW PROFILE ######################################################

@app.route('/view_asha_profile')
def view_asha_profile():
    if session['ln'] == "pn":
        db=Db()
        a_name = session['a_name']
        a_photo = session['a_photo']
        qry=db.selectOne("select * from ashaworker where ashaworker_id='"+str(session['login_id'])+"'")
        return render_template("asha worker/view_asha_profile.html",data=qry,a_name=a_name,a_photo=a_photo)
    else:
        return redirect("/")

#################################################### VIEW WORKS ########################################################

@app.route('/view_asha_works')
def view_asha_works():
    if session['ln'] == "pn":
        db=Db()
        a_name = session['a_name']
        a_photo = session['a_photo']
        qry=db.select("select * from `work` where ashaworker_id='"+str(session['login_id'])+"'")
        return render_template("asha worker/view_works.html",data=qry,a_name=a_name,a_photo=a_photo)
    else:
        return redirect("/")

#################################################### VIEW ALL PATIENTS #################################################

@app.route('/view_all_patients')
def view_all_patients():
    if session['ln'] == "pn":
        db=Db()
        a_name = session['a_name']
        a_photo = session['a_photo']
        qry=db.selectOne("select * from `work` where ashaworker_id='"+str(session['login_id'])+"'")
        p=qry['panchayat']
        qry1=db.select("select * from patient where panchayat like '%"+p+"%'")
        return render_template("asha worker/view_all_patients.html",data=qry1,a_name=a_name,a_photo=a_photo)
    else:
        return redirect("/")


@app.route('/update_quarantine/<id>')
def update_quarantine(id):
    if session['ln'] == "pn":
        db=Db()
        a_name = session['a_name']
        a_photo = session['a_photo']
        qry=db.select("select * from quarantine where patient_id='"+str(id)+"' order by date desc")
        if len(qry)>0:
           return render_template("asha worker/upload_quarantine_patient_details.html",id=id,d=qry,a_name=a_name,a_photo=a_photo)
        else:
           return render_template("asha worker/upload_quarantine_patient_details.html",id=id,a_name=a_name,a_photo=a_photo)
    else:
        return redirect("/")

@app.route('/add_quarantine_post/<id>',methods=['post'])
def add_quarantine_post(id):
    if session['ln'] == "pn":
        db=Db()
        quarantine_start_date = request.form['textfield']
        quarantine_end_date = request.form['textfield2']
        health_status = request.form['textfield3']
        qry=db.insert("insert into quarantine values('','"+str(quarantine_start_date)+"','"+str(quarantine_end_date)+"','"+str(id)+"','"+health_status+"',curdate())")
        return '<script>alert("Updated Successfully");window.location="/update_quarantine/'+id+'"</script>'
    else:
        return redirect("/")

@app.route('/delete_quarantine/<id>/<pid>')
def delete_quarantine(id,pid):
    if session['ln'] == "pn":
        db=Db()
        qry=db.delete("delete from quarantine where quarantine_id='"+str(id)+"'")
        return '<script>window.location="/update_quarantine/'+pid+'"</script>'
    else:
        return redirect("/")

################################################################################ [ PATIENT ] ##############################################################################################################################################

@app.route('/patient_registration',methods=['post','get'])
def patient_registration():
    db=Db()
    return render_template("patient/patientreg.html")

@app.route('/patient_registration_post',methods=['post'])
def patient_registration_post():
    db=Db()
    name = request.form['textfield']
    gender = request.form['RadioGroup1']
    dob = request.form['textfield2']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pincode = request.form['textfield5']
    district = request.form['select']
    phoneno = request.form['textfield6']
    email = request.form['textfield7']
    panchayat = request.form['textfield8']
    password = request.form['textfield9']
    confirmpassword = request.form['textfield10']
    photo = request.files['fileField']
    if password==confirmpassword:
        date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
        photo.save(path + date + ".jpg")
        p = "/static/photos/" + date + ".jpg"
        qry = db.insert("insert into login values('','"+email+"','"+str(password)+"','patient')")
        qry1 = db.insert("insert into patient values('"+str(qry)+"','"+name+"','"+gender+"','"+dob+"','"+place+"','"+post+"','"+pincode+"','"+district+"','"+phoneno+"','"+email+"','"+panchayat+"','"+p+"')")
        return '<script>alert("Registered Successfully");window.location="/"</script>'
    else:
        return '<script>alert("Password Mismatch");window.location="/patient_registration"</script>'


#################################################### SEARCH HOSPITALS ##################################################

@app.route('/patient_view_hospital')
def patient_view_hospital():
    if session['ln'] == "pn":
        db=Db()
        p_name = session['p_name']
        p_photo = session['p_photo']
        qry=db.select("select * from hospital")
        return render_template("patient/patient_view_hospital.html", data=qry,p_name=p_name,p_photo=p_photo)
    else:
        return redirect("/")


@app.route('/patient_hospital_view_doctor/<id>')
def patient_hospital_view_doctor(id):
    if session['ln'] == "pn":
        db=Db()
        p_name = session['p_name']
        p_photo = session['p_photo']
        qry = db.select("SELECT * FROM `doctor`,`hospital` WHERE doctor.hospital_id=hospital.hospital_id and hospital.hospital_id='"+str(id)+"'")
        return render_template("patient/patient_view_doctor.html", data=qry,p_name=p_name,p_photo=p_photo)
    else:
        return redirect("/")


@app.route('/take_appointment/<id>/<hid>')
def take_appointment(id,hid):
    if session['ln'] == "pn":
        db=Db()
        qry=db.insert("insert into patiententry values('','"+str(session['login_id'])+"','"+id+"',curdate(),'pending')")
        return '<script>alert("Appointment Requested Successfully");window.location="/patient_hospital_view_doctor/'+hid+'"</script>'
    else:
        return redirect("/")


@app.route('/patient_view_appointment')
def view_appointment():
    if session['ln'] == "pn":
        db=Db()
        p_name = session['p_name']
        p_photo = session['p_photo']
        qry=db.select("SELECT * FROM `patiententry`,`doctor` WHERE patiententry.doctor_id=doctor.doctor_id AND patiententry.patient_id='"+str(session['login_id'])+"'")
        return render_template("patient/view_patient_appointment.html",data=qry,p_name=p_name,p_photo=p_photo)
    else:
        return redirect("/")

@app.route('/patient_view_phr/<id>')
def patient_view_phr(id):
    if session['ln'] == "pn":
        db=Db()
        p_name = session['p_name']
        p_photo = session['p_photo']
        qry=db.select("select * from phr where patient_entry_id='"+str(id)+"'")
        return render_template("patient/patient_view_phr.html",data=qry,p_name=p_name,p_photo=p_photo)
    else:
        return redirect("/")


#################################################### VIEW COMPLAINTS & VIEW REPLY ######################################

@app.route('/patient_post_complaints')
def post_complaints():
    if session['ln'] == "pn":
        db=Db()
        p_name = session['p_name']
        p_photo = session['p_photo']
        return render_template("patient/post_complaints.html",p_name=p_name,p_photo=p_photo)
    else:
        return redirect("/")


@app.route('/post_patient_complaint',methods=['post'])
def post_patient_complaint():
    if session['ln'] == "pn":
        db=Db()
        complaint=request.form['textarea']
        qry=db.insert("insert into complaint values('',curdate(),'"+complaint+"','pending','pending','"+str(session['login_id'])+"')")
        return '<script>alert("Complaint Posted Successfully");window.location="/patient_post_complaints"</script>'
    else:
        return redirect("/")

@app.route('/view_patient_complaint')
def view_patient_complaint():
    if session['ln'] == "pn":
        db=Db()
        p_name = session['p_name']
        p_photo = session['p_photo']
        qry=db.select("SELECT * FROM `complaint`,`patient` WHERE complaint.patient_id=patient.patient_id and patient.patient_id='"+str(session['login_id'])+"' ")
        return render_template("patient/view_patient_complaint.html",data=qry,p_name=p_name,p_photo=p_photo)
    else:
        return redirect("/")


#################################################### POST HOSPITAL REVIEWS #############################################

@app.route('/post_patient_hospital_reviews/<id>')
def post_patient_hospital_review(id):
    if session['ln'] == "pn":
        db=Db()
        p_name = session['p_name']
        p_photo = session['p_photo']
        qry=db.select("select * from review,patient where review.patient_id=patient.patient_id")
        if len(qry)>0:
            return render_template("patient/post_hospital_reviews.html", id=id,d=qry,p_name=p_name,p_photo=p_photo)
        else:
            return render_template("patient/post_hospital_reviews.html",id=id,p_name=p_name,p_photo=p_photo)
    else:
        return redirect("/")

@app.route('/post_patient_hospital_review_post/<id>',methods=['post'])
def post_patient_hospital_review_post(id):
    if session['ln'] == "pn":
        db=Db()
        review=request.form['textarea']
        qry=db.insert("insert into review values('','"+str(id)+"','"+review+"',curdate(),'"+str(session['login_id'])+"')")
        return '<script>alert("Review Posted Successfully");window.location="/post_patient_hospital_reviews/'+id+'"</script>'
    else:
        return redirect("/")


@app.route('/patient_view_quarantine')
def patient_view_quarantine():
    if session['ln'] == "pn":
        db=Db()
        p_name=session['p_name']
        p_photo=session['p_photo']
        qry=db.select("SELECT * FROM `quarantine`,`patient` WHERE quarantine.patient_id=patient.patient_id and patient.patient_id='"+str(session['login_id'])+"'")
        return render_template("patient/view_quarantine.html",data=qry,p_name=p_name,p_photo=p_photo)
    else:
        return redirect("/")



if __name__ == '__main__':
    app.run(port=3000)