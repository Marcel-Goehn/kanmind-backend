
# API Reference

## Authentication

#### Creates a new user

```http
POST /api/registration/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `` | `` |  |

#### Request Body:

```json
{
  "fullname": "Example Username",
  "email": "example@mail.de",
  "password": "examplePassword",
  "repeated_password": "examplePassword"
}
```

#### Success Response: 201 Created

```json
{
  "token": "83bf098723b08f7b23429u0fv8274",
  "fullname": "Example Username",
  "email": "example@mail.de",
  "user_id": 123
}
```

#### User Login

```http
POST /api/login/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| ``      | `` |  |

#### Request Body:

```json
{
  "email": "example@mail.de",
  "password": "examplePassword"
}
```

#### Success Response: 200 OK

```json
{
  "token": "83bf098723b08f7b23429u0fv8274",
  "fullname": "Example Username",
  "email": "example@mail.de",
  "user_id": 123
}
```

## Board

#### Get List of boards, where the authenticated user is a member of the board of the owner

```http
GET /api/boards/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Headers -> Authorization`      | `string` | **Required**: Token <token> |

#### Success Response: 200 OK

```json
[
  {
    "id": 1,
    "title": "Projekt X",
    "member_count": 2,
    "ticket_count": 5,
    "tasks_to_do_count": 2,
    "tasks_high_prio_count": 1,
    "owner_id": 12
  },
  {
    "id": 1,
    "title": "Projekt Y",
    "member_count": 12,
    "ticket_count": 43,
    "tasks_to_do_count": 12,
    "tasks_high_prio_count": 1,
    "owner_id": 3
  }
]
```

#### Creates a new board. The authenticated user automatically will be added as the owner and can add himself to the members list.

```http
POST /api/boards/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Headers -> Authorization`      | `string` | **Required**: Token <token> |

#### Request Body:

```json
{
  "title": "Neues Projekt",
  "members": [
    12,
    5,
    54,
    2
  ]
}
```

#### Success Response: 201 Created

```json
{
  "id": 18,
  "title": "neu",
  "member_count": 4,
  "ticket_count": 0,
  "tasks_to_do_count": 0,
  "tasks_high_prio_count": 0,
  "owner_id": 2
}
```

#### Get information about a specific board. The authenticated user has to be a member or the owner of the board.

```http
GET api/boards/{board_id}/
```

| Parameter | Type   | Description |
| :-------- | :----- | :---------- |
| `Headers -> Authorization`      | `string` | **Required**: Token <token> |
| board_id    | number | **Required**: ID of the board |

#### Success Response: 200 OK

```json
{
  "id": 1,
  "title": "Projekt X",
  "owner_id": 12,
  "members": [
    {
      "id": 1,
      "email": "max.mustermann@example.com",
      "fullname": "Max Mustermann"
    },
    {
      "id": 54,
      "email": "max.musterfrau@example.com",
      "fullname": "Maxi Musterfrau"
    }
  ],
  "tasks": [
    {
      "id": 5,
      "title": "API-Dokumentation schreiben",
      "description": "Die API-Dokumentation für das Backend vervollständigen",
      "status": "to-do",
      "priority": "high",
      "assignee": null,
      "reviewer": {
        "id": 1,
        "email": "max.mustermann@example.com",
        "fullname": "Max Mustermann"
      },
      "due_date": "2025-02-25",
      "comments_count": 0
    },
    {
      "id": 8,
      "title": "Code-Review durchführen",
      "description": "Den neuen PR für das Feature X überprüfen",
      "status": "review",
      "priority": "medium",
      "assignee": {
        "id": 1,
        "email": "max.mustermann@example.com",
        "fullname": "Max Mustermann"
      },
      "reviewer": null,
      "due_date": "2025-02-27",
      "comments_count": 0
    }
  ]
}
```

#### Change members and/or title of the board. The authenticated user has to be a member or owner of the board

```http
PATCH api/boards/{board_id}/
```

| Parameter | Type   | Description |
| :-------- | :----- | :---------- |
| `Headers -> Authorization`      | `string` | **Required**: Token <token> |
| board_id    | number | **Required**: ID of the board |

#### Request Body:

