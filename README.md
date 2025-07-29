# Wingz Django Engineer Assessment

A RESTful API built with Django REST Framework for managing ride formation.

## Features

- **Authentication**: Admin-only access to all API endpoints
- **Ride Management**: Complete CRUD operations for rides
- **User Management**: Manage riders and drivers
- **Event Tracking**: Track ride events with timestamp
- **Advanced Filtering**: Filter rides by status and rider email
- **Sorting**: Sort by pickup time and distance to pickup location
- **Performance Optimized**: Minimal database queries with optimized data retrieval
- **Pagination**: Built-in pagination for all list endpoints

## Technical Highlights

### Performance Optimization
- **Optimized Queries**: Uses `select_related()` and `prefetch_related()` to minimize database hits
- **Minimal Query Count**: Ride list API achieves 2-3 queries total (including pagination count)
- **Efficient Event Filtering**: Only retrieves ride events from last 24 hours for performance
- **Distance Sorting**: Implements Haversine formula for GPS-based distance calculations

### Security
- **Admin-Only Access**: Custom permission class ensures only admin users can access the API
- **Authentication**: Supports both session and basic authentication

## Database Configuration

The application is configured to use PostgreSQL by default. Database settings are managed through environment variables in the `.env` file:

```env
# Database Configuration
DB_NAME=wingz_db
DB_USER=wingz_user
DB_PASSWORD=wingz_password
DB_HOST=localhost
DB_PORT=5432
```

If you need to use different database credentials, update the `.env` file accordingly.

### Alternative: SQLite for Development

If you prefer to use SQLite for development, modify `rides_api/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## Quick Start

### Prerequisites
- Python 3.8+
- Django 5.2+
- PostgreSQL 12+

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd wingz
   ```

2. **Install PostgreSQL**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   
   # macOS with Homebrew
   brew install postgresql
   
   # Start PostgreSQL service
   sudo systemctl start postgresql  # Linux
   brew services start postgresql   # macOS
   ```

3. **Create database and user**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE wingz_db;
   CREATE USER wingz_user WITH PASSWORD 'wingz_password';
   GRANT ALL PRIVILEGES ON DATABASE wingz_db TO wingz_user;
   GRANT ALL ON SCHEMA public TO wingz_user;
   GRANT CREATE ON SCHEMA public TO wingz_user;
   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO wingz_user;
   \q
   ```

4. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Set up environment variables**
   ```bash
   # Create .env file (already included in project)
   # Update database credentials if different from defaults
   ```

7. **Run migrations**
   ```bash
   python manage.py migrate
   ```

8. **Create sample data**
   ```bash
   python manage.py create_sample_data
   ```

9. **Run the development server**
   ```bash
   python manage.py runserver
   ```

10. **Test the API** (optional)
    ```bash
    # In a new terminal, with the server running:
    python test_api.py
    ```

### Default Admin Credentials
- **Email**: admin@wingz.com
- **Password**: admin123

## API Endpoints

### Authentication
All endpoints require authentication. Use the admin credentials to access the API.

### Base URL
```
http://localhost:8000/api/v1/
```

### Available Endpoints

#### Rides
- `GET /api/v1/rides/` - List all rides with filtering and sorting
- `POST /api/v1/rides/` - Create a new ride
- `GET /api/v1/rides/{id}/` - Retrieve a specific ride
- `PUT /api/v1/rides/{id}/` - Update a ride
- `DELETE /api/v1/rides/{id}/` - Delete a ride

#### Users
- `GET /api/v1/users/` - List all users
- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/{id}/` - Retrieve a specific user
- `PUT /api/v1/users/{id}/` - Update a user
- `DELETE /api/v1/users/{id}/` - Delete a user

#### Ride Events
- `GET /api/v1/ride-events/` - List all ride events
- `POST /api/v1/ride-events/` - Create a new ride event
- `GET /api/v1/ride-events/{id}/` - Retrieve a specific ride event
- `PUT /api/v1/ride-events/{id}/` - Update a ride event
- `DELETE /api/v1/ride-events/{id}/` - Delete a ride event

## Advanced Features

### Filtering
Filter rides using query parameters:
```bash
# Filter by status
GET /api/v1/rides/?status=en-route

# Filter by rider email
GET /api/v1/rides/?rider_email=john.doe@example.com
```

### Sorting
Sort rides by pickup time:
```bash
# Sort by pickup time (ascending)
GET /api/v1/rides/?ordering=pickup_time

# Sort by pickup time (descending)
GET /api/v1/rides/?ordering=-pickup_time
```

### Distance-based Sorting
Sort rides by distance to pickup location:
```bash
# Sort by distance to pickup (requires lat, lon, and sort_by_distance=true)
GET /api/v1/rides/?lat=37.7749&lon=-122.4194&sort_by_distance=true
```

### Pagination
All list endpoints support pagination:
```bash
# Get second page
GET /api/v1/rides/?page=2

# Results include:
{
  "count": 50,
  "next": "http://localhost:8000/api/v1/rides/?page=3",
  "previous": "http://localhost:8000/api/v1/rides/?page=1",
  "results": [...]
}
```

## API Examples

### Create a Ride
```bash
curl -X POST http://localhost:8000/api/v1/rides/ \
  -H "Content-Type: application/json" \
  -u admin@wingz.com:admin123 \
  -d '{
    "status": "en-route",
    "id_rider": 2,
    "id_driver": 3,
    "pickup_latitude": 37.7749,
    "pickup_longitude": -122.4194,
    "dropoff_latitude": 37.7849,
    "dropoff_longitude": -122.4094,
    "pickup_time": "2024-01-15T10:30:00Z"
  }'
