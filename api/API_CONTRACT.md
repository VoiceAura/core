---

# API Contract

**Status:** Draft

**Version:** v1

This document defines the API contract between the frontend and backend applications.

It describes:

* API conventions;
* Resources and entities;
* Available endpoints;
* HTTP methods;
* Request and response formats;
* HTTP status codes;
* Naming conventions;
* Request/response examples per route.

> **Note:** Not all endpoints described in this document will necessarily be implemented in the initial MVP. This contract may evolve as project requirements are clarified.

---

## 1. API Conventions

### Base URL

`/api/v1`

**Example:**
`GET /api/v1/voices`

Future versions may use:
`/api/v2/voices`

### Content-Type

All requests and responses with a body must use:
`Content-Type: application/json`

**Exception:** Audio file upload (`VoiceSample`), which must use `multipart/form-data`.

### Authentication

All endpoints, unless otherwise specified, require authentication via header:
`Authorization: Bearer <token>`

A request without a valid token must return `401 Unauthorized`. A request with a valid token but insufficient permissions must return `403 Forbidden`.

### Pagination

Listing endpoints (`GET` on collections) support pagination via query params:
`GET /voices?page=1&page_size=20`

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `page` | integer | 1 | Page number |
| `page_size` | integer | 20 | Items per page (max. 100) |

The response of a paginated collection must include metadata (see section 4).

### Filtering and Sorting

When applicable, listing endpoints can accept filters and sorting via query params:
`GET /calls?status=completed&session_id=10&sort=-started_at`

* The `-` prefix in `sort` indicates descending order.
* Multiple filters are combined with `AND`.

---

## 2. HTTP Methods

The API follows REST style conventions.

| Method | Purpose |
| --- | --- |
| **GET** | Retrieve resources |
| **POST** | Create resources |
| **PUT** | Update resources (full replacement) |
| **PATCH** | Update resources (partial update) |
| **DELETE** | Remove resources |

**Examples:**

```http
GET    /voices
GET    /voices/{voice_id}

POST   /voices

PUT    /voices/{voice_id}
PATCH  /voices/{voice_id}

DELETE /voices/{voice_id}

```

> **Note:** The original contract only defined `PUT`. It is recommended to add `PATCH` for partial updates (e.g., changing only the status of a `VoiceProfile`), avoiding the need for the frontend to resend the full object.

---

## 3. Naming Conventions

### Route Naming

Routes must use:

* Plural nouns
* `kebab-case`

**Examples:**

* `/voices`
* `/voice-samples`
* `/organizations`
* `/knowledge-base`

Avoid verbs in REST resource paths.

❌ **Avoid:**

* `/create_voice`
* `/update_voice`
* `/delete_voice`
* `/get_voices`

The HTTP method already defines the action:

```http
POST   /voices
PUT    /voices/{voice_id}
DELETE /voices/{voice_id}
GET    /voices

```

### Python Function Naming

Inside the backend, route handler functions must use `snake_case`.

```python
def create_voice():
    ...

def get_voice():
    ...

def update_voice():
    ...

def delete_voice():
    ...

```

**Example:**

```python
@router.post("/voices")
def create_voice():
    ...

```

The route is RESTful: `POST /voices`

The Python function describes the action: `create_voice`

### Field Naming

The API uses: `snake_case`

**Example:**

```json
{
  "organization_id": 1,
  "voice_profile_id": 10,
  "created_at": "2026-08-13T10:00:00Z"
}

```

Dates and times always follow the ISO 8601 format in UTC (`Z` suffix).

---

## 4. HTTP Status Codes

The API must use consistent HTTP status codes.

| Status | Meaning | Example |
| --- | --- | --- |
| **200 OK** | Successful request | Resource retrieved |
| **201 Created** | Resource created successfully | Voice created |
| **204 No Content** | Successful request without response body | Resource deleted |
| **400 Bad Request** | Invalid request | Invalid payload |
| **401 Unauthorized** | Authentication required | Missing token |
| **403 Forbidden** | User without permission | Insufficient role |
| **404 Not Found** | Resource does not exist | Voice not found |
| **409 Conflict** | Resource conflict | Email already exists |
| **422 Unprocessable Content** | Validation failure | Invalid field in request |
| **429 Too Many Requests** | Rate limit exceeded | Rate limit hit |
| **500 Internal Server Error** | Unexpected server error | Server crash |

---

## 5. Standard Response Format

