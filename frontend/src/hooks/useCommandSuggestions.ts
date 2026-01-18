import { useState, useEffect } from 'react'

interface CommandSuggestion {
  command: string
  description?: string
  tool?: string
}

// Mock suggestions - replace with actual API call
const mockSuggestions: Record<string, CommandSuggestion[]> = {
  blender: [
    { command: 'Create a cube with dimensions 10x10x10', description: 'Simple cube primitive' },
    { command: 'Generate a sphere with radius 5', description: 'Sphere primitive' },
    { command: 'Create a cylinder with height 20 and radius 3', description: 'Cylinder primitive' },
    { command: 'Generate a torus with major radius 8 and minor radius 2', description: 'Torus primitive' },
    { command: 'Create a mesh grid with 50x50 subdivisions', description: 'Grid mesh' },
  ],
  rhino: [
    { command: 'Create NURBS surface with 4 control points', description: 'NURBS surface' },
    { command: 'Generate lofted surface between 3 curves', description: 'Lofted surface' },
    { command: 'Create extruded surface from curve', description: 'Extruded surface' },
  ],
  freecad: [
    { command: 'Create parametric box with length, width, height', description: 'Parametric box' },
    { command: 'Generate sketch-based extrusion', description: 'Sketch extrusion' },
    { command: 'Create part with fillet edges', description: 'Filleted part' },
  ],
}

export function useCommandSuggestions(
  query: string,
  tool: string = 'blender',
  enabled: boolean = true
) {
  const [suggestions, setSuggestions] = useState<CommandSuggestion[]>([])
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    if (!enabled || query.length < 2) {
      setSuggestions([])
      return
    }

    setIsLoading(true)

    // Debounce
    const timer = setTimeout(() => {
      // Filter mock suggestions based on query
      const toolSuggestions = mockSuggestions[tool] || mockSuggestions.blender
      const filtered = toolSuggestions
        .filter((s) =>
          s.command.toLowerCase().includes(query.toLowerCase()) ||
          s.description?.toLowerCase().includes(query.toLowerCase())
        )
        .slice(0, 5)

      setSuggestions(filtered)
      setIsLoading(false)

      // TODO: Replace with actual API call
      // api.get(`/commands/suggestions`, { params: { q: query, tool } })
      //   .then(res => setSuggestions(res.data))
      //   .finally(() => setIsLoading(false))
    }, 200)

    return () => clearTimeout(timer)
  }, [query, tool, enabled])

  return { suggestions, isLoading }
}
