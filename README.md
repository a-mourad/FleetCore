
Fleetcore – MVP

This repository contains a simple MVP for managing organisations, vehicles, drivers, and assignments.

Backend: FastAPI + SQLAlchemy Core + PostgreSQL

Frontend: React (Vite)

Auth: Token-based (JWT), minimal

Goal: Clean, functional implementation


**Requirements**

Docker & Docker Compose
Node.js
npm


**Backend – Run**
 

 - docker compose up --build

Backend available at:

http://localhost:8000


API documentation:

http://localhost:8000/docs

**Frontend – Run**

 - cd frontend
 - npm install
 - npm run dev

Frontend available at:

http://localhost:5173


**Integration Tests**

Integration tests validate API behavior against the database.
Run tests inside the backend container:

 - docker compose run backend pytest

**Tests cover:**

CRUD operations

Assignment rules

Error cases and validation



**Features**


 - Register / Login
 - User account (view & update)
 - Organisations with sub-organisations
 - Vehicles assigned to organisations
 - Drivers assigned to organisations
 - Assign / end driver to vehicle assignments
 - Assign / end   vehicle to driver assignments
 - Server-controlled assignment dates
 - Basic validation & error handling

**Business Rules & Assumptions**

The following decisions were made to keep the MVP simple and explicit:

An organisation can have sub-organisations (one level of hierarchy)

 - A sub-organisation cannot have its own children
 - Vehicles and drivers always belong to one organisation
 - Drivers can only be assigned to vehicles within the same organisation
 - A vehicle can have only one active driver at a time
 - An assignment is considered active when end_date is NULL
 - Assignment start_date and end_date are fully controlled by the server
 - Authentication is stateless (JWT); no sessions.
 - No pagination implemented
 - Minimal UI
