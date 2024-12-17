# calendar_service
## Instructions:
1.  Ensure Docker is up and running (e.g. `docker info` or `docker ps`)
2. Build docker image: `docker build -t calendar-service .`
3. Run: `docker run -p 8000:8000 calendar-service`

You can access at http://localhost:8000

# Endpoints
GET: http://localhost:8000/events

This will show a list of all events with date from defaults to today at 00:00:00 to now.

GET: http://localhost:8000/events?[datetime_format=<STRPTIME_FORMAT>][&][from_time=<DATE_TIME>][&][to_time=<DATE_TIME>]

Example:
http://localhost:8000/events?datetime_format=%Y-%m-%dT%H:%M:%S&from_datetime=2024-12-14T00:00:00&to_datetime=2024-12-14T23:00:00
This will show all event on 14/12/2024 from 00:00:00 to 23:00:00


GET: http://localhost:8000/events/<ID>[?datetime_format=<STRPTIME_FORMAT>]

Example: http://localhost:8000/events/1?datetime_format=%d-%m
This will show event id 1 with datetime format such as 14-12 in the response.


POST: http://localhost:8000/events

Example payload:
```json
{
	"description": "Interview",
	"time": "2024-12-10"
}
```
This will create an event.

Refer to test_views and test_e2e for more information.


