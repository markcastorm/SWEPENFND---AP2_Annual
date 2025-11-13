"""
Configuration file for AP2 Annual Financial Reports Scraper
Contains all headers and settings in exact order as per sample data
"""

# ============================================================================
# OUTPUT HEADERS - EXACT ORDER FROM SAMPLE DATA (DO NOT CHANGE ORDER!)
# ============================================================================
OUTPUT_HEADERS = [
    'Unnamed: 0',
    'AP2.FUNDCAPITALCARRIEDFORWARD.LEVEL.NONE.A.1@AP2',
    'AP2.NETOUTFLOWSTOTHENATIONALPENSIONSYSTEM.FLOW.NONE.A.1@AP2',
    'AP2.TOTAL.FLOW.NONE.A.1@AP2',
    'AP2.DOMESTICEQUITIES.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'AP2.DEVELOPEDEQUITIES.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'AP2.EMERGINGEQUITIES.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'AP2.DOMESTICEQUITIES.ACTUALALLOCATION.NONE.A.1@AP2',
    'AP2.DEVELOPEDEQUITIES.ACTUALALLOCATION.NONE.A.1@AP2',
    'AP2.EMEQUITIES.ACTUALALLOCATION.NONE.A.1@AP2',
    'AP2.EQUITIES.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'AP2.PRIVATEEQUITY.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'AP2.REALASSETS.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'AP2.FIXEDINCSECURITIES.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'AP2.GOVBONDSDEVMARKETS.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'AP2.CREDITBONDSDEVMARKETS.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'AP2.BONDSEMMARKETS.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'AP2.NONLISTEDCREDITS.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'AP2.OTHER.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'AP2.TOTAL.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'AP2.CURRENCYEXPOSURE.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'AP2.EQUITIES.ACTUALALLOCATION.NONE.A.1@AP2',
    'AP2.PRIVATEEQUITY.ACTUALALLOCATION.NONE.A.1@AP2',
    'AP2.REALASSETS.ACTUALALLOCATION.NONE.A.1@AP2',
    'AP2.FIXEDINCSECURITIES.ACTUALALLOCATION.NONE.A.1@AP2',
    'AP2.GOVBONDSDEVMARKETS.ACTUALALLOCATION.NONE.A.1@AP2',
    'AP2.CREDITBONDSDEVMARKETS.ACTUALALLOCATION.NONE.A.1@AP2',
    'AP2.BONDSEMMARKETS.ACTUALALLOCATION.NONE.A.1@AP2',
    'AP2.NONLISTEDCREDITS.ACTUALALLOCATION.NONE.A.1@AP2',
    'AP2.OTHER.ACTUALALLOCATION.NONE.A.1@AP2',
    'AP2.TOTAL.ACTUALALLOCATION.NONE.A.1@AP2',
    'AP2.CURRENCYEXPOSURE.ACTUALALLOCATION.NONE.A.1@AP2',
    'AP2.SUSTAINABLEINFRASTRUCTURE.ACTUALALLOCATION.NONE.A.1@AP2',
    'AP2.TRADITIONALREALESTATE.ACTUALALLOCATION.NONE.A.1@AP2',
    'AP2.NATURALCLIMATE.ACTUALALLOCATION.NONE.A.1@AP2',
    'AP2.NORTHAMERICA.ACTUALALLOCATION.NONE.A.1@AP2',
    'AP2.SOUTHAMERICA.ACTUALALLOCATION.NONE.A.1@AP2',
    'AP2.OCEANIA.ACTUALALLOCATION.NONE.A.1@AP2',
    'AP2.EUROPE.ACTUALALLOCATION.NONE.A.1@AP2',  # Changed from EUROPEEXCLSWEDEN
    'AP2.SWEDEN.ACTUALALLOCATION.NONE.A.1@AP2',
    'AP2.ASIA.ACTUALALLOCATION.NONE.A.1@AP2',
    'AP2.OTHERS.ACTUALALLOCATION.NONE.A.1@AP2',
    'AP2.SWEDISHGOV.ACTUALALLOCATION.NONE.A.1@AP2',  # Added
    'AP2.SWMUNICIPAL.ACTUALALLOCATION.NONE.A.1@AP2',  # Added
    'AP2.SWMORTGAGE.ACTUALALLOCATION.NONE.A.1@AP2',  # Added
    'AP2.FINCOMP.ACTUALALLOCATION.NONE.A.1@AP2',  # Added
    'AP2.NONFINCOMP.ACTUALALLOCATION.NONE.A.1@AP2',  # Added
    'AP2.FOREIGNBONDS.ACTUALALLOCATION.NONE.A.1@AP2',  # Added
    'AP2.FOREIGNBONDSOTHERFORISS.ACTUALALLOCATION.NONE.A.1@AP2',  # Added
    'AP2.TOTALBONDSISSUERCAT.ACTUALALLOCATION.NONE.A.1@AP2',  # Added
    'AP2.BONDSOTHER.ACTUALALLOCATION.NONE.A.1@AP2',  # Added
    'AP2.LOANSUNLISTED.ACTUALALLOCATION.NONE.A.1@AP2',  # Added
    'AP2.FUNDSFIXEDINCOME.ACTUALALLOCATION.NONE.A.1@AP2',  # Added
    'AP2.TOTALBONDS.TYPEINSTR.ACTUALALLOCATION.NONE.A.1@AP2',  # Added - NEW MISSING FIELD
]

