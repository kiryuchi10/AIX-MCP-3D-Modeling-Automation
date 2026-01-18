import { useState, useRef, KeyboardEvent } from 'react'
import { X, Sparkles } from 'lucide-react'
import { cn } from '@/utils/cn'
import { useCommandSuggestions } from '@/hooks/useCommandSuggestions'

interface PromptInputProps {
  value: string
  onChange: (value: string) => void
  onSuggestionSelect?: (suggestion: string) => void
  placeholder?: string
  disabled?: boolean
  selectedTool?: string
  className?: string
}

export function PromptInput({
  value,
  onChange,
  onSuggestionSelect,
  placeholder = 'Describe the 3D model you want to generate...',
  disabled = false,
  selectedTool = 'blender',
  className,
}: PromptInputProps) {
  const [isFocused, setIsFocused] = useState(false)
  const [selectedIndex, setSelectedIndex] = useState(-1)
  const inputRef = useRef<HTMLTextAreaElement>(null)
  const suggestionsRef = useRef<HTMLDivElement>(null)

  const { suggestions, isLoading } = useCommandSuggestions(
    value,
    selectedTool,
    isFocused && value.length >= 2
  )

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (suggestions.length === 0) return

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault()
        setSelectedIndex((prev) =>
          prev < suggestions.length - 1 ? prev + 1 : prev
        )
        break
      case 'ArrowUp':
        e.preventDefault()
        setSelectedIndex((prev) => (prev > 0 ? prev - 1 : -1))
        break
      case 'Enter':
        if (selectedIndex >= 0) {
          e.preventDefault()
          const selected = suggestions[selectedIndex]
          onChange(selected.command)
          onSuggestionSelect?.(selected.command)
          setSelectedIndex(-1)
        }
        break
      case 'Escape':
        setSelectedIndex(-1)
        break
    }
  }

  const handleSuggestionClick = (suggestion: { command: string; description?: string }) => {
    onChange(suggestion.command)
    onSuggestionSelect?.(suggestion.command)
    setSelectedIndex(-1)
    inputRef.current?.focus()
  }

  const handleClear = () => {
    onChange('')
    inputRef.current?.focus()
  }

  return (
    <div className={cn('relative', className)}>
      <div className="relative">
        <textarea
          ref={inputRef}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          onFocus={() => setIsFocused(true)}
          onBlur={() => {
            // Delay to allow click on suggestions
            setTimeout(() => setIsFocused(false), 200)
          }}
          placeholder={placeholder}
          disabled={disabled}
          rows={4}
          className={cn(
            'w-full px-4 py-3 bg-dark-200 border border-dark-400 rounded-lg',
            'text-white placeholder-gray-500',
            'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent',
            'disabled:opacity-50 disabled:cursor-not-allowed',
            'resize-none'
          )}
        />
        {value && (
          <button
            onClick={handleClear}
            className="absolute top-3 right-3 text-gray-400 hover:text-white transition-colors"
            type="button"
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>

      {/* Suggestions Dropdown */}
      {isFocused && suggestions.length > 0 && (
        <div
          ref={suggestionsRef}
          className="absolute z-50 w-full mt-2 bg-dark-300 border border-dark-400 rounded-lg shadow-lg max-h-64 overflow-y-auto"
        >
          {suggestions.map((suggestion: { command: string; description?: string }, index: number) => (
            <button
              key={index}
              onClick={() => handleSuggestionClick(suggestion)}
              className={cn(
                'w-full px-4 py-3 text-left hover:bg-dark-400 transition-colors',
                'flex items-center gap-3',
                index === selectedIndex && 'bg-dark-400'
              )}
            >
              <Sparkles className="w-4 h-4 text-primary-400 flex-shrink-0" />
              <div className="flex-1 min-w-0">
                <div className="text-white font-medium">{suggestion.command}</div>
                {suggestion.description && (
                  <div className="text-sm text-gray-400 mt-1">
                    {suggestion.description}
                  </div>
                )}
              </div>
            </button>
          ))}
        </div>
      )}

      {isLoading && (
        <div className="absolute bottom-2 right-4 text-xs text-gray-400">
          Loading suggestions...
        </div>
      )}
    </div>
  )
}
