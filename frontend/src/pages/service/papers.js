import axios from 'axios'

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || ''
const baseUrl = `${BACKEND_URL || ''}/api/papers`

// TODO: after backend api finished, remove the mock API code
const isUseMock = import.meta.env.VITE_USE_MOCK || false

// --- Real API calls (when BACKEND_URL is provided) ---
const getAll = async () => {
  if (isUseMock) {
    return mockGetAll()
  }

  const response = await axios.get(baseUrl)
  return response.data
}

// --- Mock API (simulates real backend responses) ---
const _wait = (ms = 300) => new Promise((res) => setTimeout(res, ms))

const mockPapers = [
  {
    id: 'p1',
    title: 'Machine Learning Thesis 2024.pdf',
    size: '2.4 MB',
    citations: 67,
    timeAgo: '2 hours ago',
  },
  {
    id: 'p2',
    title: 'Climate Change Research.pdf',
    size: '1.8 MB',
    citations: 89,
    timeAgo: '5 hours ago',
  },
  {
    id: 'p3',
    title: 'Quantum Computing Paper.pdf',
    size: '1.2 MB',
    citations: 45,
    timeAgo: '1 day ago',
  },
  {
    id: 'p4',
    title: 'Neuroscience Study.pdf',
    size: '892 KB',
    citations: 34,
    timeAgo: '2 days ago',
  },
]

const mockGetAll = async () => {
  await _wait(250)
  // Return a deep copy to avoid accidental mutation from callers
  return JSON.parse(JSON.stringify(mockPapers))
}

export default { getAll }