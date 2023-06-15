from sqlalchemy import BigInteger, Boolean, Column, Date, Float, ForeignKey, Index, Integer, String, Text, text, \
    create_engine
from sqlalchemy.dialects.postgresql import TIME, TIMESTAMP, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

url = URL.create(
    drivername=os.environ.get("DB_CONNECTION"),
    username=os.environ.get("DB_USERNAME"),
    password=os.environ.get("DB_PASSWORD"),
    host=os.environ.get("DB_HOST"),
    database=os.environ.get("DB_DATABASE"),
    port=os.environ.get("DB_PORT"),
)

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Category(Base):
    __tablename__ = 'categories'

    id = Column(UUID, primary_key=True)
    name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP())
    updated_at = Column(TIMESTAMP())
    key = Column(String(255))


class District(Base):
    __tablename__ = 'districts'

    id = Column(UUID, primary_key=True)
    regency_id = Column(UUID, nullable=False)
    name = Column(String(50), nullable=False)


class Province(Base):
    __tablename__ = 'provinces'

    id = Column(UUID, primary_key=True)
    name = Column(String(255), nullable=False)


class Regency(Base):
    __tablename__ = 'regencies'

    id = Column(UUID, primary_key=True)
    province_id = Column(UUID, nullable=False)
    name = Column(String(50), nullable=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID, primary_key=True)
    username = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_super_admin = Column(Boolean, nullable=False, server_default=text("false"))
    created_at = Column(TIMESTAMP(precision=0))
    updated_at = Column(TIMESTAMP(precision=0))
    is_dummy = Column(Boolean, server_default=text("false"))
    serial = Column(BigInteger, server_default=text("nextval('users_unique_id_seq'::regclass)"))


class Village(Base):
    __tablename__ = 'villages'

    id = Column(UUID, primary_key=True)
    district_id = Column(UUID, nullable=False)
    name = Column(String(50), nullable=False)


class Business(Base):
    __tablename__ = 'businesses'

    id = Column(UUID, primary_key=True)
    claim_by = Column(ForeignKey('users.id'))
    created_by = Column(ForeignKey('users.id'))
    province_id = Column(ForeignKey('provinces.id'))
    regency_id = Column(ForeignKey('regencies.id'))
    district_id = Column(ForeignKey('districts.id'))
    village_id = Column(ForeignKey('villages.id'))
    username = Column(String(255))
    name = Column(String(255), nullable=False)
    latitude = Column(String(255), nullable=False)
    longitude = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    postal_code = Column(String(6), nullable=False)
    avatar = Column(String(255))
    description = Column(String(255))
    released_at = Column(Date)
    google_maps_rating = Column(Float(53))
    created_at = Column(TIMESTAMP(precision=0))
    updated_at = Column(TIMESTAMP(precision=0))
    deleted_at = Column(TIMESTAMP(precision=0))
    is_monday_open = Column(Boolean, server_default=text("false"))
    monday_start_time = Column(TIME(precision=0))
    monday_end_time = Column(TIME(precision=0))
    monday_notes = Column(String(255))
    is_tuesday_open = Column(Boolean, server_default=text("false"))
    tuesday_start_time = Column(TIME(precision=0))
    tuesday_end_time = Column(TIME(precision=0))
    tuesday_notes = Column(String(255))
    is_wednesday_open = Column(Boolean, server_default=text("false"))
    wednesday_start_time = Column(TIME(precision=0))
    wednesday_end_time = Column(TIME(precision=0))
    wednesday_notes = Column(String(255))
    is_thursday_open = Column(Boolean, server_default=text("false"))
    thursday_start_time = Column(TIME(precision=0))
    thursday_end_time = Column(TIME(precision=0))
    thursday_notes = Column(String(255))
    is_friday_open = Column(Boolean, server_default=text("false"))
    friday_start_time = Column(TIME(precision=0))
    friday_end_time = Column(TIME(precision=0))
    friday_notes = Column(String(255))
    is_saturday_open = Column(Boolean, server_default=text("false"))
    saturday_start_time = Column(TIME(precision=0))
    saturday_end_time = Column(TIME(precision=0))
    saturday_notes = Column(String(255))
    is_sunday_open = Column(Boolean, server_default=text("false"))
    sunday_start_time = Column(TIME(precision=0))
    sunday_end_time = Column(TIME(precision=0))
    sunday_notes = Column(String(255))
    place_id = Column(String(255))
    added_from_system = Column(Boolean, nullable=False, server_default=text("false"))
    link_theme = Column(String(255))
    serial = Column(BigInteger, server_default=text("nextval('businesses_unique_id_seq'::regclass)"))

    user = relationship('User', primaryjoin='Business.claim_by == User.id')
    user1 = relationship('User', primaryjoin='Business.created_by == User.id')
    district = relationship('District')
    province = relationship('Province')
    regency = relationship('Regency')
    village = relationship('Village')


class BusinessCategory(Base):
    __tablename__ = 'business_categories'

    id = Column(UUID, primary_key=True)
    category_id = Column(ForeignKey('categories.id'), nullable=False)
    business_id = Column(ForeignKey('businesses.id'), nullable=False)
    created_at = Column(TIMESTAMP(precision=0))
    updated_at = Column(TIMESTAMP(precision=0))

    business = relationship('Business')
    category = relationship('Category')


class Upvote(Base):
    __tablename__ = 'upvotes'

    id = Column(UUID, primary_key=True)
    user_id = Column(ForeignKey('users.id'))
    business_id = Column(ForeignKey('businesses.id'), nullable=False)
    created_at = Column(TIMESTAMP(precision=0))
    updated_at = Column(TIMESTAMP(precision=0))

    business = relationship('Business')
    user = relationship('User')


Base.metadata.create_all(engine)
