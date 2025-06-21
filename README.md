# refhandler

Refhandler - full chain of tools for writers and advisors of scientific articles and thesis, from managing the corpus of works and references to interfacing with LLM models for evaluating use of references and citations.


Plan:


Main
  - Query CorpusManager for jobs
  - Start processing jobs 
   
CorpusManager
  - Manage a database including:
  - ...WORKS: of the assessed works in the work directory, including year of publication, institution, faculty etc. information 
  - ...REFS: of the referenced works, including on whether work is available, has been downloaded to references directory
  - ...REFTEXT: of reference and citation texts including 1:1 relation to WORKS
  - ...TYPE: list of different reference types
  - ...REFREF: 1:N relation table between REFTEXT and REFS
  - ...REFCLASSIFIER: A classification system name and version
  - ...REFTYPE: TYPE classification of REFTEXT given by REFCLASSIFIER
  - ...LLM: LLM models and versions available 
  - ...ASSESSMENT: assessments of REFTEXT by specific LLM
  - Provide a job list for subsequent actions

LLMinterface
  - Provide interface to pose prompts to LLM models via API or to locally run models
  - Prompt injection recognition
  - Provide a list of LLM models with version info

ReferenceExtractor
  - Process through a given work and extract:
    - Necessary data to table WORKS    
    - The list of references and add to table REFS
    - Each reference and citation to table REFTEXT and REFREF and add an empty PDF annotation with REFTEXT row ID to add the annotation later
   
ReferenceClassifier
  - Given a reference text, classify it using all not yet deprecated classifiers, and return classifier version and result

ReferenceFetcher
  - Given a reference, try to obtain original PDF text and update REFS table

ReferenceAssessment
  - Given a REFTEXT, REFTYPE and REFS entry with available PDF, query available LLM's on the accuracy of the reference
  - Annotate WORKS pdf with the outcome
  - Update ASSESSMENT entry with results
  - 



