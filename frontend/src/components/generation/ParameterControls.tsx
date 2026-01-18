import { Check } from 'lucide-react'
import { cn } from '@/utils/cn'

interface ParameterControlsProps {
  selectedTool: string
  onToolChange: (tool: string) => void
  quality: string
  onQualityChange: (quality: string) => void
  exportFormat: string
  onExportFormatChange: (format: string) => void
  disabled?: boolean
  className?: string
}

const tools = [
  {
    id: 'blender',
    name: 'Blender',
    description: 'Free, open-source 3D creation suite',
    capabilities: ['Modeling', 'Animation', 'Rendering'],
  },
  {
    id: 'rhino',
    name: 'Rhino 3D',
    description: 'Professional CAD modeling software',
    capabilities: ['NURBS', 'Precision', 'Industry CAD'],
  },
  {
    id: 'freecad',
    name: 'FreeCAD',
    description: 'Parametric 3D CAD modeler',
    capabilities: ['Parametric', 'Open Source', 'CAD'],
  },
]

const qualityLevels = [
  { id: 'draft', label: 'Draft', time: '~1min', memory: 'Low' },
  { id: 'standard', label: 'Standard', time: '~5min', memory: 'Medium' },
  { id: 'high', label: 'High', time: '~15min', memory: 'High' },
  { id: 'ultra', label: 'Ultra', time: '~30min', memory: 'Very High' },
]

const formats = ['.stl', '.obj', '.fbx', '.step', '.iges', '.dae']

export function ParameterControls({
  selectedTool,
  onToolChange,
  quality,
  onQualityChange,
  exportFormat,
  onExportFormatChange,
  disabled = false,
  className,
}: ParameterControlsProps) {
  return (
    <div className={cn('space-y-6', className)}>
      {/* Tool Selection */}
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-3">
          3D Modeling Tool
        </label>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {tools.map((tool) => (
            <button
              key={tool.id}
              onClick={() => !disabled && onToolChange(tool.id)}
              disabled={disabled}
              className={cn(
                'p-4 rounded-lg border-2 text-left transition-all',
                selectedTool === tool.id
                  ? 'border-primary-500 bg-primary-600/10'
                  : 'border-dark-400 bg-dark-200 hover:border-dark-300',
                disabled && 'opacity-50 cursor-not-allowed'
              )}
            >
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-semibold text-white">{tool.name}</h3>
                {selectedTool === tool.id && (
                  <Check className="w-5 h-5 text-primary-500" />
                )}
              </div>
              <p className="text-sm text-gray-400 mb-2">{tool.description}</p>
              <div className="flex flex-wrap gap-1">
                {tool.capabilities.map((cap) => (
                  <span
                    key={cap}
                    className="px-2 py-0.5 text-xs bg-dark-300 text-gray-300 rounded"
                  >
                    {cap}
                  </span>
                ))}
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Quality & Format Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Quality Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-3">
            Quality Level
          </label>
          <div className="space-y-2">
            {qualityLevels.map((level) => (
              <button
                key={level.id}
                onClick={() => !disabled && onQualityChange(level.id)}
                disabled={disabled}
                className={cn(
                  'w-full px-4 py-3 rounded-lg border text-left transition-all',
                  quality === level.id
                    ? 'border-primary-500 bg-primary-600/10 text-white'
                    : 'border-dark-400 bg-dark-200 text-gray-300 hover:border-dark-300',
                  disabled && 'opacity-50 cursor-not-allowed'
                )}
              >
                <div className="flex items-center justify-between">
                  <span className="font-medium">{level.label}</span>
                  <span className="text-xs text-gray-400">
                    {level.time} • {level.memory}
                  </span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Export Format */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-3">
            Export Format
          </label>
          <div className="grid grid-cols-2 gap-2">
            {formats.map((format) => (
              <button
                key={format}
                onClick={() => !disabled && onExportFormatChange(format)}
                disabled={disabled}
                className={cn(
                  'px-4 py-3 rounded-lg border text-center transition-all',
                  exportFormat === format
                    ? 'border-primary-500 bg-primary-600/10 text-white font-medium'
                    : 'border-dark-400 bg-dark-200 text-gray-300 hover:border-dark-300',
                  disabled && 'opacity-50 cursor-not-allowed'
                )}
              >
                {format}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