### Success Response — Single Resource

```json
{
  "id": 1,
  "name": "TAAG",
  "status": "active"
}

```

### Success Response — Paginated Collection

```json
{
  "items": [
    {
      "id": 1,
      "name": "TAAG"
    }
  ],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total_items": 57,
    "total_pages": 3
  }
}

```

### Error Response

Errors must follow a consistent structure.

```json
{
  "detail": "Voice profile not found"
}

```

Future versions may expand this format:

```json
{
  "error": {
    "code": "VOICE_NOT_FOUND",
    "message": "Voice profile not found"
  }
}

```

For validation errors (`422`), it is recommended to include the affected fields:

```json
{
  "detail": "Validation failed",
  "errors": [
    {
      "field": "name",
      "message": "This field is required"
    },
    {
      "field": "provider",
      "message": "Must be one of: elevenlabs, azure, custom"
    }
  ]
}

```

---

## 6. Entity Overview

The platform is organized around an `Organization`.

```text
Organization
│
├── Users
│
├── Voice Profiles
│     └── Voice Samples
│     └── Voice Embedding
│
├── Sessions
│
│   └── Calls
│
├── Tools
│
└── Knowledge Base

```

**Example:**

```text
TAAG
├── Users
├── Voices
├── Calls
├── Tools
└── Knowledge Base

```

---

## 7. Organization

Represents a company or organization using the platform.

**Examples:**

* TAAG
* Sonangol
* Company X

### Fields

| Field | Type | Description |
| --- | --- | --- |
| `id` | integer | Organization identifier |
| `name` | string | Organization name |
| `slug` | string | Unique URL-safe identifier |
| `status` | string | Organization status (`active`, `inactive`) |
| `created_at` | datetime | Creation date |
| `updated_at` | datetime | Last update |

### Routes

| Method | Endpoint | Handler | Description |
| --- | --- | --- | --- |
| **GET** | `/organizations` | `get_organizations` | List organizations |
| **GET** | `/organizations/{organization_id}` | `get_organization` | Get organization |
| **POST** | `/organizations` | `create_organization` | Create organization |
| **PUT** | `/organizations/{organization_id}` | `update_organization` | Update organization |
| **DELETE** | `/organizations/{organization_id}` | `delete_organization` | Delete organization |

---

## 8. User

Represents an authenticated person within an organization.

```text
Organization
      │
      └── Users

```

### Fields

| Field | Type |
| --- | --- |
| `id` | integer |
| `organization_id` | integer |
| `email` | string |
| `password_hash` | string |
| `first_name` | string |
| `last_name` | string |
| `role` | string |
| `created_at` | datetime |
| `updated_at` | datetime |

> `password_hash` must **never** be returned by the API.

### Routes

| Method | Endpoint | Handler |
| --- | --- | --- |
| **GET** | `/users` | `get_users` |
| **GET** | `/users/{user_id}` | `get_user` |
| **POST** | `/users` | `create_user` |
| **PUT** | `/users/{user_id}` | `update_user` |
| **DELETE** | `/users/{user_id}` | `delete_user` |

---

## 9. Roles

Defines a user's access level.

**Available Roles:**

* `Admin`
* `Developer`
* `Operator`
* `Viewer`

**Suggested Relationship:**

```text
User
 │
 └── Role

```

Permissions must be managed by the backend.

The frontend can use the role to control UI visibility, but the backend remains responsible for authorization (do not rely solely on the UI to restrict actions).

---

## 10. VoiceProfile

Represents a cloned voice.

The system must allow users to:

* Record or upload a voice sample;
* Generate a cloned voice;
* Store multiple voice profiles;
* Select a voice profile;
* Reuse the voice in future conversations.

### Fields

| Field | Type |
| --- | --- |
| `id` | integer |
| `organization_id` | integer |
| `name` | string |
| `provider` | string |
| `provider_voice_id` | string |
| `status` | string |
| `created_at` | datetime |
| `updated_at` | datetime |

**Possible values for `status`:**

* `processing`
* `ready`
* `failed`
* `disabled`

### Routes

| Method | Endpoint | Handler | Description |
| --- | --- | --- | --- |
| **GET** | `/voice-profiles` | `get_voices` | List voices |
| **GET** | `/voice-profiles/{voice_id}` | `get_voice` | Get voice |
| **POST** | `/voice-profiles` | `create_voice` | Create voice profile |
| **PUT** | `/voice-profiles/{voice_id}` | `update_voice` | Update voice |
| **DELETE** | `/voice-profiles/{voice_id}` | `delete_voice` | Remove voice |

