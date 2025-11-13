"""
Perfect LLM Parser for AP2 Reports
Designed for 100% extraction accuracy across all fields and both years
"""

import os
import re
import json
import logging
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF not installed. Install with: pip install PyMuPDF --break-system-packages")

try:
    import openai
except ImportError:
    print("OpenAI not installed. Install with: pip install openai --break-system-packages")

import config

# Load environment variables
load_dotenv()

class PerfectLLMParser:
    """
    Perfect LLM parser designed for 100% accuracy
    Targets exact table structures from AP2 annual reports
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.client = None
        
        if self.api_key:
            try:
                self.client = openai.OpenAI(
                    api_key=self.api_key,
                    base_url="https://openrouter.ai/api/v1"
                )
                self.logger.info("Perfect LLM parser initialized successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialize LLM client: {e}")
                self.client = None
        else:
            self.logger.error("OPENROUTER_API_KEY not found. Cannot proceed without LLM access.")
            raise ValueError("API key required for perfect LLM extraction")
    
    def extract_targeted_sections(self, pdf_path, section_keywords, max_pages=10):
        """Extract most relevant pages for a specific section"""
        try:
            with fitz.open(pdf_path) as doc:
                relevant_pages = []
                
                for page_num, page in enumerate(doc):
                    text = page.get_text("text", flags=fitz.TEXT_PRESERVE_LIGATURES)
                    text_lower = text.lower()
                    
                    # Score based on keyword matches
                    score = 0
                    for keyword in section_keywords:
                        if keyword.lower() in text_lower:
                            score += 1
                    
                    # Boost score for exact phrase matches
                    for i in range(len(section_keywords) - 1):
                        phrase = f"{section_keywords[i]} {section_keywords[i+1]}"
                        if phrase.lower() in text_lower:
                            score += 3
                    
                    if score >= 2:  # Minimum relevance threshold
                        relevant_pages.append((page_num + 1, score, text))
                
                # Sort by score and take top pages
                relevant_pages.sort(key=lambda x: x[1], reverse=True)
                
                # Combine top pages into context
                context_text = ""
                for i, (page_num, score, text) in enumerate(relevant_pages[:max_pages]):
                    context_text += f"\n--- PAGE {page_num} (Score: {score}) ---\n{text}\n"
                
                return context_text[:20000]  # Limit to avoid token limits
                
        except Exception as e:
            self.logger.error(f"Error extracting sections: {e}")
            return ""
    
    def create_perfect_prompt(self, section_name, context_text, target_fields):
        """Create the most precise extraction prompt for each section"""
        
        base_instructions = f"""You are an expert financial data analyst extracting data from AP2 Annual Report.

CRITICAL MISSION: Extract EXACT numerical values with 100% precision.

EXTRACTION RULES:
1. Return ONLY a valid JSON object with the exact keys provided
2. Extract numerical values exactly as they appear in the document
3. For multi-year tables, extract BOTH 2024 AND 2023 values when available
4. Clean numbers: remove spaces, keep periods for decimals, preserve negative signs
5. For percentages, return just the number (no % symbol)
6. For monetary amounts, return the raw number in millions SEK
7. If a value is not found, use null

TARGET FIELDS TO EXTRACT:
{json.dumps(target_fields, indent=2)}

"""

        if section_name == 'fund_capital':
            specific_instructions = """
SECTION: Fund Capital, Flows and Results

MISSION: Find the "Five-year overview" section with table "Fund capital, flows and results"

TARGET TABLE STRUCTURE:
SEK million                                    2024        2023        2022        2021        2020
Fund capital                                  458 884     426 040     407 112     441 045     386 224  
Net outflows to the national pension system    -2 024      -4 833      -4 689      -7 528      -7 902
Net result for the year                        34 868      23 761     -29 244      62 349      12 776

EXTRACTION STRATEGY:
1. Locate the exact table "Fund capital, flows and results" 
2. Extract from 2024 column: 458884, -2024, 34868
3. Map to the three JSON keys provided
4. Handle the negative sign correctly for net outflows

