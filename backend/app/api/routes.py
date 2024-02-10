from flask import Blueprint, request, jsonify
from app.helpers import token_required
from app.models import db, User, Project, project_schema, projects_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
@token_required
def getdata(current_user_data):
    return{ 'A': 'Value' }

@api.route('/projects', methods=['POST'])
@token_required
def create_project(current_user_token):
    name = request.json['name']
    description = request.json['description']
    language_to_use = request.json['language_to_use']
    amount_of_lines_to_use = request.json['amount_of_lines_to_use']
    is_it_a_webpage = request.json['is_it_a_webpage']
    user_token = current_user_token.token 
    
    print(f"Test: {user_token}")
    
    project = Project(
        name=name,
        description=description,
        language_to_use=language_to_use,
        amount_of_lines_to_use=amount_of_lines_to_use,
        is_it_a_webpage=is_it_a_webpage,
        user_token=user_token
    )
    
    db.session.add(project)
    db.session.commit()
    
    response = project_schema.dump(project)
    return jsonify(response)


@api.route('/projects', methods=['GET'])
@token_required
def get_projects(current_user_token):
    user_token = current_user_token.token
    projects = Project.query.filter_by(user_token=user_token).all()
    response = projects_schema.dump(projects)
    return jsonify(response)

    
@api.route('/projects/<id>', methods = ['POST', 'PUT'])
@token_required
def update_project(current_user_token, id):
    project = Project.query.get(id)
    
    project.name = request.json['name']
    project.description = request.json['description']
    project.language_to_use = request.json['language_to_use']
    project.amount_of_lines_to_use = request.json['amount_of_lines_to_use']
    project.is_it_a_webpage = request.json['is_it_a_webpage']
    project.user_token = current_user_token.token
    
    db.session.commit()
    response = project_schema.dump(project)
    return jsonify(response)

@api.route('/projects/<id>', methods = ['DELETE'])
@token_required
def delete_project(current_user_token, id):
    project = Project.query.get(id)
    db.session.delete(project)
    db.session.commit()
    response = project_schema.dump(project)
    return jsonify(response)