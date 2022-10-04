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
| venue | Optional[Venue] | paper venue |
| year | int | year of writing |
| keywords | Optional[List[str]] | list of keywords for the paper |
| n_citation | Optional[int] | citation count |
| lang | Optional[str] | paper language |
| doi | Optional[str] | paper doi |
| abstact | Optional[str] | paper abstract |

## Usage

1. `git clone https://github.com/Volodimirich/MadeFinalProject.git`
2. `MADE_PATH=${PWD}/MadeFinalProject ./MadeFinalProject/scripts/download-main-data.sh` for downloading and processing dataset (~11min duration)
3. `cd MadeFinalProject && docker-compose up` and wait until `mongo-main-seed` containter complete import (~12min duration)

- `http://127.0.0.1:8000/` get hello;
- `http://127.0.0.1:8000/papers` get all papers;
- `http://127.0.0.1:8000/docs` `Swagger UI` with other API methods.

## Monitoring and logging
Prometheus was chosen as the monitoring system. 

Prometheus can be founded on next address - `http://127.0.0.1:9090`

The following command is required to verify access to the database:
`http://127.0.0.1:9090/targets?search=`. After redirecting you should
 check availability of `http://mongodb-exporter:9216/metrics`.

As a dashboard Grafana was chosen. To use it you should do next steps:
1. Go to `http://127.0.0.1:3000` (login: _admin_, password: _pass@123_).
2. In opened window go to Datasources -> Prometheus. In the new window set next url - `http://prometheus:9090`. After 
that press on **Save & test** button and after the success message appeared press on **Back** button.
3. In left panel choose Dashboard, in the pop-up window select **+Import** button. In new window set and load 
next code - **2583**. And after that select prometheus and press andother **load** button.
