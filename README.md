All-in-one plant management app for hobbyists that have too many plants to name them. If you're the sort of person that propagates 10 plants at a time, sows exotic seeds and makes a note about it or you just want to share a subset of plants at a given time and are sick of keeping things in your phone's notes...this might be for you.

**CURRENT STATUS: **Back-end functional + basic front end. No features beyond adding/editing plants.

BACKEND:

This is a lightweight, RESTful API built using Flask and SQLite, designed to help manage simple data models—such as inventories,  task scheduling, collections, or lists of other items with full CRUD functionality. It includes a minimal but functional frontend integration and can be extended to handle different schemas and use cases.

FEATURES:
- SQLite-backed database with commented and customizable schema
- CRUD endpoints to add, read, update, and delete entries
- Data served as JSON for easy frontend integration
- Easily extendable: modify tables, fields, and queries as needed


API ENDPOINTS (editable)
- /api/greenhouse	GET	Fetch all items in the database
- /api/owned-plants	GET	Fetch items with quantity > 0
- /api/wishlist-plants	GET	Fetch items marked as wishlist
- /api/add-plant	POST	Add a new item (via JSON)
- /api/edit-plant	POST	Update an item (via JSON)
- /api/delete-plant	POST	Delete an item by ID


SETUP:
    1. Clone the repo
    2. Navigate to the backend directory
    3. Run the server: flask --app server run -p 5000

This will create an SQLite database (plants.db by default) with a basic table structure if one doesn’t exist.


CUSTOMIZATION:
This microservice is intended as a template as discussed. You are encouraged to:

    - Rename the database or table(s)
    - Change fields (e.g., status, wishlist, qty) in db.py
    - Modify or add new SQL queries
    - Add filtering endpoints
    - Reach out to me for help editing it


FRONTEND INTEGRATION:
This backend serves JSON responses that can be easily consumed by any frontend—React, Vue, plain JavaScript, etc. The current setup expects that the frontend will make fetch() calls to the listed endpoints and send/receive JSON.