---

## 11. VoiceSample

Represents an audio sample uploaded by the user.

A `VoiceSample` is not the cloned voice itself.

The audio sample should preferably:

* Be stored temporarily;
* Be encrypted when necessary;
* Be deleted when no longer needed.

### Fields

| Field | Type |
| --- | --- |
| `id` | integer |
| `voice_profile_id` | integer |
| `storage_reference` | string |
| `duration` | number |
| `format` | string |
| `created_at` | datetime |

**Relationship Example:**

```text
VoiceProfile
      │
      └── VoiceSamples

```

### Routes

| Method | Endpoint | Handler |
| --- | --- | --- |
| **POST** | `/voice-profiles/{voice_id}/samples` | `create_voice_sample` |
| **GET** | `/voice-profiles/{voice_id}/samples` | `get_voice_samples` |
| **DELETE** | `/voice-samples/{sample_id}` | `delete_voice_sample` |

---

## 12. VoiceEmbedding

Represents the embedding generated from one or more voice samples.

```text
Organization
│
└── VoiceProfile
      │
      ├── VoiceSample [1..N]
      │
      └── VoiceEmbedding [0..N or 1]

```

### Fields

| Field | Type |
| --- | --- |
| `id` | integer |
| `voice_profile_id` | integer |
| `storage_reference` | string |
| `provider` | string |
| `provider_reference` | string |
| `created_at` | datetime |
| `expires_at` | datetime |

The embedding itself does not necessarily need to be stored directly in the relational database.

The `storage_reference` can point to:

* Object Storage
* Vector Database
* Provider Storage
* Encrypted File Storage

No public routes are defined for `VoiceEmbedding` in this contract — it is an internal resource, automatically managed when a `VoiceSample` is processed.

---

## 13. Session

Represents the lifecycle of a conversation.

A session can use a selected voice profile.

### Fields

| Field | Type |
| --- | --- |
| `id` | integer |
| `organization_id` | integer |
| `user_id` | integer |
| `voice_profile_id` | integer |
| `channel` | string |
| `status` | string |
| `started_at` | datetime |
| `ended_at` | datetime |

**Available Channels:**

* `web`
* `phone`
* `whatsapp`

### Routes

| Method | Endpoint | Handler |
| --- | --- | --- |
| **GET** | `/sessions` | `get_sessions` |
| **GET** | `/sessions/{session_id}` | `get_session` |
| **POST** | `/sessions` | `create_session` |
| **PUT** | `/sessions/{session_id}` | `update_session` |
| **DELETE** | `/sessions/{session_id}` | `delete_session` |

---

## 14. Call

Represents an individual call or interaction associated with a session.

### Fields

| Field | Type |
| --- | --- |
| `id` | integer |
| `session_id` | integer |
| `organization_id` | integer |
| `channel` | string |
| `status` | string |
| `started_at` | datetime |
| `ended_at` | datetime |
| `duration` | number |

### Relationship with Session

A session can contain multiple calls.

```text
Session
│
├── Call 1
├── Call 2
└── Call 3

```

### Routes

| Method | Endpoint | Handler |
| --- | --- | --- |
| **GET** | `/calls` | `get_calls` |
| **GET** | `/calls/{call_id}` | `get_call` |
| **POST** | `/calls` | `create_call` |
| **PUT** | `/calls/{call_id}` | `update_call` |
| **DELETE** | `/calls/{call_id}` | `delete_call` |

---

## 15. Endpoint Summary

| Entity | GET | POST | PUT | DELETE |
| --- | --- | --- | --- | --- |
| **Organization** | `/organizations` | `/organizations` | `/organizations/{id}` | `/organizations/{id}` |
| **User** | `/users` | `/users` | `/users/{id}` | `/users/{id}` |
| **VoiceProfile** | `/voices` | `/voices` | `/voices/{id}` | `/voices/{id}` |
| **VoiceSample** | `/voices/{id}/samples` | `/voices/{id}/samples` | — | `/voice-samples/{id}` |
| **Session** | `/sessions` | `/sessions` | `/sessions/{id}` | `/sessions/{id}` |
| **Call** | `/calls` | `/calls` | `/calls/{id}` | `/calls/{id}` |

---