```json
{
  "title": "Changed title",
  "members": [
    1,
    54
  ]
}
```

#### Success Response: 200 OK

```json
{
  "id": 3,
  "title": "Changed title",
  "owner_data": {
    "id": 1,
    "email": "max.mustermann@example.com",
    "fullname": "Max Mustermann"
  },
  "members_data": [
    {
      "id": 1,
      "email": "max.mustermann@example.com",
      "fullname": "Max Mustermann"
    },
    {
      "id": 54,
      "email": "max.musterfrau@example.com",
      "fullname": "Maxi Musterfrau"
    }
  ]
}
```

#### Delete a specific board. Only the owner of the board can delete it.

```http
DELETE api/boards/{board_id}/
```

| Parameter | Type   | Description |
| :-------- | :----- | :---------- |
| `Headers -> Authorization`      | `string` | **Required**: Token <token> |
| board_id    | number | **Required**: ID of the board |

#### Success Response: 204 No Content

#### Check if Email is already in use.

```http
GET api/email-check/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Headers -> Authorization`      | `string` | **Required**: Token <token> |

#### Response Success: 200 OK

```json
{
  "id": 1,
  "email": "max.mustermann@example.com",
  "fullname": "Max Mustermann"
}
```

## Tasks

#### Get all tasks that are assigned to the authenticated user.

```http
GET api/tasks/assigned-to-me/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Headers -> Authorization`      | `string` | **Required**: Token <token> |

#### Success Response: 200 OK

```json
[
  {
    "id": 1,
    "board": 1,
    "title": "Task 1",
    "description": "Beschreibung der Task 1",
    "status": "to-do",
    "priority": "high",
    "assignee": {
      "id": 13,
      "email": "marie.musterfraun@example.com",
      "fullname": "Marie Musterfrau"
    },
    "reviewer": {
      "id": 1,
      "email": "max.mustermann@example.com",
      "fullname": "Max Mustermann"
    },
    "due_date": "2025-02-25",
    "comments_count": 0
  },
  {
    "id": 2,
    "board": 12,
    "title": "Task 2",
    "description": "Beschreibung der Task 2",
    "status": "in-progress",
    "priority": "medium",
    "assignee": {
      "id": 13,
      "email": "marie.musterfraun@example.com",
      "fullname": "Marie Musterfrau"
    },
    "reviewer": null,
    "due_date": "2025-02-20",
    "comments_count": 0
  }
]
```

#### Get all tasks that the authenticated user has to review.

```http
GET api/tasks/reviewing/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Headers -> Authorization`      | `string` | **Required**: Token <token> |

#### Success Response: 200 OK

```json
[
  {
    "id": 1,
    "board": 1,
    "title": "Task 1",
    "description": "Beschreibung der Task 1",
    "status": "to-do",
    "priority": "high",
    "assignee": null,
    "reviewer": {
      "id": 1,
      "email": "max.mustermann@example.com",
      "fullname": "Max Mustermann"
    },
    "due_date": "2025-02-25",
    "comments_count": 0
  },
  {
    "id": 2,
    "board": 12,
    "title": "Task 2",
    "description": "Beschreibung der Task 2",
    "status": "in-progress",
    "priority": "medium",
    "assignee": {
      "id": 13,
      "email": "marie.musterfraun@example.com",
      "fullname": "Marie Musterfrau"
    },
    "reviewer": {
      "id": 1,
      "email": "max.mustermann@example.com",
      "fullname": "Max Mustermann"
    },
    "due_date": "2025-02-20",
    "comments_count": 0
  }
]
```

#### Create a new task. The authenticated user has to be a member of the board. The assignee and reviewer also have to be members of the board. If not chosen, the fields will return null. For the status field, the following values are allowed: to-do, in-progress, review and done. For the priority field, the following values are allowed: low, medium and high.

```http
POST api/tasks/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Headers -> Authorization`      | `string` | **Required**: Token <token> |

#### Request Body:

```json
{
  "board": 12,
  "title": "Code-Review durchführen",
  "description": "Den neuen PR für das Feature X überprüfen",
  "status": "review",
  "priority": "medium",
  "assignee_id": 13,
  "reviewer_id": 1,
  "due_date": "2025-02-27"
}
```

