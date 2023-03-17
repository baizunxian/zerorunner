"""
HttpRunner html report

- result: define resultclass for unittest TextTestRunner
- gen_report: render html report with jinja2 template

"""

from zerorunner.report.html.result import HtmlTestResult
from zerorunner.report.html.gen_report import gen_html_report

__all__ = ["HtmlTestResult", "gen_html_report"]