## 16. Request and Response Examples per Route

All examples assume the header `Authorization: Bearer <token>` and, when applicable, `Content-Type: application/json`.

### 16.1 Organization

#### GET /organizations

**Request:**
`GET /api/v1/organizations?page=1&page_size=20`

**Response 200 OK:**

```json
{
  "items": [
    {
      "id": 1,
      "name": "TAAG",
      "slug": "taag",
      "status": "active",
      "created_at": "2026-08-13T10:00:00Z",
      "updated_at": "2026-08-13T10:00:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total_items": 1,
    "total_pages": 1
  }
}

```

#### GET /organizations/{organization_id}

**Request:**
`GET /api/v1/organizations/1`

**Response 200 OK:**

```json
{
  "id": 1,
  "name": "TAAG",
  "slug": "taag",
  "status": "active",
  "created_at": "2026-08-13T10:00:00Z",
  "updated_at": "2026-08-13T10:00:00Z"
}

```

**Response 404 Not Found:**

```json
{
  "detail": "Organization not found"
}

```

#### POST /organizations

**Request:**

```json
{
  "name": "TAAG",
  "slug": "taag"
}

```

**Response 201 Created:**

```json
{
  "id": 1,
  "name": "TAAG",
  "slug": "taag",
  "status": "active",
  "created_at": "2026-08-13T10:00:00Z",
  "updated_at": "2026-08-13T10:00:00Z"
}

```

**Response 409 Conflict (slug already exists):**

```json
{
  "detail": "Organization slug already exists"
}

```

#### PUT /organizations/{organization_id}

**Request:**

```json
{
  "name": "TAAG SA",
  "slug": "taag",
  "status": "active"
}

```

**Response 200 OK:**

```json
{
  "id": 1,
  "name": "TAAG SA",
  "slug": "taag",
  "status": "active",
  "created_at": "2026-08-13T10:00:00Z",
  "updated_at": "2026-08-13T10:15:00Z"
}

```

#### DELETE /organizations/{organization_id}

**Request:**
`DELETE /api/v1/organizations/1`

**Response 204 No Content:** *(No body)*

---

### 16.2 User

#### GET /users

**Request:**
`GET /api/v1/users?organization_id=1&page=1&page_size=20`

**Response 200 OK:**

```json
{
  "items": [
    {
      "id": 5,
      "organization_id": 1,
      "email": "ana@taag.ao",
      "first_name": "Ana",
      "last_name": "Silva",
      "role": "Admin",
      "created_at": "2026-08-13T10:00:00Z",
      "updated_at": "2026-08-13T10:00:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total_items": 1,
    "total_pages": 1
  }
}

```

*(Note that `password_hash` is not returned in any response).*

#### GET /users/{user_id}

**Request:**
`GET /api/v1/users/5`

**Response 200 OK:**

```json
{
  "id": 5,
  "organization_id": 1,
  "email": "ana@taag.ao",
  "first_name": "Ana",
  "last_name": "Silva",
  "role": "Admin",
  "created_at": "2026-08-13T10:00:00Z",
  "updated_at": "2026-08-13T10:00:00Z"
}

```

#### POST /users

**Request:**

```json
{
  "organization_id": 1,
  "email": "ana@taag.ao",
  "password": "S3nhaForte!",
  "first_name": "Ana",
  "last_name": "Silva",
  "role": "Admin"
}

```

**Response 201 Created:**

```json
{
  "id": 5,
  "organization_id": 1,
  "email": "ana@taag.ao",
  "first_name": "Ana",
  "last_name": "Silva",
  "role": "Admin",
  "created_at": "2026-08-13T10:00:00Z",
  "updated_at": "2026-08-13T10:00:00Z"
}

```

**Response 422 Unprocessable Content:**

```json
{
  "detail": "Validation failed",
  "errors": [
    { "field": "email", "message": "Must be a valid email address" }
  ]
}

```

#### PUT /users/{user_id}

**Request:**

```json
{
  "first_name": "Ana",
  "last_name": "Silva Santos",
  "role": "Operator"
}

```

**Response 200 OK:**

```json
{
  "id": 5,
  "organization_id": 1,
  "email": "ana@taag.ao",
  "first_name": "Ana",
  "last_name": "Silva Santos",
  "role": "Operator",
  "created_at": "2026-08-13T10:00:00Z",
  "updated_at": "2026-08-13T11:00:00Z"
}

```

