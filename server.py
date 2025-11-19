from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import List, Optional
import os
import jwt
import bcrypt
from pydantic import BaseModel, Field, EmailStr
import uuid
from enum import Enum
import logging
from pathlib import Path

# Import routes
from routes.auth import router as auth_router
from routes.programs import router as programs_router
from routes.events import router as events_router
from routes.applications import router as applications_router
from routes.success_stories import router as success_stories_router
from routes.contact import router as contact_router
from routes.admin_users import router as admin_users_router
from routes.dashboard import router as dashboard_router

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# JWT Configuration
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24

# Create the main app
app = FastAPI(title=\"RS Innovation Hub API\")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=[\"*\"],
    allow_methods=[\"*\"],
    allow_headers=[\"*\"],
)

# Security
security = HTTPBearer()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Enums
class UserRole(str, Enum):
    USER = \"USER\"
    EDITOR = \"EDITOR\" 
    MANAGER = \"MANAGER\"
    OWNER = \"OWNER\"

class ApplicationStatus(str, Enum):
    PENDING = \"PENDING\"
    REVIEWED = \"REVIEWED\"
    APPROVED = \"APPROVED\"
    REJECTED = \"REJECTED\"

class ApplicationType(str, Enum):
    PROGRAM = \"PROGRAM\"
    EVENT = \"EVENT\"

class ContactStatus(str, Enum):
    UNREAD = \"UNREAD\"
    read = \"read\"
    REPLIED = \"REPLIED\"

class EventStatus(str, Enum):
    UPCOMING = \"upcoming\"
    ONGOING = \"ongoing\"
    COMPLETED = \"completed\"

class ProgramCategory(str, Enum):
    INCUBATION = \"incubation\"
    COURSES = \"courses\"
    INTERNSHIP = \"internship\"
    EMPLOYMENT = \"employment\"

# Pydantic Models
class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    phone: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class GoogleAuthData(BaseModel):
    google_id: str
    name: str
    email: EmailStr
    picture: Optional[str] = None

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    role: UserRole = UserRole.USER
    profile_picture: Optional[str] = None
    phone: Optional[str] = None
    google_id: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: UserRole
    profile_picture: Optional[str]
    phone: Optional[str]
    is_active: bool
    created_at: datetime

class ProgramCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=10)
    features: List[str]
    duration: str
    category: ProgramCategory
    image: Optional[str] = None
    max_participants: Optional[int] = None

class Program(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    features: List[str]
    duration: str
    category: ProgramCategory
    image: Optional[str]
    is_active: bool = True
    max_participants: Optional[int]
    current_participants: int = 0
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class EventCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=10)
    date: str
    type: str
    participants: str
    prizes: str
    status: EventStatus = EventStatus.UPCOMING
    image: Optional[str] = None
    max_registrations: Optional[int] = None

class Event(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    date: str
    type: str
    participants: str
    prizes: str
    status: EventStatus
    image: Optional[str]
    max_registrations: Optional[int]
    current_registrations: int = 0
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ApplicationData(BaseModel):
    name: str
    email: EmailStr
    phone: str
    experience: Optional[str] = None
    motivation: Optional[str] = None
    organization: Optional[str] = None  # for events

class ApplicationCreate(BaseModel):
    program_id: Optional[str] = None
    event_id: Optional[str] = None
    type: ApplicationType
    form_data: ApplicationData

class Application(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    program_id: Optional[str]
    event_id: Optional[str]
    type: ApplicationType
    form_data: ApplicationData
    status: ApplicationStatus = ApplicationStatus.PENDING
    review_notes: Optional[str] = None
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class SuccessStoryCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    company: str = Field(..., min_length=2, max_length=200)
    story: str = Field(..., min_length=10)
    achievement: str = Field(..., min_length=3, max_length=200)
    image: Optional[str] = None

class SuccessStory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    company: str
    story: str
    achievement: str
    image: Optional[str]
    is_published: bool = True
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ContactCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str
    subject: str = Field(..., min_length=3, max_length=200)
    message: str = Field(..., min_length=10)

class Contact(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    phone: str
    subject: str
    message: str
    status: ContactStatus = ContactStatus.UNREAD
    reply_message: Optional[str] = None
    replied_by: Optional[str] = None
    replied_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Utility Functions
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_jwt_token(user_data: dict) -> str:
    payload = {
        **user_data,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=\"Token expired\")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=\"Invalid token\")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    payload = verify_jwt_token(token)
    
    user = await db.users.find_one({\"id\": payload[\"id\"]})
    if not user or not user.get(\"is_active\", True):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=\"User not found or inactive\")
    
    return user

def require_role(min_role: UserRole):
    role_hierarchy = {
        UserRole.USER: 0,
        UserRole.EDITOR: 1, 
        UserRole.MANAGER: 2,
        UserRole.OWNER: 3
    }
    
    async def role_checker(current_user: dict = Depends(get_current_user)):
        user_role = UserRole(current_user.get(\"role\", UserRole.USER))
        if role_hierarchy[user_role] < role_hierarchy[min_role]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f\"Insufficient permissions. Required: {min_role.value}\"
            )
        return current_user
    
    return role_checker

# Include all routers
app.include_router(auth_router)
app.include_router(programs_router)
app.include_router(events_router)
app.include_router(applications_router)
app.include_router(success_stories_router)
app.include_router(contact_router)
app.include_router(admin_users_router)
app.include_router(dashboard_router)

# Root endpoint
@app.get(\"/api/\")
async def root():
    return {\"message\": \"RS Innovation Hub API\", \"version\": \"1.0.0\"}

@app.on_event(\"shutdown\")
async def shutdown_db_client():
    client.close()