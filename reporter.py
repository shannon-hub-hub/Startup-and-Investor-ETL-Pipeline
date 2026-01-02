"""
Data Quality Reporter
"""

from datetime import datetime
import html

class DataQualityReporter:
    def __init__(self):
        self.issues = {
            'missing_values': [],
            'missing_categories': [],
            'duplicates': [],
            'format_issues': []
        }

    def check_missing_values(self, data):
        print("Checking for missing values...")

        if not data:
            return
        
        field_names = list(data[0].keys())
        missing_counts = {field: 0 for field in field_names}

        for record in data:
            for field in field_names:
                if not record.get(field):
                    missing_counts[field] += 1

        for field, count in missing_counts.items():
            if count > 0:
                percentage = (count / len(data)) * 100
                self.issues['missing_values'].append({
                    'field': field,
                    'count': count,
                    'total': len(data),
                    'percentage': round(percentage, 2)
                })
                print(f"Found {len(self.issues['missing_values'])} fields with missing values.")

    def check_duplicates(self, data, unique_fields=['name','website']):
        print("Checking for duplicates...")

        seen = {}

        for idx, record in enumerate(data):
            for field in unique_fields:
                value = record.get(field)
                if value:
                    key = f"{field}: {value}"
                    if key in seen:
                        self.issues['duplicates'].append({
                            'field': field,
                            'value': value,
                            'first_index': seen[key],
                            'duplicate_index': idx
                        })
                    else:
                        seen[key] = idx
        print(f"Found {len(self.issues['duplicates'])} duplicates.")
        
    def check_format_issues(self, data):
        print("Checking for format issues...")
        for record in data:
            # Check website format
            website = record.get('website')
            if website and not website.startswith("http"):
                self.issues['format_issues'].append({
                    'field': 'website',
                    'value': website,
                    'issue': 'Missing http/https protocol',
                    'record_name': record.get('name', 'Unknown')
                })

            # Check name capitalization
            name = record.get('name')
            if name:
                if name.isupper():
                    self.issues['format_issues'].append({
                        'field': 'name',
                        'issue': 'All uppercase',
                        'value': name,
                        'record_name': name
                    })
                elif name.islower():
                    self.issues['format_issues'].append({
                        'field': 'name',
                        'issue': 'All lowercase',
                        'value': name,
                        'record_name': name
                    })
        print(f"Found {len(self.issues['format_issues'])} format issues.")

    def generate_report(self, filename='data_quality_report.html'):
        
        html = [
            "<!DOCTYPE html>",
            "<html>"
            "<head>",
            "<meta charset='UTF-8'>",
            "<title>Data Quality Report</title>",
            "<style>",
            "body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }",
            "h1 { color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px;}",
            "h2 { color: #555; }",
            ".summary { background: white; padding: 20px; border-radius: 8px; margin: 20px 0; "
            "box-shadow: 0 2px 4px rgba(0,0,0,0.1); }",
            ".summary-item { display: inline-block; margin: 10px 20px; }",
            ".count { font-size: 32px; font-weight: bold; color: #4CAF50; }",
            "table { width: 100%; border-collapse: collapse; background: white; margin: 20px 0; "
            "box-shadow: 0 2px 4px rgba(0,0,0,0.1); }",
            "th { background: #4CAF50; color: white; padding: 12px; text-align: left; }",
            "td { padding: 10px; border-bottom: 1px solid #ddd; }",
            "tr:hover { background: #f9f9f9; }",
            ".issue { color: #f44336; font-weight: bold; }",
            ".warning { color: #ff9800; }",
            "</style>",
            "</head>",
            "<body>",
            f"<h1>📊 Data Quality Report</h1>",
            f"<p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>",
            "<div class='summary'>",
            f"<div class='summary-item'><div class='count'>{len(self.issues['missing_values'])}</div><div>Missing Values</div></div>",
            f"<div class='summary-item'><div class='count'>{len(self.issues['duplicates'])}</div><div>Duplicates</div></div>",
            f"<div class='summary-item'><div class='count'>{len(self.issues['format_issues'])}</div><div>Format Issues</div></div>",
            "</div>",
        ]

        # Missing Values
        if self.issues['missing_values']:
            html.append("<h2>1. Missing Values</h2>")
            html.append("<table><tr><th>Field</th><th>Missing</th><th>Total</th><th>%</th></tr>")
            for issue in self.issues['missing_values']:
                html.append(
                    f"<tr><td>{issue['field']}</td>"
                    f"<td class='issue'>{issue['count']}</td>"
                    f"<td>{issue['total']}</td>"
                    f"<td>{issue['percentage']}%</td></tr>"
                )
            html.append("</table>")
        else:
            html.append("<h2>1. Missing Values</h2><p>✅ No missing values found!</p>")

        # Duplicates
        if self.issues['duplicates']:
            html.append("<h2>2. Duplicate Records</h2>\n")
            html.append("<table>\n<tr><th>Field</th><th>Value</th><th>Record</th></tr>\n")
            for issue in self.issues['duplicates'][:20]:
                html.append(f"<tr><td>{issue['field']}</td><td class='issue'>{issue['value']}</td><td>{issue['record_name']}</td></tr>\n")
            if len(self.issues['duplicates']) > 20:
                html.append(f"<tr><td colspan='3'>...and {len(self.issues['duplicates']) - 20} more</td></tr>\n")
            html.append("</table>\n")
        else:
            html.append("<h2>2. Duplicate Records</h2>\n<p>✅ No duplicates found!</p>\n")

        # Format Issues
        if self.issues['format_issues']:
            html.append("<h2>3. Format Issues</h2>\n")
            html.append("<table>\n<tr><th>Record</th><th>Field</th><th>Issue</th><th>Value</th></tr>\n")
            for issue in self.issues['format_issues'][:20]:
                value = str(issue['value'])[:50] + '...' if len(str(issue['value'])) > 50 else issue['value']
                html.append(f"<tr><td>{issue['record_name']}</td><td>{issue['field']}</td><td class='warning'>{issue['issue']}</td><td>{value}</td></tr>\n")
            if len(self.issues['format_issues']) > 20:
                html.append(f"<tr><td colspan='4'>...and {len(self.issues['format_issues']) - 20} more</td></tr>\n")
            html.append("</table>\n")
        else:
            html.append("<h2>3. Format Issues</h2>\n<p>✅ No format issues found!</p>\n")
        
        html.append("</body>\n</html>")

        # Write to file
        with open("report.html", 'w', encoding='utf-8') as f:
            f.write("\n".join(html))
        print(f"report saved to: report.html")
        return "report.html"

    def run_all_checks(self, data):
        """Run all data quality checks."""
        print("\n" + "="*60)
        print("RUNNING DATA QUALITY CHECKS")
        print("="*60)
        
        self.check_missing_values(data)
        self.check_duplicates(data)
        self.check_format_issues(data)
        
        print("\n" + "="*60)
        print("DATA QUALITY CHECKS COMPLETED")
        print("="*60)
 
        
        