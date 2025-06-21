# refhandler

Refhandler - full chain of tools for writers and advisors of scientific articles and thesis, from managing the corpus of works and references to interfacing with LLM models for evaluating use of references and citations.


Plan:


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



