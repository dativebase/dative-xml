"""dative-xml-validate.py is a Python script that validates a Dative XML
document against a Dative Relax NG pattern (schema) in compact form.

Usage::

    $ python dative-xml-validate.py xml-file relaxng-file

Requirements:

    - lxml
    - rnc2rng

It converts the .rnc file to a .rng file and prints validation success or
errors to stdout.

Note: if you have Trang installed, you can convert the .rng file to an XML
Schema Datatype (.xsd) document with the following command::

    $ trang -I rng -O xsd dative-xml.rng dative-xml.xsd
"""

from lxml import etree
from rnc2rng import parser, serializer
import os
import sys

OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'


def fail(txt):
    print('{fail}{txt}{end}'.format(fail=FAIL, txt=txt, end=ENDC))


def ok(txt):
    print('{ok}{txt}{end}'.format(ok=OKGREEN, txt=txt, end=ENDC))


def write_rnc_to_rng(rnc_file_path, rng_file_path):
    if not os.path.isfile(rnc_file_path):
        fail('There is no Dative Relax NG (compact) file at %s.' %
             rnc_file_path)
        sys.exit(1)
    with open(rnc_file_path) as input_:
        try:
            xml = serializer.XMLSerializer().toxml(parser.parse(f=input_))
        except parser.ParseError as e:
            fail('rnc2rng parse error ' + e.msg)
            sys.exit(1)
    with open(rng_file_path, 'w') as output:
        output.write(xml + '\n')


def parse_rng(rng_file_path):
    with open(rng_file_path) as f:
        relaxng_doc = etree.parse(f)
    relaxng = etree.RelaxNG(relaxng_doc)
    return relaxng


def validate(xml_file_path, rnc_file_path):
    rng_file_path = '%s.rng' % os.path.splitext(rnc_file_path)[0]
    write_rnc_to_rng(rnc_file_path, rng_file_path)
    relaxng = parse_rng(rng_file_path)
    if not os.path.isfile(xml_file_path):
        fail('There is no Dative XML file at %s.' % xml_file_path)
        sys.exit(1)
    with open(xml_file_path) as f:
        doc = etree.parse(f)
    try:
        relaxng.assertValid(doc)
        ok('{} is a valid Dative XML document.'.format(xml_file_path))
    except etree.DocumentInvalid:
        fail('{} is NOT a valid Dative XML document:'.format(xml_file_path))
        """
        for attr in dir(relaxng.error_log.last_error):
            if not attr.startswith('__'):
                print('{}: {}'.format(attr, getattr(relaxng.error_log.last_error, attr)))
        """
        fail(relaxng.error_log.last_error)


if __name__ == '__main__':

    if len(sys.argv) != 3:
        sys.exit('Usage: dative-xml-validate.py xml-file relaxng-file')
    xml_file_path, rnc_file_path = sys.argv[1:]
    validate(xml_file_path, rnc_file_path)
