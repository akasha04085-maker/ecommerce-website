from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    
    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )
    
    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )
    
    password = db.Column(
        db.String(255),
        default="user"
    )
    
    role = db.Column(
    db.String(20),
    default="user"
    )
    def to_dict(self):
        return{
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role
        }