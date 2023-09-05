# Project description:  
This is an educational project on Django Rest Framework and group work on the project.  

The project YaMDb collects user's reviews on products(TITLES). The titles themselves are not stored in YaMDb.

The titles are divided into categories. 

A title can be assigned a genre from the predefined list.

Only the administrator can add titles, categories and genres.

Grateful or indignant users leave text reviews for the titles and rate the titles.

A user can leave only one review per title.

Users can leave comments on reviews.

Only authenticated users can add reviews, comments and rate.

Used libraries:  
- [Django                        3.2.16](https://docs.djangoproject.com/en/3.2/)  
- [djangorestframework           3.12.4](https://www.django-rest-framework.org/)  
- [djangorestframework-simplejwt 5.2.2](https://django-rest-framework-simplejwt.readthedocs.io/)
- [django-filter                 2.4.0](https://django-filter.readthedocs.io/en/stable/)
---
# Installation:
Clone the repository and change into it on the command line:

	git clone https://github.com/mityay36/api_yamdb/
 
 Create and activate virtual environment:
 
	cd api_yamdb
	python3 -m venv env
	source env/bin/activate
 
Install dependencies from a file requirements.txt:

	python3 -m pip install --upgrade pip
	pip install -r requirements.txt
 
Perform migrations:
 	
	python3 manage.py migrate

Run project:

	python3 manage.py runserver
---
# Full API docs located http://127.0.0.1:8000/redoc/ after run project
### Some examples of API requests:

	###GET CATEGORIES
	GET http://127.0.0.1:8000/api/v1/categories/

	Response:
	{
		"count": 0,
		"next": "string",
		"previous": "string",
		"results": [
		  {
			  "name": "string",
			  "slug": "string"
		  }
		]
	}

---
	###GET GENRES
	GET http://127.0.0.1:8000/api/v1/genres/

	Response:
	{
		"count": 0,
		"next": "string",
		"previous": "string",
		"results": [
		  {
			  "name": "string",
			  "slug": "string"
		  }
		]
	}

---
	###GET TITLES
	GET http://127.0.0.1:8000/api/v1/titles/

	Response:
	{
		"count": 0,
		"next": "string",
		"previous": "string",
		"results": [
		  {
		  "id": 0,
		  "name": "string",
		  "year": 0,
		  "rating": 0,
		  "description": "string",
		  "genre": [
		    {
		      "name": "string",
		      "slug": "string"
		    }
		  ],
		  "category": 
		    {
		      "name": "string",
		      "slug": "string"
		    }
		  }
	  ]
	}

---
	###GET REVIEWS
	GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/

	Response:
	{
		"count": 0,
		"next": "string",
		"previous": "string",
		"results": [
		  {
		  "id": 0,
		  "text": "string",
		  "author": "string",
		  "score": 1,
		  "pub_date": "date"
		  }
	  ]
	}

---
	###ADD REVIEW
	POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
	Content-Type: application/json
	Authorization: Token your_token
	
	{
	    "text": "review for title title_id",
	    "score": 7
	}

---
	###GET COMMENTS
	GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/

	Response:
	{
		"count": 0,
		"next": "string",
		"previous": "string",
		"results": [
		  {
		  "id": 0,
		  "text": "string",
		  "author": "string",
		  "pub_date": "date"
		  }
	  ]
	}

---
	###ADD COMMENTS
	POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
	Content-Type: application/json
	Authorization: Token your_token
 
	{
	    "text": "comment for review review_id"
	}

---
# Authors
- [https://github.com/yandex-praktikum/](https://github.com/yandex-praktikum/)
- [https://github.com/mityay36/](https://github.com/mityay36)
- [https://github.com/NikitaDesyatov/](https://github.com/NikitaDesyatov)
- [https://github.com/smishin87/](https://github.com/smishin87)

