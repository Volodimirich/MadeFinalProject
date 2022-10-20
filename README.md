# MadeFinalProject

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
| _id | ObjectId | paper id |
| title | str | paper name |
| authors | Optional[List[Author]] | lift of authors |
| venue | Optional[Venue] | paper venue |
| year | int | year of writing |
| keywords | Optional[List[str]] | list of keywords for the paper |
| fos | Optional[List[str]] | paper fields of study |
| n_citation | Optional[int] | citation count |
| lang | Optional[str] | paper language |
| doi | Optional[str] | paper doi |
| abstact | Optional[str] | paper abstract |

### Paper tags model

| Field name | Type | Meaning |
|---|---|---|
| _id | ObjectId | paper id |
| tag | int | paper tag |

## Installation

1. `git clone https://github.com/Volodimirich/MadeFinalProject.git`
2. `MADE_PATH=${PWD}/MadeFinalProject ./MadeFinalProject/scripts/download-main-data.sh` for downloading and processing dataset (~11min duration)
3. `cd MadeFinalProject`
4. Possible runs:
  - `docker-compose up app db test-seed tag-seed` run app with import test dataset;
  - `docker-compose up app db main-seed tag-seed` run app with import main dataset (need run 2. script);
  - add `mongo-express` to run mongodb web interface;
  - add `grafana` to run monitoring.


## Usage

- `http://127.0.0.1:8000` Homepage;
- `http://127.0.0.1:8000/docs` `Swagger UI` API methods.

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
