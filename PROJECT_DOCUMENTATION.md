# Community Skill Swap Platform - Project Documentation

## Project Overview

The Community Skill Swap Platform is a web-based application that enables users to share, exchange, and learn skills from each other in a community-driven environment. The platform facilitates skill-based networking where users can offer their expertise and request to learn from others through a structured exchange system.

## Objectives

1. **Skill Sharing**: Enable users to showcase their skills and expertise
2. **Skill Exchange**: Facilitate requests for skill exchanges between users
3. **Community Building**: Create a platform for knowledge sharing and collaboration
4. **User Management**: Provide secure authentication and user profile management
5. **Notification System**: Keep users informed about exchange requests and responses

## Features

### Core Features
- **User Authentication**: Secure JWT-based login and registration system
- **Skill Management**: Create, view, update, and delete skills
- **Skill Exchange**: Send and manage skill swap requests
- **Notification System**: Real-time notifications for exchange activities
- **User Dashboard**: Personal dashboard with statistics and quick actions
- **Responsive Design**: Mobile-friendly interface

### Advanced Features
- **Skill Valuation**: Numeric value system for skill ranking
- **Proficiency Levels**: Beginner, Intermediate, Advanced, Expert categories
- **Status Tracking**: Pending, Accepted, Rejected, Completed exchange states
- **Search & Filter**: Find skills by category and search terms

## Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: Microsoft SQL Server with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: Swagger/OpenAPI
- **Validation**: Pydantic schemas

### Frontend
- **Languages**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Custom CSS with responsive design
- **API Communication**: Fetch API with async/await
- **Storage**: LocalStorage for authentication tokens

### Database
- **System**: Microsoft SQL Server (blogDb)
- **ORM**: SQLAlchemy with declarative models
- **Migrations**: Automated table creation
- **Relationships**: Foreign keys with proper constraints

## Use Case Diagram

### Text Explanation

**Actors:**
1. **User**: Community member who offers and requests skills
2. **System**: Automated processes for authentication and notifications

**Primary Use Cases:**

1. **User Registration**
   - User provides username, email, password, full name, bio
   - System validates data and creates account
   - System sends welcome notification

2. **User Login**
   - User provides credentials
   - System validates and returns JWT token
   - Token stored for session management

3. **Skill Management**
   - User creates skill with title, description, category, proficiency, value
   - System validates and stores skill
   - User can update or delete own skills

4. **Skill Exchange Request**
   - User browses available skills
   - User sends exchange request with message
   - System creates notification for skill owner
   - Request status: Pending → Accepted/Rejected

5. **Notification Management**
   - System creates notifications for requests and responses
   - Users can view and mark notifications as read
   - Real-time updates for exchange activities

## Data Flow Diagram (DFD Level 0)

### Text Explanation

**External Entities:**
- User: Community member interacting with the system

**Processes:**
1. **Authentication Process**: Handles login, registration, token validation
2. **Skill Management Process**: Manages CRUD operations for skills
3. **Exchange Process**: Handles skill swap requests and status updates
4. **Notification Process**: Manages notification creation and delivery

**Data Stores:**
- User Database: Stores user profiles and credentials
- Skills Database: Stores skill information and metadata
- Exchange Database: Stores exchange requests and status
- Notification Database: Stores user notifications

## Data Flow Diagram (DFD Level 1)

### Text Explanation

**Process 1: Authentication Module**
- Input: User credentials (username, password)
- Processing: JWT token generation, validation
- Output: Authentication token, user session

**Process 2: Skill Management Module**
- Input: Skill data (title, description, category, etc.)
- Processing: Validation, database storage, user association
- Output: Skill record, confirmation message

**Process 3: Exchange Management Module**
- Input: Exchange request (skill_id, message, requester_id)
- Processing: Validation, notification creation, status tracking
- Output: Exchange record, notifications to involved users

**Process 4: Notification Module**
- Input: Notification data (user_id, title, message, type)
- Processing: Database storage, unread status tracking
- Output: Notification record, real-time updates

## Database Schema

### Users Table
- **id**: Primary key, auto-increment
- **username**: Unique user identifier (50 chars)
- **email**: Unique email address (100 chars)
- **password_hash**: Encrypted password (255 chars)
- **full_name**: User display name (100 chars)
- **bio**: Optional user biography (text)
- **created_at**: Account creation timestamp
- **is_active**: Account status flag

### Skills Table
- **id**: Primary key, auto-increment
- **user_id**: Foreign key to users table
- **title**: Skill name (100 chars)
- **description**: Detailed skill description (text)
- **category**: Skill category (50 chars)
- **proficiency_level**: Expertise level (20 chars)
- **value**: Skill valuation (integer, 0-1000)
- **created_at**: Skill creation timestamp
- **is_active**: Skill status flag

### Skill Exchange Requests Table
- **id**: Primary key, auto-increment
- **skill_id**: Foreign key to skills table
- **requester_id**: Foreign key to users (requester)
- **skill_owner_id**: Foreign key to users (owner)
- **message**: Exchange request message (text)
- **status**: Request status (pending, accepted, rejected, completed)
- **created_at**: Request creation timestamp
- **updated_at**: Last update timestamp

### Notifications Table
- **id**: Primary key, auto-increment
- **user_id**: Foreign key to users table
- **title**: Notification title (200 chars)
- **message**: Notification content (text)
- **type**: Notification category (swap_request, swap_accepted, swap_rejected)
- **related_id**: Associated object ID (optional)
- **is_read**: Read status flag
- **created_at**: Notification timestamp

