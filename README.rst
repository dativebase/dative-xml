================================================================================
  Dative XML - README
================================================================================

This project contains Relax NG schemata and a Python validator for Dative XML.

- dative-xml-validate.py: Python validator script
- dative-xml.rnc        :  Relax NG compact syntax schema - SOURCE
- dative-xml.rng        :  Relax NG schema - DERIVED from .rnc
- dative-xml.xsd        :  XML Schema Datatype schema - DERIVED from .rng via Trang

To validate a file like dative-xml-test.xml against the RNC schema
dative-xml.rnc (and generate the RNG file dative-xml.rng in the process)::

    $ python dative-xml-validate.py dative-xml-test.xml dative-xml.rnc

If you have Trang installed, you can convert the .rng file to an XML Schema
Datatype (.xsd) document with the following command::

    $ trang -I rng -O xsd dative-xml.rng dative-xml.xsd

TODOs
================================================================================

1. Write Selenium or PhantomJS scripts that download every possible type of XML
   export from a live Dative system with data in it and then run them through
   the Python validator to confirm they are valid.

