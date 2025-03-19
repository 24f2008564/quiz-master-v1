from flask_restful import Resource, Api
from flask import request

from .models import *

api = Api()

class ShowAPi(Resource):
    # GET /api/subjects returns all subjects with their chapters
    
    def get(self):
        subjects = Subject.query.all() 
        s_list = []
        for subject in subjects:
            s_list.append({"id": subject.id, "name": subject.name, "description": subject.description, "chapters":[chapter.name for chapter in subject.chapters]})
        return (s_list)
    

    def post(self):
        name = request.json.get('name')
        description = request.json.get('description')
        subject = Subject.query.filter_by(name = name).first()
        if not subject:
            new_subject=  Subject(name = name, description = description)
            db.session.add(new_subject)
            db.session.commit()
            return {"message":"Subject added succesfully"}, 201
        return {"message":"subject already exist"}

    def put (self, id):
        subject =Subject.query.filter_by(id = id).first()
        if subject:
            subject.name = request.json.get('name')
            subject.description = request.json.get('description')
            db.session.commit()
            return {"message": "subject updated successfully"} ,200
        return {"message":"SUbject does not exist. First add then do edit"}, 404
    
    def delete(self, id):
        subject = Subject.query.filter_by(id = id).first()
        db.session.delete(subject)
        db.session.commit()
        return {"message": "Subject deleted successfully"}, 200
        
    
api.add_resource(ShowAPi, "/api/view_subjects", "/api/add_subjects", "/api/put_subjects/<int:id>", "/api/deletesubject/<int:id>")
