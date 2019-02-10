# iDoor


## About

iDoor: a vulnerable web app based on [insecure direct object references](https://www.owasp.org/index.php/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet) (IDOR). Proper access control has been left out so
that an insecure direct object reference can be exploited.


## Goal

Your goal is to see what the secret 6th door looks like.


## Hints

See what the /doors/index page says when logged in and out

See what the URLs look like when viewing each door


## User Accounts:

| User  | Password|
|-------|---------|
|admin  | secret  |
|foo    | bar     |


## Solution:

Notice on the /doors/index page, when not logged in, you see that the admin has access to the secret
6th door.

When you log in and view the /doors/index page, you are greeted with 5 buttons to view the doors.
When you click on one, you are taken to /doors/number. To view the secret 6th door, just change the
url to /doors/6.
