from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
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
    
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({
            "message": "Email and password are required"
        }), 400 
        
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({
            "message": "Invalid email or password"
        }), 400 
        
    if not check_password_hash(user.password, password):
        return jsonify({
            "message": "Invalid email or password"
        }), 400
        
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        "message": "Login successful",
        "access_token": access_token
    }), 400 
    
@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    
    user_id = get_jwt_identity()
    
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({
            "message": "User not found"
        }), 404
        
    return jsonify({
        "user": user.to_dict()
    }), 200