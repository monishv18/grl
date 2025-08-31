"""
Document-specific configurations for different types of technical specifications
"""

class DocumentConfig:
    """Base configuration class for document parsing"""
    
    def __init__(self, doc_type: str):
        self.doc_type = doc_type
        self.toc_patterns = []
        self.section_patterns = []
        self.content_cleanup_rules = []
        self.tag_mapping = {}
        self.toc_scan_pages = 12
        self.max_file_size_mb = 50

class USBPDConfig(DocumentConfig):
    """Configuration for USB Power Delivery specifications"""
    
    def __init__(self):
        super().__init__("usb_pd")
        
        # TOC patterns specific to USB PD docs
        self.toc_patterns = [
            # Standard USB PD format
            r'^(\d+(?:\.\d+)*)\s+(.*?)\s*\.+\s*(\d+)$',
            # Format without dots
            r'^(\d+(?:\.\d+)*)\s+(.*?)\s+(\d+)$',
            # Chapter format
            r'^Chapter\s+(\d+)\s+(.*?)\s*\.+\s*(\d+)$',
            # Section format
            r'^Section\s+(\d+(?:\.\d+)*)\s+(.*?)\s*\.+\s*(\d+)$',
            # Annex format
            r'^Annex\s+([A-Z])\s+(.*?)\s*\.+\s*(\d+)$'
        ]
        
        # Content cleanup rules
        self.content_cleanup_rules = [
            (r'^\s*\d+\s*$', ''),  # Remove standalone page numbers
            (r'^\s*USB.*?Specification.*?\s*$', ''),  # Remove headers
            (r'^\s*Page\s+\d+\s*$', ''),  # Remove page indicators
            (r'\n\s*\n\s*\n', '\n\n'),  # Normalize multiple line breaks
        ]
        
        # Tag mapping for USB PD content
        self.tag_mapping = {
            'power': 'power_management',
            'voltage': 'power_management',
            'current': 'power_management',
            'watt': 'power_management',
            'negotiation': 'negotiation',
            'contract': 'negotiation',
            'agreement': 'negotiation',
            'communication': 'communication',
            'protocol': 'communication',
            'message': 'communication',
            'cc': 'communication',
            'state': 'state_machine',
            'machine': 'state_machine',
            'transition': 'state_machine',
            'cable': 'hardware',
            'connector': 'hardware',
            'plug': 'hardware',
            'receptacle': 'hardware',
            'compatibility': 'compatibility',
            'revision': 'compatibility',
            'version': 'compatibility',
            'overview': 'overview',
            'introduction': 'overview',
            'background': 'overview',
            'table': 'reference',
            'figure': 'reference',
            'diagram': 'reference',
            'safety': 'safety',
            'protection': 'safety',
            'fault': 'safety'
        }
        
        self.toc_scan_pages = 15
        self.max_file_size_mb = 100

class GenericTechSpecConfig(DocumentConfig):
    """Configuration for generic technical specifications"""
    
    def __init__(self):
        super().__init__("generic_tech_spec")
        
        # Generic TOC patterns
        self.toc_patterns = [
            # Standard numbered format
            r'^(\d+(?:\.\d+)*)\s+(.*?)\s*\.+\s*(\d+)$',
            # Chapter format
            r'^Chapter\s+(\d+)\s+(.*?)\s*\.+\s*(\d+)$',
            # Section format
            r'^Section\s+(\d+(?:\.\d+)*)\s+(.*?)\s*\.+\s*(\d+)$',
            # Letter-based sections
            r'^([A-Z])\s+(.*?)\s*\.+\s*(\d+)$',
            # Roman numeral chapters
            r'^([IVX]+)\.\s+(.*?)\s*\.+\s*(\d+)$'
        ]
        
        # Generic content cleanup
        self.content_cleanup_rules = [
            (r'^\s*\d+\s*$', ''),
            (r'^\s*[A-Z][a-z]+\s+\d+\s*$', ''),
            (r'\n\s*\n\s*\n', '\n\n'),
        ]
        
        # Generic tag mapping
        self.tag_mapping = {
            'overview': 'overview',
            'introduction': 'overview',
            'background': 'overview',
            'specification': 'specification',
            'requirement': 'requirement',
            'implementation': 'implementation',
            'testing': 'testing',
            'validation': 'validation',
            'reference': 'reference',
            'appendix': 'appendix',
            'annex': 'appendix'
        }
        
        self.toc_scan_pages = 10
        self.max_file_size_mb = 50

class IEEEStandardConfig(DocumentConfig):
    """Configuration for IEEE standards documents"""
    
    def __init__(self):
        super().__init__("ieee_standard")
        
        # IEEE-specific TOC patterns
        self.toc_patterns = [
            # IEEE standard format
            r'^(\d+(?:\.\d+)*)\s+(.*?)\s*\.+\s*(\d+)$',
            # Clause format
            r'^Clause\s+(\d+)\s+(.*?)\s*\.+\s*(\d+)$',
            # Subclause format
            r'^(\d+)\.(\d+)\s+(.*?)\s*\.+\s*(\d+)$',
            # Annex format
            r'^Annex\s+([A-Z])\s+(.*?)\s*\.+\s*(\d+)$',
            # Bibliography
            r'^Bibliography\s*\.+\s*(\d+)$'
        ]
        
        # IEEE content cleanup
        self.content_cleanup_rules = [
            (r'^\s*\d+\s*$', ''),
            (r'^\s*IEEE\s+Std\s+\d+.*?\s*$', ''),
            (r'^\s*Copyright\s+.*?\s*$', ''),
            (r'\n\s*\n\s*\n', '\n\n'),
        ]
        
        # IEEE tag mapping
        self.tag_mapping = {
            'scope': 'scope',
            'normative': 'normative',
            'informative': 'informative',
            'reference': 'reference',
            'definition': 'definition',
            'symbols': 'symbols',
            'abbreviations': 'abbreviations',
            'conformance': 'conformance',
            'test': 'testing',
            'measurement': 'measurement',
            'safety': 'safety',
            'environmental': 'environmental'
        }
        
        self.toc_scan_pages = 20
        self.max_file_size_mb = 200

def get_document_config(doc_type: str = "usb_pd") -> DocumentConfig:
    """Factory function to get document configuration"""
    
    configs = {
        "usb_pd": USBPDConfig,
        "generic": GenericTechSpecConfig,
        "ieee": IEEEStandardConfig
    }
    
    if doc_type not in configs:
        print(f"Warning: Unknown document type '{doc_type}', using generic config")
        doc_type = "generic"
    
    return configs[doc_type]()

def list_supported_document_types():
    """List all supported document types"""
    return [
        "usb_pd - USB Power Delivery specifications",
        "generic - Generic technical specifications",
        "ieee - IEEE standards documents"
    ]
