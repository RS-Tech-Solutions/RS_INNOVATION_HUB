"#!/usr/bin/env python3

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import uuid
import bcrypt
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

async def main():
    print(\"Initializing database...\")
    
    try:
        await db.command(\"ping\")
        print(\"Database connected successfully\")
        
        # Create admin user
        existing_admin = await db.users.find_one({\"email\": \"admin@rsinnovationhub.com\"})
        if not existing_admin:
            admin_user = {
                \"id\": str(uuid.uuid4()),
                \"name\": \"Admin User\",
                \"email\": \"admin@rsinnovationhub.com\", 
                \"password\": hash_password(\"admin123\"),
                \"role\": \"OWNER\",
                \"profile_picture\": None,
                \"phone\": \"+91 98765 43210\",
                \"google_id\": None,
                \"is_active\": True,
                \"created_at\": datetime.utcnow(),
                \"updated_at\": datetime.utcnow()
            }
            await db.users.insert_one(admin_user)
            print(\"Admin user created: admin@rsinnovationhub.com / admin123\")
        else:
            print(\"Admin user already exists\")
            
        print(\"Database initialization complete!\")
        
    except Exception as e:
        print(f\"Error: {e}\")
    finally:
        client.close()

if __name__ == \"__main__\":
    asyncio.run(main())"