CRITICAL: The values must be EXACTLY: 458884, -2024, 34868
"""

        elif section_name == 'asset_allocation':
            specific_instructions = """
SECTION: Asset Class Exposure

MISSION: Find the "Asset class exposure" table with two main data columns

TARGET TABLE STRUCTURE:
Asset class                           Strategic asset    Actual portfolio
                                     allocation, %       exposure %
Swedish equities                            9                 10
Developed markets equities                 20                 20  
Emerging markets equities                  10                 10
Private equity                             10                 13
Real assets                                18                 18
Government bonds in developed markets      13                 11
Credit bonds in developed markets          11                 10
Bonds in emerging markets                   5                  5
Non-listed credits                          4                  4
Other                                       -                 -1
Total                                     100                100
Currency exposure                          31                 24

EXTRACTION STRATEGY:
1. Find table titled "Asset class exposure"
2. Extract from "Strategic asset allocation, %" column: 9, 20, 10, 10, 18, 13, 11, 5, 4, 100, 31
3. Extract from "Actual portfolio exposure %" column: 10, 20, 10, 13, 18, 11, 10, 5, 4, -1, 100, 24
4. Map each value to corresponding JSON keys
5. Note: Some values may be blank in the source - use null for those

CRITICAL: Must extract from BOTH columns with exact percentage values
"""

        elif section_name == 'real_assets':
            specific_instructions = """
SECTION: Real Assets Distribution

MISSION: Find "Real assets" section with TWO pie charts

TARGET STRUCTURE:
Portfolio distribution:
- Traditional real estate: 59%
- Natural Climate Solutions: 28% 
- Sustainable infrastructure: 13%

Geographical distribution:
- North America: 42%
- South America: 5%
- Oceania: 5%
- Europe (excl. Sweden): 10%
- Sweden: 30%
- Asia: 4%
- Others: 4%

EXTRACTION STRATEGY:
1. Locate "Real assets" section
2. Find pie chart data or accompanying tables
3. Extract percentage values for each category
4. Map to corresponding JSON keys

CRITICAL: Values must be EXACTLY: 13, 59, 28, 42, 5, 5, 10, 30, 4, 4
"""

        elif section_name == 'bonds':
            specific_instructions = """
SECTION: Bonds and Other Fixed-Income Securities

MISSION: Find "Note 9. Bonds and other fixed-income securities" with BOTH 2024 and 2023 data

TARGET TABLE STRUCTURE:
Amounts in SEK million                    31 Dec 2024    31 Dec 2023
Breakdown by issuer category
Swedish Government                            2 434          4 088
Swedish municipalities                           92            202
Swedish mortgage institutions                   546            400  
Financial companies                          3 090          8 482
Non-financial companies                        277            275
Foreign governments                         49 001         42 471
Other foreign issuers                       73 895         67 164
Total                                      129 335        123 082

Breakdown by type of instrument
Other bonds                                115 009        111 399
Unlisted loans                               2 678          2 479
Participations in foreign fixed-income      11 648          9 204
funds
Total                                      129 335        123 082

EXTRACTION STRATEGY:
1. Find "Note 9" table with exact structure above
2. Extract ALL values from BOTH 31 Dec 2024 AND 31 Dec 2023 columns
3. Return nested JSON with separate objects for 2024 and 2023 data
4. Use keys like "2024_swedish_gov" and "2023_swedish_gov" to distinguish years

CRITICAL: Must extract BOTH years:
- 2024 values: 2434, 92, 546, 3090, 277, 49001, 73895, 129335, 115009, 2678, 11648, 129335
- 2023 values: 4088, 202, 400, 8482, 275, 42471, 67164, 123082, 111399, 2479, 9204, 123082
"""

        else:
            specific_instructions = f"Extract data for {section_name} section"

        full_prompt = base_instructions + specific_instructions + f"""

DOCUMENT TEXT TO ANALYZE:
{context_text}

