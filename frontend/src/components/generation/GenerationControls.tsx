import { useRef, DragEvent, useState } from 'react'
import { Upload, Download, RotateCcw, File, X } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { cn } from '@/utils/cn'

interface GenerationControlsProps {
  onGenerate: () => void
  onUploadReference: (file: File | null) => void
  onDownload?: () => void
  onReset?: () => void
  isGenerating: boolean
  canGenerate: boolean
  canDownload: boolean
  generationProgress?: number
  generationStep?: string
  error?: string | null
  referenceFile?: File | null
  disabled?: boolean
  className?: string
}

export function GenerationControls({
  onGenerate,
  onUploadReference,
  onDownload,
  onReset,
  isGenerating,
  canGenerate,
  canDownload,
  generationProgress = 0,
  generationStep,
  error,
  referenceFile,
  disabled = false,
  className,
}: GenerationControlsProps) {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [isDragging, setIsDragging] = useState(false)

  const handleDragOver = (e: DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleDrop = (e: DragEvent) => {
    e.preventDefault()
    setIsDragging(false)

    const file = e.dataTransfer.files[0]
    if (file && isValidFile(file)) {
      onUploadReference(file)
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file && isValidFile(file)) {
      onUploadReference(file)
    }
  }

  const isValidFile = (file: File) => {
    const validTypes = ['image/', 'model/', 'application/']
    return validTypes.some((type) => file.type.startsWith(type))
  }

  const getFileIcon = () => {
    if (!referenceFile) return <Upload className="w-5 h-5" />
    if (referenceFile.type.startsWith('image/')) return <File className="w-5 h-5" />
    return <File className="w-5 h-5" />
  }

  const getFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  return (
    <div className={cn('space-y-4', className)}>
      {/* Reference File Upload */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={cn(
          'p-6 border-2 border-dashed rounded-lg transition-colors',
          isDragging
            ? 'border-primary-500 bg-primary-600/10'
            : 'border-dark-400 bg-dark-200',
          disabled && 'opacity-50 cursor-not-allowed'
        )}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*,model/*"
          onChange={handleFileSelect}
          className="hidden"
          disabled={disabled}
        />

        {referenceFile ? (
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              {getFileIcon()}
              <div>
                <div className="text-sm font-medium text-white">
                  {referenceFile.name}
                </div>
                <div className="text-xs text-gray-400">
                  {getFileSize(referenceFile.size)}
                </div>
              </div>
            </div>
            <button
              onClick={() => onUploadReference(null)}
              className="text-gray-400 hover:text-white transition-colors"
              type="button"
              disabled={disabled}
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        ) : (
          <button
            onClick={() => fileInputRef.current?.click()}
            className="w-full flex flex-col items-center gap-2 text-gray-400 hover:text-white transition-colors"
            type="button"
            disabled={disabled}
          >
            {getFileIcon()}
            <span className="text-sm">Upload reference image or 3D model</span>
            <span className="text-xs text-gray-500">or drag and drop</span>
          </button>
        )}
      </div>

      {/* Progress */}
      {isGenerating && (
        <div className="p-4 bg-dark-200 rounded-lg border border-dark-400">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-white">
              {generationStep || 'Generating...'}
            </span>
            <span className="text-sm text-gray-400">{generationProgress}%</span>
          </div>
          <div className="w-full bg-dark-400 rounded-full h-2">
            <div
              className="bg-primary-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${generationProgress}%` }}
            />
          </div>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="p-4 bg-red-600/10 border border-red-600/20 rounded-lg">
          <p className="text-sm text-red-400">{error}</p>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex gap-3">
        <Button
          variant="primary"
          onClick={onGenerate}
          disabled={!canGenerate || disabled}
          className="flex-1"
        >
          {isGenerating ? 'Generating...' : 'Generate Model'}
        </Button>

        {canDownload && onDownload && (
          <Button
            variant="secondary"
            onClick={onDownload}
            disabled={disabled}
          >
            <Download className="w-4 h-4 mr-2" />
            Download
          </Button>
        )}

        {onReset && (
          <Button
            variant="ghost"
            onClick={onReset}
            disabled={isGenerating || disabled}
          >
            <RotateCcw className="w-4 h-4" />
          </Button>
        )}
      </div>
    </div>
  )
}
