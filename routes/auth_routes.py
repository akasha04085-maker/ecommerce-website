from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models.user import db, User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    
    data = request.get_json()
    
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    if not username or not email or not password:
        return jsonify({
            "message": "All field are required"
        }), 400
        
    
    existing_user = User.query.filter_by(email=email).first()
    
    if existing_user:
        return jsonify({
            "message": "Email already exists"
        }), 400
        
    hashed_password = generate_password_hash(password)
    
    new_user = User(
        username=username,
        email=email,
        password=hashed_password
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        "message": "User registered successfully"
    }), 201