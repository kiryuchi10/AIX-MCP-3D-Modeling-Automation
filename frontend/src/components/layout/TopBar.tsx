import { Plus, HelpCircle } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { Button } from '../ui/Button'

export function TopBar() {
  const navigate = useNavigate()

  return (
    <header className="h-16 bg-dark-100 border-b border-dark-300 px-6 flex items-center justify-between">
      <div>
        <h2 className="text-lg font-semibold text-white">Workspace</h2>
        <p className="text-xs text-gray-400">Upload → Scale → Extract → Script → Run</p>
      </div>
      <div className="flex items-center gap-3">
        <Button
          variant="primary"
          size="sm"
          onClick={() => navigate('/generation')}
        >
          <Plus className="w-4 h-4 mr-2" />
          New Project
        </Button>
        <Button variant="ghost" size="sm">
          <HelpCircle className="w-4 h-4 mr-2" />
          Help
        </Button>
      </div>
    </header>
  )
}