# Human-readable sub-headers (Row 2 in Excel) - EXACT match to sample
OUTPUT_SUBHEADERS = [
    None,
    'AP2 annual: Fund capital carried forward',
    'AP2 annual: Net outflows to the national pension system',
    'AP2 annual: Net result for the year',
    'AP2 annual: Strategic portfolio - Swedish equities',
    'AP2 annual: Strategic portfolio - Developed markets equities',
    'AP2 annual: Strategic portfolio - Emerging markets equities',
    'AP2 annual: Exposure - Swedish equities',
    'AP2 annual: Exposure - Developed markets equities',
    'AP2 annual: Exposure - Emerging markets equities',
    'AP2 annual: Strategic portfolio - Equities',
    'AP2 annual: Strategic portfolio - Private Equity',
    'AP2 annual: Strategic portfolio - Real assets',
    'AP2 annual: Strategic portfolio - Fixed-income securities',
    'AP2 annual: Strategic portfolio - Government bonds in developed markets',
    'AP2 annual: Strategic portfolio - Credit bonds in developed markets',
    'AP2 annual: Strategic portfolio - Bonds in emerging markets',
    'AP2 annual: Strategic portfolio - Non-listed credits',
    'AP2 annual: Strategic portfolio - Other',
    'AP2 annual: Strategic portfolio - Total',
    'AP2 annual: Strategic portfolio - Currency exposure',
    'AP2 annual: Exposure - Equities',
    'AP2 annual: Alternative investments - Private equity',
    'AP2 annual: Exposure - Real assets',
    'AP2 annual: Exposure - Fixed-income securities',
    'AP2 annual: Exposure - Government bonds in developed markets',
    'AP2 annual: Exposure - Credit bonds in developed markets',
    'AP2 annual: Exposure - Bonds in emerging markets',
    'AP2 annual: Exposure - Non-listed credits',
    'AP2 annual: Exposure - Other',
    'AP2 annual: Exposure - Total',
    'AP2 annual: Exposure - Currency exposure',
    'AP2 annual: Alternative investments - Sustainable infrastructure',
    'AP2 annual: Real Assets, Portfolio distribution - Traditional real estate',
    'AP2 annual: Real Assets, Portfolio distribution - Natural Climate Solutions',
    'AP2 annual: Real Assets, Geographical distribution - North America',
    'AP2 annual: Real Assets, Geographical distribution - South America',
    'AP2 annual: Real Assets, Geographical distribution - Oceania',
    'AP2 annual: Real Assets, Geographical distribution - Europe',  # Changed from Europe (excl. Sweden)
    'AP2 annual: Real Assets, Geographical distribution - Sweden',
    'AP2 annual: Real Assets, Geographical distribution - Asia',
    'AP2 annual: Real Assets, Geographical distribution - Others',
    'AP2 annual: Bonds and other fixed-income securities, Swedish Government',  # Added
    'AP2 annual: Bonds and other fixed-income securities, Swedish municipalities',  # Added
    'AP2 annual: Bonds and other fixed-income securities, Swedish mortgage institutions',  # Added
    'AP2 annual: Bonds and other fixed-income securities, Financial companies',  # Added
    'AP2 annual: Bonds and other fixed-income securities, Non-financial companies',  # Added
    'AP2 annual: Bonds and other fixed-income securities, Foreign governments',  # Added
    'AP2 annual: Bonds and other fixed-income securities, Other foreign issuers',  # Added
    'AP2 annual: Bonds and other fixed-income securities, Total (Issuer Category)',  # Added
    'AP2 annual: Bonds and other fixed-income securities, Other bonds',  # Added
    'AP2 annual: Bonds and other fixed-income securities, Unlisted loans',  # Added
    'AP2 annual: Bonds and other fixed-income securities, Participations in foreign fixed-income funds',  # Added
    'AP2 annual: Bonds and other fixed-income securities, Total (Instrument Type)',  # Added - NEW MISSING FIELD
]

