# HealthLens AI - Complete Frontend

A full-featured React + Next.js frontend for the HealthLens AI medical report analysis platform.

## 🎯 Features

### Core Features
- **Report Upload**: Drag-and-drop upload with validation (PDF, JPEG, PNG, TIFF)
- **Dashboard**: Overview with real-time stats and quick metrics
- **Report Analysis**: View extracted markers with severity levels (normal/abnormal/critical)
- **Real-time Processing**: Track OCR and AI analysis progress
- **Responsive Design**: Mobile-friendly with Tailwind CSS
- **Authentication**: Login/register with token management

### Advanced Features
- **Health Trends**: Interactive charts showing marker trends over time
- **AI Chat**: Ask questions about your medical report to AI assistant
- **Doctor Visit Prep**: Generate preparation guide with questions and talking points
- **Quick Actions**: Fast access to all report-related functions
- **User Profile**: Manage account settings, security, and notifications

## 📁 Project Structure

```
frontend/
├── pages/                           # Next.js pages (routes)
│   ├── index.tsx                   # Root page (redirects)
│   ├── login.tsx                   # Login page
│   ├── register.tsx                # Registration page
│   ├── dashboard.tsx               # Main dashboard
│   ├── upload.tsx                  # Report upload page
│   ├── profile.tsx                 # User settings
│   ├── report/
│   │   └── [id].tsx               # Report detail view
│   ├── chat/
│   │   └── [id].tsx               # AI chat interface
│   ├── trends/
│   │   └── [id].tsx               # Health trends visualization
│   └── doctor-visit/
│       └── [id].tsx               # Doctor visit preparation
├── components/                      # Reusable React components
│   ├── Layout.tsx                  # App layout with nav/footer
│   ├── MarkerCard.tsx              # Health marker display
│   ├── ReportUpload.tsx            # File upload component
│   ├── ReportList.tsx              # Report cards list
│   ├── QuickActions.tsx            # Action buttons for reports
│   ├── MobileNavMenu.tsx           # Mobile navigation
│   └── Toast.tsx                   # Notification component
├── lib/
│   ├── api.ts                      # Axios HTTP client with interceptors
│   └── hooks/
│       └── useReports.ts           # Custom hook for report operations
├── globals.css                      # Global styles
├── tailwind.config.js              # Tailwind configuration
├── next.config.js                  # Next.js configuration
└── package.json                    # Dependencies
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn
- Backend API running on port 8000

### Installation

1. Navigate to frontend:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

Visit `http://localhost:3000`

## 📖 Pages Guide

### Authentication
- **Login** (`/login`): Demo authentication (any email/password works)
- **Register** (`/register`): Create new account

### Main Pages
- **Dashboard** (`/dashboard`): Overview of all reports with stats
- **Upload** (`/upload`): Upload medical reports with drag-drop support
- **Profile** (`/profile`): Account settings, security, and notifications

### Report Pages
- **Report Detail** (`/report/[id]`): View full report with all markers
  - See normal and abnormal markers
  - Run AI analysis
  - Access quick actions

- **Health Trends** (`/trends/[id]`): Interactive charts
  - Glucose trends
  - Hemoglobin tracking
  - Platelet count visualization
  - Trend analysis and recommendations

- **AI Chat** (`/chat/[id]`): Conversational interface
  - Ask questions about markers
  - Get AI-powered explanations
  - Real-time chat responses

- **Doctor Visit** (`/doctor-visit/[id]`): Preparation guide
  - Generated questions for doctor
  - Health summary for printing
  - Action checklist
  - Preparation tips

## 🎨 UI Components

### Layout
- Sticky navigation bar
- Mobile responsive menu
- Footer with links
- Main content area

### Report Components
- **MarkerCard**: Displays individual health markers with color-coded severity
- **ReportList**: Paginated list of user's reports
- **ReportUpload**: Drag-drop file upload with validation
- **QuickActions**: Fast links to trends, chat, doctor visit prep

### Utilities
- **Toast**: Notification system for success/error/info messages
- **MobileNavMenu**: Mobile navigation drawer

## 🔧 Configuration

### Environment Variables
Create `.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### Tailwind CSS
- Colors: Blue (#0066cc), Red (#dc2626), Yellow (#f97316), Green (#16a34a)
- Responsive breakpoints: sm, md, lg
- Full customization in `tailwind.config.js`

## 📡 API Integration

All API calls go through `lib/api.ts` (Axios instance) with:
- Automatic Bearer token attachment
- 401 redirect to login
- Error handling

### Endpoints Used
```
POST   /upload                          # Upload report
GET    /reports                         # List reports
GET    /reports/{id}                   # Get report detail
POST   /reports/{id}/analyze           # Trigger AI analysis
DELETE /reports/{id}                   # Delete report
```

## 🛠️ Development Commands

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start dev server (port 3000) |
| `npm run build` | Build for production |
| `npm start` | Run production build |
| `npm run lint` | Check code quality |

## 📱 Responsive Design

- **Mobile**: Single column, full-width buttons
- **Tablet**: Two-column grid layouts
- **Desktop**: Full multi-column layouts with sidebar navigation

## 🎯 Key Features In-Depth

### Dashboard Analytics
- Total reports count
- Reports with abnormal markers
- Processing queue status
- Completed reports count

### Report Analysis
- Color-coded severity (green/yellow/red)
- Reference ranges for each marker
- Numeric value tracking
- Categorized markers

### Health Trends
- Time-series visualization with Recharts
- Multiple markers on same chart
- AI-powered analysis for each trend
- Recommendations based on data

### Doctor Visit Prep
- AI-generated questions
- Health summary export (PDF ready)
- Checklist for preparation
- Discussion topics organized by category

## 🔐 Security

- JWT tokens in localStorage
- Bearer token in API requests
- Auto-logout on 401 response
- Input validation on forms
- XSS protection with React

## 📊 Tech Stack

- **Framework**: Next.js 14
- **UI**: React 18 + Tailwind CSS
- **HTTP**: Axios with interceptors
- **Charts**: Recharts
- **Icons**: Lucide React
- **Language**: TypeScript
- **Date Handling**: date-fns

## 🚨 Error Handling

- API error messages displayed to user
- Form validation with helpful messages
- Graceful fallbacks for missing data
- Console error logging

## 📚 Future Enhancements

- [ ] Export reports as PDF
- [ ] Multi-language support
- [ ] Dark mode
- [ ] Advanced filtering/search
- [ ] Appointment scheduling
- [ ] Integration with healthcare providers
- [ ] Real-time notifications
- [ ] Video consultation booking

## 🤝 Contributing

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## ⚖️ Legal Disclaimer

HealthLens AI is for **educational purposes only**. It does not provide medical diagnoses or treatment recommendations. Always consult qualified healthcare professionals regarding medical decisions.

## 📄 License

Proprietary - HealthLens AI 2026
