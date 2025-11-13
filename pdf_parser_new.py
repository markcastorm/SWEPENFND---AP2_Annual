"""
AP2 PDF Parser - New Robust Version
Keyword-based text extraction with LLM fallback
Built based on manual analysis of AP2 annual reports
"""

import os
import re
import sys
import glob
import json
import logging
import pandas as pd
from datetime import datetime

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF not installed. Install with: pip install PyMuPDF --break-system-packages")
    sys.exit(1)

import config
from perfect_llm_parser import PerfectLLMParser

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RobustPDFParser:
    """
    A robust PDF parser that uses keyword-based text extraction as primary method
    with LLM extraction as fallback when text parsing fails.
    """
    
    def __init__(self):
        self.logger = logger
        self.llm_extractor = None
        
        # Initialize Perfect LLM extractor as primary method
        try:
            self.perfect_llm = PerfectLLMParser()
            self.logger.info("Perfect LLM parser initialized successfully")
        except Exception as e:
            self.logger.error(f"Perfect LLM parser initialization failed: {e}")
            self.perfect_llm = None
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF with better handling"""
        try:
            with fitz.open(pdf_path) as doc:
                full_text = ""
                page_texts = []
                
                for page_num, page in enumerate(doc):
                    # Try multiple text extraction methods
                    text_methods = [
                        lambda p: p.get_text("text", flags=fitz.TEXT_PRESERVE_LIGATURES),
                        lambda p: p.get_text("dict"),
                        lambda p: p.get_text("blocks")
                    ]
                    
                    page_text = ""
                    for method in text_methods:
                        try:
                            result = method(page)
                            if isinstance(result, str) and result.strip():
                                page_text = result
                                break
                            elif isinstance(result, dict):
                                # Extract text from dict format
                                page_text = self._extract_text_from_dict(result)
                                if page_text.strip():
                                    break
                            elif isinstance(result, list):
                                # Extract text from blocks format
                                page_text = "\n".join([block[4] if len(block) > 4 and isinstance(block[4], str) else "" for block in result])
                                if page_text.strip():
                                    break
                        except Exception:
                            continue
                    
                    page_texts.append(page_text)
                    full_text += f"\n--- PAGE {page_num + 1} ---\n" + page_text + "\n"
                
                self.logger.info(f"Extracted text from {len(page_texts)} pages")
                return full_text, page_texts
                
        except Exception as e:
            self.logger.error(f"Error extracting text from PDF: {e}")
            return "", []
    
    def _extract_text_from_dict(self, text_dict):
        """Extract text from PyMuPDF dict format"""
        text = ""
        if 'blocks' in text_dict:
            for block in text_dict['blocks']:
                if 'lines' in block:
                    for line in block['lines']:
                        if 'spans' in line:
                            for span in line['spans']:
                                if 'text' in span:
                                    text += span['text'] + " "
                        text += "\n"
        return text
    
    def find_section_pages(self, page_texts, section_keywords, min_score=2):
        """Find pages containing specific section keywords"""
        matching_pages = []
        
        for page_num, text in enumerate(page_texts):
            if not text:
                continue
                
            text_lower = text.lower()
            score = 0
            
            # Count keyword matches
            for keyword in section_keywords:
                if keyword.lower() in text_lower:
                    score += 1
            
            # Also check for exact phrase matches
            exact_phrases = [" ".join(section_keywords[:2]), " ".join(section_keywords[1:3])]
            for phrase in exact_phrases:
                if phrase.lower() in text_lower:
                    score += 2
            
            if score >= min_score:
                matching_pages.append((page_num + 1, score, text))
        
        # Sort by score (highest first)
        matching_pages.sort(key=lambda x: x[1], reverse=True)
        return matching_pages
    
    def clean_number_value(self, value_str):
        """Clean and convert number strings to float"""
        if not value_str:
            return None
            
        # Remove common formatting
        cleaned = re.sub(r'[^\d.,\-–−()]', '', str(value_str))
        
        # Handle Swedish/European number formatting
        if ',' in cleaned and '.' in cleaned:
            # Both comma and period present, assume comma is thousands separator
            cleaned = cleaned.replace(',', '')
        elif ',' in cleaned:
            # Only comma, assume it's decimal separator
            cleaned = cleaned.replace(',', '.')
        
        # Handle negative numbers in parentheses
        if cleaned.startswith('(') and cleaned.endswith(')'):
            cleaned = '-' + cleaned[1:-1]
        
        # Handle different dash types for negative numbers
        cleaned = re.sub(r'^[–−]', '-', cleaned)
        
        try:
            return float(cleaned)
        except (ValueError, TypeError):
            return None
    
    def extract_fund_capital_section(self, page_texts, year):
        """Extract Fund Capital, flows and results data"""
        self.logger.info("Extracting Fund capital, flows and results...")
        
        # Keywords for finding the five-year overview section
        keywords = ['five', 'year', 'overview', 'fund', 'capital', 'flows', 'results']
        matching_pages = self.find_section_pages(page_texts, keywords, min_score=3)
        
        data = {}
        target_year = str(year)
        
        for page_num, score, text in matching_pages:
            self.logger.info(f"Searching page {page_num} (score: {score})")
            
            # Look for the table structure
            lines = text.split('\n')
            year_line_idx = -1
            
            # Find year headers
            for i, line in enumerate(lines):
                if target_year in line and any(x in line.lower() for x in ['2024', '2023', '2022']):
                    year_line_idx = i
                    break
            
            if year_line_idx == -1:
                continue
                
            # Extract patterns around the year line
            search_lines = lines[max(0, year_line_idx-10):year_line_idx+20]
            
            # Patterns to match based on screenshots
            patterns = {
                'AP2.FUNDCAPITALCARRIEDFORWARD.LEVEL.NONE.A.1@AP2': [
                    r'fund\s+capital[\s\n]*(\d+[\s,]*\d*)',
                    r'(\d+[\s,]*\d+).*fund.*capital'
                ],
                'AP2.NETOUTFLOWSTOTHENATIONALPENSIONSYSTEM.FLOW.NONE.A.1@AP2': [
                    r'net\s+outflows.*(\-?\d+[\s,]*\d*)',
                    r'outflows.*pension.*(\-?\d+[\s,]*\d*)'
                ],
                'AP2.TOTAL.FLOW.NONE.A.1@AP2': [
                    r'net\s+result.*year[\s\n]*(\d+[\s,]*\d*)',
                    r'result.*(\d+[\s,]*\d+)'
                ]
            }
            
            combined_text = '\n'.join(search_lines).lower()
            
            for field_key, regex_list in patterns.items():
                if field_key in data:
                    continue
                    
                for pattern in regex_list:
                    match = re.search(pattern, combined_text, re.IGNORECASE | re.DOTALL)
                    if match:
                        value = self.clean_number_value(match.group(1))
                        if value is not None:
                            data[field_key] = value
                            self.logger.info(f"Found {field_key}: {value}")
                            break
        
        return data
    
    def extract_asset_allocation_section(self, page_texts, year):
        """Extract Asset class exposure data"""
        self.logger.info("Extracting Asset class exposure...")
        
        # Keywords for finding asset allocation table
        keywords = ['asset', 'class', 'exposure', 'strategic', 'portfolio', 'allocation']
        matching_pages = self.find_section_pages(page_texts, keywords, min_score=3)
        
        data = {}
        
        # Mapping of config keys to text patterns
        field_patterns = {
            # Strategic Portfolio fields
            'AP2.DOMESTICEQUITIES.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2': ['swedish equities', 'domestic equities'],
            'AP2.DEVELOPEDEQUITIES.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2': ['developed markets equities', 'developed equities'],
            'AP2.EMERGINGEQUITIES.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2': ['emerging markets equities', 'emerging equities'],
            'AP2.PRIVATEEQUITY.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2': ['private equity'],
            'AP2.REALASSETS.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2': ['real assets'],
            'AP2.GOVBONDSDEVMARKETS.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2': ['government bonds', 'govt bonds'],
            'AP2.CREDITBONDSDEVMARKETS.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2': ['credit bonds'],
            'AP2.BONDSEMMARKETS.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2': ['bonds in emerging', 'emerging markets bonds'],
            'AP2.NONLISTEDCREDITS.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2': ['non-listed credits', 'unlisted credits'],
            'AP2.TOTAL.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2': ['total'],
            'AP2.CURRENCYEXPOSURE.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2': ['currency exposure'],
            
            # Actual Portfolio fields (similar patterns)
            'AP2.DOMESTICEQUITIES.ACTUALALLOCATION.NONE.A.1@AP2': ['swedish equities', 'domestic equities'],
            'AP2.DEVELOPEDEQUITIES.ACTUALALLOCATION.NONE.A.1@AP2': ['developed markets equities', 'developed equities'],
            'AP2.EMEQUITIES.ACTUALALLOCATION.NONE.A.1@AP2': ['emerging markets equities', 'emerging equities'],
        }
        
        for page_num, score, text in matching_pages:
            self.logger.info(f"Processing asset allocation on page {page_num} (score: {score})")
            
            lines = text.split('\n')
            
            # Look for table structure with percentages
            for field_key, patterns in field_patterns.items():
                if field_key in data:
                    continue
                    
                for pattern in patterns:
                    # Find lines containing the pattern
                    for line in lines:
                        line_lower = line.lower()
                        if pattern in line_lower:
                            # Look for percentages in the same line or nearby
                            numbers = re.findall(r'\b(\d{1,2}(?:\.\d)?)\b', line)
                            if numbers:
                                # Take the first reasonable percentage
                                for num in numbers:
                                    val = float(num)
                                    if 0 <= val <= 100:  # Valid percentage range
                                        data[field_key] = val
                                        self.logger.info(f"Found {field_key}: {val}%")
                                        break
                            break
        
        return data
    
    def extract_real_assets_section(self, page_texts, year):
        """Extract Real assets distribution data"""
        self.logger.info("Extracting Real assets distribution...")
        
        keywords = ['real', 'assets', 'portfolio', 'distribution', 'geographical']
        matching_pages = self.find_section_pages(page_texts, keywords, min_score=2)
        
        data = {}
        
        # Field patterns for real assets
        field_patterns = {
            'AP2.SUSTAINABLEINFRASTRUCTURE.ACTUALALLOCATION.NONE.A.1@AP2': ['sustainable infrastructure', 'infrastructure'],
            'AP2.TRADITIONALREALESTATE.ACTUALALLOCATION.NONE.A.1@AP2': ['traditional real estate', 'real estate'],
            'AP2.NATURALCLIMATE.ACTUALALLOCATION.NONE.A.1@AP2': ['natural climate', 'climate solutions'],
            'AP2.NORTHAMERICA.ACTUALALLOCATION.NONE.A.1@AP2': ['north america'],
            'AP2.SOUTHAMERICA.ACTUALALLOCATION.NONE.A.1@AP2': ['south america'],
            'AP2.OCEANIA.ACTUALALLOCATION.NONE.A.1@AP2': ['oceania'],
            'AP2.EUROPE.ACTUALALLOCATION.NONE.A.1@AP2': ['europe'],
            'AP2.SWEDEN.ACTUALALLOCATION.NONE.A.1@AP2': ['sweden'],
            'AP2.ASIA.ACTUALALLOCATION.NONE.A.1@AP2': ['asia'],
            'AP2.OTHERS.ACTUALALLOCATION.NONE.A.1@AP2': ['others'],
        }
        
        for page_num, score, text in matching_pages:
            lines = text.split('\n')
            
            for field_key, patterns in field_patterns.items():
                if field_key in data:
                    continue
                    
                for pattern in patterns:
                    for line in lines:
                        line_lower = line.lower()
                        if pattern in line_lower:
                            # Extract percentage values
                            numbers = re.findall(r'\b(\d{1,2}(?:\.\d)?)\b', line)
                            if numbers:
                                for num in numbers:
                                    val = float(num)
                                    if 0 <= val <= 100:
                                        data[field_key] = val
                                        self.logger.info(f"Found {field_key}: {val}%")
                                        break
                            break
        
        return data
    
    def extract_bonds_section(self, page_texts, year):
        """Extract Bonds and other fixed-income securities data"""
        self.logger.info("Extracting Bonds and other fixed-income securities...")
        
        keywords = ['bonds', 'fixed-income', 'securities', 'government', 'mortgage']
        matching_pages = self.find_section_pages(page_texts, keywords, min_score=2)
        
        data = {}
        
        # Field patterns for bonds
        field_patterns = {
            'AP2.SWEDISHGOV.ACTUALALLOCATION.NONE.A.1@AP2': ['swedish government'],
            'AP2.SWMUNICIPAL.ACTUALALLOCATION.NONE.A.1@AP2': ['swedish municipalities'],
            'AP2.SWMORTGAGE.ACTUALALLOCATION.NONE.A.1@AP2': ['swedish mortgage', 'mortgage institutions'],
            'AP2.FINCOMP.ACTUALALLOCATION.NONE.A.1@AP2': ['financial companies'],
            'AP2.NONFINCOMP.ACTUALALLOCATION.NONE.A.1@AP2': ['non-financial companies'],
            'AP2.FOREIGNBONDS.ACTUALALLOCATION.NONE.A.1@AP2': ['foreign governments'],
            'AP2.FOREIGNBONDSOTHERFORISS.ACTUALALLOCATION.NONE.A.1@AP2': ['other foreign issuers'],
            'AP2.BONDSOTHER.ACTUALALLOCATION.NONE.A.1@AP2': ['other bonds'],
            'AP2.LOANSUNLISTED.ACTUALALLOCATION.NONE.A.1@AP2': ['unlisted loans'],
            'AP2.FUNDSFIXEDINCOME.ACTUALALLOCATION.NONE.A.1@AP2': ['participations in foreign', 'fixed-income funds'],
        }
        
        for page_num, score, text in matching_pages:
            lines = text.split('\n')
            
            for field_key, patterns in field_patterns.items():
                if field_key in data:
                    continue
                    
                for pattern in patterns:
                    for line in lines:
                        line_lower = line.lower()
                        if pattern in line_lower:
                            # Look for large numbers (bond values in millions)
                            numbers = re.findall(r'\b(\d{1,6}(?:[\s,]\d{3})*)\b', line)
                            if numbers:
                                for num_str in numbers:
                                    cleaned_num = self.clean_number_value(num_str)
                                    if cleaned_num and cleaned_num > 10:  # Reasonable bond amount
                                        data[field_key] = cleaned_num
                                        self.logger.info(f"Found {field_key}: {cleaned_num}")
                                        break
                            break
        
        return data
    
    def extract_data_with_llm_fallback(self, pdf_path, section_name, year, text_data):
        """Use LLM as fallback when text extraction fails"""
        if not self.llm_extractor or not self.llm_extractor.client:
            self.logger.warning("LLM fallback not available")
            return {}
        
        self.logger.info(f"Using LLM fallback for {section_name}")
        
        try:
            return self.llm_extractor.extract_section_data(pdf_path, section_name, year)
        except Exception as e:
            self.logger.error(f"LLM fallback failed for {section_name}: {e}")
            return {}
    
    def parse_annual_report(self, pdf_path):
        """Main method to parse a single annual report using Perfect LLM extraction"""
        year = self.extract_year_from_filename(pdf_path)
        self.logger.info(f"Processing {os.path.basename(pdf_path)} with Perfect LLM Parser (Year: {year})")
        
        if not self.perfect_llm:
            self.logger.error("Perfect LLM parser not available - cannot proceed")
            return {}
        
        try:
            # Use Perfect LLM extraction for all sections
            result = self.perfect_llm.extract_all_sections(pdf_path)
            
            # Count total fields across all years
            total_fields = sum(len(data) for data in result.values())
            expected_fields = len(config.OUTPUT_HEADERS) - 1 + 11  # Minus index column + 2023 bonds
            accuracy = (total_fields / expected_fields * 100) if expected_fields > 0 else 0
            
            self.logger.info(f"Perfect LLM extraction completed: {total_fields}/{expected_fields} fields ({accuracy:.1f}%)")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Perfect LLM extraction failed: {e}")
            return {year: {}}
    
    def extract_year_from_filename(self, filename):
        """Extract year from filename"""
        basename = os.path.basename(filename)
        match = re.search(r'(\d{4})', basename)
        if match:
            year = int(match.group(1))
            if 2000 <= year <= datetime.now().year + 1:
                return year
        return datetime.now().year

def find_latest_download_folder():
    """Find the most recent download folder"""
    try:
        download_folders = glob.glob(os.path.join(config.DOWNLOADS_DIR, '*'))
        if not download_folders:
            logger.error("No download folders found")
            return None
        latest_folder = max(download_folders, key=os.path.getmtime)
        logger.info(f"Processing folder: {latest_folder}")
        return latest_folder
    except Exception as e:
        logger.error(f"Error finding download folder: {e}")
        return None

def create_output(all_data):
    """Create Excel output file"""
    logger.info("Creating output file...")
    
    # Create DataFrame
    df = pd.DataFrame.from_dict(all_data, orient='index')
    df.index.name = 'Unnamed: 0'
    df.reset_index(inplace=True)
    
    # Ensure all columns from config are present
    for col in config.OUTPUT_HEADERS:
        if col not in df.columns:
            df[col] = None
    df = df[config.OUTPUT_HEADERS]
    
    # Create output folders
    run_folders = config.create_run_folders()
    output_folder = run_folders['output']
    latest_folder = run_folders['latest_output']
    
    timestamp = run_folders['timestamp']
    output_filename = f"AP2_Annual_Financial_Data_{timestamp}.xlsx"
    output_filepath = os.path.join(output_folder, output_filename)
    latest_filepath = os.path.join(latest_folder, 'AP2_Annual_Financial_Data_latest.xlsx')
    
    # Save to Excel
    with pd.ExcelWriter(output_filepath, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, header=config.OUTPUT_SUBHEADERS, startrow=1)
        # Write main headers
        ws = writer.sheets['Sheet1']
        for idx, header in enumerate(config.OUTPUT_HEADERS):
            ws.cell(row=1, column=idx+1).value = header
    
    # Copy to latest
    import shutil
    shutil.copy(output_filepath, latest_filepath)
    
    filled_cells = df.notna().sum().sum() - len(df)  # Subtract index column
    total_cells = len(config.OUTPUT_HEADERS) - 1  # Subtract index column
    accuracy = (filled_cells / total_cells * 100) if total_cells > 0 else 0
    
    logger.info(f"✓ Output saved: {output_filepath}")
    logger.info(f"✓ Latest copy: {latest_filepath}")
    logger.info(f"✓ Filled {filled_cells}/{total_cells} cells ({accuracy:.1f}%)")
    
    return output_filepath

def main():
    """Main execution function"""
    logger.info("=" * 80)
    logger.info("AP2 PDF Parser - New Robust Version")
    logger.info("=" * 80)
    
    # Find latest download folder
    latest_folder = find_latest_download_folder()
    if not latest_folder:
        return
    
    # Find PDF files
    pdf_files = glob.glob(os.path.join(latest_folder, '*.pdf'))
    if not pdf_files:
        logger.error(f"No PDF files found in {latest_folder}")
        return
    
    logger.info(f"Found {len(pdf_files)} PDF file(s)")
    
    # Initialize parser
    parser = RobustPDFParser()
    all_data = {}
    
    # Process each PDF
    for pdf_path in pdf_files:
        try:
            data = parser.parse_annual_report(pdf_path)
            all_data.update(data)
        except Exception as e:
            logger.error(f"Failed to process {pdf_path}: {e}")
    
    if all_data:
        # Create output
        output_file = create_output(all_data)
        logger.info(f"✓ Processing completed successfully")
        logger.info(f"✓ Output: {output_file}")
    else:
        logger.error("No data extracted from any PDF files")

if __name__ == "__main__":
    main()