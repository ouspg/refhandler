# refhandler

Refhandler - full chain of tools for writers and advisors of scientific articles and thesis, from managing the corpus of works and references to interfacing with LLM models for evaluating use of references and citations.

## Installation

### Linux

### Option A: CLI

Install [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/)

### Option B: Docker Desktop

Install [Docker Desktop for Linux](https://docs.docker.com/desktop/setup/install/linux/)

### Windows

Install [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/)

### MacOS

Install [Docker Desktop for MacOS](https://docs.docker.com/desktop/setup/install/mac-install/)

## Deployment

1. Clone the Refhandler repository
2. (Optional) Change `POSTGRES_PASSWORD` in .env file
3. Open a terminal in the project root folder
4. Run the command `docker-compose up`
5. Open <http://localhost:8000/> in your browser

## Refhandler components

- [Frontend](frontend): #TODO
- [Test Frontend](test_frontend): Developer frontend for testing the backend and process containers
- [Postgres](postgres): Relational SQL database
- [compose.yaml](compose.yaml): Configuration and deployment of project's docker containers
- [.env](.env): Project configuration

## Plan:

Main

- Query CorpusManager for jobs
- Start processing jobs

DatabaseWrapper

- Keep all database -related code in one place to permit database migration depending on need
- Start with SQLite?

CorpusManager

- Manage a database including:
- ...WORKS: of the assessed works in the work directory, including year of publication, institution, faculty etc. information 
- ...REFS: of the referenced works, including on whether work is available, has been downloaded to references directory
- ...REFTEXT: of reference and citation texts including 1:1 relation to WORKS
- ...REFTAXONOMY: a taxonomy of reference types, including a description of the taxonomy
- ...TYPE: reference types (N:1) related to specific TAXONOMY
- ...REFREF: N:N relation table between REFTEXT and REFS
- ...REFTYPE: TYPE classification of REFTEXT given by LLM model for specific REFTAXONOMY
- ...LLM: LLM models and versions available 
- ...ASSESSMENT: assessments of REFTEXT by specific LLM
- Provide a job list for subsequent actions

LLMinterface

- Provide interface to pose prompts to LLM models via API or to locally run models
- Prompt injection recognition :P
- Provide a list of LLM models with version info

ReferenceExtractor

- Process through a given work and extract:
  - Necessary data to table WORKS
  - The list of references and add to table REFS
  - Each reference and citation to table REFTEXT and REFREF and add an empty PDF annotation with REFTEXT row ID to add the annotation later

ReferenceClassifier

- Given a reference text, query available LLM's to classify the reference according to each available REFTAXONOMY to TYPE
- Annotate WORKS pdf with the outcome

ReferenceFetcher

- Given a reference, try to obtain original PDF text and update REFS table

ReferenceAssessment

- Given a REFTEXT, REFTYPE and REFS entry with available PDF, query available LLM's on the accuracy of the reference
- Annotate WORKS pdf with the outcome
- Update ASSESSMENT entry with results

Statistics

- Provide statistics and export CSV results

## Development project plan:

```graphviz
digraph G {
  rankdir="TB"; // Top to bottom
  node [shape=box style=filled fontsize=10];
  
  node [shape=circle style=filled];
  subgraph cluster_legend {
    label="Projects (by color)";
    rank=min;
    key1 [label="INFRA", fillcolor=lightblue];
    key2 [label="WEB", fillcolor=lightgreen];
    key3 [label="SQL", fillcolor=lightgray];
    key4 [label="PROSESSIT", fillcolor=khaki];
  }
  
  I0 [label="Dockerfile\nfor Apache\nand SQL", fillcolor=lightblue];
  I1 [label="Varmuuskopiointi-\nkontti ja prosessi\n(cron)", fillcolor=lightblue];
  I2 [label="SQL-\nvarmuuskopiointi", fillcolor=lightblue];
  I3 [label="Dockerfilepäivitys\ntiedostoprosessi", fillcolor=lightblue];
  I4 [label="Dockerfilepäivitys\nPDF-käsittely", fillcolor=lightblue];
  I5 [label="Dockerfilepäivitys\nKehotetunnistus", fillcolor=lightblue];
  I6 [label="Dockerfilepäivitys\nViittausten\nkategorisointi", fillcolor=lightblue];
  I7 [label="Dockerfilepäivitys\nLähteiden\nkategorisointi", fillcolor=lightblue];
  I8 [label="Dockerfilepäivitys\nLähteiden haku", fillcolor=lightblue];
  I9 [label="Dockerfilepäivitys\nUusien teesien\nhaku", fillcolor=lightblue];
  I10 [label="Dockerfilepäivitys\nVastaavuusarviointi", fillcolor=lightblue];
  I11 [label="Dockerfilepäivitys\nTilastointiajot", fillcolor=lightblue];

  S0 [label="SQL Docker\n+\ntietokannan\nalustus", fillcolor=lightgray];
  S1 [label="SQL: alustus\nvarmuuskopiolla\nkäynnistettäessä", fillcolor=lightgray];
  S2 [label="SQL:\nteesi", fillcolor=lightgray];
  S3 [label="SQL:\ntekstit\nlähteet", fillcolor=lightgray];

  W0 [label="Apache\n+\nhelloworld", fillcolor=lightgreen];
  W1 [label="Tiedoston\nlataus", fillcolor=lightgreen];
  W2 [label="Tiedostojen\nlistaus\nja etenemistilanne", fillcolor=lightgreen];
  W3 [label="Tilastonäkymä ja\ntilastoja tiedostoista", fillcolor=lightgreen];
  
  I3 [label="Tiedosto-\njärjestelmä", fillcolor=lightblue];
  P0 [label="Kansion tiedostot\n tauluun\nkäsittelylistalle", fillcolor=khaki];
  P1 [label="Tekstit ja lähteet\nulos tiedostosta", fillcolor=khaki];
  P2 [label="Kehotetunnistus:\nepäilyttävien\ntekstien\ntunnistus", fillcolor=khaki];
  P3 [label="Viittausten\nkategorisointi", fillcolor=khaki];
  P4 [label="Lähteiden\nkategorisointi", fillcolor=khaki];
  P5 [label="Lähteiden\nhaku", fillcolor=khaki];
  P6 [label="Uusien teesien\npollaus ja\nnouto", fillcolor=khaki];
  P7 [label="Vastaavuuden\narviointi", fillcolor=khaki];
  P8 [label="Tilastointiajot", fillcolor=khaki];
  
  // Cross-project dependencies
  W0 -> I0;
  S0 -> I0;
  I1 -> I2;
  S0 -> I2;
  I1 -> I0;
  I0 -> S1;
  I2 -> S1;
  W0 -> W1;
  I3 -> W1;
  S1 -> P0;
  W1 -> P0;
  P0 -> P1;
  P1 -> P2;
  P2 -> P3;
  P3 -> P4;
  P4 -> P5;
  P5 -> P6;
  P6 -> P7;
  S0 -> S2;
  S2 -> W1;
  W1 -> W2;
  W2 -> W3;
  S3 -> P1;
  P0 -> I3;
  P1 -> I4;
  P2 -> I5;
  P3 -> I6;
  P4 -> I7;
  P5 -> I8;
  P6 -> I9;
  P7 -> I10;
  P8 -> I11;
  W3 -> P8;
}
```
