# -*- coding: utf-8 -*-

from flask_testing import TestCase
import unittest

import exportsrv.app as app

from stubdata import solrdata, bibTexTest, fieldedTest, xmlTest, cslTest, customTest
from exportsrv.views import default_solr_fields, \
    return_bibTex_format_export, return_fielded_format_export, return_xml_format_export, return_csl_format_export
from exportsrv.formatter.bibTexFormat import BibTexFormat
from exportsrv.formatter.fieldedFormat import FieldedFormat
from exportsrv.formatter.xmlFormat import XMLFormat
from exportsrv.formatter.cslJson import CSLJson
from exportsrv.formatter.csl import CSL, adsFormatter
from exportsrv.formatter.customFormat import CustomFormat
from exportsrv.formatter.convertCF import convert


class TestExports(TestCase):
    def create_app(self):
        app_ = app.create_app()
        return app_

    def test_bibtex(self):
        # format the stubdata using the code
        bibtex_export = BibTexFormat(solrdata.data).get(include_abs=False)
        # now compare it with an already formatted data that we know is correct
        assert(bibtex_export == bibTexTest.data)

    def test_bibtex_with_abs(self):
        # format the stubdata using the code
        bibtex_export = BibTexFormat(solrdata.data).get(include_abs=True)
        # now compare it with an already formatted data that we know is correct
        assert (bibtex_export == bibTexTest.data_with_abs)

    def test_ads(self):
        # format the stubdata using the code
        fielded_export = FieldedFormat(solrdata.data).get_ads_fielded()
        # now compare it with an already formatted data that we know is correct
        assert (fielded_export == fieldedTest.data_ads)

    def test_endnote(self):
        # format the stubdata using the code
        fielded_export = FieldedFormat(solrdata.data).get_endnote_fielded()
        # now compare it with an already formatted data that we know is correct
        assert (fielded_export == fieldedTest.data_endnote)

    def test_procite(self):
        # format the stubdata using the code
        fielded_export = FieldedFormat(solrdata.data).get_procite_fielded()
        # now compare it with an already formatted data that we know is correct
        assert (fielded_export == fieldedTest.data_procite)

    def test_refman(self):
        # format the stubdata using the code
        fielded_export = FieldedFormat(solrdata.data).get_refman_fielded()
        # now compare it with an already formatted data that we know is correct
        assert (fielded_export == fieldedTest.data_refman)

    def test_refworks(self):
        # format the stubdata using the code
        fielded_export = FieldedFormat(solrdata.data).get_refworks_fielded()
        # now compare it with an already formatted data that we know is correct
        assert (fielded_export == fieldedTest.data_refworks)

    def test_medlars(self):
        # format the stubdata using the code
        fielded_export = FieldedFormat(solrdata.data).get_medlars_fielded()
        # now compare it with an already formatted data that we know is correct
        assert (fielded_export == fieldedTest.data_medlars)

    def test_dublinxml(self):
        # format the stubdata using the code
        xml_export = XMLFormat(solrdata.data).get_dublincore_xml()
        # now compare it with an already formatted data that we know is correct
        assert(xml_export == xmlTest.data_dublin_core)

    def test_refxml(self):
        # format the stubdata using the code
        xml_export = XMLFormat(solrdata.data).get_reference_xml(include_abs=False)
        # now compare it with an already formatted data that we know is correct
        assert(xml_export == xmlTest.data_ref)

    def test_refxml_with_abs(self):
        # format the stubdata using the code
        xml_export = XMLFormat(solrdata.data).get_reference_xml(include_abs=True)
        # now compare it with an already formatted data that we know is correct
        assert(xml_export == xmlTest.data_ref_with_abs)

    def test_aastex(self):
        # format the stubdata using the code
        csl_export = CSL(CSLJson(solrdata.data).get(), 'aastex', adsFormatter.latex).get()
        # now compare it with an already formatted data that we know is correct
        assert (csl_export == cslTest.data_AASTex)

    def test_icarus(self):
        # format the stubdata using the code
        csl_export = CSL(CSLJson(solrdata.data).get(), 'icarus', adsFormatter.latex).get()
        # now compare it with an already formatted data that we know is correct
        assert (csl_export == cslTest.data_Icarus)

    def test_mnras(self):
        # format the stubdata using the code
        csl_export = CSL(CSLJson(solrdata.data).get(), 'mnras', adsFormatter.latex).get()
        # now compare it with an already formatted data that we know is correct
        assert(csl_export == cslTest.data_MNRAS)

    def test_soph(self):
        # format the stubdata using the code
        csl_export = CSL(CSLJson(solrdata.data).get(), 'soph', adsFormatter.latex).get()
        # now compare it with an already formatted data that we know is correct
        assert (csl_export == cslTest.data_SoPh)

    def test_aspc(self):
        # format the stubdata using the code
        csl_export = CSL(CSLJson(solrdata.data).get(), 'aspc', adsFormatter.latex).get()
        # now compare it with an already formatted data that we know is correct
        assert (csl_export == cslTest.data_ASPC)

    def test_apsj(self):
        # format the stubdata using the code
        csl_export = CSL(CSLJson(solrdata.data).get(), 'apsj', adsFormatter.latex).get()
        # now compare it with an already formatted data that we know is correct
        assert (csl_export == cslTest.data_APSJ)

    def test_aasj(self):
        # format the stubdata using the code
        csl_export = CSL(CSLJson(solrdata.data).get(), 'aasj', adsFormatter.latex).get()
        # now compare it with an already formatted data that we know is correct
        assert (csl_export == cslTest.data_AASJ)

    def test_custom(self):
        # format the stubdata using the code
        custom_format = CustomFormat(custom_format=r'\\bibitem[%m\(%Y)]{%2H%Y}\ %5.3l\ %Y\,%j\,%V\,%p \n')
        custom_format.set_json_from_solr(solrdata.data)
        # now compare it with an already formatted data that we know is correct
        assert (custom_format.get() == customTest.data)

    def test_convert(self):
        assert(convert("\\\\bibitem[%\\2m%(y)]\{%za1%y} %\\8l %\\Y,%\\j,%\\V,%\\p") == "\\\\bibitem[%2m\\(%Y)]\\{%H%Y} %8l\\ %Y\\,%j\\,%V\\,%p\\")

    def test_ads_formatter(self):
        assert(adsFormatter().verify('1'), True)
        assert(adsFormatter().verify(1), True)
        assert(adsFormatter().verify('10'), False)
        assert(adsFormatter().verify(10), False)

    def test_default_solr_fields(self):
        default_fields = 'author,title,year,date,pub,pub_raw,issue,volume,page,page_range,aff,doi,abstract,' \
                         'citation_count,read_count,bibcode,identifier,copyright,keyword,doctype,' \
                         'reference,comment,property,esources,data,isbn,pubnote'
        assert (default_solr_fields() == default_fields)

    def test_bibtex_status(self):
        bibTex_export = BibTexFormat(solrdata.data)
        assert(bibTex_export.get_status() == 0)

    def test_bibtex_no_num_docs(self):
        solr_data = \
            {
               "responseHeader":{
                  "status":1,
                  "QTime":1,
                  "params":{
                     "sort":"date desc",
                     "fq":"{!bitset}",
                     "rows":"19",
                     "q":"*:*",
                     "start":"0",
                     "wt":"json",
                     "fl":"author,title,year,date,pub,pub_raw,issue,volume,page,page_range,aff,doi,abstract,citation_count,read_count,bibcode,identification,copyright,keyword,doctype,reference,comment,property,esources,data"
                  }
               }
            }
        bibTex_export = BibTexFormat(solr_data)
        assert(bibTex_export.get_num_docs() == 0)

    def test_bibtex(self):
        response = return_bibTex_format_export(solrdata.data, False)
        assert(response._status_code == 200)

    def test_bibtex_no_data(self):
        response = return_bibTex_format_export(None, False)
        assert(response._status_code == 404)

    def test_bibtex_data_error(self):
        solr_data = {"error" : "data error"}
        response = return_bibTex_format_export(solr_data, False)
        assert(response._status_code == 400)

    def test_bibtex_eprint(self):
        bibTex_export = BibTexFormat(solrdata.data)

        a_doc_no_eprint = solrdata.data['response'].get('docs')[0]
        assert(bibTex_export._BibTexFormat__add_eprint(a_doc_no_eprint) == '')

        a_doc_eprint = \
            {
                "bibcode": "1997NuPhB.490..121R",
                "identifier": ["1996hep.th...11047R",
                               "1996hep.th...11047R",
                               "hep-th/9611047",
                               "10.1016/S0550-3213(97)00055-2",
                               "10.1016/S0550-3213(97)00055-2",
                               "1997NuPhB.490..121R"],
                "esources": ["EPRINT_HTML",
                             "EPRINT_PDF",
                             "PUB_HTML"]
            }
        assert(bibTex_export._BibTexFormat__add_eprint(a_doc_eprint) == 'arXiv:hep-th/9611047')

        a_doc_ascl = \
            {
                "identifier": ["ascl:1308.009",
                               "2013ascl.soft08009C",
                               "ascl:1308.009"],
                "bibcode": "2013ascl.soft08009C",
                "esources": ["PUB_HTML"]
            }
        assert(bibTex_export._BibTexFormat__add_eprint(a_doc_ascl) == 'ascl:1308.009')

    def test_fielded_status(self):
        fielded_export = FieldedFormat(solrdata.data)
        assert(fielded_export.get_status() == 0)

    def test_bibtex_no_num_docs(self):
        solr_data = \
            {
               "responseHeader":{
                  "status":1,
                  "QTime":1,
                  "params":{
                     "sort":"date desc",
                     "fq":"{!bitset}",
                     "rows":"19",
                     "q":"*:*",
                     "start":"0",
                     "wt":"json",
                     "fl":"author,title,year,date,pub,pub_raw,issue,volume,page,page_range,aff,doi,abstract,citation_count,read_count,bibcode,identification,copyright,keyword,doctype,reference,comment,property,esources,data"
                  }
               }
            }
        fielded_export = FieldedFormat(solr_data)
        assert(fielded_export.get_num_docs() == 0)

    def test_fielded(self):
        for fielded_style in ['ADS','EndNote','ProCite','Refman','RefWorks','MEDLARS']:
            response = return_fielded_format_export(solrdata.data, fielded_style)
            assert(response._status_code == 200)

    def test_fielded_no_data(self):
        for fielded_style in ['ADS','EndNote','ProCite','Refman','RefWorks','MEDLARS']:
            response = return_fielded_format_export(None, fielded_style)
            assert(response._status_code == 404)

    def test_fielded_data_error(self):
        solr_data = {"error" : "data error"}
        for fielded_style in ['ADS','EndNote','ProCite','Refman','RefWorks','MEDLARS']:
            response = return_fielded_format_export(solr_data, fielded_style)
            assert(response._status_code == 400)

    def test_fielded_eprint(self):
        fielded_export = FieldedFormat(solrdata.data)

        a_doc_no_eprint = solrdata.data['response'].get('docs')[0]
        assert(fielded_export._FieldedFormat__add_eprint(a_doc_no_eprint) == '')

        a_doc_eprint = \
            {
                "bibcode": "1997NuPhB.490..121R",
                "identifier": ["1996hep.th...11047R",
                               "1996hep.th...11047R",
                               "hep-th/9611047",
                               "10.1016/S0550-3213(97)00055-2",
                               "10.1016/S0550-3213(97)00055-2",
                               "1997NuPhB.490..121R"],
                "esources": ["EPRINT_HTML",
                             "EPRINT_PDF",
                             "PUB_HTML"]
            }
        assert(fielded_export._FieldedFormat__add_eprint(a_doc_eprint) == 'arXiv:hep-th/9611047')

        a_doc_ascl = \
            {
                "identifier": ["ascl:1308.009",
                               "2013ascl.soft08009C",
                               "ascl:1308.009"],
                "bibcode": "2013ascl.soft08009C",
                "esources": ["PUB_HTML"]
            }
        assert(fielded_export._FieldedFormat__add_eprint(a_doc_ascl) == 'ascl:1308.009')

    def test_xml_status(self):
        xml_export = XMLFormat(solrdata.data)
        assert(xml_export.get_status() == 0)

    def test_xml_no_num_docs(self):
        solr_data = \
            {
               "responseHeader":{
                  "status":1,
                  "QTime":1,
                  "params":{
                     "sort":"date desc",
                     "fq":"{!bitset}",
                     "rows":"19",
                     "q":"*:*",
                     "start":"0",
                     "wt":"json",
                     "fl":"author,title,year,date,pub,pub_raw,issue,volume,page,page_range,aff,doi,abstract,citation_count,read_count,bibcode,identification,copyright,keyword,doctype,reference,comment,property,esources,data"
                  }
               }
            }
        xml_export = XMLFormat(solr_data)
        assert(xml_export.get_num_docs() == 0)

    def test_xml(self):
        for xml_style in ['DublinCore','Reference','ReferenceAbs']:
            response = return_xml_format_export(solrdata.data, xml_style)
            assert(response._status_code == 200)

    def test_xml_no_data(self):
        for xml_style in ['DublinCore','Reference','ReferenceAbs']:
            response = return_xml_format_export(None, xml_style)
            assert(response._status_code == 404)

    def test_xml_data_error(self):
        solr_data = {"error" : "data error"}
        for xml_style in ['DublinCore','Reference','ReferenceAbs']:
            response = return_xml_format_export(solr_data, xml_style)
            assert(response._status_code == 400)

    def test_xml_eprint(self):
        xml_export = XMLFormat(solrdata.data)

        a_doc_no_eprint = solrdata.data['response'].get('docs')[0]
        assert(xml_export._XMLFormat__add_eprint(a_doc_no_eprint) == '')

        a_doc_eprint = \
            {
                "bibcode": "1997NuPhB.490..121R",
                "identifier": ["1996hep.th...11047R",
                               "1996hep.th...11047R",
                               "hep-th/9611047",
                               "10.1016/S0550-3213(97)00055-2",
                               "10.1016/S0550-3213(97)00055-2",
                               "1997NuPhB.490..121R"],
                "esources": ["EPRINT_HTML",
                             "EPRINT_PDF",
                             "PUB_HTML"]
            }
        assert(xml_export._XMLFormat__add_eprint(a_doc_eprint) == 'arXiv:hep-th/9611047')

        a_doc_ascl = \
            {
                "identifier": ["ascl:1308.009",
                               "2013ascl.soft08009C",
                               "ascl:1308.009"],
                "bibcode": "2013ascl.soft08009C",
                "esources": ["PUB_HTML"]
            }
        assert(xml_export._XMLFormat__add_eprint(a_doc_ascl) == 'ascl:1308.009')

    def test_csl_status(self):
        csl_export = CSLJson(solrdata.data)
        assert(csl_export.get_status() == 0)

    def test_csl_no_num_docs(self):
        solr_data = \
            {
               "responseHeader":{
                  "status":1,
                  "QTime":1,
                  "params":{
                     "sort":"date desc",
                     "fq":"{!bitset}",
                     "rows":"19",
                     "q":"*:*",
                     "start":"0",
                     "wt":"json",
                     "fl":"author,title,year,date,pub,pub_raw,issue,volume,page,page_range,aff,doi,abstract,citation_count,read_count,bibcode,identification,copyright,keyword,doctype,reference,comment,property,esources,data"
                  }
               }
            }
        csl_export = CSLJson(solr_data)
        assert(csl_export.get_num_docs() == 0)

    def test_csl(self):
        export_format = 2
        for csl_style in ['aastex','icarus','mnras', 'soph', 'aspc', 'apsj', 'aasj']:
            response = return_csl_format_export(solrdata.data, csl_style, export_format)
            assert(response._status_code == 200)

    def test_csl_no_data(self):
        export_format = 2
        for csl_style in ['aastex','icarus','mnras', 'soph', 'aspc', 'apsj', 'aasj']:
            response = return_csl_format_export(None, csl_style, export_format)
            assert(response._status_code == 404)

    def test_csl_data_error(self):
        export_format = 2
        solr_data = {"error" : "data error"}
        for csl_style in ['aastex','icarus','mnras', 'soph', 'aspc', 'apsj', 'aasj']:
            response = return_csl_format_export(solr_data, csl_style, export_format)
            assert(response._status_code == 400)

if __name__ == '__main__':
  unittest.main()
