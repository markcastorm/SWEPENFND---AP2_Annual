"""
AP2 Annual Financial Reports Scraper
Downloads PDF reports from AP2 website, specifically for annual reports.
"""

import os
import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

import config

# Setup logging
logger = logging.getLogger(__name__)

def setup_driver(download_path):
    """Initialize Chrome driver"""
    logger.info("Setting up Chrome driver...")

    options = uc.ChromeOptions()
    prefs = {
        "download.default_directory": os.path.abspath(download_path),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
    }
    options.add_experimental_option("prefs", prefs)

    driver = uc.Chrome(options=options)
    driver.implicitly_wait(config.SELENIUM_CONFIG['implicit_wait'])

    logger.info(f"OK Chrome driver ready. Downloads will be saved to: {download_path}")
    return driver


def wait_for_download(download_folder, initial_files, timeout=config.SELENIUM_CONFIG['download_timeout']):
    """Wait for download to complete"""
    logger.info(f"  Waiting for download to appear in {os.path.basename(download_folder)}...")
    start_time = time.time()

    while time.time() - start_time < timeout:
        current_files = set(os.listdir(download_folder))
        new_files = current_files - initial_files
        complete_files = {f for f in new_files if not f.endswith((".crdownload", ".tmp", ".part"))}

        if complete_files:
            new_file = list(complete_files)[0]
            file_path = os.path.join(download_folder, new_file)

            # Check file stability
            time.sleep(1)
            size1 = os.path.getsize(file_path)
            time.sleep(2)
            size2 = os.path.getsize(file_path)

            if size1 == size2 and size2 > 0:
                logger.info(f"  OK Downloaded: {new_file} ({size2 / 1024:.1f} KB)")
                return file_path

        time.sleep(1)

    raise TimeoutError(f"Download timeout after {timeout}s. No new file appeared in the target folder.")


def parse_reports_page(driver):
    """Parse the financial reports page"""
    logger.info(f"Navigating to {config.BASE_URL}...")
    driver.get(config.BASE_URL)
    time.sleep(3)

    # Accept cookies
    try:
        accept_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'cmplz-accept')]" ))
        )
        accept_btn.click()
        logger.info("OK Accepted cookies")
        time.sleep(2)
    except:
        logger.debug("No cookie consent banner found or clickable.")
        pass

    # Parse page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    content_div = soup.find('div', class_='content')

    if not content_div:
        logger.error("ERROR: Could not find content div")
        return []

    reports = []
    current_year = None

    for element in content_div.find_all(['h2', 'div', 'p']):
        # Check for year header
        if element.name == 'h2' and element.get('class') and 'wp-block-heading' in element.get('class'):
            try:
                current_year = int(element.text.strip())
            except:
                continue

        # Check for report links
        if current_year:
            links = element.find_all('a', href=True)
            for link in links:
                href = link.get('href')
                if href and href.endswith('.pdf'):
                    report_name = link.text.strip()
                    report_type = 'half_year' if 'half' in report_name.lower() else 'annual'

                    reports.append({
                        'year': current_year,
                        'name': report_name,
                        'url': href,
                        'type': report_type
                    })

    # Deduplicate by URL (same report may appear multiple times on page)
    seen_urls = set()
    unique_reports = []
    for report in reports:
        if report['url'] not in seen_urls:
            seen_urls.add(report['url'])
            unique_reports.append(report)

    logger.info(f"OK Found {len(unique_reports)} unique reports on page")
    return unique_reports


def filter_reports(all_reports):
    """Filter reports based on config"""
    # Determine target year
    if config.TARGET_YEAR == "latest":
        if all_reports:
            target_year = max(r['year'] for r in all_reports)
            logger.info(f"'latest' resolved to year: {target_year}")
        else:
            logger.error("ERROR: No reports found to determine latest year.")
            return []
    else:
        target_year = int(config.TARGET_YEAR)
        logger.info(f"Target year: {target_year}")

    # Filter
    filtered = []
    for report in all_reports:
        if report['year'] == target_year:
            # Only download if the report type is enabled in config
            if config.REPORT_TYPES.get(report['type'], False):
                filtered.append(report)
                logger.info(f"  - {report['name']} (Type: {report['type']})")

    logger.info(f"OK Filtered to {len(filtered)} reports to download")
    return filtered


def download_reports(driver, reports, run_downloads_dir):
    """Download all filtered reports"""
    logger.info(f"\n{'='*80}")
    logger.info("DOWNLOADING REPORTS")
    logger.info(f"{ '='*80}")

    downloaded = []

    for i, report in enumerate(reports, 1):
        logger.info(f"\n[{i}/{len(reports)}] {report['name']}...")

        try:
            initial_files = set(os.listdir(run_downloads_dir))
            driver.get(report['url'])
            downloaded_file = wait_for_download(run_downloads_dir, initial_files)

            # Rename with year and type
            new_name = f"AP2_{report['year']}_{report['type']}.pdf"
            new_path = os.path.join(run_downloads_dir, new_name)

            if os.path.exists(new_path):
                os.remove(new_path)
            os.rename(downloaded_file, new_path)

            downloaded.append(new_path)
            time.sleep(2)

        except Exception as e:
            logger.error(f"  FAILED Failed to download {report['name']}: {e}")

    return downloaded


def main():
    """Main execution"""
    # Setup logging for this script
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file_path = os.path.join(config.LOGS_DIR, f'downloader_{timestamp}.log')
    
    # Ensure log directory exists
    os.makedirs(config.LOGS_DIR, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, config.LOGGING_CONFIG['log_level'].upper()),
        format=config.LOGGING_CONFIG['log_format'],
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler()
        ]
    )

    logger.info("=" * 80)
    logger.info("AP2 Annual Financial Reports Scraper")
    logger.info(f"Execution Time: {timestamp}")
    logger.info("=" * 80)

    # Create run-specific folders first
    run_folders = config.create_run_folders(timestamp)
    run_downloads_dir = run_folders['downloads']

    driver = None

    try:
        # Pass the correct download path to the driver setup
        driver = setup_driver(run_downloads_dir)
        
        all_reports = parse_reports_page(driver)
        reports_to_download = filter_reports(all_reports)

        if not reports_to_download:
            logger.warning("\nWARNING: No reports match filter criteria")
            logger.warning("Check config.py TARGET_YEAR and REPORT_TYPES settings")
            return

        downloaded = download_reports(driver, reports_to_download, run_downloads_dir)

        logger.info(f"\n{'='*80}")
        logger.info("SCRAPER COMPLETED")
        logger.info(f"{ '='*80}")
        logger.info(f"OK Downloaded {len(downloaded)} reports")
        logger.info(f"OK Location: {run_downloads_dir}")
        logger.info(f"{ '='*80}")

    except Exception as e:
        logger.error(f"\nERROR: An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        raise

    finally:
        if driver:
            logger.info("Shutting down browser...")
            try:
                driver.close()
                logger.debug("  - driver.close() called")
                driver.quit()
                logger.debug("  - driver.quit() called")
                time.sleep(2) # Give processes time to terminate
                logger.info("OK Browser appears to be closed.")
            except Exception as e:
                logger.error(f"  - Error during browser shutdown: {e}")
            finally:
                # This is a final attempt to ensure the process is gone,
                # especially if driver.quit() hangs or fails.
                try:
                    if driver.service and driver.service.process:
                        driver.service.process.kill()
                        logger.debug("  - Killed driver service process.")
                except Exception:
                    pass



if __name__ == "__main__":
    main()
