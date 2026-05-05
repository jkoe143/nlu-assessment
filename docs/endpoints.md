# API Endpoint Documentation

## 1. Get Property Information

**Request URL:** `http://127.0.0.1:5000/property/<address>/`

**Request Method:** `GET`

**Request Payload:** None

**Response Code:** `200 OK`

**Response Payload:**

```
{
    "address": string,
    "last_violation_date": string,
    "total_violation_count": number,
    "violations": [
        {
            "date": string,
            "code": string,
            "status": string,
            "description": string,
            "inspector_comments": string
        },
        ...
    ],
    "scofflaw": boolean
}
```

**Response Code:** `404 Not Found`

**Response Payload:**

```
{
    "error": string
}
```

## 2. Post Property Comment

**Request URL:** `http://127.0.0.1:5000/property/<address>/comments/`

**Request Method:** `POST`

**Request Payload:**

```
{
    "author": string,
    "comment": string
}
```

**Response Code:** `201 Created`

**Response Payload:**

```
{
    "message": string
}
```

**Response Code:** `400 Bad Request`

**Response Payload:**

```
{
    "error": string
}
```

## 3. Get Scofflaw Violations

**Request URL:** `http://127.0.0.1:5000/property/scofflaws/violations?since=<yyyy-mm-dd>`

**Request Method:** `GET`

**Request Payload:** None

**Response Code:** `200 OK`

**Response Payload:**

```
{
    "addresses": [
        string,
        string,
        ...
    ]
}
```

**Response Code:** `400 Bad Request`

**Response Payload:**

```
{
    "error": string
}
```
