import { Routes, Route } from "react-router-dom"

import Login from "./components/Login/login"
import Dashboard from "./components/Dashboard/Dashboard"

function App() {
  return (
    <>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </>
  )
}

export default App
