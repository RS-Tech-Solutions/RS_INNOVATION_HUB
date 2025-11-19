"# RS Innovation Hub - Backend Integration Contracts

## Authentication System

### User Roles & Permissions
```
OWNER: Full access to everything
MANAGER: Manage programs, events, view applications, manage users (except owners)  
EDITOR: Add/Edit content, view applications (no delete permissions)
USER: Public user who can apply for programs
```

### Authentication Methods
- Email/Password authentication
- Google OAuth integration
- JWT token-based sessions
- Role-based access control (RBAC)

## API Endpoints

### Authentication Endpoints
```
POST /api/auth/register - User registration
POST /api/auth/login - Email/password login  
POST /api/auth/google - Google OAuth login
POST /api/auth/logout - Logout user
GET /api/auth/me - Get current user info
PUT /api/auth/profile - Update user profile
```

### Admin User Management
```
GET /api/admin/users - List all users (Manager+)
PUT /api/admin/users/:id/role - Change user role (Owner only)
DELETE /api/admin/users/:id - Delete user (Owner only)
GET /api/admin/users/:id - Get user details (Manager+)
```

### Programs Management  
```
GET /api/programs - Public: Get all programs
POST /api/admin/programs - Create program (Editor+)
PUT /api/admin/programs/:id - Update program (Editor+)  
DELETE /api/admin/programs/:id - Delete program (Manager+)
GET /api/admin/programs/:id - Get program details (Editor+)
```

### Events Management
```
GET /api/events - Public: Get all events
POST /api/admin/events - Create event (Editor+)
PUT /api/admin/events/:id - Update event (Editor+)
DELETE /api/admin/events/:id - Delete event (Manager+)  
GET /api/admin/events/:id - Get event details (Editor+)
```

### Applications Management
```
POST /api/applications - Submit application (Authenticated users)
GET /api/admin/applications - List all applications (Editor+)
GET /api/admin/applications/:id - Get application details (Editor+)
PUT /api/admin/applications/:id/status - Update application status (Editor+)
DELETE /api/admin/applications/:id - Delete application (Manager+)
```

### Success Stories Management
```
GET /api/success-stories - Public: Get all stories
POST /api/admin/success-stories - Create story (Editor+)
PUT /api/admin/success-stories/:id - Update story (Editor+)
DELETE /api/admin/success-stories/:id - Delete story (Manager+)
```

### Contact Messages
```
POST /api/contact - Submit contact form (Public)
GET /api/admin/contacts - List all contacts (Editor+)
GET /api/admin/contacts/:id - Get contact details (Editor+)  
PUT /api/admin/contacts/:id/status - Mark as read/replied (Editor+)
DELETE /api/admin/contacts/:id - Delete contact (Manager+)
```

### Dashboard Stats
```
GET /api/admin/dashboard - Get dashboard statistics (Editor+)
- Total users, applications, events, programs
- Recent activities
- Application status breakdown
```

## Database Models

### User Model
```javascript
{
  _id: ObjectId,
  name: String,
  email: String (unique),
  password: String (hashed), // null for Google OAuth users
  googleId: String, // for Google OAuth users
  role: Enum['USER', 'EDITOR', 'MANAGER', 'OWNER'],
  profilePicture: String (URL),
  phone: String,
  isActive: Boolean,
  createdAt: Date,
  updatedAt: Date
}
```

### Application Model
```javascript
{
  _id: ObjectId,
  userId: ObjectId (ref: User),
  programId: ObjectId (ref: Program), // null for event registrations
  eventId: ObjectId (ref: Event), // null for program applications
  type: Enum['PROGRAM', 'EVENT'],
  formData: {
    name: String,
    email: String,
    phone: String,
    experience: String,
    motivation: String,
    organization: String // for events
  },
  status: Enum['PENDING', 'REVIEWED', 'APPROVED', 'REJECTED'],
  reviewNotes: String,
  reviewedBy: ObjectId (ref: User),
  reviewedAt: Date,
  createdAt: Date,
  updatedAt: Date
}
```

### Program Model (Updated)
```javascript
{
  _id: ObjectId,
  title: String,
  description: String,
  features: [String],
  duration: String,
  category: Enum['incubation', 'courses', 'internship', 'employment'],
  image: String (URL),
  isActive: Boolean,
  maxParticipants: Number,
  currentParticipants: Number,
  createdBy: ObjectId (ref: User),
  createdAt: Date,
  updatedAt: Date
}
```

### Event Model (Updated)
```javascript
{
  _id: ObjectId,
  title: String,
  description: String,
  date: String,
  type: String,
  participants: String,
  prizes: String,
  status: Enum['upcoming', 'ongoing', 'completed'],
  image: String (URL),
  maxRegistrations: Number,
  currentRegistrations: Number,
  createdBy: ObjectId (ref: User),
  createdAt: Date,
  updatedAt: Date
}
```

### Success Story Model (Updated)
```javascript
{
  _id: ObjectId,
  name: String,
  company: String,
  story: String,
  achievement: String,
  image: String (URL),
  isPublished: Boolean,
  createdBy: ObjectId (ref: User),
  createdAt: Date,
  updatedAt: Date
}
```

### Contact Model
```javascript
{
  _id: ObjectId,
  name: String,
  email: String,
  phone: String,
  subject: String,
  message: String,
  status: Enum['UNREAD', 'READ', 'REPLIED'],
  replyMessage: String,
  repliedBy: ObjectId (ref: User),
  repliedAt: Date,
  createdAt: Date,
  updatedAt: Date
}
```

## Frontend Changes Required

### Mock Data Replacement
- Remove mock.js usage in all components
- Replace mockSubmissions with real API calls
- Add authentication context/provider
- Add loading states and error handling

### New Components Needed
1. **LoginPage** - Email/password + Google OAuth
2. **RegisterPage** - User registration
3. **AdminLayout** - Admin dashboard wrapper
4. **AdminDashboard** - Statistics and overview
5. **AdminPrograms** - CRUD operations for programs
6. **AdminEvents** - CRUD operations for events  
7. **AdminApplications** - View and manage applications
8. **AdminSuccessStories** - CRUD operations for stories
9. **AdminContacts** - View and respond to contacts
10. **AdminUsers** - User management (for Manager+ roles)
11. **ProtectedRoute** - Route protection based on roles
12. **UserProfile** - User profile management

### Authentication Flow
1. Public users can view website content
2. Login/signup required for program applications and event registrations
3. Role-based access to admin sections
4. JWT token stored in localStorage/cookies
5. Automatic logout on token expiration

### Admin Panel Structure
```
/admin/dashboard - Overview and statistics
/admin/programs - Manage programs and courses
/admin/events - Manage events and hackathons
/admin/applications - View and process applications
/admin/success-stories - Manage testimonials  
/admin/contacts - Handle contact form submissions
/admin/users - User management (Manager+ only)
/admin/profile - Admin profile settings
```

This comprehensive system will allow you to easily manage all website content without touching any code, while providing proper user authentication and role-based access control." 