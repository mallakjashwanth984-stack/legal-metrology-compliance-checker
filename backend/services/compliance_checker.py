from datetime import datetime

class ComplianceChecker:
    """
    Check product compliance against Legal Metrology (Packaged Commodities) Rules, 2011
    """
    
    # Mandatory declarations as per Legal Metrology Rules
    MANDATORY_DECLARATIONS = [
        'manufacturer_name',
        'manufacturer_address',
        'net_quantity',
        'unit_of_measurement',
        'mrp',
        'manufacturing_date',
        'expiry_date',
        'consumer_care_details'
    ]
    
    # Minimum font size requirements (in points)
    MIN_FONT_SIZES = {
        'manufacturer_name': 6,
        'manufacturer_address': 6,
        'net_quantity': 8,
        'mrp': 10,
        'manufacturing_date': 6,
        'expiry_date': 6,
        'consumer_care_details': 4
    }
    
    def __init__(self):
        pass
    
    def check_product_compliance(self, product, declarations):
        """
        Check overall compliance of a product
        Returns: (violations, compliance_status, compliance_percentage)
        """
        violations = []
        
        # Check for mandatory declarations
        violations.extend(self._check_mandatory_declarations(product, declarations))
        
        # Check font sizes
        violations.extend(self._check_font_sizes(product, declarations))
        
        # Check readability
        violations.extend(self._check_readability(product, declarations))
        
        # Check MRP declaration
        if product.mrp:
            violations.extend(self._check_mrp_format(product))
        
        # Check date format
        violations.extend(self._check_date_format(product))
        
        # Calculate compliance status
        total_violations = len(violations)
        compliance_percentage = max(0, 100 - (total_violations * 10))
        compliance_status = 'compliant' if total_violations == 0 else 'non_compliant'
        
        return violations, compliance_status, compliance_percentage
    
    def _check_mandatory_declarations(self, product, declarations):
        """
        Check if all mandatory declarations are present
        """
        violations = []
        
        if not product.manufacturer_name:
            violations.append({
                'type': 'missing_manufacturer_name',
                'severity': 'critical',
                'description': 'Manufacturer name is missing',
                'rule_reference': 'Rule 4(1)(a), Legal Metrology (Packaged Commodities) Rules, 2011'
            })
        
        if not product.net_quantity:
            violations.append({
                'type': 'missing_net_quantity',
                'severity': 'critical',
                'description': 'Net quantity is missing',
                'rule_reference': 'Rule 4(1)(c), Legal Metrology (Packaged Commodities) Rules, 2011'
            })
        
        if not product.mrp:
            violations.append({
                'type': 'missing_mrp',
                'severity': 'critical',
                'description': 'Maximum Retail Price (MRP) is missing',
                'rule_reference': 'Rule 4(1)(e), Legal Metrology (Packaged Commodities) Rules, 2011'
            })
        
        if not product.manufacturing_date:
            violations.append({
                'type': 'missing_manufacturing_date',
                'severity': 'major',
                'description': 'Manufacturing date/packing date is missing',
                'rule_reference': 'Rule 4(1)(f), Legal Metrology (Packaged Commodities) Rules, 2011'
            })
        
        return violations
    
    def _check_font_sizes(self, product, declarations):
        """
        Check if font sizes meet minimum requirements
        """
        violations = []
        
        # Group declarations by type and check font sizes
        for declaration in declarations:
            decl_type = declaration.declaration_type
            font_size = declaration.font_size
            
            if decl_type in self.MIN_FONT_SIZES:
                min_size = self.MIN_FONT_SIZES[decl_type]
                if font_size and font_size < min_size:
                    violations.append({
                        'type': 'incorrect_font_size',
                        'severity': 'major',
                        'description': f'{decl_type}: Font size {font_size}pt is below minimum {min_size}pt',
                        'rule_reference': 'Rule 4(3), Legal Metrology (Packaged Commodities) Rules, 2011'
                    })
        
        return violations
    
    def _check_readability(self, product, declarations):
        """
        Check if declarations are readable
        """
        violations = []
        
        for declaration in declarations:
            if not declaration.is_readable:
                violations.append({
                    'type': 'low_readability',
                    'severity': 'major',
                    'description': f'{declaration.declaration_type}: Text is not clearly readable',
                    'rule_reference': 'Rule 4(2), Legal Metrology (Packaged Commodities) Rules, 2011'
                })
            elif declaration.confidence_score and declaration.confidence_score < 0.7:
                violations.append({
                    'type': 'unclear_declaration',
                    'severity': 'minor',
                    'description': f'{declaration.declaration_type}: Text clarity is questionable (confidence: {declaration.confidence_score:.0%})',
                    'rule_reference': 'Rule 4(2), Legal Metrology (Packaged Commodities) Rules, 2011'
                })
        
        return violations
    
    def _check_mrp_format(self, product):
        """
        Check if MRP is correctly declared
        """
        violations = []
        
        if product.mrp <= 0:
            violations.append({
                'type': 'invalid_mrp',
                'severity': 'critical',
                'description': 'MRP must be greater than zero',
                'rule_reference': 'Rule 4(1)(e), Legal Metrology (Packaged Commodities) Rules, 2011'
            })
        
        return violations
    
    def _check_date_format(self, product):
        """
        Check if dates are properly formatted
        """
        violations = []
        
        # Check if manufacturing date is valid
        if product.manufacturing_date:
            if product.manufacturing_date > datetime.utcnow():
                violations.append({
                    'type': 'invalid_manufacturing_date',
                    'severity': 'critical',
                    'description': 'Manufacturing date cannot be in the future',
                    'rule_reference': 'Rule 4(1)(f), Legal Metrology (Packaged Commodities) Rules, 2011'
                })
        
        # Check if product is expired
        if product.expiry_date:
            if product.expiry_date < datetime.utcnow():
                violations.append({
                    'type': 'expired_product',
                    'severity': 'critical',
                    'description': 'Product has expired',
                    'rule_reference': 'Rule 4(1)(g), Legal Metrology (Packaged Commodities) Rules, 2011'
                })
        
        return violations
