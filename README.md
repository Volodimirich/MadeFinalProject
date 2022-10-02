# MadeFinalProject
Made final project

## Why did we choose MongoDB?

- The used dataset is the mongodb dump, so it's easy to import.
- Thanks to the bson data storage format, there is no need to use an ORM, which means fewer components and lower development costs.
- Flexible document schemas, so there is no need to develop the database structure, while data validation remains.

## Database indexes:

- `papers._id` default index;
- `papers.title` to search papers by title;
- `papers.abstract` to search papers by abstract;
- `papers.keywords` to search papers by tags;
- `papers.authors.name` to search papers by authors;
- `papers.venue.raw` to search papers by venue names.

## Usage

1. `git clone https://github.com/Volodimirich/MadeFinalProject.git && cd MadeFinalProject`
2. `docker-compose up app`

- `http://127.0.0.1:8000/` get hello;
- `http://127.0.0.1:8000/papers` get all papers;
- `http://127.0.0.1:8000/docs` `Swagger UI`.
