
---

## Key Components

### 1. Enhanced AI Model Service
- **Path**: `backend/app/services/enhanced_ai_model_service.py`
- **Role**:
  - Unified interface for research-driven 3D generation
  - Prompt parsing and model routing
  - Script generation for downstream CAD tools
  - Quality assessment and constraint validation

---

### 2. Research Integration Service
- **Path**: `backend/app/services/research_integration_service.py`
- **Role**:
  - Research paper registry and lifecycle management
  - Integration with AI UI Builder
  - Integration with Paper2Code
  - Research-specific environment configuration

---

### 3. Research Integration API
- **Path**: `backend/app/api/v1/endpoints/research_integration.py`
- **Endpoints**:
  - `GET /research/status`
  - `GET /research/papers`
  - `POST /research/generate`
  - `POST /research/ui/generate`
  - `POST /research/paper/analyze`

---

### 4. Research Integration Dashboard
- **Path**: `frontend/src/components/ResearchIntegrationDashboard.jsx`
- **Capabilities**:
  - Research paper browsing
  - Method-specific parameter tuning
  - Real-time generation monitoring
  - 3D preview and comparison
  - Paper-to-UI and Paper-to-Code workflows

---

## Installation and Setup

### Install Core Dependencies

```bash
pip install torch torchvision torchaudio
pip install pytorch3d
pip install kaolin
pip install clip-by-openai
pip install diffusers transformers
pip install trimesh open3d
