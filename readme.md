# Tunity

### Introduction

Tunity is a job search web app where you can find jobs as a person or post job vacancy as a company.
In this modern world, as job opportunities diminished due to its competitiveness, landing a job would be very difficult.
This is when Tunity shines. With tunity, you could search and apply to all of the available jobs that suits you. All you need is
to register , upload your cv and you are all set to apply for jobs. In addition, companies can register as a company account and start open job vacancies.

### Distinctiveness and Complexity

I believe this project is distinct from the past projects. It is distinct from social network since you do not
connect with other people and interaction is just between user and companies regarding jobs appliance. Moreover,
This projects has nothing to do with transactions(buying/selling), therefore it is distinctive from e-commerce(project2).

In terms of complexity, it clearly satisfied the requirements as the project is build with django, models with complex relation are included,
upload file feature for resume,javascript is utilized, uses AJAX call, and Bootsrap gridsystem is used in all pages to ensure mobile-responsiveness.

### Files & Directories

- `media`- contains all of the files(resumes)
- `Tunity`
  - `models.py`- contains all of the models which has all of the user's data.
  - `forms.py` - contains upload file form
  - `urls.py`- contains all url paths(register,profile,job view,etc).
  - `views.py`- contains all of view functions for every url.
  - `static`
    - `tunity`- contains all of the image used, css file used, and javascript file.
  - `templates`
    - `tunity`
      `acceptance.html` - page for company to accept/decline job applications.
      `all.html` - all job vacancies in this website.
      `appliedPage.html` - page for personal user to see all of their applications.
      `find.html`- search page for jobs.
      `index.html`- home page.
      `jobPage.html` - details ofa job vacancy.
      `layout.html` - layout for the webpage.
      `login.html` - login page.
      `postJob.html`- page for company to create job vacancies.
      `profile.html` - profile page.
      `register.html`- page for user to choose what type of account they want to create.
      `registerPersonal.html` - register for a personal account.
      `registerStartup.html` - register for a startup/company account.

### How to run

- clone repository to a local directory

- open command line in newly created directory/repository

- initialize the DB - type in the command line : 'python manage.py makemigrations' then, 'python manage.py migrate'

- create a local admin account with 'python manage.py createsuperuser'

- clear the 'media' folder to start new.

- to start server: 'python manage.py runserver'
