from flask import render_template, redirect, url_for, flash, session, request
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from app import app, db
from app.models import User, Team, Practice
from app import app
from app.forms import LoginForm, TeamForm,PracticeForm
from app.functions import *

#####   LOGIN Stuff needed
#####   User Management   #####  FOUND : https://www.youtube.com/watch?v=2dEM-s3mRLE
login_manager = LoginManager()
login_manager.init_app(app)


####   This method is used to as part of the flask_login_code
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
#    session.pop('user_name', default=None)
    print('First...', session.get('user_name'))

    return render_template('index.html')


####   LOGIN LOGOUT Stuff  #######

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get("name"):
#if current_user.is_authenticated:
        return redirect(url_for('index'))
        print('Anonymous User...', str(current_user)+str(current_user.is_authenticated)+str(current_user.is_anonymous))
    form = LoginForm()

    # Get form data
    form_username = form.username.data
    form_password = form.password.data

    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form_username).first()
        if user is not None :
           password = user.password
        else :
            password ='Invalid'

        if user is None or password != form_password:
            flash('Invalid UserName or Password', 'Error')
            return redirect(url_for('login'))
        print('After Validation...', str(current_user) + str(current_user.is_authenticated) + str(current_user.is_anonymous))
        login_user(user)
        session["user_name"] = form_username
        session.permanent = True
        flash_str='Log In Successfull : UserName - '+form_username
        flash(flash_str,'Success')
        print('Session Param : ',session.get("user_name"))
        return redirect(url_for('index'))
    return render_template('login.html', tittle='Sign In', form=form)

########  Teams - Add, EDIT, DELETE

########  Add Team - READ
@app.route('/teams', methods=['GET', 'POST'])
@login_required
def teams():
     form=TeamForm()
     if request.method == 'POST' :
         team_name = request.form.get('team_name')
         team_mascot = request.form.get('team_mascot')
         teams= Team(team_name=team_name, team_mascot=team_mascot)
         db.session.add(teams)
         db.session.commit()
         return redirect(url_for('teams'))
     teams = get_teams()
     return render_template('teams.html', form=form, teams=teams)

########  Update Team - READ, WRITE
@app.route('/team_update/<team_id>', methods=['GET', 'POST'])
def team_update(team_id):
    team = Team.query.get(team_id)
    team.team_name = request.form.get('team_name')
    team.team_mascot = request.form.get('team_mascot')
    db.session.commit()
    flash(f"{team.team_name} has been updated.", 'Success')
    return redirect(url_for('teams'))

########  Delete Team - READ, WRITE
@app.route('/team_delete/<team_id>', methods=['GET', 'POST'])
def team_delete(team_id):
    db.session.query(Team).filter(Team.team_id==team_id).delete(synchronize_session='fetch')
    db.session.commit()
    flash(f"The Team with Team ID - {team_id} has been deleted.", 'Success')
    return redirect(url_for('teams'))


########  Add Practices - READ
@app.route('/practices', methods=['GET', 'POST'])
@login_required
def practices():
     form=PracticeForm()

     teams = get_teams()
     form.teams.choices = [(team['team_id'], team['team_name']) for team in teams]

     if request.method == 'POST' :
         practice_length = request.form.get('practice_length')
         practice_date = request.form.get('practice_date')
         team_id = request.form.get('teams')

         practices= Practice(practice_length=practice_length, practice_date=practice_date, team_id=team_id)
         db.session.add(practices)
         db.session.commit()
         return redirect(url_for('practices'))
     practices = get_practices()
     return render_template('practices.html', form=form, teams=teams, practices=practices)

########  Update Practices - READ, WRITE
@app.route('/practice_update/<practice_id>', methods=['GET', 'POST'])
def practice_update(practice_id):
    practice = Practice.query.get(practice_id)
    practice.practice_length = request.form.get('practice_length')
    practice.practice_date = request.form.get('practice_date')
    practice.team_id = request.form.get('teams')
    db.session.commit()
    team = get_team_name(request.form.get('teams'))
    flash_str = 'The Practices has been updated. Team : '+team[0]['team_name']+' Practice Date : '+practice.practice_date.strftime("%Y-%m-%d")+'  Practice Length : '+str(practice.practice_length)
    flash(flash_str, 'Success')
    return redirect(url_for('practices'))

########  Delete Practices - READ, WRITE
@app.route('/practice_delete/<practice_id>', methods=['GET', 'POST'])
def practice_delete(practice_id):
    practice = get_practice(practice_id)
    db.session.query(Practice).filter(Practice.practice_id==practice_id).delete()
    db.session.commit()
    flash(f"The Practice - Team name: { practice[0]['team_name'] } with Practice Length : { practice[0]['practice_length']} Min. on date(yy-mm-dd) : {practice[0]['practice_date']}: has been deleted.", 'Success')
    return redirect(url_for('practices'))



@app.route('/logout')
@login_required
def logout():
    session.pop('user_name', default=None)
#    load_user('')
    logout_user()
    return redirect(url_for('index'))