# Readable header mapping for reference
HEADER_MAPPING = {
    'Fund Capital Carried Forward (Level)': 'AP2.FUNDCAPITALCARRIEDFORWARD.LEVEL.NONE.A.1@AP2',
    'Net Outflows to National Pension System': 'AP2.NETOUTFLOWSTOTHENATIONALPENSIONSYSTEM.FLOW.NONE.A.1@AP2',
    'Total': 'AP2.TOTAL.FLOW.NONE.A.1@AP2',
    'Domestic Equities (Strategic Portfolio)': 'AP2.DOMESTICEQUITIES.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'Developed Equities (Strategic Portfolio)': 'AP2.DEVELOPEDEQUITIES.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'Emerging Equities (Strategic Portfolio)': 'AP2.EMERGINGEQUITIES.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'Domestic Equities (Exposure)': 'AP2.DOMESTICEQUITIES.ACTUALALLOCATION.NONE.A.1@AP2',
    'Developed Equities (Exposure)': 'AP2.DEVELOPEDEQUITIES.ACTUALALLOCATION.NONE.A.1@AP2',
    'Emerging Equities (Exposure)': 'AP2.EMEQUITIES.ACTUALALLOCATION.NONE.A.1@AP2',
    'Equities (Strategic Portfolio)': 'AP2.EQUITIES.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'Private Equity (Strategic Portfolio)': 'AP2.PRIVATEEQUITY.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'Real Assets (Strategic Portfolio)': 'AP2.REALASSETS.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'Fixed-income Securities (Strategic Portfolio)': 'AP2.FIXEDINCSECURITIES.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'Government Bonds Developed Markets (Strategic Portfolio)': 'AP2.GOVBONDSDEVMARKETS.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'Credit Bonds Developed Markets (Strategic Portfolio)': 'AP2.CREDITBONDSDEVMARKETS.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'Bonds Emerging Markets (Strategic Portfolio)': 'AP2.BONDSEMMARKETS.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'Non-listed Credits (Strategic Portfolio)': 'AP2.NONLISTEDCREDITS.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'Other (Strategic Portfolio)': 'AP2.OTHER.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'Total (Strategic Portfolio)': 'AP2.TOTAL.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'Currency Exposure (Strategic Portfolio)': 'AP2.CURRENCYEXPOSURE.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2',
    'Equities (Exposure)': 'AP2.EQUITIES.ACTUALALLOCATION.NONE.A.1@AP2',
    'Private Equity (Alternative Investments)': 'AP2.PRIVATEEQUITY.ACTUALALLOCATION.NONE.A.1@AP2',
    'Real Assets (Exposure)': 'AP2.REALASSETS.ACTUALALLOCATION.NONE.A.1@AP2',
    'Fixed-income Securities (Exposure)': 'AP2.FIXEDINCSECURITIES.ACTUALALLOCATION.NONE.A.1@AP2',
    'Government Bonds Developed Markets (Exposure)': 'AP2.GOVBONDSDEVMARKETS.ACTUALALLOCATION.NONE.A.1@AP2',
    'Credit Bonds Developed Markets (Exposure)': 'AP2.CREDITBONDSDEVMARKETS.ACTUALALLOCATION.NONE.A.1@AP2',
    'Bonds Emerging Markets (Exposure)': 'AP2.BONDSEMMARKETS.ACTUALALLOCATION.NONE.A.1@AP2',
    'Non-listed Credits (Exposure)': 'AP2.NONLISTEDCREDITS.ACTUALALLOCATION.NONE.A.1@AP2',
    'Other (Exposure)': 'AP2.OTHER.ACTUALALLOCATION.NONE.A.1@AP2',
    'Total (Exposure)': 'AP2.TOTAL.ACTUALALLOCATION.NONE.A.1@AP2',
    'Currency Exposure (Exposure)': 'AP2.CURRENCYEXPOSURE.ACTUALALLOCATION.NONE.A.1@AP2',
    'Sustainable Infrastructure (Alternative Investments)': 'AP2.SUSTAINABLEINFRASTRUCTURE.ACTUALALLOCATION.NONE.A.1@AP2',
    'Traditional Real Estate (Real Assets Portfolio distribution)': 'AP2.TRADITIONALREALESTATE.ACTUALALLOCATION.NONE.A.1@AP2',
    'Natural Climate Solutions (Real Assets Portfolio distribution)': 'AP2.NATURALCLIMATE.ACTUALALLOCATION.NONE.A.1@AP2',
    'North America (Real Assets Geographical distribution)': 'AP2.NORTHAMERICA.ACTUALALLOCATION.NONE.A.1@AP2',
    'South America (Real Assets Geographical distribution)': 'AP2.SOUTHAMERICA.ACTUALALLOCATION.NONE.A.1@AP2',
    'Oceania (Real Assets Geographical distribution)': 'AP2.OCEANIA.ACTUALALLOCATION.NONE.A.1@AP2',
    'Europe (Real Assets Geographical distribution)': 'AP2.EUROPE.ACTUALALLOCATION.NONE.A.1@AP2',
    'Sweden (Real Assets Geographical distribution)': 'AP2.SWEDEN.ACTUALALLOCATION.NONE.A.1@AP2',
    'Asia (Real Assets Geographical distribution)': 'AP2.ASIA.ACTUALALLOCATION.NONE.A.1@AP2',
    'Others (Real Assets Geographical distribution)': 'AP2.OTHERS.ACTUALALLOCATION.NONE.A.1@AP2',
    'Swedish Government (Bonds and other fixed-income securities)': 'AP2.SWEDISHGOV.ACTUALALLOCATION.NONE.A.1@AP2',  # Added
    'Swedish Municipalities (Bonds and other fixed-income securities)': 'AP2.SWMUNICIPAL.ACTUALALLOCATION.NONE.A.1@AP2',  # Added
    'Swedish Mortgage Institutions (Bonds and other fixed-income securities)': 'AP2.SWMORTGAGE.ACTUALALLOCATION.NONE.A.1@AP2',  # Added
    'Financial Companies (Bonds and other fixed-income securities)': 'AP2.FINCOMP.ACTUALALLOCATION.NONE.A.1@AP2',  # Added
    'Non-financial Companies (Bonds and other fixed-income securities)': 'AP2.NONFINCOMP.ACTUALALLOCATION.NONE.A.1@AP2',  # Added
    'Foreign Governments (Bonds and other fixed-income securities)': 'AP2.FOREIGNBONDS.ACTUALALLOCATION.NONE.A.1@AP2',  # Added
    'Other Foreign Issuers (Bonds and other fixed-income securities)': 'AP2.FOREIGNBONDSOTHERFORISS.ACTUALALLOCATION.NONE.A.1@AP2',  # Added
    'Total Issuer Category (Bonds and other fixed-income securities)': 'AP2.TOTALBONDSISSUERCAT.ACTUALALLOCATION.NONE.A.1@AP2',  # Added
    'Other Bonds (Bonds and other fixed-income securities)': 'AP2.BONDSOTHER.ACTUALALLOCATION.NONE.A.1@AP2',  # Added
    'Unlisted Loans (Bonds and other fixed-income securities)': 'AP2.LOANSUNLISTED.ACTUALALLOCATION.NONE.A.1@AP2',  # Added
    'Participations in foreign fixed-income funds (Bonds and other fixed-income securities)': 'AP2.FUNDSFIXEDINCOME.ACTUALALLOCATION.NONE.A.1@AP2',  # Added
    'Total Instrument Type (Bonds and other fixed-income securities)': 'AP2.TOTALBONDS.TYPEINSTR.ACTUALALLOCATION.NONE.A.1@AP2',  # Added - NEW MISSING FIELD
}

