# Legal Metrology Compliance Checker

An automated compliance checking system for packaged commodities against the Legal Metrology (Packaged Commodities) Rules, 2011 (India). This application uses OCR technology to extract product label information and validates compliance with statutory requirements.

## Features

### Core Functionality
- **Product Upload & Processing**: Upload product images for automatic text extraction using OCR (Tesseract)
- **Automated Compliance Checking**: Validates against Legal Metrology Rules including:
  - Mandatory declarations (Manufacturer name, address, net quantity, MRP, dates)
  - Font size requirements for different declarations
  - Text readability and clarity checks
  - Date format validation
  - MRP format validation
- **Violation Detection**: Identifies and categorizes violations as:
  - Critical (Major regulatory violations)
  - Major (Significant compliance issues)
  - Minor (Minor formatting issues)
- **PDF Report Generation**: Generates detailed compliance reports with violation details
- **Dashboard Analytics**: Real-time insights including:
  - Compliance statistics
  - Violation trends over time
  - Recent inspections
  - Top violations by type
- **User Management**: Role-based access control (Admin, Inspector, User)
- **Product Database**: Maintain searchable database of all checked products

## Project Structure

```
legal-metrology-compliance-checker/
├── backend/
│   ├── app.py                 # Flask application factory
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment variables template
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py           # User model
│   │   ├── product.py        # Product model
│   │   ├── declaration.py    # Declaration model
│   │   ├── violation.py      # Violation model
│   │   └── compliance_report.py  # Report model
│   ├── routes/
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── products.py       # Product management endpoints
│   │   ├── compliance.py     # Compliance checking endpoints
│   │   ├── reports.py        # Report generation endpoints
│   │   └── dashboard.py      # Dashboard analytics endpoints
│   └── services/
│       ├── image_processor.py    # OCR and image analysis
│       ├── compliance_checker.py # Compliance validation logic
│       └── report_generator.py   # PDF report generation
├── frontend/
│   ├── app/
│   │   ├── layout.tsx        # Root layout
│   │   ├── providers.tsx     # Redux and Toast providers
│   │   ├── login/
│   │   ├── register/
│   │   ├── dashboard/
│   │   ├── upload/
│   │   └── products/
│   ├── components/
│   │   ├── Navbar.tsx
│   │   ├── DashboardCard.tsx
│   │   ├── ComplianceChart.tsx
│   │   ├── RecentInspections.tsx
│   │   ├── ProductList.tsx
│   │   ├── ProductUploadForm.tsx
│   │   └── ...
│   ├── services/
│   │   ├── authService.ts
│   │   ├── productService.ts
│   │   ├── complianceService.ts
│   │   ├── reportService.ts
│   │   └── dashboardService.ts
│   ├── store/
│   │   ├── index.ts          # Redux store configuration
│   │   └── authSlice.ts      # Auth reducer
│   ├── styles/
│   │   └── globals.css
│   ├── utils/
│   │   └── api.ts            # API client configuration
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── next.config.js
└── README.md
```

## Technology Stack

### Backend
- **Framework**: Flask (Python 3.8+)
- **Database**: PostgreSQL
- **Authentication**: JWT (Flask-JWT-Extended)
- **OCR**: Tesseract (pytesseract)
- **Image Processing**: OpenCV, Pillow
- **Report Generation**: ReportLab
- **Server**: Gunicorn
- **ORM**: SQLAlchemy

### Frontend
- **Framework**: Next.js 13+ with React 18
- **Styling**: Tailwind CSS
- **State Management**: Redux Toolkit
- **HTTP Client**: Axios
- **Charts**: Recharts
- **File Upload**: React Dropzone
- **Notifications**: React Hot Toast
- **Language**: TypeScript

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+ and npm/yarn
- PostgreSQL 12+
- Tesseract OCR engine

### Backend Setup

1. **Install Tesseract OCR** (Required for image text extraction)
   ```bash
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr
   
   # macOS
   brew install tesseract
   
   # Windows
   # Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
   ```

2. **Clone and navigate to backend**
   ```bash
   cd backend
   ```

3. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

6. **Initialize database**
   ```bash
   flask db upgrade
   ```

7. **Run backend server**
   ```bash
   python app.py
   # or with gunicorn for production
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

### Frontend Setup

1. **Navigate to frontend**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Create environment file**
   ```bash
   cp .env.example .env.local
   # Edit with your backend API URL
   NEXT_PUBLIC_API_URL=http://localhost:5000/api
   ```

4. **Run development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```
   Application will be available at `http://localhost:3000`

## Environment Variables

### Backend (.env)
```bash
FLASK_ENV=development
FLASK_APP=app.py
DATABASE_URL=postgresql://username:password@localhost:5432/metrology_db
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ACCESS_TOKEN_EXPIRES=3600
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=52428800
TESSERACT_CMD=/usr/bin/tesseract
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:5000/api
```

## API Documentation

### Authentication Endpoints

#### Register
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password",
  "full_name": "John Doe",
  "department": "Quality Control"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password"
}
```

### Product Endpoints

#### Upload Product
```http
POST /api/products/upload
Authorization: Bearer {token}
Content-Type: multipart/form-data

FormData:
  - image: [file]
  - product_name: "Milk Pack 1L"
  - category: "Dairy"
```

#### Get Products
```http
GET /api/products/?page=1&per_page=10&search=milk&category=dairy
Authorization: Bearer {token}
```

#### Get Product Details
```http
GET /api/products/{product_id}
Authorization: Bearer {token}
```

### Compliance Endpoints

#### Check Compliance
```http
POST /api/compliance/check/{product_id}
Authorization: Bearer {token}
```

#### Get Violations
```http
GET /api/compliance/violations/{product_id}?severity=critical
Authorization: Bearer {token}
```

#### Resolve Violation
```http
PUT /api/compliance/violations/{violation_id}/resolve
Authorization: Bearer {token}
Content-Type: application/json