```

### Get Rides with Filtering
```bash
curl -X GET "http://localhost:8000/api/v1/rides/?status=pickup&rider_email=john" \
  -u admin@wingz.com:admin123
```

### Get Rides Sorted by Distance
```bash
curl -X GET "http://localhost:8000/api/v1/rides/?lat=37.7749&lon=-122.4194&sort_by_distance=true" \
  -u admin@wingz.com:admin123
```

## Database Schema

### User Table
| Field | Type | Description |
|-------|------|-------------|
| id_user | AutoField | Primary key |
| role | CharField | User role (admin, driver, rider) |
| first_name | CharField | User's first name |
| last_name | CharField | User's last name |
| email | EmailField | User's email (unique) |
| phone_number | CharField | User's phone number |

### Ride Table
| Field | Type | Description |
|-------|------|-------------|
| id_ride | AutoField | Primary key |
| status | CharField | Ride status |
| id_rider | ForeignKey | Reference to User |
| id_driver | ForeignKey | Reference to User |
| pickup_latitude | FloatField | Pickup latitude |
| pickup_longitude | FloatField | Pickup longitude |
| dropoff_latitude | FloatField | Dropoff latitude |
| dropoff_longitude | FloatField | Dropoff longitude |
| pickup_time | DateTimeField | Pickup time |

### RideEvent Table
| Field | Type | Description |
|-------|------|-------------|
| id_ride_event | AutoField | Primary key |
| id_ride | ForeignKey | Reference to Ride |
| description | CharField | Event description |
| created_at | DateTimeField | Event timestamp |

## Performance Considerations

### Query Optimization
The application implements several optimizations:

1. **Select Related**: User foreign keys are loaded with the rides to avoid N+1 queries
2. **Prefetch Related**: Recent ride events are prefetched with a filtered queryset
3. **Indexed Fields**: Database indexes on frequently queried fields
4. **Limited Event Retrieval**: Only events from last 24 hours are retrieved

### Query Count Analysis
For the rides list endpoint:
- **Query 1**: Fetch rides with related users and recent events
- **Query 2**: Count total rides for pagination
- **Result**: 2-3 total queries regardless of result size

## Bonus: SQL Query for Reporting

The following SQL query returns the count of trips that took more than 1 hour from pickup to dropoff, grouped by month and driver:

```sql
WITH ride_durations AS (
    SELECT 
        r.id_ride,
        r.id_driver,
        u.first_name || ' ' || LEFT(u.last_name, 1) as driver_name,
        pickup_event.created_at as pickup_time,
        dropoff_event.created_at as dropoff_time,
        EXTRACT(EPOCH FROM (dropoff_event.created_at - pickup_event.created_at)) / 3600 as duration_hours,
        TO_CHAR(pickup_event.created_at, 'YYYY-MM') as month
    FROM ride r
    JOIN "user" u ON r.id_driver = u.id_user
    JOIN ride_event pickup_event ON r.id_ride = pickup_event.id_ride 
        AND pickup_event.description = 'Status changed to pickup'
    JOIN ride_event dropoff_event ON r.id_ride = dropoff_event.id_ride 
        AND dropoff_event.description = 'Status changed to dropoff'
    WHERE pickup_event.created_at < dropoff_event.created_at
)
SELECT 
    month,
    driver_name as "Driver",
    COUNT(*) as "Count of Trips > 1 hr"
FROM ride_durations
WHERE duration_hours > 1
GROUP BY month, driver_name, id_driver
ORDER BY month, driver_name;
```

## Testing

### Running Tests
```bash
python manage.py test
```

### Manual Testing
1. Use the Django admin interface at `/admin/`
2. Use the browsable API at `/api/v1/`
3. Use curl or Postman for API testing

### Sample Data
The `create_sample_data` command creates:
- 1 admin user
- 3 drivers (Chris H, Howard Y, Randy W)
- 5 riders
- 50 sample rides with realistic Bay Area coordinates
- Multiple ride events per ride

## Design Decisions

### Custom User Model
- Extended Django's AbstractUser to match the required schema
- Used email as the username field for better UX
- Added role-based permissions

### Database Optimization
- Added strategic indexes for frequently queried fields
- Used custom table names to match requirements
- Optimized foreign key relationships

### Distance Calculation
- Implemented Haversine formula for accurate GPS distance calculations
- For production with very large datasets, consider using PostGIS or similar spatial database extensions

### API Design
- RESTful design following Django REST Framework conventions
- Comprehensive error handling and validation
- Flexible filtering and sorting options

## Production Considerations

### Database
- Use PostgreSQL for production
- Consider adding database connection pooling
- Implement database query monitoring

### Security
- Use environment variables for sensitive settings
- Implement rate limiting
- Add HTTPS in production
- Consider JWT tokens for stateless authentication

### Performance
- Add Redis for caching
- Implement database query optimization monitoring
- Consider adding API response caching for read-heavy workloads

### Monitoring
- Add logging for API requests
- Implement health check endpoints
- Monitor database query performance

## License
This project is developed as part of the Wingz Django Engineer Assessment.
