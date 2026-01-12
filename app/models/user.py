from datetime import datetime
from datetime import UTC
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.extensions import Base

class User(Base):
    __tablename__ = 'users'
    
    # Basic info
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    
    # Profile info
    display_name: Mapped[str] = mapped_column(String(100), nullable=True)
    bio: Mapped[str] = mapped_column(String(500), nullable=True)
    profile_picture_url: Mapped[str] = mapped_column(String(255), nullable=True)
    cover_photo_url: Mapped[str] = mapped_column(String(255), nullable=True)
    location: Mapped[str] = mapped_column(String(100), nullable=True)
    website: Mapped[str] = mapped_column(String(255), nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_json(self, include_email=False):
        """"Convert user to dict (for API responses)"""
        data = {
            'id': self.id,
            'username': self.username,
            'display_name': self.display_name,
            'bio': self.bio,
            'profile_picture_url': self.profile_picture_url,
            'cover_photo_url': self.cover_photo_url,
            'location': self.location,
            'website': self.website,
            'created_at': self.created_at.isoformat()
        }
        if include_email:
            data['email'] = self.email
        
        return data
    