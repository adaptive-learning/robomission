# User Management

To get the current user, visit `/learn/api/users/current/`.
This endpoint always return a user - if a user hasn't been created in the current seesion yet, a new one (LazyUser) is created.
When a new user is created, a student entity for this user is created automatically as well.
User serializer provides a link to the associated student.
In the code, associdated student can be accessed simply by `user.student`.
