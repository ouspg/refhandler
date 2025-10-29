import { Routes, Route } from "react-router-dom"

import Login from "./pages/Login/login"
import Dashboard from "./pages/Dashboard/Dashboard"
import ProtectedRoute from "./components/routes/protectedRoute"

function App() {
  return (
    <>
      <Routes>
        <Route element={<ProtectedRoute requireAuth={false} />}>
          <Route path="/login" element={<Login />} />
        </Route>
        
        <Route element={<ProtectedRoute requireAuth={true} />}>
          <Route path="/dashboard" element={<Dashboard />} />
        </Route>
      </Routes>
    </>
  )
}

export default App
