# RoadWatch System Architecture

RoadWatch is a modern, modular web application designed for civic accountability. It operates on a three-tier architecture:

## 1. Frontend (Vite + React)
- **Tech Stack**: React 18, Vite, Tailwind CSS.
- **Role**: Provides a conversational UI for citizens to report issues and a dashboard for viewing public spending.
- **State Management**: React Hooks and Context.
- **Routing**: `react-router-dom`.

## 2. Backend API (FastAPI)
- **Tech Stack**: Python 3.13, FastAPI, Pydantic, httpx.
- **Role**: Orchestrates the business logic, handles sessions, and interacts with the LLM and database.
- **Key Services**:
  - `LLMService`: Wraps Groq API for intent classification and natural language generation.
  - `CVService`: Sends images to the ML microservice.
  - `GeocodingService`: Converts text addresses to coordinates.

## 3. ML Microservice (FastAPI + YOLOv8)
- **Tech Stack**: Python 3.13, FastAPI, Ultralytics (YOLOv8), PyTorch.
- **Role**: A standalone service running on port `8001` that performs Computer Vision inference.
- **Design Choice**: Separated from the main backend to prevent heavy PyTorch tensors from blocking standard asynchronous web requests, and to allow independent scaling.

## 4. Database Layer (Supabase)
- **Tech Stack**: PostgreSQL + PostgREST.
- **Role**: Stores relational data (`complaints`, `road_segments`, `spending`).
- **Spatial Queries**: Uses H3 indices for ultra-fast localized queries instead of complex PostGIS geographic intersections.
