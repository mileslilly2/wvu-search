# xml_cleaner.py
import re

def clean_xml_with_log(xml_string, log_file="sanitization_log.txt"):
    issues = []

    # Find unescaped ampersands
    bad_amps = re.findall(r'&(?!amp;|lt;|gt;|quot;|apos;)', xml_string)
    if bad_amps:
        issues.append(f"Unescaped ampersands: {len(bad_amps)}")

    # Find illegal control characters
    bad_ctrl = re.findall(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', xml_string)
    if bad_ctrl:
        issues.append(f"Control characters: {len(bad_ctrl)}")

    if issues:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write("Sanitization issues detected:\n")
            for issue in issues:
                f.write(f"- {issue}\n")
            f.write("\n")

    # Fix the XML
    xml_string = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;)', '&amp;', xml_string)
    xml_string = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', xml_string)

    return xml_string
