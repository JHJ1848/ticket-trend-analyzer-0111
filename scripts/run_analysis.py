import os
import sys
import json

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from src.analyzer import TicketAnalyzer
from src.visualizer import ReportGenerator

def main():
    data_path = os.path.join(ROOT_DIR, "data", "tickets.json")
    report_output_path = os.path.join(ROOT_DIR, "docs", "analysis_report.md")
    json_output_path = os.path.join(ROOT_DIR, "docs", "full_analysis_data.json")
    web_data_path = os.path.join(ROOT_DIR, "web", "data.js")

    analyzer = TicketAnalyzer.load_from_file(data_path)
    full_data = analyzer.generate_full_report_data()

    os.makedirs(os.path.dirname(report_output_path), exist_ok=True)
    os.makedirs(os.path.dirname(web_data_path), exist_ok=True)

    generator = ReportGenerator(full_data)
    generator.generate_markdown_report(report_output_path)
    generator.generate_web_data_js(web_data_path)

    with open(json_output_path, "w", encoding="utf-8") as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
