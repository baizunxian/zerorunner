# encoding: utf-8

import io
import json
import os
from base64 import b64encode
from collections import Iterable
from datetime import datetime

from jinja2 import Template
from loguru import logger

from autotest.httprunner.compat import basestring, bytes, numeric_types


def render_html_report(summary, html_report_name=None, html_report_template=None):
    """ render html report with specified report name and template
        if html_report_name is not specified, use current datetime
        if html_report_template is not specified, use default report template
    """
    if not html_report_template:
        html_report_template = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "templates",
            "default_report_template.html"
        )
        logger.debug("No html report template specified, use default.")
    else:
        logger.info("render with html report template: {}".format(html_report_template))

    logger.info("Start to render Html report ...")
    logger.debug("render data: {}".format(summary))

    report_dir_path = os.path.join(os.getcwd(), "reports")
    start_at_timestamp = int(summary["time"]["start_at"])
    summary["time"]["start_datetime"] = datetime.fromtimestamp(start_at_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    if html_report_name:
        summary["html_report_name"] = html_report_name
        report_dir_path = os.path.join(report_dir_path, html_report_name)
        html_report_name += "-{}.html".format(start_at_timestamp)
    else:
        summary["html_report_name"] = ""
        html_report_name = "{}.html".format(start_at_timestamp)

    if not os.path.isdir(report_dir_path):
        os.makedirs(report_dir_path)

    for index, suite_summary in enumerate(summary["details"]):
        if not suite_summary.get("name"):
            suite_summary["name"] = "test suite {}".format(index)
        for record in suite_summary.get('step_datas'):
            meta_data = record['data']['req_resps'][0]
            stringify_data(meta_data, 'request')
            stringify_data(meta_data, 'response')

    with io.open(html_report_template, "r", encoding='utf-8') as fp_r:
        template_content = fp_r.read()
        report_path = os.path.join(report_dir_path, html_report_name)
        with io.open(report_path, 'w', encoding='utf-8') as fp_w:
            rendered_content = Template(template_content).render(summary)
            fp_w.write(rendered_content)

    logger.info("Generated Html report: {}".format(report_path))

    return report_path


def stringify_data(meta_data, request_or_response):
    headers = meta_data[request_or_response]["headers"]

    request_or_response_dict = meta_data[request_or_response]

    for key, value in request_or_response_dict.items():

        if isinstance(value, list):
            value = json.dumps(value, indent=2, ensure_ascii=False)

        elif isinstance(value, bytes):
            try:
                encoding = meta_data["response"].get("encoding")
                if not encoding or encoding == "None":
                    encoding = "utf-8"

                content_type = meta_data["response"]["content_type"]
                if "image" in content_type:
                    meta_data["response"]["content_type"] = "image"
                    value = "data:{};base64,{}".format(
                        content_type,
                        b64encode(value).decode(encoding)
                    )
                else:
                    value = value.decode(encoding)
            except UnicodeDecodeError:
                pass

        elif not isinstance(value, (basestring, numeric_types, Iterable)):
            # class instance, e.g. MultipartEncoder()
            value = repr(value)

        meta_data[request_or_response][key] = value