# ============================================================================
# SCRAPER CONFIGURATION
# ============================================================================

# Target website
BASE_URL = 'https://ap2.se/en/news-and-reports/reports/financial-reports/'

# Target year for scraping (can be a year like 2024, or "latest" for most recent)
TARGET_YEAR = 2024  # Changed from "latest" to 2024

# Multiple years scraping (overrides TARGET_YEAR if set)
# YEARS_TO_SCRAPE = [2024, 2023, 2022]  # Can be a list of years
YEARS_TO_SCRAPE = None  # Set to None to use TARGET_YEAR setting

# Report types to download
REPORT_TYPES = {
    'annual': True,      # Download Annual Reports
    'half_year': False,   # Download Half-year Reports
    'year_end': False    # Download Year-end Reports (rare, only some years)
}

# ============================================================================
# FOLDER STRUCTURE CONFIGURATION
# ============================================================================

# Base project directory (auto-detected)
import os
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Folder names
LOGS_FOLDER = "logs"
DOWNLOADS_FOLDER = "downloads"
OUTPUT_FOLDER = "output"
LATEST_FOLDER_NAME = "latest"

# Full paths (auto-generated)
LOGS_DIR = os.path.join(PROJECT_ROOT, LOGS_FOLDER)
DOWNLOADS_DIR = os.path.join(PROJECT_ROOT, DOWNLOADS_FOLDER)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, OUTPUT_FOLDER)

