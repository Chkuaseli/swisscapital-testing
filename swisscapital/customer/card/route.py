from customer import app,db,photos,search
from flask import redirect, render_template, url_for, flash, request,current_app,jsonify,session,make_response
from .forms import CardInfoForm,DepartmentForm,HumanFeatureform,UpdateInfoForm
from .models import User,HumanFeature,Department,userfeature
import secrets,os
import pdfkit


# main dashboard
@app.route('/',methods=['GET','POST'])
def home():
    total_departments = db.session.query(Department).count()
    total_features = db.session.query(HumanFeature).count()
    total_users = db.session.query(User).count()
    print(total_departments,total_features)
    data = {'task':'departments analysis'}
    for i in Department.query.all():
        department = User.query.filter_by(department=i).count()
        data[str(i)] = department
    data_feature = {'task':'feature analysis'}
    for i in HumanFeature.query.all():
        feature = User.query.join(HumanFeature.features).filter(HumanFeature.id == i.id).count()
        data_feature[str(i)] = feature
    return render_template('card/dashboard.html',data=data,data_feature=data_feature,
    total_departments=total_departments,total_features=total_features,total_users=total_users,title = 'Analysis main page')

# department dashboard
@app.route('/department',methods=['GET','POST'])
def department():
    department = Department.query.all()
    return render_template('card/department.html',department=department)

# add department
@app.route('/add_department',methods=['GET','POST'])
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit() and request.method =='POST':
        department=form.department.data
        des=form.des.data
        add_dep = Department(department = department, description = des )
        db.session.add(add_dep)
        flash(f'the department {department} has bin adedd to your database','success')
        db.session.commit()
    return render_template('card/add_department.html',form = form , title = 'add department')

# update department
@app.route('/update_department/<int:id>',methods=['GET','POST'])
def update_department(id):
    updatedep=Department.query.get_or_404(id)
    if request.method =='POST':
        department=request.form.get('department')
        des=request.form.get('desc')
        updatedep.department = department
        updatedep.description = des
        flash(f'the department {updatedep.description} has bin updated to your database','success')
        db.session.commit()
    return render_template('card/update_department.html',title = 'update department',updatedep = updatedep)

# delete department
@app.route('/delete_department/<int:id>',methods=['GET','POST'])
def delete_department(id):
    department = Department.query.get_or_404(id)
    if request.method=='POST':
        db.session.delete(department)
        db.session.commit()
        flash(f'the department {department.department} was deleted from your database','success')
        return redirect(url_for('department'))
    flash(f'the department {department.department} cant be deleted','warning')
    return redirect(url_for('department'))

# human feature dashboard  
@app.route('/humanfeature',methods=['GET'])
def humanfeature():
    features = HumanFeature.query.all()
    return render_template('card/department.html',features = features)

# add human feature
@app.route('/add_humanfeature',methods=['GET','POST'])
def add_humanfeature():
    form = HumanFeatureform()    
    if form.validate_on_submit() and request.method == 'POST':
        feature=form.feature.data
        des=form.des.data
        add_feature = HumanFeature(feature = feature, description = des )
        db.session.add(add_feature)
        flash(f'the human feature {feature} has bin adedd to your database','success')
        db.session.commit()
    return render_template('card/add_humanfeature.html',form = form, title = 'add feature')

# update human feature
@app.route('/update_feature/<int:id>',methods=['GET','POST'])
def update_feature(id):
    features = HumanFeature.query.get_or_404(id)
    if request.method =='POST':
        feature=request.form.get('feature')
        desc = request.form.get('desc')
        features.feature = feature
        features.description = desc
        flash(f'the department {features.feature} has bin updated to your database','success')
        db.session.commit()
    return render_template('card/update_department.html',title = 'update feature',features = features)

# delete human feature
@app.route('/delete_feature/<int:id>',methods=['GET','POST'])
def delete_feature(id):
    feature = HumanFeature.query.get_or_404(id)
    if request.method=='POST':
        db.session.delete(feature)
        db.session.commit()
        flash(f'the hummnan feature {feature.feature} was deleted from your database','success')
        return redirect(url_for('humanfeature'))
    flash(f'the hummna feature {feature.feature} cant be deleted','warning')
    return redirect(url_for('humanfeature'))
