# Compliance Checking Algorithm

## Overview

The compliance checker validates product labels against Legal Metrology (Packaged Commodities) Rules, 2011.

## Violation Detection Flow

```
Product Image
    ↓
[OCR Processing] → Extract text, positions, confidence
    ↓
[Mandatory Declarations Check]
  - Check each required field is present
  - Generate CRITICAL violations if missing
    ↓
[Font Size Validation]
  - Measure font sizes from OCR data
  - Compare against minimum requirements
  - Generate MAJOR violations if below threshold
    ↓
[Readability Analysis]
  - Check OCR confidence scores
  - Analyze contrast and brightness
  - Generate MAJOR/MINOR violations
    ↓
[Date Validation]
  - Verify date formats
  - Check for expired products
  - Check for future manufacturing dates
    ↓
[Compliance Report Generation]
  - Aggregate all violations
  - Calculate compliance percentage
  - Generate PDF report
```

## Violation Severity Matrix

| Violation Type | Severity | Rule Reference |
|---|---|---|
| Missing mandatory declaration | CRITICAL | Rule 4(1) |
| Invalid MRP | CRITICAL | Rule 4(1)(e) |
| Expired product | CRITICAL | Rule 4(1)(g) |
| Future manufacturing date | CRITICAL | Rule 4(1)(f) |
| Font size below minimum | MAJOR | Rule 4(3) |
| Unclear text/Low readability | MAJOR | Rule 4(2) |
| Low OCR confidence | MINOR | Rule 4(2) |
| Minor formatting issues | MINOR | General |

## Compliance Scoring

```
Compliance % = max(0, 100 - (violations × severity_weight))

Where:
- CRITICAL violation = 30 points
- MAJOR violation = 15 points
- MINOR violation = 5 points
```

## Mandatory Declarations Checklist

- [ ] Manufacturer name and address
- [ ] Net quantity (weight/volume)
- [ ] Unit of measurement (kg, L, etc.)
- [ ] Maximum Retail Price (MRP)
- [ ] Manufacturing date/Batch number
- [ ] Expiry/Best before date
- [ ] Consumer care/Usage instructions

## Font Size Requirements

Minimum font sizes are based on label area and declaration type:

| Declaration | Minimum Size | Rationale |
|---|---|---|
| Manufacturer Name | 6 pt | Identification |
| Manufacturer Address | 6 pt | Traceability |
| Net Quantity | 8 pt | Consumer information |
| MRP | 10 pt | Price transparency |
| Manufacturing Date | 6 pt | Product identification |
| Expiry Date | 6 pt | Consumer safety |
| Consumer Care | 4 pt | Instructions |

## OCR Quality Metrics

- **Confidence Score**: Percentage confidence in text recognition (0-100%)
- **Contrast Ratio**: Difference between text and background colors
- **Image Brightness**: Overall illumination level
- **Sharpness**: Edge detection ratio

## Decision Logic Examples

### Example 1: Missing MRP
```
Input: Product image without MRP
OCR Output: No "MRP", "Price", "₹" detected
Decision: CRITICAL violation - "missing_mrp"
Result: Non-compliant, 0% compliance (before other checks)
```

### Example 2: Small Font Size
```
Input: Product with net quantity in 5pt font
OCR Output: Text detected, font_height = 5px (≈3.75pt)
Decision: MAJOR violation - "incorrect_font_size"
Rule: Minimum 8pt required
Result: Non-compliant, reduced compliance score
```

### Example 3: Expired Product
```
Input: Product with expiry date 01-01-2023
Current Date: 01-09-2024
Decision: CRITICAL violation - "expired_product"
Result: Non-compliant, automatically flagged as dangerous
```

## Confidence Thresholds

- **High Confidence** (>90%): Text is clearly readable
- **Medium Confidence** (70-90%): Minor recognition issues
- **Low Confidence** (50-70%): Significant recognition challenges
- **Very Low** (<50%): Text may be unreadable

## Date Format Detection

Supported formats:
- DD-MM-YYYY
- DD/MM/YYYY
- MM-DD-YYYY
- DD MMM YYYY
- DD Month YYYY

## Compliance Percentage Calculation

```python
def calculate_compliance(violations):
    weights = {
        'critical': 30,
        'major': 15,
        'minor': 5
    }
    total_deduction = sum(weights[v.severity] for v in violations)
    compliance = max(0, 100 - total_deduction)
    return min(100, compliance)
```

## Report Generation

PDF reports include:
1. Report header with timestamp
2. Product information
3. Compliance summary
4. Detailed violation list with:
   - Violation type
   - Severity level
   - Description
   - Applicable rule reference
5. Recommendations
6. Company footer with contact info