#### Success Response: 201 Created

```json
{
  "id": 10,
  "board": 12,
  "title": "Code-Review durchführen",
  "description": "Den neuen PR für das Feature X überprüfen",
  "status": "review",
  "priority": "medium",
  "assignee": {
    "id": 13,
    "email": "marie.musterfraun@example.com",
    "fullname": "Marie Musterfrau"
  },
  "reviewer": {
    "id": 1,
    "email": "max.mustermann@example.com",
    "fullname": "Max Mustermann"
  },
  "due_date": "2025-02-27",
  "comments_count": 0
}
```

#### Update a specific task. The authenticated user has to be a member of the board. Assignee and Reviewer also have to be members of the board.

```http
PATCH api/tasks/{task_id}/
```

| Parameter | Type   | Description |
| :-------- | :----- | :---------- |
| `Headers -> Authorization`      | `string` | **Required**: Token <token> |
| task_id    | number | **Required**: ID of the task |

#### Request Body:

```json
{
  "title": "Code-Review abschließen",
  "description": "Den PR fertig prüfen und Feedback geben",
  "status": "done",
  "priority": "high",
  "assignee_id": 13,
  "reviewer_id": 1,
  "due_date": "2025-02-28"
}
```

#### Success Response: 200 OK

```json
{
  "id": 10,
  "title": "Code-Review abschließen",
  "description": "Den PR fertig prüfen und Feedback geben",
  "status": "done",
  "priority": "high",
  "assignee": {
    "id": 13,
    "email": "marie.musterfraun@example.com",
    "fullname": "Marie Musterfrau"
  },
  "reviewer": {
    "id": 1,
    "email": "max.mustermann@example.com",
    "fullname": "Max Mustermann"
  },
  "due_date": "2025-02-28"
}
```

#### Deletes a task. Only the creator of the task or the owner of the board is allowed to delete it.

```http
DELETE api/tasks/{task_id}/
```

| Parameter | Type   | Description |
| :-------- | :----- | :---------- |
| `Headers -> Authorization`      | `string` | **Required**: Token <token> |
| task_id    | number | **Required**: ID of the task |

#### Success Response: 204 No Content

#### Get all comments, that belong to a specific task. The authenticated user has to be a member of the board, where the task belongs to.

```http
GET api/tasks/{task_id}/comments/
```

| Parameter | Type   | Description |
| :-------- | :----- | :---------- |
| `Headers -> Authorization`      | `string` | **Required**: Token <token> |
| task_id    | number | **Required**: ID of the task |

#### Success Response: 200 OK

```json
[
  {
    "id": 1,
    "created_at": "2025-02-20T14:30:00Z",
    "author": "Max Mustermann",
    "content": "Das ist ein Kommentar zur Task."
  },
  {
    "id": 2,
    "created_at": "2025-02-21T09:15:00Z",
    "author": "Erika Musterfrau",
    "content": "Ein weiterer Kommentar zur Diskussion."
  }
]
```

#### Create a new comment for a specific task. The authenticated user has to be a member of the board, where the task belongs to.

```http
POST api/tasks/{task_id}/comments/
```

| Parameter | Type   | Description |
| :-------- | :----- | :---------- |
| `Headers -> Authorization`      | `string` | **Required**: Token <token> |
| task_id    | number | **Required**: ID of the task |

#### Request Body:

```json
{
  "content": "Das ist ein neuer Kommentar zur Task."
}
```

#### Success Response: 201 Created

```json
{
  "id": 15,
  "created_at": "2025-02-20T15:00:00Z",
  "author": "Max Mustermann",
  "content": "Das ist ein neuer Kommentar zur Task."
}
```

#### Deletes a specific comment of a task. Only the creator of the comment can delete it.

```http
DELETE api/tasks/{task_id}/comments/{comment_id}/
```

| Parameter  | Type   | Description |
| :--------- | :----- | :---------- |
| `Headers -> Authorization`      | `string` | **Required**: Token <token> |
| task_id    | number | **Required**: ID of the task |
| comment_id | number | **Required**: ID of the comment |

#### Success Response: 204 No Content