#### DELETE /users/{user_id}

**Request:**
`DELETE /api/v1/users/5`

**Response 204 No Content:** *(No body)*

---

### 16.3 VoiceProfile

#### GET /voices

**Request:**
`GET /api/v1/voices?status=ready&page=1&page_size=20`

**Response 200 OK:**

```json
{
  "items": [
    {
      "id": 10,
      "organization_id": 1,
      "name": "Voz Institucional TAAG",
      "provider": "elevenlabs",
      "provider_voice_id": "el_abc123",
      "status": "ready",
      "created_at": "2026-08-13T09:00:00Z",
      "updated_at": "2026-08-13T09:30:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total_items": 1,
    "total_pages": 1
  }
}

```

#### GET /voices/{voice_id}

**Request:**
`GET /api/v1/voices/10`

**Response 200 OK:**

```json
{
  "id": 10,
  "organization_id": 1,
  "name": "Voz Institucional TAAG",
  "provider": "elevenlabs",
  "provider_voice_id": "el_abc123",
  "status": "ready",
  "created_at": "2026-08-13T09:00:00Z",
  "updated_at": "2026-08-13T09:30:00Z"
}

```

#### POST /voices

Creates a voice profile (no samples associated yet — initial state becomes `processing` only after a `VoiceSample` is submitted and processed; during raw creation the status may start as `processing` or a backend-defined transient state).

**Request:**

```json
{
  "organization_id": 1,
  "name": "Voz Institucional TAAG",
  "provider": "elevenlabs"
}

```

**Response 201 Created:**

```json
{
  "id": 10,
  "organization_id": 1,
  "name": "Voz Institucional TAAG",
  "provider": "elevenlabs",
  "provider_voice_id": null,
  "status": "processing",
  "created_at": "2026-08-13T09:00:00Z",
  "updated_at": "2026-08-13T09:00:00Z"
}

```

**Response 422 Unprocessable Content:**

```json
{
  "detail": "Validation failed",
  "errors": [
    { "field": "provider", "message": "Must be one of: elevenlabs, azure, custom" }
  ]
}

```

#### PUT /voices/{voice_id}

**Request:**

```json
{
  "name": "Voz Institucional TAAG v2",
  "status": "disabled"
}

```

**Response 200 OK:**

```json
{
  "id": 10,
  "organization_id": 1,
  "name": "Voz Institucional TAAG v2",
  "provider": "elevenlabs",
  "provider_voice_id": "el_abc123",
  "status": "disabled",
  "created_at": "2026-08-13T09:00:00Z",
  "updated_at": "2026-08-13T12:00:00Z"
}

```

#### DELETE /voices/{voice_id}

**Request:**
`DELETE /api/v1/voices/10`

**Response 204 No Content:** *(No body)*

**Response 409 Conflict (voice in use by an active session):**

```json
{
  "detail": "Voice profile is in use by an active session and cannot be deleted"
}

```

---

### 16.4 VoiceSample

#### POST /voices/{voice_id}/samples

Audio sample upload. Uses `multipart/form-data`.

**Request:**

```http
POST /api/v1/voices/10/samples
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="sample-01.wav"
Content-Type: audio/wav

<binary audio data>
------WebKitFormBoundary--

```

**Response 201 Created:**

```json
{
  "id": 30,
  "voice_profile_id": 10,
  "storage_reference": "s3://voice-samples/org-1/voice-10/sample-30.wav",
  "duration": 42.5,
  "format": "wav",
  "created_at": "2026-08-13T09:05:00Z"
}

```

**Response 400 Bad Request (unsupported format):**

```json
{
  "detail": "Unsupported audio format. Allowed formats: wav, mp3, m4a"
}

```

#### GET /voices/{voice_id}/samples

**Request:**
`GET /api/v1/voices/10/samples`

**Response 200 OK:**

```json
{
  "items": [
    {
      "id": 30,
      "voice_profile_id": 10,
      "storage_reference": "s3://voice-samples/org-1/voice-10/sample-30.wav",
      "duration": 42.5,
      "format": "wav",
      "created_at": "2026-08-13T09:05:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total_items": 1,
    "total_pages": 1
  }
}

```

#### DELETE /voice-samples/{sample_id}

**Request:**
`DELETE /api/v1/voice-samples/30`

**Response 204 No Content:** *(No body)*

---

### 16.5 Session

#### GET /sessions

