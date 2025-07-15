# fastapi-ddd-abs-libs

With DDD recreate a API with Abstract Libraries, you can apply other libraries too

## CheckList

- [x] Configure each thing in infra related to configure and use that implementation
- [x] Security Integration
- [x] Integration in Infra with DB
    - [x] Use UOW pattern
    - [x] Add Layer for Migrations
    - [x] Use Repository Pattern
    - [x] Use Mixin Pattern
    - [x] Inject that implementation
    - [x] Add base rules for Criteria Pattern
    - [x] Add CRUD Repository
    - [x] Implement CRUD in a Repository using Builder
    - [x] Inject Builder Execute Migrations Base
    - [x] Execute Migrations
- [x] Entrypoint HealthCheck
- [x] Integration of App Domain
    - [x] Integrate Entrypoints
    - [x] Integrate Repositories
- [X] Integration CLI
    - [X] Add Infra CLI Library
    - [X] Create Entrypoint CLI
    - [X] Create CLI for Generate Client
    - [X] Add in Domain
    - [X] Create First Super User
    - [x] Organize Code - PENDING
- [ ] Integration for Profile
    - [X] Challenge for Path Params - Query Params and Payload
    - [ ] Entrypoint for Generate Token
    - [ ] Entrypoint for Refresh Token
    - [ ] Entrypoint for Create Client
    - [ ] Entrypoint for Get Profile of Client