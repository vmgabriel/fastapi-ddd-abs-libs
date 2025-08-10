# fastapi-ddd-abs-libs

With DDD recreate a API with Abstract Libraries, you can apply other libraries too

## CheckList

v0.1.0

- Check Tag v0.1.0

v0.2.0

- [ ] Do Todo
    - [X] Add App With Domain Layer
    - [X] Add Properties attribute for Board
    - [X] Add Service Layer
    - [X] Migrate new Table for Task
    - [X] Migrate new Table for History
    - [X] Migrate new Table for Desk
    - [X] Add Repository
    - [X] Add Command
    - [X] Check List of Tasks - **Require a Validation**
    - [X] Get Board
    - [X] Create Board
    - [X] Get With Details of Tasks and Members for Board
    - [X] Adjust Get By ID for Board Details
    - [X] Update Board Data
    - [X] Delete Board Data
    - [X] Not Show in Get By ID - List - Deleted Board
    - [X] Add Member in Board
    - [X] Remove Member in Board
    - [X] New Rules for Remove Member
        - [X] Should have least one member
        - [X] I shouldn't Remove Member if it's myself
    - [X] Modify Member Role in Board
    - [X] Add priority attribute to Task
    - [X] Get List of Task for each Board
    - [X] Create Task and Save History
    - [X] Get By ID Task And Get TaskHistory
    - [X] Update Task and Save History
    - [X] Delete Task and Save History
    - [X] Use of Email for Authenticate
    - [X] No repeat username and Email with Create User
    - [X] Send Updated At to Profile Get User
    - [ ] Paginator Not receive page - This require update request data for change of page
    - [ ] Paginator Not send has_next - This is required for iteration general
    - [ ] Update Profile for Add bio, and other attributes in profile of current user
    - [ ] Remove Contact Data in SQL and Configuration extend, no require all data and security layer
    - [ ] Add attribute for color in board
    - [ ] Add layer for Sync depends on the relation with the table and updated at rows in this table
- [ ] Global Backlog
    - [ ] Recovery Password
    - [ ] List of Users
        - [ ] Getting using username like
    - [ ] Change Permissions Online
        - [ ] Allow Add/Remove/Update Audiences in roles
        - [ ] Table Organization for Audiences
    - [ ] Validation for Logic Delete
        - [X] Check of Validation for Board
        - [ ] Check of Validation for User
    - [ ] Logic for Integration installation and save security
    - [X] Use of Email for Authenticate
    - [ ] Notifications for User
    - [ ] Integration of Events for background themes
    - [ ] Revision for Entrypoint Healthcheck
    - [ ] Revision for Entrypoint Example, maybe delete this