## API Endpoints

### Authentication Endpoints
- `POST /users/register`: User registration
- `POST /users/login`: User authentication
- `GET /users/me`: Current user profile
- `PUT /users/{user_id}`: Update user profile

### Skills Endpoints
- `POST /skills/`: Create new skill
- `GET /skills/`: List all skills (with filters)
- `GET /skills/my-skills`: Current user's skills
- `GET /skills/{skill_id}`: Get specific skill
- `PUT /skills/{skill_id}`: Update skill
- `DELETE /skills/{skill_id}`: Delete skill

### Exchange Endpoints
- `POST /exchanges/`: Create exchange request
- `GET /exchanges/`: User's exchange requests
- `GET /exchanges/{request_id}`: Get specific request
- `PUT /exchanges/{request_id}`: Update request status

### Notification Endpoints
- `GET /notifications/`: User notifications
- `GET /notifications/unread-count`: Unread notification count
- `PUT /notifications/{notification_id}/read`: Mark as read

## Testing Instructions

### Backend Testing (Swagger UI)

**Required Screenshots for Assignment:**

1. **Authentication Screenshots:**
   - `POST /users/register` - Show successful registration response
   - `POST /users/login` - Show JWT token response
   - `GET /users/me` - Show user profile data

2. **Skills Management Screenshots:**
   - `POST /skills/` - Show skill creation with value field
   - `GET /skills/` - Show skills list with filtering
   - `GET /skills/my-skills` - Show user's skills

3. **Exchange Flow Screenshots:**
   - `POST /exchanges/` - Show exchange request creation
   - `PUT /exchanges/{request_id}` - Show status update (accept/reject)
   - `GET /exchanges/` - Show user's exchange requests

4. **Notification System Screenshots:**
   - `GET /notifications/` - Show notifications list
   - `GET /notifications/unread-count` - Show unread count
   - `PUT /notifications/{id}/read` - Show mark as read

### Frontend Testing

**Manual Testing Steps:**

1. **User Registration:**
   - Navigate to `register.html`
   - Fill form with valid data
   - Submit and verify success message
   - Redirect to login page

2. **User Login:**
   - Navigate to `login.html`
   - Enter credentials
   - Verify dashboard redirect
   - Check token storage in localStorage

3. **Dashboard Functionality:**
   - Verify user statistics display
   - Check notifications loading
   - Test navigation links
   - Verify logout functionality

4. **Skill Management:**
   - Navigate to `add-skill.html`
   - Create skill with all fields
   - Verify success and redirect
   - Check skill appears in `skills.html`

5. **Exchange Requests:**
   - Browse skills in `skills.html`
   - Click "Request Exchange" on a skill
   - Enter message and submit
   - Verify notification creation

## How to Run the Project

### Prerequisites
- Python 3.8+ installed
- Microsoft SQL Server with `blogDb` database
- Required Python packages (see requirements.txt)

### Installation Steps

1. **Clone/Download Project:**
   ```bash
   cd "c:/Users/Javy/Desktop/skill swap"
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup:**
   - Ensure SQL Server is running
   - Verify `blogDb` database exists
   - Run table creation scripts if needed

4. **Start Backend Server:**
   ```bash
   python main.py
   ```
   - Server runs on `http://localhost:8000`
   - Swagger UI available at `http://localhost:8000/docs`

5. **Access Frontend:**
   - Open `frontend/login.html` in web browser
   - Or use simple HTTP server for frontend:
   ```bash
   cd frontend
   python -m http.server 3000
   ```

### Testing URLs
- **Frontend**: `http://localhost:3000/login.html`
- **Backend API**: `http://localhost:8000`
- **Swagger Docs**: `http://localhost:8000/docs`

## Conclusion

The Community Skill Swap Platform successfully implements a comprehensive skill exchange system with modern web technologies. The project demonstrates:

- **Full-Stack Development**: Complete frontend and backend integration
- **Database Design**: Proper relational database with constraints
- **API Development**: RESTful API with proper validation
- **Authentication**: Secure JWT-based authentication system
- **User Experience**: Responsive, intuitive interface design

The platform provides a solid foundation for community-based skill sharing and can be extended with additional features like messaging, ratings, or skill matching algorithms.

## Future Improvements

### Short-term Enhancements
1. **Real-time Notifications**: WebSocket integration for live updates
2. **Skill Ratings**: User feedback and rating system
3. **Advanced Search**: Full-text search with filters
4. **File Uploads**: Skill portfolios with images/documents
5. **User Profiles**: Enhanced profile pages with skills showcase

### Long-term Features
1. **Mobile Application**: Native iOS/Android apps
2. **Payment Integration**: Monetization for premium skills
3. **AI Matching**: Automated skill compatibility matching
4. **Video Chat**: Integrated video conferencing for skill exchange
5. **Analytics Dashboard**: Advanced usage and engagement metrics

### Technical Improvements
1. **Caching**: Redis integration for performance
2. **Load Balancing**: Multiple server instances
3. **CI/CD Pipeline**: Automated testing and deployment
4. **Containerization**: Docker deployment setup
5. **Monitoring**: Application performance monitoring

---

**Project Status**: ✅ Complete and Functional
**Last Updated**: January 2026
**Academic Level**: 3rd Semester University Project