**Request:**
`GET /api/v1/sessions?user_id=5&status=active&page=1&page_size=20`

**Response 200 OK:**

```json
{
  "items": [
    {
      "id": 100,
      "organization_id": 1,
      "user_id": 5,
      "voice_profile_id": 10,
      "channel": "web",
      "status": "active",
      "started_at": "2026-08-13T14:00:00Z",
      "ended_at": null
    }
  ],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total_items": 1,
    "total_pages": 1
  }
}

```

#### GET /sessions/{session_id}

**Request:**
`GET /api/v1/sessions/100`

**Response 200 OK:**

```json
{
  "id": 100,
  "organization_id": 1,
  "user_id": 5,
  "voice_profile_id": 10,
  "channel": "web",
  "status": "active",
  "started_at": "2026-08-13T14:00:00Z",
  "ended_at": null
}

```

#### POST /sessions

**Request:**

```json
{
  "organization_id": 1,
  "user_id": 5,
  "voice_profile_id": 10,
  "channel": "web"
}

```

**Response 201 Created:**

```json
{
  "id": 100,
  "organization_id": 1,
  "user_id": 5,
  "voice_profile_id": 10,
  "channel": "web",
  "status": "active",
  "started_at": "2026-08-13T14:00:00Z",
  "ended_at": null
}

```

**Response 422 Unprocessable Content:**

```json
{
  "detail": "Validation failed",
  "errors": [
    { "field": "channel", "message": "Must be one of: web, phone, whatsapp" }
  ]
}

```

#### PUT /sessions/{session_id}

Typically used to end a session.

**Request:**

```json
{
  "status": "ended",
  "ended_at": "2026-08-13T14:20:00Z"
}

```

**Response 200 OK:**

```json
{
  "id": 100,
  "organization_id": 1,
  "user_id": 5,
  "voice_profile_id": 10,
  "channel": "web",
  "status": "ended",
  "started_at": "2026-08-13T14:00:00Z",
  "ended_at": "2026-08-13T14:20:00Z"
}

```

#### DELETE /sessions/{session_id}

**Request:**
`DELETE /api/v1/sessions/100`

**Response 204 No Content:** *(No body)*

---

### 16.6 Call

#### GET /calls

**Request:**
`GET /api/v1/calls?session_id=100&page=1&page_size=20`

**Response 200 OK:**

```json
{
  "items": [
    {
      "id": 500,
      "session_id": 100,
      "organization_id": 1,
      "channel": "web",
      "status": "completed",
      "started_at": "2026-08-13T14:00:05Z",
      "ended_at": "2026-08-13T14:05:00Z",
      "duration": 295
    }
  ],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total_items": 1,
    "total_pages": 1
  }
}

```

#### GET /calls/{call_id}

**Request:**
`GET /api/v1/calls/500`

**Response 200 OK:**

```json
{
  "id": 500,
  "session_id": 100,
  "organization_id": 1,
  "channel": "web",
  "status": "completed",
  "started_at": "2026-08-13T14:00:05Z",
  "ended_at": "2026-08-13T14:05:00Z",
  "duration": 295
}

```

#### POST /calls

**Request:**

```json
{
  "session_id": 100,
  "organization_id": 1,
  "channel": "web"
}

```

**Response 201 Created:**

```json
{
  "id": 500,
  "session_id": 100,
  "organization_id": 1,
  "channel": "web",
  "status": "in_progress",
  "started_at": "2026-08-13T14:00:05Z",
  "ended_at": null,
  "duration": null
}

```

#### PUT /calls/{call_id}

**Request:**

```json
{
  "status": "completed",
  "ended_at": "2026-08-13T14:05:00Z",
  "duration": 295
}

```

**Response 200 OK:**

```json
{
  "id": 500,
  "session_id": 100,
  "organization_id": 1,
  "channel": "web",
  "status": "completed",
  "started_at": "2026-08-13T14:00:05Z",
  "ended_at": "2026-08-13T14:05:00Z",
  "duration": 295
}

```

#### DELETE /calls/{call_id}

**Request:**
`DELETE /api/v1/calls/500`

**Response 204 No Content:** *(No body)*

---

## 17. Final Notes

* This document serves as the single source of truth between backend and frontend.
* Any changes to routes, fields, or response formats must be reflected here before (or during) implementation.
* It is recommended to maintain a changelog at the top of this document (or in a separate file) to track modifications across contract versions.
