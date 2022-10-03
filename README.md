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

## Data scheme

We found the following fields and data models useful.

### Author model

| Field name | Type | Meaning |
|---|---|---|
| name | str | author's name |
| org | str | org's name |

### Venue model

| Field name | Type | Meaning |
|---|---|---|
| raw | str | venue's name |
| publisher | Optional(str) | publisher's name |

### Paper model

| Field name | Type | Meaning |
|---|---|---|
| title | str | paper name |
| authors | Optional[List[Author]] | lift of authors |
| venue | Venue | paper venue |
| year | int | year of writing |
| keywords | List[str] | list of keywords for the paper |
| n_citation | Optional[int] | citation count |
| lang | Optional[str] | paper language |
| doi | Optional[str] | paper doi |
| abstact | Optional[str] | paper abstract |

## Usage

1. `git clone https://github.com/Volodimirich/MadeFinalProject.git && cd MadeFinalProject`
2. `docker-compose up app`

- `http://127.0.0.1:8000/` get hello;
- `http://127.0.0.1:8000/papers` get all papers;
- `http://127.0.0.1:8000/docs` `Swagger UI` with other API methods.
