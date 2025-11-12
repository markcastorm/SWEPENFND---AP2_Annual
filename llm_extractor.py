"""
LLM-based PDF Field Extractor for Annual Reports
Uses OpenRouter API with free models for robust extraction when Camelot/Regex fail
Zero cost using deepseek/deepseek-chat-v3.1 or other free models
"""
import os
import sys
import json
import logging
import requests
from typing import Dict, List
from dotenv import load_dotenv
import config

# Create a mapping from technical header to human-readable subheader
HEADER_TO_SUBHEADER = {
    header: subheader
    for header, subheader in zip(config.OUTPUT_HEADERS, config.OUTPUT_SUBHEADERS)
    if header and subheader
}
# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class LLMExtractor:
    """Extract fields using LLM when traditional methods fail"""

    def __init__(self):
        """Initialize LLM extractor with OpenRouter API"""
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.model = os.getenv('LLM_MODEL', 'deepseek/deepseek-chat-v3.1')
        self.enabled = os.getenv('ENABLE_LLM_FALLBACK', 'true').lower() == 'true'

        if not self.api_key:
            logger.warning("  [WARNING] OPENROUTER_API_KEY not found in .env file")
            logger.warning("  [WARNING] LLM fallback will be disabled")
            self.enabled = False

        self.api_url = "https://openrouter.ai/api/v1/chat/completions"

    def extract_annual_data(self, text: str, target_fields: List[str], year: int) -> Dict[str, float]:
        """
        Extract various annual report fields using LLM.
        """
        if not self.enabled:
            logger.debug("  LLM extraction disabled (no API key or disabled in .env)")
            return {}

        # Construct a detailed prompt for the LLM
        field_descriptions = []
        for field in target_fields:
            description = HEADER_TO_SUBHEADER.get(field, field)
            field_descriptions.append(f"- {field} (Description: '{description}')")
        
        field_descriptions_str = "\n".join(field_descriptions)

        prompt = f"""Extract the following financial data points for the year {year} from the provided text.
Return ONLY a JSON object with these exact field names and their numeric values.
If a value is a percentage, return it as a float (e.g., 9.0 for 9%).
If a value is in SEK billion, return it as a float.
If a value is in SEK million, return it as an integer.
Preserve negative signs. If a field is not found, omit it from the JSON.

Required fields and their descriptions/context:
{field_descriptions_str}

IMPORTANT NOTES:
1. Pay attention to the units (SEK million, SEK billion, percentage) and convert values accordingly.
2. For percentage values, remove the '%' sign and provide as a float.
3. If multiple years are present, extract only the value corresponding to the year {year}.
4. Return ONLY valid JSON, no markdown, no explanations.

TEXT TO EXTRACT FROM:
{text}"""

        try:
            response = self._call_llm(prompt)
            data = json.loads(response)

            result = {}
            for key, value in data.items():
                if value is None:
                    continue
                try:
                    float_val = float(value)
                    if float_val == int(float_val):
                        result[key] = int(float_val)
                    else:
                        result[key] = float_val
                except (ValueError, TypeError):
                    logger.warning(f"  [WARNING] LLM returned non-numeric value for {key}: '{value}'")
                    continue

            logger.info(f"  [LLM] Extracted {len(result)}/{len(target_fields)} annual fields for {year}")
            return result

        except Exception as e:
            logger.error(f"  [LLM ERROR] Annual data extraction failed for year {year}: {e}")
            return {}

    def _call_llm(self, prompt: str) -> str:
        """
        Call OpenRouter API with the given prompt
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/yourusername/ap2-scraper-annual",
            "X-Title": "AP2 Annual PDF Parser"
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0
        }

        logger.debug(f"  [LLM] Calling {self.model} via OpenRouter...")

        response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        result = response.json()
        content = result['choices'][0]['message']['content']

        content = content.replace('```json', '').replace('```', '').strip()
        start_idx = content.find('{')
        end_idx = content.rfind('}')
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            content = content[start_idx:end_idx+1]

        return content


def extract_annual_data_llm(pdf_path: str, page_num: int, target_fields: List[str], year: int) -> Dict[str, float]:
    """
    Extract annual data using LLM fallback.
    """
    import fitz

    logger.info(f"  [LLM FALLBACK] Attempting LLM-based annual data extraction for page {page_num}, year {year}...")

    doc = fitz.open(pdf_path)
    page = doc[page_num - 1]
    text = page.get_text()
    doc.close()

    extractor = LLMExtractor()
    return extractor.extract_annual_data(text, target_fields, year)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    # Use a relative path for the sample PDF
    sample_pdf_path = os.path.join(config.PROJECT_ROOT, "downloads", "Annual-Report-2024.pdf")
    sample_page_num = 5
    target_year = 2024

    sample_target_fields = [
        'AP2.FUNDCAPITALCARRIEDFORWARD.LEVEL.NONE.A.1@AP2',
        'AP2.NETOUTFLOWSTOTHENATIONALPENSIONSYSTEM.FLOW.NONE.A.1@AP2',
        'AP2.TOTAL.FLOW.NONE.A.1@AP2',
    ]

    if not os.path.exists(sample_pdf_path):
        logger.warning(f"Sample PDF not found at {sample_pdf_path}. Trying alternative.")
        sample_pdf_path_alt = os.path.join(config.PROJECT_ROOT, "downloads", "Annual-Report-2024 (1).pdf")
        if os.path.exists(sample_pdf_path_alt):
            sample_pdf_path = sample_pdf_path_alt
            logger.info(f"Found alternative sample PDF: {sample_pdf_path}")
        else:
            logger.error("No 2024 annual report found in downloads folder. Exiting.")
            sys.exit(1)

    print("="*80)
    print(f"LLM EXTRACTOR TEST - {target_year} Annual PDF")
    print("="*80)

    print(f"\n[TEST] Annual Data Extraction for {target_year}")
    data = extract_annual_data_llm(sample_pdf_path, sample_page_num, sample_target_fields, target_year)
    
    print(f"\nExtracted {len(data)}/{len(sample_target_fields)} fields:")
    for field, value in data.items():
        print(f"  {field}: {value}")
