import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin

class SHLScraper:
    def __init__(self):
        self.base_url = "https://www.shl.com/solutions/products/product-catalog/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
        self.session = requests.Session()
        self.assessments = []

    def get_assessment_links(self):
        """Get all assessment links from the catalog page dynamically"""
        response = self.session.get(self.base_url, headers=self.headers)
        if response.status_code != 200:
            print(f"Failed to fetch catalog: {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.content, "html.parser")
        assessment_links = []
        
        # Try multiple approaches to find assessment links
        
        # Look for links in a table structure (based on image 2)
        table_links = soup.select("table a") if soup.select("table") else []
        if table_links:
            assessment_links.extend(table_links)
        
        # Look for links under any "Job Solutions" or similar headings
        solutions_headers = soup.find_all(["h2", "h3", "h4"], string=lambda s: s and "Solution" in s)
        for header in solutions_headers:
            # Get links within this section
            section_links = header.find_next_siblings()
            for element in section_links:
                links = element.find_all("a")
                if links:
                    assessment_links.extend(links)
        
        # Look for any links that have assessment-like URLs
        catalog_links = soup.select("a[href*='/product-catalog/']")
        assessment_links.extend([link for link in catalog_links if link not in assessment_links])
        
        # If we still don't have links, try to find all links that might be job assessments
        if not assessment_links:
            # Look for any links under the main container
            main_content = soup.select_one("main") or soup.select_one(".main-content") or soup.select_one("#content") or soup
            potential_links = main_content.find_all("a")
            
            # Filter for links that seem to be assessment solutions
            assessment_links = [link for link in potential_links if link.get("href") and 
                               (re.search(r'solution|assessment|test', link.get("href"), re.IGNORECASE) or
                                (link.text and re.search(r'solution|assessment|test', link.text, re.IGNORECASE)))]
        
        # Make sure we have unique links
        unique_links = []
        seen_hrefs = set()
        for link in assessment_links:
            href = link.get("href")
            if href and href not in seen_hrefs:
                seen_hrefs.add(href)
                unique_links.append({
                    "name": link.text.strip(),
                    "url": self._make_absolute_url(href)
                })
        
        return unique_links

    def _make_absolute_url(self, url):
        """Convert relative URLs to absolute URLs"""
        if not url:
            return None
        return urljoin(self.base_url, url)

    def extract_assessment_data(self, assessment_info):
        """Extract details from an individual assessment page"""
        url = assessment_info["url"]
        name = assessment_info["name"]
        
        print(f"Scraping: {name} at {url}")
        
        response = self.session.get(url, headers=self.headers)
        if response.status_code != 200:
            print(f"Failed to fetch assessment details: {response.status_code}")
            return {}
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extract assessment details
        details = {
            "name": name,
            "url": url,
            "remote_testing": "No",
            "adaptive_irt": "No",

            "duration": "Unknown",
            "test_type": "Unknown"
        }
        
        # Look for Remote Testing indicator
        remote_testing_elements = soup.find_all(string=lambda s: s and "Remote Testing" in s)
        for element in remote_testing_elements:
            parent = element.parent
            if parent:
                # Check if there's a green checkmark or "Yes" nearby
                if "✓" in parent.text or "Yes" in parent.text or parent.find(["img", "i", "span"], class_=lambda c: c and ("check" in c or "yes" in c or "green" in c)):
                    details["remote_testing"] = "Yes"
                    break
        
        # Look for Adaptive/IRT Support indicator
        adaptive_elements = soup.find_all(string=lambda s: s and ("Adaptive" in s or "IRT" in s))
        for element in adaptive_elements:
            parent = element.parent
            if parent:
                # Check if there's a green checkmark or "Yes" nearby
                if "✓" in parent.text or "Yes" in parent.text or parent.find(["img", "i", "span"], class_=lambda c: c and ("check" in c or "yes" in c or "green" in c)):
                    details["adaptive_irt"] = "Yes"
                    break
        
        # Look for duration/assessment length
        duration_patterns = [
            r"(\d+)\s*minutes",
            r"completion time.*?(\d+)",
            r"assessment length.*?(\d+)",
            r"duration.*?(\d+)",
            r"takes.*?(\d+)\s*minutes"
        ]
        
        for pattern in duration_patterns:
            # Find all text nodes
            for text_node in soup.find_all(text=True):
                match = re.search(pattern, text_node.lower())
                if match:
                    details["duration"] = f"{match.group(1)} minutes"
                    break
            if details["duration"] != "Unknown":
                break
        
        # Look for test type
        test_type_elements = soup.find_all(string=lambda s: s and "Test Type" in s)
        for element in test_type_elements:
            parent = element.parent
            if parent:
                # Extract test type information
                test_type_text = parent.text.replace("Test Type:", "").strip()
                if test_type_text:
                    details["test_type"] = test_type_text
                    break
        
        return details

    def scrape_all_assessments(self):
        """Scrape data for all available assessments"""
        assessment_links = self.get_assessment_links()
        
        if not assessment_links:
            print("No assessments found in the catalog")
            return []
        
        print(f"Found {len(assessment_links)} assessments to scrape")
        
        for assessment in assessment_links:
            details = self.extract_assessment_data(assessment)
            if details:
                self.assessments.append(details)
                print(f"\nAssessment #{len(self.assessments)} details:")
                print(json.dumps(details, indent=2))
            
            # Be respectful with the server
            time.sleep(2)
        
        return self.assessments
    
    def save_to_json(self, filename="shl_assessments.json"):
        """Save scraped data to a JSON file"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.assessments, f, indent=4)
        print(f"Data saved to {filename}")

# Usage example
if __name__ == "__main__":
    scraper = SHLScraper()
    scraper.scrape_all_assessments()
    scraper.save_to_json()