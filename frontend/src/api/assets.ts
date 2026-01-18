import { api } from './client'

export type AssetType = 'image' | 'drawing2d' | 'model3d'

export interface AssetOut {
  id: string
  project_id: string
  asset_type: AssetType
  filename: string
  content_type: string
  size_bytes: number
  created_at: string
  updated_at: string
  preview_url?: string
}

export const assetsApi = {
  list: () => api.get<AssetOut[]>('/assets'),
  get: (id: string) => api.get<AssetOut>(`/assets/${id}`),
  upload: (projectId: string, assetType: AssetType, files: File[]) => {
    const formData = new FormData()
    formData.append('project_id', projectId)
    formData.append('asset_type', assetType)
    files.forEach(file => formData.append('files', file))
    return api.post<AssetOut[]>('/assets/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}
