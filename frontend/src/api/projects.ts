import { api } from './client'

export interface ProjectOut {
  id: string
  name: string
  description?: string
  created_at: string
  updated_at: string
}

export interface ProjectCreate {
  name: string
  description?: string
}

export const projectsApi = {
  list: () => api.get<ProjectOut[]>('/projects'),
  get: (id: string) => api.get<ProjectOut>(`/projects/${id}`),
  create: (data: ProjectCreate) => api.post<ProjectOut>('/projects', data),
}
