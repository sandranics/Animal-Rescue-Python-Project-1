from flask import Blueprint, render_template, request, flash, jsonify, Response
from flask_login import login_required, current_user
from .models import Ad, Image
from werkzeug.utils import secure_filename
from . import db
import json

views = Blueprint('views', __name__) #views is te blueprint of our application, the routes/urls are defined here

@views.route('/', methods=['GET', 'POST']) #home page --- differentiate get and post 
@login_required
def home():
    if request.method == 'POST': 
        file = request.files['file'] #Gets the ad from the HTML 
        name = request.form.get('name') 
        breed = request.form.get('breed')
        age = request.form.get('age')
        health_status = request.form.get('health_status')
        location = request.form.get('location')

        filename = secure_filename(file.filename)
        mimetype = file.mimetype

        #could add checks here
        image = Image(img=file.read(), name=filename, mimetype=mimetype)
        db.session.add(image)
        new_ad = Ad(name=name, breed=breed,age=age, health_status=health_status, location=location, user_id=current_user.id, image=image)  #providing the schema for the ad 
        db.session.add(new_ad) #adding the ad to the database 
        db.session.commit()
            
        flash('Ad added!', category='success')

    return render_template("home.html", user=current_user) #to access all ads ...
 
@views.route('/<int:id>')
def get_img(id):
    img = Image.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img, mimetype=img.mimetype)

@views.route('/delete-ad', methods=['POST'])
def delete_ad():  
    ad = json.loads(request.data) # this function expects a JSON from the INDEX.js file --- that's how we get the id
    adId = ad['adId'] #the string is turned to a python dictionary object
    ad = Ad.query.get(adId)
    if ad:
        if ad.user_id == current_user.id:
            db.session.delete(ad)
            image=Image.query.get(adId)
            db.session.delete(image)
            db.session.commit()

    return jsonify({})
