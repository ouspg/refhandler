export const mockHeader = {
  title: 'FinalProject_Analysis_final.pdf',
};

export const mockPdf = {
  pages: 15,
  words: 8136,
};

export const mockStatistics = {
  overall: 8,
  groups: [
    { label: 'Missing Quotations', percent: 1 },
    { label: 'Missing Citation', percent: 0 },
    { label: 'Wrong Quotations', percent: 1 },
    { label: 'Wrong Citation', percent: 0 },
  ],
};

export const mockSources = [
  {
    id: 1,
    type: 'Internet',
    title: 'deepblue.lib.umich.edu',
    matchedWords: 101,
    percent: 1,
  },
  {
    id: 2,
    type: 'Internet',
    title: 'escritura.cua.uam.mx',
    matchedWords: 39,
    percent: 0.5,
  },
  {
    id: 3,
    type: 'Submitted works',
    title: 'University of Adelaide',
    matchedWords: 25,
    percent: 0.3,
  },
  {
    id: 4,
    type: 'Submitted works',
    title: 'University of Cape Town',
    matchedWords: 25,
    percent: 0.2,
  },
];
