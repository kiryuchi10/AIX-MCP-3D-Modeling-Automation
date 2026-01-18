import { Routes, Route } from 'react-router-dom'
import { AppShell } from './components/layout/AppShell'
import { Dashboard } from './pages/Dashboard/Dashboard'
import { Generation } from './pages/Generation/Generation'
import { Projects } from './pages/Projects/Projects'
import { Models } from './pages/Models/Models'
import { Settings } from './pages/Settings/Settings'

function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/generation" element={<Generation />} />
        <Route path="/projects" element={<Projects />} />
        <Route path="/models" element={<Models />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </AppShell>
  )
}

export default App
