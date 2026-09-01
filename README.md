# Legal Metrology Compliance Checker

A comprehensive software system for automated compliance checking of packaged commodities against the Legal Metrology (Packaged Commodities) Rules, 2011.

## Overview

This application helps enforcement officials and compliance teams automatically detect, extract, and validate mandatory declarations on packaged product labels to ensure compliance with Indian Legal Metrology regulations.

## Features

- **Image Upload & Analysis**: Scan and analyze packaged commodity labels and product images
- **Automated Declaration Extraction**: Extract mandatory declarations from product labels
- **Compliance Validation**: Check completeness, correctness, and placement of declarations
- **Readability Analysis**: Analyze font sizes and readability requirements
- **Non-compliance Detection**: Identify missing, misleading, or non-standard declarations
- **Report Generation**: Generate detailed compliance/non-compliance reports in PDF and editable formats
- **Product Repository**: Maintain comprehensive database of scanned products and inspection history
- **Dashboard**: Monitor inspections, violations, and product compliance status
- **Role-based Access**: Secure authentication with role-based user permissions
- **Search & Retrieval**: Easy access to previously scanned products and reports

## Tech Stack

### Frontend
- React.js with TypeScript
- Next.js for server-side rendering
- Tailwind CSS for styling
- Redux for state management
- Axios for API communication

### Backend
- Python with Flask/FastAPI
- PostgreSQL for database
- OpenCV and Pytesseract for image processing
- PIL for image manipulation
- JWT for authentication
- SQLAlchemy ORM

## Project Structure

```
legal-metrology-compliance-checker/
├── frontend/              # React.js frontend application
├── backend/               # Python backend application
├── docs/                  # Documentation
├── docker-compose.yml     # Docker configuration
└── README.md             # This file
```

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- PostgreSQL 12+
- Docker (optional)

### Installation

**Frontend Setup:**
```bash
cd frontend
npm install
npm run dev
```

**Backend Setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Documentation

See the `/docs` folder for detailed technical documentation including:
- System architecture
- API documentation
- Database schema
- Deployment guide
- User guide

## License

MIT License

## Support

For issues and support, please create an issue in the GitHub repository.
