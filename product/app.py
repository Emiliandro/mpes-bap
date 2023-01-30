from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# File name
app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demo_messages.db'
db = SQLAlchemy(app)


class Demo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

#  regarding cyber security non repudiation, this assures that the sender of
#  information is provided with proof of delivery and the recipient is provided
#  with proof of the sender's request made, so neither can later deny having
#  processed the information throw the field "Suas ultimas buscas".
@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Demo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Demo.query.order_by(Demo.date_created).all()

    title = "Bem vindo ao Bap 🤖"
    return render_template('demonstration.html',title=title, tasks=tasks)

# to access the feed and receive a table of values
# @app.route('/feed/<str:categorie>')
# def filter_categorie():

#    return redirect('/')

# to delete a research made previously 
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Demo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

if (__name__ == "__main__"):
    app.run(debug=True)