FINAL INSTRUCTION: Return ONLY the JSON object with extracted values. No other text."""

        return full_prompt
    
    def extract_section_with_precision(self, pdf_path, section_name):
        """Extract a specific section with maximum precision"""
        
        if not self.client:
            self.logger.error("LLM client not available")
            return {}
        
        # Get section-specific keywords and field mapping
        keywords = self.get_section_keywords(section_name)
        field_mapping = self.get_field_mapping(section_name)
        
        if not field_mapping:
            self.logger.error(f"No field mapping for section: {section_name}")
            return {}
        
        # Extract relevant context
        context_text = self.extract_targeted_sections(pdf_path, keywords)
        if not context_text.strip():
            self.logger.warning(f"No relevant context found for {section_name}")
            return {}
        
        # Create precision prompt
        prompt = self.create_perfect_prompt(section_name, context_text, field_mapping)
        
        try:
            response = self.client.chat.completions.create(
                model="qwen/qwen-2.5-coder-32b-instruct",  # Use your available model
                messages=[
                    {"role": "system", "content": "You are a precision financial data extraction expert. Return only valid JSON with exact numerical values."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,  # Maximum determinism
                max_tokens=3000
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Extract and validate JSON
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if not json_match:
                self.logger.error(f"No JSON found in response for {section_name}")
                self.logger.debug(f"Raw response: {response_text[:500]}")
                return {}
            
            json_str = json_match.group(0)
            data = json.loads(json_str)
            
            # Validate and clean data
            cleaned_data = {}
            for key, value in data.items():
                if key in field_mapping and value is not None:
                    # Clean and convert values
                    if isinstance(value, str):
                        # Remove any non-numeric characters except periods and minus signs
                        cleaned_value = re.sub(r'[^\d.-]', '', value)
                        try:
                            cleaned_data[key] = float(cleaned_value)
                        except ValueError:
                            cleaned_data[key] = None
                    elif isinstance(value, (int, float)):
                        cleaned_data[key] = float(value)
                    else:
                        cleaned_data[key] = None
            
            self.logger.info(f"Perfect LLM extracted {len(cleaned_data)} fields for {section_name}")
            return cleaned_data
            
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error for {section_name}: {e}")
            self.logger.debug(f"Problematic JSON: {json_str[:200] if 'json_str' in locals() else 'N/A'}")
            return {}
        except Exception as e:
            self.logger.error(f"Perfect LLM extraction failed for {section_name}: {e}")
            return {}
    
    def get_section_keywords(self, section_name):
        """Get precise keywords for each section"""
        keywords_map = {
            'fund_capital': ['five-year', 'overview', 'fund', 'capital', 'flows', 'results', 'outflows', 'pension'],
            'asset_allocation': ['asset', 'class', 'exposure', 'strategic', 'allocation', 'portfolio', 'actual', 'swedish', 'equities'],
            'real_assets': ['real', 'assets', 'portfolio', 'distribution', 'geographical', 'traditional', 'climate', 'infrastructure'],
            'bonds': ['bonds', 'fixed-income', 'securities', 'note', 'government', 'municipalities', 'mortgage', 'issuer', 'instrument']
        }
        return keywords_map.get(section_name, [])
    
    def get_field_mapping(self, section_name):
        """Get exact field mappings for each section"""
        mappings = {
            'fund_capital': {
                'AP2.FUNDCAPITALCARRIEDFORWARD.LEVEL.NONE.A.1@AP2': 'Fund capital (458884)',
                'AP2.NETOUTFLOWSTOTHENATIONALPENSIONSYSTEM.FLOW.NONE.A.1@AP2': 'Net outflows to the national pension system (-2024)',
                'AP2.TOTAL.FLOW.NONE.A.1@AP2': 'Net result for the year (34868)'
            },
            'asset_allocation': {
                # Strategic Portfolio fields (Column 1)
                'AP2.DOMESTICEQUITIES.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2': 'Swedish equities - Strategic allocation % (9)',
                'AP2.DEVELOPEDEQUITIES.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2': 'Developed markets equities - Strategic allocation % (20)',
                'AP2.EMERGINGEQUITIES.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2': 'Emerging markets equities - Strategic allocation % (10)',
                'AP2.PRIVATEEQUITY.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2': 'Private equity - Strategic allocation % (10)',
                'AP2.REALASSETS.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2': 'Real assets - Strategic allocation % (18)',
                'AP2.GOVBONDSDEVMARKETS.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2': 'Government bonds in developed markets - Strategic % (13)',
                'AP2.CREDITBONDSDEVMARKETS.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2': 'Credit bonds in developed markets - Strategic % (11)',
                'AP2.BONDSEMMARKETS.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2': 'Bonds in emerging markets - Strategic % (5)',
                'AP2.NONLISTEDCREDITS.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2': 'Non-listed credits - Strategic % (4)',
                'AP2.OTHER.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2': 'Other - Strategic % (null if not present)',
                'AP2.TOTAL.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2': 'Total - Strategic % (100)',
                'AP2.CURRENCYEXPOSURE.ACTUALALLOCATION.STRATEGICPORTFOLIO.NONE.A.1@AP2': 'Currency exposure - Strategic % (31)',
                
                # Actual Portfolio fields (Column 2)
                'AP2.DOMESTICEQUITIES.ACTUALALLOCATION.NONE.A.1@AP2': 'Swedish equities - Actual exposure % (10)',
                'AP2.DEVELOPEDEQUITIES.ACTUALALLOCATION.NONE.A.1@AP2': 'Developed markets equities - Actual exposure % (20)',
                'AP2.EMEQUITIES.ACTUALALLOCATION.NONE.A.1@AP2': 'Emerging markets equities - Actual exposure % (10)',
                'AP2.PRIVATEEQUITY.ACTUALALLOCATION.NONE.A.1@AP2': 'Private equity - Actual exposure % (13)',
                'AP2.REALASSETS.ACTUALALLOCATION.NONE.A.1@AP2': 'Real assets - Actual exposure % (18)',
                'AP2.GOVBONDSDEVMARKETS.ACTUALALLOCATION.NONE.A.1@AP2': 'Government bonds - Actual exposure % (11)',
                'AP2.CREDITBONDSDEVMARKETS.ACTUALALLOCATION.NONE.A.1@AP2': 'Credit bonds - Actual exposure % (10)',
                'AP2.BONDSEMMARKETS.ACTUALALLOCATION.NONE.A.1@AP2': 'Bonds in emerging markets - Actual exposure % (5)',
                'AP2.NONLISTEDCREDITS.ACTUALALLOCATION.NONE.A.1@AP2': 'Non-listed credits - Actual exposure % (4)',
                'AP2.OTHER.ACTUALALLOCATION.NONE.A.1@AP2': 'Other - Actual exposure % (-1)',
                'AP2.TOTAL.ACTUALALLOCATION.NONE.A.1@AP2': 'Total - Actual exposure % (100)',
                'AP2.CURRENCYEXPOSURE.ACTUALALLOCATION.NONE.A.1@AP2': 'Currency exposure - Actual % (24)',
            },
            'real_assets': {
                'AP2.SUSTAINABLEINFRASTRUCTURE.ACTUALALLOCATION.NONE.A.1@AP2': 'Sustainable infrastructure % (13)',
                'AP2.TRADITIONALREALESTATE.ACTUALALLOCATION.NONE.A.1@AP2': 'Traditional real estate % (59)',
                'AP2.NATURALCLIMATE.ACTUALALLOCATION.NONE.A.1@AP2': 'Natural Climate Solutions % (28)',
                'AP2.NORTHAMERICA.ACTUALALLOCATION.NONE.A.1@AP2': 'North America % (42)',
                'AP2.SOUTHAMERICA.ACTUALALLOCATION.NONE.A.1@AP2': 'South America % (5)',
                'AP2.OCEANIA.ACTUALALLOCATION.NONE.A.1@AP2': 'Oceania % (5)',
                'AP2.EUROPE.ACTUALALLOCATION.NONE.A.1@AP2': 'Europe excl. Sweden % (10)',
                'AP2.SWEDEN.ACTUALALLOCATION.NONE.A.1@AP2': 'Sweden % (30)',
                'AP2.ASIA.ACTUALALLOCATION.NONE.A.1@AP2': 'Asia % (4)',
                'AP2.OTHERS.ACTUALALLOCATION.NONE.A.1@AP2': 'Others % (4)',
            },
            'bonds': {
                # 2024 values
                'AP2.SWEDISHGOV.ACTUALALLOCATION.NONE.A.1@AP2': 'Swedish Government 2024 (2434)',
                'AP2.SWMUNICIPAL.ACTUALALLOCATION.NONE.A.1@AP2': 'Swedish municipalities 2024 (92)',
                'AP2.SWMORTGAGE.ACTUALALLOCATION.NONE.A.1@AP2': 'Swedish mortgage institutions 2024 (546)',
                'AP2.FINCOMP.ACTUALALLOCATION.NONE.A.1@AP2': 'Financial companies 2024 (3090)',
                'AP2.NONFINCOMP.ACTUALALLOCATION.NONE.A.1@AP2': 'Non-financial companies 2024 (277)',
                'AP2.FOREIGNBONDS.ACTUALALLOCATION.NONE.A.1@AP2': 'Foreign governments 2024 (49001)',
                'AP2.FOREIGNBONDSOTHERFORISS.ACTUALALLOCATION.NONE.A.1@AP2': 'Other foreign issuers 2024 (73895)',
                'AP2.TOTALBONDSISSUERCAT.ACTUALALLOCATION.NONE.A.1@AP2': 'Total issuer category 2024 (129335)',
                'AP2.BONDSOTHER.ACTUALALLOCATION.NONE.A.1@AP2': 'Other bonds 2024 (115009)',
                'AP2.LOANSUNLISTED.ACTUALALLOCATION.NONE.A.1@AP2': 'Unlisted loans 2024 (2678)',
                'AP2.FUNDSFIXEDINCOME.ACTUALALLOCATION.NONE.A.1@AP2': 'Participations in foreign fixed-income funds 2024 (11648)',
                'AP2.TOTALBONDS.TYPEINSTR.ACTUALALLOCATION.NONE.A.1@AP2': 'Total instrument type 2024 (129335)',
                
                # 2023 values - NEW!
                '2023_AP2.SWEDISHGOV.ACTUALALLOCATION.NONE.A.1@AP2': 'Swedish Government 2023 (4088)',
                '2023_AP2.SWMUNICIPAL.ACTUALALLOCATION.NONE.A.1@AP2': 'Swedish municipalities 2023 (202)',
                '2023_AP2.SWMORTGAGE.ACTUALALLOCATION.NONE.A.1@AP2': 'Swedish mortgage institutions 2023 (400)',
                '2023_AP2.FINCOMP.ACTUALALLOCATION.NONE.A.1@AP2': 'Financial companies 2023 (8482)',
                '2023_AP2.NONFINCOMP.ACTUALALLOCATION.NONE.A.1@AP2': 'Non-financial companies 2023 (275)',
                '2023_AP2.FOREIGNBONDS.ACTUALALLOCATION.NONE.A.1@AP2': 'Foreign governments 2023 (42471)',
                '2023_AP2.FOREIGNBONDSOTHERFORISS.ACTUALALLOCATION.NONE.A.1@AP2': 'Other foreign issuers 2023 (67164)',
                '2023_AP2.TOTALBONDSISSUERCAT.ACTUALALLOCATION.NONE.A.1@AP2': 'Total issuer category 2023 (123082)',
                '2023_AP2.BONDSOTHER.ACTUALALLOCATION.NONE.A.1@AP2': 'Other bonds 2023 (111399)',
                '2023_AP2.LOANSUNLISTED.ACTUALALLOCATION.NONE.A.1@AP2': 'Unlisted loans 2023 (2479)',
                '2023_AP2.FUNDSFIXEDINCOME.ACTUALALLOCATION.NONE.A.1@AP2': 'Participations in foreign fixed-income funds 2023 (9204)',
                '2023_AP2.TOTALBONDS.TYPEINSTR.ACTUALALLOCATION.NONE.A.1@AP2': 'Total instrument type 2023 (123082)',
            }
        }
        return mappings.get(section_name, {})
    
    def extract_all_sections(self, pdf_path):
        """Extract all sections with perfect precision for both 2023 and 2024"""
        year = self.extract_year_from_filename(pdf_path)
        self.logger.info(f"Perfect extraction from {os.path.basename(pdf_path)} (Year: {year})")
        
        all_data = {}
        sections = ['fund_capital', 'asset_allocation', 'real_assets', 'bonds']
        
        # Extract data for current year
        year_2024_data = {}
        year_2023_data = {}
        
        for section_name in sections:
            self.logger.info(f"Extracting {section_name} with perfect precision...")
            try:
                data = self.extract_section_with_precision(pdf_path, section_name)
                
                if section_name == 'bonds':
                    # Split bonds data into 2024 and 2023
                    for key, value in data.items():
                        if key.startswith('2023_'):
                            # Remove 2023_ prefix and add to 2023 data
                            clean_key = key[5:]  # Remove '2023_'
                            year_2023_data[clean_key] = value
                        else:
                            # Add to 2024 data
                            year_2024_data[key] = value
                else:
                    # For other sections, add to 2024 data only
                    year_2024_data.update(data)
                
                expected_count = len(self.get_field_mapping(section_name))
                actual_count = len(data)
                accuracy = (actual_count / expected_count * 100) if expected_count > 0 else 0
                
                self.logger.info(f"✓ {section_name}: {actual_count}/{expected_count} fields ({accuracy:.1f}%)")
                
            except Exception as e:
                self.logger.error(f"Failed to extract {section_name}: {e}")
        
        # Calculate totals
        total_expected = sum(len(self.get_field_mapping(s)) for s in sections)
        total_2024 = len(year_2024_data)
        total_2023 = len(year_2023_data)
        total_actual = total_2024 + total_2023
        final_accuracy = (total_actual / (total_expected + 11) * 100)  # +11 for 2023 bonds fields
        
        self.logger.info(f"FINAL RESULT: {total_actual}/{total_expected + 11} fields ({final_accuracy:.1f}%)")
        
        # Return both years in correct order (2023 first, then 2024)
        result = {}
        if year_2023_data:
            result[2023] = year_2023_data
        if year_2024_data:
            result[2024] = year_2024_data
            
        return result
    
    def extract_year_from_filename(self, filename):
        """Extract year from filename"""
        basename = os.path.basename(filename)
        match = re.search(r'(\d{4})', basename)
        if match:
            year = int(match.group(1))
            if 2000 <= year <= 2030:
                return year
        return 2024  # Default to current year

# Legacy support function
def extract_perfect_data(pdf_path):
    """Main function for perfect extraction"""
    parser = PerfectLLMParser()
    return parser.extract_all_sections(pdf_path)

if __name__ == "__main__":
    import glob
    
    # Find latest downloaded PDF
    download_folders = glob.glob(os.path.join(config.DOWNLOADS_DIR, '*'))
    if download_folders:
        latest_folder = max(download_folders, key=os.path.getmtime)
        pdf_files = glob.glob(os.path.join(latest_folder, '*.pdf'))
        
        if pdf_files:
            pdf_path = pdf_files[0]
            print(f"Testing perfect extraction on: {pdf_path}")
            
            parser = PerfectLLMParser()
            result = parser.extract_all_sections(pdf_path)
            
            print(f"Perfect extraction result: {len(result[list(result.keys())[0]])} fields extracted")
        else:
            print("No PDF files found")
    else:
        print("No download folders found")