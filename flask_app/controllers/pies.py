from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.pie import Pie
from flask_app.models.user import User


@app.route('/create/pie',methods=['POST'])
def create_pie():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Pie.validate_pie(request.form):
        return redirect('/dashboard')
    data = {
        "name": request.form["name"],
        "filling": request.form["filling"],
        "crust": request.form["crust"],
        "user_id": session["user_id"]
    }
    Pie.create_pie(data)
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def edit_pie(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }

    edit=Pie.get_one(data)
    
    return render_template("edit.html",edit=edit)

@app.route('/delete/pie/<int:id>')
def delete_pie(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id,
        "pie_id": id
    }
    Pie.destroy_pie(data)
    return redirect('/dashboard')

@app.route('/update/pie/<int:id>',methods=['POST'])
def update_pie(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Pie.validate_pie(request.form):
        return redirect(f'/edit/{id}')
    
    data = {
        "name": request.form["name"],
        "filling": request.form["filling"],
        "crust": request.form["crust"],
        "id": id
    }
    
    Pie.update_pie(data)
    return redirect('/dashboard')

@app.route('/pies')
def show_pies():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    user = User.get_by_id(data)
    pies = Pie.show_all_pies()
    return render_template('pies.html',pies=pies,user=user)

@app.route('/show/<int:id>')
def show_pie(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    
    pie=Pie.get_one(data)
    vote_pie=Pie.get_all_voted_pies(user_data)
    user = Pie.get_pie_and_user(data)[0]

    return render_template("show.html",pie=pie,vote_pie=vote_pie,user=user)

@app.route('/vote/<int:id>')
def like(id):
    data = {
        "user_id": session['user_id'],
        "pie_id": id
        }
    Pie.vote(data)
    return redirect('/pies') 

@app.route('/remove_vote/<int:id>')
def unlike(id):
    data = {
        "user_id": session['user_id'],
        "pie_id": id
        }
    Pie.remove_vote(data)
    return redirect('/pies')






