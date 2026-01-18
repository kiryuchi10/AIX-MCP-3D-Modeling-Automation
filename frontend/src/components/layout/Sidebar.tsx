import { NavLink } from 'react-router-dom'
import { 
  LayoutDashboard, 
  Sparkles, 
  FolderOpen, 
  Box, 
  Settings 
} from 'lucide-react'
import { cn } from '@/utils/cn'

const navItems = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/generation', label: 'Generation', icon: Sparkles },
  { to: '/projects', label: 'Projects', icon: FolderOpen },
  { to: '/models', label: 'Models', icon: Box },
  { to: '/settings', label: 'Settings', icon: Settings },
]

export function Sidebar() {
  return (
    <aside className="w-64 bg-dark-100 border-r border-dark-300 flex flex-col">
      {/* Brand */}
      <div className="p-6 border-b border-dark-300">
        <h1 className="text-xl font-bold text-white">MCP 3D</h1>
        <p className="text-xs text-gray-400 mt-1">Modeling Automation</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === '/'}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-3 px-4 py-3 rounded-lg transition-colors',
                'hover:bg-dark-200 hover:text-white',
                isActive
                  ? 'bg-primary-600 text-white'
                  : 'text-gray-400'
              )
            }
          >
            <item.icon className="w-5 h-5" />
            <span className="font-medium">{item.label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-dark-300">
        <div className="px-4 py-2 text-xs text-gray-400 bg-dark-200 rounded-lg">
          API: localhost:8000
        </div>
      </div>
    </aside>
  )
}
