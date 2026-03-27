from sqlalchemy import Column, Integer, String, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user") # "user" or "admin"

class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True) # Normalized name e.g. "mumbai"
    display_name = Column(String) # e.g. "Mumbai, India"

    places = relationship("Place", back_populates="destination", cascade="all, delete-orphan")
    hotels = relationship("Hotel", back_populates="destination", cascade="all, delete-orphan")

class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    destination_id = Column(Integer, ForeignKey("destinations.id"))

    destination = relationship("Destination", back_populates="places")

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String) # "Budget", "Mid-range", "Luxury"
    price_per_night = Column(String) # e.g. "₹5,000"
    rating = Column(String) # e.g. "4.5/5"
    location = Column(String)
    highlights = Column(JSON) # List of highlights
    destination_id = Column(Integer, ForeignKey("destinations.id"))

    destination = relationship("Destination", back_populates="hotels")