{
  "resolution_notes": "Label was corrected and reprinted"
}
```

### Report Endpoints

#### Generate Report
```http
POST /api/reports/{product_id}
Authorization: Bearer {token}
```

#### Get Reports
```http
GET /api/reports/?page=1&per_page=10&product_id={product_id}
Authorization: Bearer {token}
```

#### Download Report
```http
GET /api/reports/download/{report_id}
Authorization: Bearer {token}
```

### Dashboard Endpoints

#### Get Overview
```http
GET /api/dashboard/overview
Authorization: Bearer {token}
```

#### Get Compliance Trends
```http
GET /api/dashboard/compliance-trends?days=30
Authorization: Bearer {token}
```

## Compliance Rules Implemented

The system checks compliance against the following Legal Metrology Rules:

### Mandatory Declarations (Rule 4)
1. **Manufacturer's Name & Address** - Must be present and readable
2. **Net Quantity** - Clear declaration of net weight/volume
3. **Unit of Measurement** - Proper SI unit specification
4. **Maximum Retail Price (MRP)** - Clear price declaration
5. **Manufacturing Date/Batch** - Product identification
6. **Expiry/Best Before Date** - For perishables
7. **Consumer Care Details** - Usage and storage instructions

### Font Size Requirements (Rule 4(3))
- Manufacturer Name: Minimum 6 pt
- Manufacturer Address: Minimum 6 pt
- Net Quantity: Minimum 8 pt
- MRP: Minimum 10 pt
- Manufacturing Date: Minimum 6 pt
- Expiry Date: Minimum 6 pt
- Consumer Care: Minimum 4 pt

### Text Quality Requirements
- Minimum OCR confidence: 50%
- Minimum contrast ratio: For readability
- Text must be clearly visible and legible

## Usage Guide

### For Inspectors/Users

1. **Login/Register**
   - Create account with department information
   - Login with credentials

2. **Upload Product Label**
   - Click "Upload" in navigation
   - Capture clear image of product label
   - Fill in product details (name, category)
   - System automatically extracts text using OCR

3. **Check Compliance**
   - Review extracted information
   - Click "Check Compliance"
   - System analyzes against Legal Metrology Rules
   - View violations with severity levels

4. **Generate Report**
   - Generate PDF report with all findings
   - Download for record keeping
   - Share with manufacturers for corrective action

5. **Track Products**
   - View all inspected products
   - Search by name or category
   - Monitor compliance trends

### For Administrators

1. **Dashboard Analytics**
   - View overall compliance statistics
   - Monitor critical violations
   - Track inspection trends

2. **User Management**
   - Create/manage user accounts
   - Assign roles and departments
   - Monitor user activity

3. **System Configuration**
   - Configure compliance rules
   - Set violation severity levels
   - Manage system settings

## Violation Severity Levels

### Critical
- Missing mandatory declarations
- Invalid MRP format
- Expired products
- Manufacturing date in future

### Major
- Font size below minimum requirements
- Low text readability
- Unclear declarations

### Minor
- Questionable OCR confidence
- Minor formatting issues
- Spacing concerns

## Database Schema

### Users Table
- id, username, email, password_hash, full_name, role, department, is_active, created_at, updated_at

### Products Table
- id, product_name, product_category, manufacturer_name, manufacturer_address, barcode, batch_number, net_quantity, unit_of_measurement, mrp, manufacturing_date, expiry_date, image_path, created_by, created_at, updated_at

### Declarations Table
- id, product_id, declaration_type, extracted_text, font_size, position (JSON), is_readable, confidence_score, created_at

### Violations Table
- id, product_id, violation_type, severity, description, rule_reference, is_resolved, resolution_notes, created_at, resolved_at

### Compliance Reports Table
- id, product_id, report_title, total_violations, critical_violations, major_violations, minor_violations, compliance_status, compliance_percentage, summary, detailed_findings (JSON), report_file_path, created_by, created_at, updated_at

## Troubleshooting

### Tesseract Not Found
```
Error: tesseract is not installed or it's not in your PATH
```
Solution: Install Tesseract and update `TESSERACT_CMD` in .env

### Database Connection Error
```
Error: could not connect to server
```
Solution: Ensure PostgreSQL is running and DATABASE_URL is correct

### CORS Error
```
Error: Cross-Origin Request Blocked
```
Solution: Frontend and backend must be on same domain or CORS must be configured

## Performance Optimization

- Images are compressed before processing
- Database queries use pagination
- API responses are cached where appropriate
- Frontend uses lazy loading for components
- PDF generation is optimized for large batches

## Security Features

- JWT token-based authentication
- Password hashing with werkzeug
- Role-based access control (RBAC)
- Request validation and sanitization
- CORS protection
- Rate limiting (can be added)
- File upload validation

## Future Enhancements

- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] Batch processing capabilities
- [ ] Advanced analytics and reporting
- [ ] Integration with manufacturer systems
- [ ] Machine learning for violation prediction
- [ ] Real-time compliance alerts
- [ ] Audit trail and compliance history
- [ ] API for third-party integrations
- [ ] Barcode scanning support

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For support, email: support@metrologychecker.com

## Disclaimer

This system is designed to assist in compliance checking but does not replace official inspections by legal metrology authorities. Always verify with official requirements.

---

**Last Updated**: September 2024
**Version**: 1.0.0
