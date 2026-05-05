# NLU Backend Assessment

Uses two real-world Chicago city datasets:

- [Building Violations](https://data.cityofchicago.org/Buildings/Building-Violations/22u3-xenr)
- [Building Code Scofflaw List](https://data.cityofchicago.org/Buildings/Building-Code-Scofflaw-List/crg5-4zyp)

## Tech Stack

- **Language:** Python 3.11
- **Framework:** Flask - chosen due to familiarity and explicit control over request/response handling. Also matched the small scope of this project
- **Database:** PostgreSQL - chosen because it is industry standard, handles relational data well, and supports the JOIN operations this project relies on
- **Adapter:** psycopg2 - required for database interaction since ORM is not allowed

## Setup Instructions

### 1. Clone the repository and navigate to the project folder

### 2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file in the project root

```
DB_NAME=nlu_assessment
DB_USER=postgres
DB_PASSWORD=your_postgres_password_here
DB_HOST=localhost
DB_PORT=5432
```

### 5. Create the PostgreSQL database

```bash
psql -U postgres
```

```sql
CREATE DATABASE nlu_assessment;
\q
```

### 6. Run the table creation script

```bash
psql -U postgres -d nlu_assessment -f database/createSchema.sql
```

### 7. Run the ingestion script

```bash
python etl/ingest.py
```

Expected output:

```
Ingesting violations dataset...
Ingesting scofflaws dataset...
Ingestion complete.
```

### 8. Start the API

```bash
python app.py
```

The API will be available at `http://127.0.0.1:5000`

## Database Design

Three tables were created:

**violations** - stores building violation records from January 1, 2024 onward.
Fields `id`, `date`, `code`, `status`, `description`, `inspector_comments`, and
`address` were ingested. `id` serves as the primary key. `address` and `date` are
marked `NOT NULL` since they are required for the query logic. Indexed on `address`
and `date` for improved query performance.

**scofflaws** - stores properties flagged as priority buildings with serious and
chronic code violations. Fields `record_id` and `address` were ingested. `record_id`
serves as the primary key. Indexed on `address` for improved query performance.

**comments** - stores user submitted comments tied to a property address. `id` is
auto generated and serves as the primary key. `datetime` is server generated at time
of insert. `author`, `address`, and `comment` are provided by the user via POST request.

Address columns are normalized to lowercase and trimmed at both ingestion time and
query time to ensure safe JOINs across tables.

## API Endpoints

See `docs/endpoints.md` for full request and response documentation.

### API References

- `GET /property/<address>/` - get date of last violation, total violation count, array of all violations, and scofflaw status for an address
- `POST /property/<address>/comments/` - submit a comment for an address
- `GET /property/scofflaws/violations?since=<yyyy-mm-dd>` - get scofflaw addresses with violations on or after a date

## Testing

Start the API with `python app.py` then use Postman to test endpoints.

**Example requests:**

GET a property:
`http://127.0.0.1:5000/property/7120 s rockwell st/`

POST a comment:
`http://127.0.0.1:5000/property/7120 s rockwell st/comments/`

```json
{
  "author": "Jason",
  "comment": "This building looks rat infested!"
}
```

GET scofflaw violations:
`http://127.0.0.1:5000/property/scofflaws/violations?since=2024-01-01`