# ============================================================================
# PDF PARSING CONFIGURATION
# ============================================================================

# Table keywords to search for in PDFs
TABLE_KEYWORDS = [
    'balance sheet',
    'statement of financial position',
    'assets and liabilities',
    'fund capital',
    'total assets',
    'income statement',
    'statement of comprehensive income',
    'strategic allocation',
    'actual allocation',
    'portfolio distribution',
    'geographical distribution'
]

# PDF parsing settings
PDF_PARSING = {
    'use_tabula': True,      # Use tabula-py for table extraction
    'use_camelot': True,     # Use camelot for table extraction (fallback)
    'multiple_tables': True,  # Extract multiple tables from each PDF
    'lattice_mode': True,    # Use lattice mode for tables with borders
    'stream_mode': True,     # Use stream mode for tables without borders
}

# ============================================================================
# SELENIUM/BROWSER CONFIGURATION
# ============================================================================

SELENIUM_CONFIG = {
    'implicit_wait': 10,        # Implicit wait time in seconds
    'page_load_timeout': 30,    # Page load timeout
    'download_timeout': 120,    # Download completion timeout
    'use_undetected_chrome': True,  # Use undetected_chromedriver
}

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOGGING_CONFIG = {
    'log_level': 'INFO',  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
    'log_format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'log_to_console': True,
    'log_to_file': True,
}

# ============================================================================
# OUTPUT FILE CONFIGURATION
# ============================================================================

OUTPUT_CONFIG = {
    'output_format': 'xlsx',  # Options: 'xlsx', 'csv', 'both'
    'include_metadata': True,  # Include metadata sheet with run information
    'preserve_formatting': True,  # Preserve number formatting
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_timestamp():
    """Generate timestamp for folder naming"""
    from datetime import datetime
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def get_run_folders(timestamp=None):
    """Get folder paths for a specific run"""
    if timestamp is None:
        timestamp = get_timestamp()

    return {
        'timestamp': timestamp,
        'logs': os.path.join(LOGS_DIR, timestamp),
        'downloads': os.path.join(DOWNLOADS_DIR, timestamp),
        'output': os.path.join(OUTPUT_DIR, timestamp),
        'latest_output': os.path.join(OUTPUT_DIR, LATEST_FOLDER_NAME)
    }

def create_run_folders(timestamp=None):
    """Create all necessary folders for a run"""
    folders = get_run_folders(timestamp)

    for folder_path in [folders['logs'], folders['downloads'], folders['output'], folders['latest_output']]:
        os.makedirs(folder_path, exist_ok=True)

    return folders

# ============================================================================
# VALIDATION
# ============================================================================

def validate_config():
    """Validate configuration settings"""
    errors = []

    # Validate headers
    if len(OUTPUT_HEADERS) != len(OUTPUT_SUBHEADERS):
        errors.append(f"Mismatch between OUTPUT_HEADERS ({len(OUTPUT_HEADERS)}) and OUTPUT_SUBHEADERS ({len(OUTPUT_SUBHEADERS)})")

    # Validate year settings - be flexible with string/int
    if TARGET_YEAR is not None:
        if isinstance(TARGET_YEAR, str) and TARGET_YEAR.lower() != "latest":
            try:
                int(TARGET_YEAR)
            except ValueError:
                errors.append(f"TARGET_YEAR must be 'latest' or a year number, got '{TARGET_YEAR}'")

    # Validate report types
    if not any(REPORT_TYPES.values()):
        errors.append("At least one report type must be enabled")

    if errors:
        raise ValueError("Configuration validation failed:\n" + "\n".join(errors))

    return True

# Validate on import
validate_config()