# card register
@app.route('/register',methods=['GET','POST'])
def CardRegister():
    form = CardInfoForm()
    department = Department.query.all()
    features = HumanFeature.query.all()
    mult_feature = request.form.getlist('feature')
    dep_form = request.form.get('department')
    if form.validate_on_submit() and request.method =='POST':
        first_name = form.first_name.data
        last_name = form.last_name.data
        cit = form.cit.data
        gender = form.gender.data
        personal_no = form.personal_no.data
        birth_of_date = form.birth_of_date.data
        date_of_exspiry = form.date_of_exspiry.data
        card_no = form.card_no.data
        signature =  photos.save(request.files.get('signature'),name = secrets.token_hex(10)+".")
        place_of_birth = form.place_of_birth.data
        date_of_issue = form.date_of_issue.data
        issuing_autority = form.issuing_autority.data
        profile = photos.save(request.files.get('profile'),name = secrets.token_hex(10)+".")
        department = dep_form
        # feature = mult_feature
        users = User(
            first_name=first_name,last_name=last_name,cit=cit,gender=gender,personal_no=personal_no,
            birth_of_date=birth_of_date,date_of_exspiry=date_of_exspiry,card_no=card_no,
            signature=signature,place_of_birth=place_of_birth,date_of_issue=date_of_issue,
        issuing_autority=issuing_autority,profile=profile,department_id=department
        )
        for i in mult_feature:
            d = HumanFeature.query.get(i)
            users.feature.append(d)
        db.session.add(users)
        db.session.commit()
        flash(f'the personal card {first_name} has bin adedd','success')
        return redirect(url_for('home'))
    return render_template('card/register_card.html',form = form,features=features,department=department)

# update card data
@app.route('/update_card/<int:id>',methods=['GET','POST'])
def update_card(id):
    form = UpdateInfoForm()
    department = Department.query.all()
    mult_feature = request.form.getlist('feature')
    dep_form = request.form.get('department')
    users=User.query.get_or_404(id)
    features = [i for i in HumanFeature.query.all() if i not in users.feature]

    if form.validate_on_submit() and request.method =='POST':
        users.first_name = form.first_name.data
        users.last_name = form.last_name.data
        users.cit = form.cit.data
        users.gender = form.gender.data
        users.personal_no = form.personal_no.data
        users.birth_of_date = form.birth_of_date.data
        users.date_of_exspiry = form.date_of_exspiry.data
        users.card_no = form.card_no.data
        users.department_id = dep_form
        # add signature image
        if request.files.get('signature'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/" + users.signature))
                users.signature = photos.save(request.form.get('signature'), name = secrets.token_hex(10)+".")
            except:
                users.signature = photos.save(request.files.get('signature'), name = secrets.token_hex(10)+".")

        users.place_of_birth = form.place_of_birth.data
        users.date_of_issue = form.date_of_issue.data
        users.issuing_autority = form.issuing_autority.data
        # add profile image
        if request.files.get('profile'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/" + users.profile))
                users.profile = photos.save(request.form.get('profile'), name = secrets.token_hex(10)+".")
            except:
                users.profile = photos.save(request.files.get('profile'), name = secrets.token_hex(10)+".")
        department = dep_form
        # feature = mult_feature
        users.feature.clear()
        for i in mult_feature:
            print(mult_feature)
            print('iiiiiiii',i)
            d = HumanFeature.query.get(i)
            users.feature.append(d)
        db.session.commit()
        db.session.close()
        flash(f'your Card has been updated','success')
        return redirect(url_for('home'))
    form.first_name.data = users.first_name
    form.last_name.data = users.last_name
    form.cit.data = users.cit
    form.gender.data = users.gender
    form.personal_no.data = users.personal_no
    form.birth_of_date.data = users.birth_of_date
    form.date_of_exspiry.data = users.date_of_exspiry
    form.card_no.data = users.card_no
    form.place_of_birth.data = users.place_of_birth
    form.date_of_issue.data = users.date_of_issue
    form.issuing_autority.data = users.issuing_autority
    return render_template(
        'card/update_card.html',form = form, department = department,
        features= features,users=users,title='Update your card data'
        )

# card main dashboard and pagenate 
@app.route('/card_dashboard',methods=['GET','POST'])
def card_dashboard():
    page = request.args.get('page',1,type = int)
    users = User.query.order_by(User.id.desc()).paginate(page=page,per_page = 5)
    return render_template('card/card_dashboard.html',users = users,title = 'card dashboard')


@app.route('/delete_card/<int:id>', methods=['POST'])
def delete_card (id):
    card = User.query.get_or_404(id)
    if request.method=="POST":
        try:
            os.unlink(os.path.join(current_app.root_path,"static/images/" + card.profile))
            os.unlink(os.path.join(current_app.root_path,"static/images/" + card.signature))
        except Exception as e:
            print(e)
        db.session.delete(card)
        db.session.commit()
        flash(f'the Card {card.first_name} PN {card.personal_no } was deleted in your record','success')
        return redirect(url_for('home'))
    return redirect(url_for('home'))

# serch results
@app.route('/result')
def result():
    searchword =request.args.get('q')
    users = User.query.msearch(searchword, fields=['first_name','last_name','card_no'])
    print(type(searchword))
    return render_template('card/search_result.html',users=users)

# convert to pdf
@app.route('/card/<int:id>',methods=['GET','POST'])
def card(id):
    users = User.query.get(id)
    rendered = render_template('card/card.html',users=users )
    pdf = pdfkit.from_string(rendered,False)
    response = make_response(pdf)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition'] = 'atteched;filename = '+users.first_name+secrets.token_hex(10)+'.pdf'
    return response
    

