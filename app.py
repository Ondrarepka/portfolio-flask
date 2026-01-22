from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
Scss(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
db = SQLAlchemy(app)

class MyCampaigns(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    system = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean, default=True)
    started_on = db.Column(db.Date, nullable=False)
    my_character = db.Column(db.String(100), nullable=True)
    added_on = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self) -> str:
        return f"<Campaign {self.name} - {self.system}>"

# routes 
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/campaigns", methods=["GET", "POST"])
def campaigns():
    # Add campaign

    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        system = request.form['system']
        active = 'active' in request.form
        started_on = datetime.strptime(request.form['started_on'], '%Y-%m-%d').date()
        my_character = request.form['my_character']

        new_campaign = MyCampaigns(
            name = name,
            description = description,
            system = system,
            active = active,
            started_on = started_on,
            my_character = my_character
        )
        db.session.add(new_campaign)
        db.session.commit()
        return redirect("/campaigns")
    else:
        Campaigns = MyCampaigns.query.order_by(MyCampaigns.started_on).all()
        return render_template("campaigns.html", campaigns=Campaigns)

@app.route("/editcampaign/<int:id>", methods=["GET", "POST"])
def editcampaign(id):
    campaign = MyCampaigns.query.get_or_404(id)
    
    if request.method == "POST":
        campaign.name = request.form['name']
        campaign.description = request.form['description']
        campaign.system = request.form['system']
        campaign.active = 'active' in request.form
        campaign.started_on = datetime.strptime(request.form['started_on'], '%Y-%m-%d').date()
        campaign.my_character = request.form['my_character']
        
        db.session.commit()
        return redirect("/campaigns")
    else:
        return render_template("editcampaign.html", campaign=campaign)

@app.route("/deletecampaign/<int:id>")
def delete(id):
    campaign = MyCampaigns.query.get_or_404(id)
    try:
        db.session.delete(campaign)
        db.session.commit()
        return redirect("/campaigns")
    except Exception as e:
        return f"An error occurred deleting the campaign: {e}"













if __name__ in "__main__":
    with app.app_context():
        db.create_all()


    app.run(debug=True)
