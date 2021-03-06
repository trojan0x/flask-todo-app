from asyncio import tasks
from crypt import methods
from django.shortcuts import redirect
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from git import Commit
from httpx import request
from pytest import Session


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    
    def __msg__(self):
        return "<Task %r>" % self.id
        


@app.route("/", methods=['POST', 'GET'])

def index():
    if request.method =="POST":
        taskcontent = request.form['content']
        newtask = Todo(content=taskcontent)
        try:
            db.session.add(newtask)
            db.session.commit()
            return redirect("/")
        except:
            return "Error adding task"
    
    else:
        tasks = Todo.query.all()
        return render_template("index.html", tasks=tasks)
@app.route("/delete/<int:id>")
def delete(id):
    delete_task = Todo.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    
    except:
        "An error occured while trying to delete task..."
@app.route("/update/<int:id>")
def update(id):
    task =Todo.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']

        try: 
            db.Session.Commit()
            return redirect("/")
        except:
            return "An error occured while trying to update task"
    
    else:
        return render_template("update.html", task=task)




if __name__ == "__main__":

    app.run(debug=True)
