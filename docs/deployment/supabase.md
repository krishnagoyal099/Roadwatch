# Supabase Configuration

RoadWatch uses Supabase as its primary PostgreSQL database.

## 1. Database Schema
The database requires four primary tables to function correctly:
1. `road_segments`: Contains baseline road data, H3 indices, and contractors.
2. `complaints`: Stores citizen-reported issues, severity, and status.
3. `contractors`: Details of infrastructure builders.
4. `engineers`: Assigned executive engineers for segments.

> **Note**: A complete schema dump is located in the root directory at `schema.json`. You can apply this directly in the Supabase SQL editor.

## 2. Storage Buckets
For production use, if you are saving images, you need to create a public storage bucket.
- **Bucket Name**: `complaint-images`
- **Permissions**: Make the bucket Public so the frontend can render the image URLs directly in the chat UI.

## 3. Environment Variables
Connect your FastAPI backend to Supabase by adding the following to your `apps/backend/.env`:
```env
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_KEY=your-anon-or-service-role-key
```
For local development, the Anon key is sufficient as Row Level Security (RLS) policies are open by default in the provided schema.
