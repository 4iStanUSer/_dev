import json
from iap.common.template_builder import generate_templates


def test_generate_templates():
    generate_templates('D:\Projects\IAP\SourceCode\IAP\dev_templates')
    filename = 'D:\Projects\IAP\SourceCode\IAP\dev_templates\JJOralCare.json'
    with open(filename) as file:
        data = json.load(file)
    filename = 'D:\Projects\IAP\SourceCode\IAP\dev_templates\JJLean.json'
    with open(filename) as file:
        data = json.load(file)