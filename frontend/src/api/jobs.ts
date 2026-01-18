import { api } from './client'

export type JobType = 'extract' | 'generate_script' | 'run_blender'
export type JobStatus = 'queued' | 'running' | 'succeeded' | 'failed'

export interface JobOut {
  id: string
  project_id: string
  job_type: JobType
  status: JobStatus
  progress: number
  message?: string | null
  result?: any
  params: Record<string, any>
  created_at: string
  updated_at: string
}

export interface JobCreate {
  project_id: string
  job_type: JobType
  params?: Record<string, any>
}

export const jobsApi = {
  list: (params?: { project_id?: string; status?: JobStatus; limit?: number }) => {
    const queryParams = new URLSearchParams()
    if (params?.project_id) queryParams.append('project_id', params.project_id)
    if (params?.status) queryParams.append('status', params.status)
    if (params?.limit) queryParams.append('limit', params.limit.toString())
    return api.get<JobOut[]>(`/jobs?${queryParams.toString()}`)
  },
  get: (id: string) => api.get<JobOut>(`/jobs/${id}`),
  create: (data: JobCreate) => api.post<JobOut>('/jobs', data),
}
