# TheraPlace
    *Personalised therapy for you*
______
  
## ABOUT
_______


This is a web API that helps clients looking for therapists connect with the said therapists.
The User can search and view profiles of the Therapists they wish and request for an appointment.
The project was inspired by the fact that it's very hard to access quality therapy services if someone
travels outside of their designated therapists location and at the same time can't access the hospital,
this application hopes to get users connected for an inhouse therapy sessions, a hospital appointment if applicable, or online consultation/directions.

## TEAM
____
This is a project I did alone with help from my peers and friends from other cohorts to finish off the specilaisation
on [ALX AFRICA](https://www.alxafrica.com/) webstack portfolio project for Backend specialisation.
You can check me out on socials:
- X - [Metrine Makana](https://x.com/makanametrine)
- Linkedin - [Metrine Makana](https:/www.linkedin.com/in/metrine-makana/)

## USAGE
____
- You can access this project by cloning it using:
```
https://github.com/Metrinenaliaka/TheraPlace_v1.git
```
- On your terminal activate the virtual environment using `. ./venv/bin/activate`
- Then run `python manage.py runserver` to start the server on localhost

after cloning you can use CLI or POSTMAN, here are the endpoints that can be used on another terminal with the server still running:

## API Endpoints
______
1. Use this for signing up `/api/v1/register/`, it uses http POST
2. Use this for logging in `/api/v1/login/`, it uses http POST and returns a Token
3. Use this for updatting profile details `/api/v1/update-profile/`, it uses http POST
4. Use this to view other users details `/api/v1/list-profiles/`, it uses http GET
5. Use this to view user own details `/api/v1/profile/{id}/`, it uses http GET
6. Use this to delete a profile `/api/v1/delete/`. it uses http DELETE

### examples
- Signup
  ```
  curl -X POST -H "Content-Type: application/json" -d '{ "username": "tee", "email": "tee@gmail.com", "password": "password", "role": "CL" }' http://127.0.0.1:8000/api/v1/register/
  ```
  It will return the newly created users data including the id, The role part has 2 options it can either be *CL* for client or *TH* for therapist
- Login
  ```
  curl -X POST -H "Content-Type: application/json" -d '{ "username": "tee", "email": "tee@gmail.com", "password": "password", "role": "CL" }' http://127.0.0.1:8000/api/v1/register/
  ```
  This one returns a token that will be used for Authentication in the other requests for this example only
  {"token":"6146371287d38683a0b5b8bee6955dba44894374"}
- Updating Profile
  ```
  curl -X POST -H "Content-Type: application/json" -H "Authorization: Token 6146371287d38683a0b5b8bee6955dba44894374" -d '{ "age": "2", "description": "This was done via curl", "condition": "Celebral Palsy" }' http://127.0.0.1:8000/api/v1/update-profile/
  ```
  This user is a CL so the updated details are as per the models in the code you can check them out if you register as CL or TH

- List Profiles
  ```
  curl -X GET -H "Content-Type: application/json" -H "Authorization: Token 6146371287d38683a0b5b8bee6955dba44894374" http://127.0.0.1:8000/api/v1/list-profiles/
  ```
  Here when the above user requests for profiles they ones that show up are those of Therapists since they are registered as Clients it will be opposite if they were Therapists
- List Own Profile
  ```
  curl -X GET -H "Content-Type: application/json" -H "Authorization: Token 6146371287d38683a0b5b8bee6955dba44894374" http://127.0.0.1:8000/api/v1/profile/5/
  ```
  here the user decides to list their own data, you need a PK which was generated when one registered

- Deleting a profile
  ```
  curl -X POST -H "Content-Type: application/json" -H "Authorization: Token f5c4a76795ca4b532f2295d62921a4ff53ac52a9" http://127.0.0.1:8000/api/v1/delete/
  ```
  A user deletes their account, they wont be users anymore

## Technologies
______
1. [Django Rest Framework](https://www.django-rest-framework.org/)
   I used it for writing the API's the authentication and also for Testing.

