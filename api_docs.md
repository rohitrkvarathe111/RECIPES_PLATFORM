
# 🍴 Recipe API Documentation
This project provides user authentication, recipe management, and rating APIs.

## Authentication & User APIs
Base URL: "_________"
### Register
- Endpoint: POST /api/auth/register/
- Description: Register a new user.
- Request Body: 
```bash
{
  "username": "rohit",
  "email": "rohit@varathe.com",
  "password": "Rohit123",
  "role": "customer"   // or "seller"
}
```
### Login (Obtain Token)

- Endpoint: POST /api/auth/token/
- Description: Obtain JWT access and refresh tokens.
- Request Body:

```bash
{
  "username": "rohit",
  "password": "Rohit123"
}

```

### Refresh Token

- Endpoint: POST /api/auth/token/refresh/

- Request Body:
```bash
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR..."
}

```


### Get Current User

- Endpoint: GET /api/auth/me/
- Description: Returns details of the logged-in user.

- Headers: Authorization: Bearer <access_token>


---

## Recipe APIs

### List Recipes

- Endpoint: GET /api/recipes/

- Description: Returns a list of recipes with average ratings.

- Headers: Authorization: Bearer <access_token>

### Retrieve Recipe

- Endpoint: GET /api/recipes/{id}/

- Headers:
Authorization: Bearer <access_token>

### Create Recipe (Sellers Only)

- Endpoint: POST /api/recipes/

- Headers:
Authorization: Bearer <access_token>

- Request Body:
```bash
{
  "name": "New Dish",
  "description": "Delicious and spicy",
  "image": "base64-encoded-image"
}

```


### Update Recipe (Sellers Only)

- Endpoint: PUT /api/recipes/{id}/

- Headers:
Authorization: Bearer <access_token>

- Request Body:
```bash
{
  "name": "Updated Dish",
  "description": "Now even tastier!"
}

```

### Delete Recipe (Sellers Only, Owner Only)

- Endpoint: DELETE /api/recipes/{id}/
- Headers:
Authorization: Bearer <access_token>

---

## Rating APIs
### List Ratings

- Endpoint: GET /api/ratings/
- Query Params: ?recipe={id}
- Headers: Authorization: Bearer <access_token>

## Create Rating (Customers Only)
- Endpoint: POST /api/ratings

- Headers: Authorization: Bearer <access_token>

Request Body:
```bash
{
    "recipe": 9,
    "score": 3,
    "comment": "AVG!"
}
```


# Validation Rules:

- Score must be between 1–5.
- A seller cannot rate their own recipe.
- A user cannot rate the same recipe more than once.



