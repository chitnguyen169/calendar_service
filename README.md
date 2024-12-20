# Calendar Service

## Introduction
The library is a simple calendar service. The service accepts calendar events comprised of a date-time and description, in JSON format, and save them persistently. On request, the service should return the saved calendar events in a JSON format aligned to the input one.

## Instructions
1. Clone repo: `git clone git@github.com:chitnguyen169/calendar_service.git`
2. Ensure Docker is up and running (e.g. `docker info` or `docker ps`)
3. Build docker image: `docker build -t calendar-service .`
4. Run: `docker run -p 8000:8000 calendar-service`

You can access at http://localhost:8000

## Endpoints

| Method | Endpoint           | Description                                                                    | Optional parameters                               | 
|--------|--------------------|--------------------------------------------------------------------------------|---------------------------------------------------|
| GET    | `/api/events`      | List all events within date range, by default set to "today" at 00:00:00 to now| `datetime_format`, `from_datetime`, `to_datetime` |
| POST   | `/api/events`      | Create a new event                                                             | `None`                                            |
| GET    | `/api/events/{id}` | Retrieve a specific event                                                      | `datetime_format`                                 |
 
## Examples:
- Create an event: 
   
    **POST** http://localhost:8000/events
    
    ```json 
    {
        "description": "Interview",
        "time": "2024-12-10"
    }
- Retrieve event without time range - this should return event with date range set to "today" at 00:00:00 to now

   **GET** http://localhost:8000/events

- Retrieve event with time range:
   
    **GET:** http://localhost:8000/events?datetime_format=%Y-%m-%dT%H:%M:%S&from_datetime=2024-12-14T00:00:00&to_datetime=2024-12-14T23:00:00

- Retrieve an event by ID with specified `datetime_format`
   
   **GET** http://localhost:8000/events/1?datetime_format=%d-%m


Refer to `test_views.py` and `test_e2e.py` for more details.
## Testings
To run all tests: `python manage.py test calendar_service_app/tests`

## Notes on further extensions
This is a lightweight and simple exercise, so I try to stay within the scope requirements. However, we could consider followings to productionise this:
1. Add authentication: ensure appropriate permission to access endpoints.
2. Rate limiting: Control the number of requests a client can make within a specific period of time using throttling.
3. If this is a heavy service with lots of data, we could use Asynchronous view when fetching events and pagination if required.
4. Database: lightweight SQLite3 is used but for production, we should have proper database such as PostgreSQL.
5. Hosting the service: More work required in order to host this.




