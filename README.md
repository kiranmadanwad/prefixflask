
```markdown
# IP Prefix Search API

This Flask application provides an API to search for IP addresses within known IP prefixes of various cloud service providers.

## API Documentation

### 1. Prefix Search API

#### 1.1. Search by Single IP Address

**Endpoint**: `/api/v1/prefixes`

**Method**: `GET`

**Parameters**:

- `ip` (query parameter): Single IP address to search.

**Example Request**:

```bash
curl -X GET "http://localhost:5000/api/v1/prefixes?ip=192.168.1.1"
```

**Example Response**:

```json
{
  "result": [
    {
      "subnet": "192.168.1.0/24",
      "provider": "Example Cloud",
      "ip": "192.168.1.1",
      "tags": ["Cloud", "Networking"]
    }
  ]
}
```

#### 1.2. Search by Multiple IP Addresses

**Endpoint**: `/api/v1/prefixes`

**Method**: `POST`

**Request Body**:

```json
{
  "ips": ["192.168.1.1", "10.0.0.1"]
}
```

**Example Request**:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"ips":["192.168.1.1","10.0.0.1"]}' "http://localhost:5000/api/v1/prefixes"
```

**Example Response**:

```json
{
  "result": [
    {
      "subnet": "192.168.1.0/24",
      "provider": "Example Cloud",
      "ip": "192.168.1.1",
      "tags": ["Cloud", "Networking"]
    },
    {
      "subnet": "10.0.0.0/8",
      "provider": "Another Cloud",
      "ip": "10.0.0.1",
      "tags": ["Cloud", "Testing"]
    }
  ]
}
```

## Docker Build and Docker Compose

### 1. Build Docker Image

```bash
docker build -t ip-prefix-search .
```

### 2. Run Using Docker

```bash
docker run -p 5000:5000 ip-prefix-search
```

### 3. Run Using Docker Compose

```bash
docker-compose up
```

The application will be accessible at [http://localhost:5000](http://localhost:5000).

## Dependencies

- Flask
- Flask-RESTful
- ipaddress
- json
- os


## Running Tests

### Prerequisites

Ensure you have the required Python packages installed:

```bash
pip install -r requirements.txt
```

### Run Tests

```bash
pytest
```
