# LeoBBS X REST API

## Overview

This is a REST API layer for LeoBBS X forum system, enabling modern frontend applications (e.g., Vue.js 3 mobile SPA) to interact with the forum data.

## Quick Start

1. Access Swagger UI for interactive API testing:
   ```
   http://your-server/cgi-bin/swagger-ui.html
   ```

2. API base endpoint:
   ```
   http://your-server/cgi-bin/api.cgi
   ```

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `api.cgi` | GET | API info and available endpoints |
| `api.cgi?endpoint=forums` | GET | List all forums |
| `api.cgi?endpoint=forums&id=N` | GET | Get forum detail |
| `api.cgi?endpoint=topics&forum=N` | GET | List topics in a forum |
| `api.cgi?endpoint=topic&forum=N&id=M` | GET | Get topic posts |
| `api.cgi?endpoint=auth&action=login` | POST | Login (returns token) |
| `api.cgi?endpoint=auth&action=verify` | POST | Verify token |
| `api.cgi?endpoint=user&name=USERNAME` | GET | Get user profile |
| `api.cgi?endpoint=search&q=KEYWORD` | GET | Search topics |
| `api.cgi?endpoint=stats` | GET | Board statistics |
| `api.cgi?endpoint=online` | GET | Online users |

## Authentication

1. Login to get a token:
   ```
   POST api.cgi?endpoint=auth&action=login
   Body: username=xxx&******
   ```

2. Use token in subsequent requests:
   ```
   Header: X-API-Token: <token>
   ```
   Or as query parameter:
   ```
   api.cgi?endpoint=...&token=<token>
   ```

## Pagination

Topic and search endpoints support pagination:
- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 20, max: 50)

Response includes pagination info:
```json
{
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "total_pages": 8
  }
}
```

## CORS

All endpoints include CORS headers allowing cross-origin requests from any domain. Preflight OPTIONS requests are handled automatically.

## Character Encoding

The API attempts to convert GB2312/GBK encoded data to UTF-8 for JSON output. If the Perl `Encode` module is available, conversion is automatic. Response Content-Type is `application/json; charset=utf-8`.

## Files Structure

```
cgi-bin/
├── api.cgi              # Main API gateway (entry point)
├── api/                 # API handler modules
│   ├── auth.pl          # Authentication
│   ├── forums.pl        # Forum listing
│   ├── topics.pl        # Topic listing
│   ├── topic_detail.pl  # Topic posts
│   ├── user.pl          # User profiles
│   ├── search.pl        # Search
│   ├── stats.pl         # Board statistics
│   └── online.pl        # Online users
├── api-docs.json        # OpenAPI 3.0 specification
└── swagger-ui.html      # Swagger UI test page
```
