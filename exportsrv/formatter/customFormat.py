# -*- coding: utf-8 -*-

from datetime import datetime
from flask import current_app
from textwrap import fill
import re
import cgi

from adsutils.ads_utils import get_pub_abbreviation

from exportsrv.formatter.format import Format
from exportsrv.formatter.ads import adsFormatter, adsOrganizer
from exportsrv.formatter.cslJson import CSLJson
from exportsrv.formatter.csl import CSL
from exportsrv.formatter.toLaTex import encode_laTex, encode_laTex_author
from exportsrv.formatter.strftime import strftime

# This class accepts JSON object created by Solr and can reformats it
# for the user define Custom Format Export.
# To get custom formatted data first pass in the custom format string
# to parse it and determine the Solr fields needed
#    custom_format = CustomFormat(customFormatStr)
#    custom_format.get_solr_fields()
# Next pass the fields to Solr and get the JSON code back and finaly use
#    custom_format.set_json_from_solr(jsonFromSolr)
#    custom_format.getCustomFormat()

class CustomFormat(Format):

    REGEX_AUTHOR = re.compile(r'%(\d*\.?\d*)(\w)')
    REGEX_ENUMERATION = re.compile(r'(%z)')
    REGEX_COMMAND = [
        re.compile(r'(%Z(?:Encoding|Linelength):(?:unicode|html|latex|\d+)\s?)'),
        re.compile(r'(%Z(?:Header|Footer):\".+?\"\s?)'),
    ]
    REGEX_CUSTOME_FORMAT = re.compile(
        r'''(                                           # start of capture group 1
            %                                           # literal "%"
            (?:                                         # first option
            (?:\d+|\*)?                                 # width
            (?:\.(?:\d+|\*))?                           # precision
            [AaBcCdDEFGgHhIJjKLlMmNnOpPQqRSTUuVWXxY]    # type
            )
        )''', flags=re.X
    )

    custom_format = ''
    parsed_spec = []
    from_cls = {}
    author_count = {}

    def __init__(self, custom_format):
        """

        :param custom_format:
        """
        Format.__init__(self, None)
        self.custom_format = custom_format
        self.export_format = adsFormatter.unicode
        self.line_length = 80
        self.header = ''
        self.footer = ''
        self.enumeration = False
        self.__parse()


    def get_solr_fields(self):
        """
        from the user specified specifiers, compile a list of fields to get from Solr
        
        :return: 
        """
        solr_fields = ''
        for element in self.parsed_spec:
            if element[2] not in solr_fields:
                solr_fields += element[2] + ','
        # make sure we always bring back the bibcode
        # note that if at some point we allow alternative bibcode to be part
        # of custom formating this line fails, but until then we should be OK
        if 'bibcode' not in solr_fields:
            solr_fields += 'bibcode,'
        # don't need the last comma
        return solr_fields[:-len(',')]


    def __get_num_authors(self):
        """

        :return:
        """
        num_authors = []
        for a_doc in self.from_solr['response'].get('docs'):
            if 'author' in a_doc:
                num_authors.append(len(a_doc['author']))
            else:
                num_authors.append(0)
        return num_authors

    
    def set_json_from_solr(self, from_solr):
        """
        save the data from Solr, and go through it
        for every author format call CSL to style the authors
        
        :param from_solr: 
        :return: 
        """
        self.from_solr = from_solr
        if (self.from_solr.get('responseHeader')):
            self.status = self.from_solr['responseHeader'].get('status', self.status)
        json_for_csl = CSLJson(self.from_solr).get_author()
        for element in self.parsed_spec:
            if (element[2] == 'author'):
                # my mac has been formatted for case-insensitive
                # so need to make lower case doubled to be different
                # shall continue with this eventhough on the Linux side we shall be OK
                if (element[1][-1].isupper()):
                    csl_file_name = 'ads-author-' + element[1][-1]
                else:
                    csl_file_name = 'ads-author-' + element[1][-1] + element[1][-1]
                key = element[1]
                self.from_cls[key] = CSL(json_for_csl, csl_file_name).get(adsOrganizer.bibliography)
                self.author_count[key] = self.__get_num_authors()


    def __get_solr_field(self, specifier):
        """
        from specifier to Solr fields
        
        :param specifier: 
        :return: 
        """
        fieldDict = {
            'A': 'author',
            'a': 'author',
            'B': 'abstract',
            'c': 'citation_count',
            'C': 'copyright',
            'd': 'doi',
            'D': 'date',
            'F': 'aff',
            'G': 'author',
            'g': 'author',
            'H': 'author',
            'h': 'author',
            'I': 'author',
            'J': 'pub',
            'j': 'pub',
            'K': 'keyword',
            'L': 'author',
            'l': 'author',
            'M': 'author',
            'm': 'author',
            'N': 'author',
            'n': 'author',
            'O': '',  # Object Names
            'p': 'page',
            'P': 'lastpage',  # Last Page
            'Q': 'pub_raw',
            'q': 'pub',
            'R': 'bibcode',
            'T': 'title',
            'U': 'url',
            'u': 'url',
            'V': 'volume',
            'W': 'doctype',
            'X': 'pub_raw',
            'x': 'comment',
            'Y': 'year'
        }
        specifier = specifier[-1]
        return fieldDict.get(specifier, '')


    def __set_export_format(self, format):
        """
        format can be one of the followings: unicode, html, latex
        
        :param format: 
        :return: 
        """
        if (format == 'unicode'):
            self.export_format = adsFormatter.unicode
        elif (format == 'html'):
            self.export_format = adsFormatter.html
        elif (format == 'latex'):
            self.export_format = adsFormatter.latex
        else:
            self.export_format = adsFormatter.unicode


    def __parse_enumeration(self):
        """
        see if enumeration specifier has been defined in the custom format string

        :return:
        """
        matches = self.REGEX_ENUMERATION.findall(self.custom_format)
        if (len(matches) >= 1):
            for match in matches:
                self.custom_format = match.replace('', self.custom_format)
                self.enumeration = True


    def __parse_command(self):
        """
        see if command specifier has been defined in the custom format string

        :return:
        """
        for token in self.REGEX_COMMAND:
            matches = token.findall(self.custom_format)
            if (len(matches) >= 1):
                for match in matches:
                    self.custom_format = self.custom_format.replace(match, '', len(match))
                    # remove %Z and split on :
                    parts = match[2:].strip().split(':')
                    if (len(parts) == 2):
                        if (parts[0] == 'Encoding'):
                            self.__set_export_format(parts[1])
                        elif (parts[0] == 'Linelength'):
                            self.line_length = int(parts[1])
                        elif (parts[0] == 'Header'):
                            self.header = parts[1].replace('"', '').decode('string_escape')
                        elif (parts[0] == 'Footer'):
                            self.footer = parts[1].replace('"', '').decode('string_escape')


    def __parse(self):
        """
        parse the custom format string to identify the requested fields

        :return:
        """
        self.parsed_spec = []
        self.__parse_command()
        self.__parse_enumeration()
        for m in self.REGEX_CUSTOME_FORMAT.finditer(self.custom_format):
            self.parsed_spec.append(tuple((m.start(1), m.group(1), self.__get_solr_field(m.group(1)))))


    def __format_date(self, solr_date, date_format):
        """

        :param solr_date:
        :param date_format:
        :return:
        """
        # solr_date has the format 2017-12-01T00:00:00Z
        date_time = datetime.strptime(solr_date, '%Y-%m-%dT%H:%M:%SZ')
        formats = {'D': '%m/%Y', 'Y': '%Y'}
        return strftime(date_time, formats[date_format])


    def __format_url(self, bibcode, url_format):
        """

        :param bibcode:
        :param url_format:
        :return:
        """
        # U: has form: <a href="url">bibcode</a>
        # u: has the form: url/bibcode
        formats = {'U': u'<a href="{}">{}</a>', 'u': u'{}/{}'}
        path = current_app.config['EXPORT_SERVICE_FROM_BBB_URL']
        if (len(bibcode) > 0):
            return formats[url_format].format(path, bibcode)
        return ''


    def __format_line_wrapped(self, text, index):
        """

        :param text:
        :param index:
        :return:
        """
        # remove line break if any
        text = text.replace('\\n', '')

        formatStyle = u'{0:>2} {1}'
        if (self.line_length == 0):
            # no linewrap here, so just adjust the linefeed if exists
            if (self.enumeration):
                result = formatStyle.format(index+1, text)
            else:
                result = text
        else:
            if (self.enumeration):
                wrapped = fill(text, width=self.line_length, subsequent_indent=' ' * 4, replace_whitespace=False)
                result = formatStyle.format(index+1, wrapped)
            else:
                result = fill(text, width=self.line_length, replace_whitespace=False)
        return result + '\n'


    def __get_affiliation_list(self, a_doc):
        """

        :param a_doc:
        :return:
        """
        if ('aff') in a_doc:
            counter = [''.join(i) for i in self.generate_counter_id(len(a_doc['aff']))]
            separator = '; '
            affiliation_list = ''
            for affiliation, i in zip(a_doc['aff'], range(len(a_doc['aff']))):
                affiliation_list += counter[i] + '(' + affiliation + ')' + separator
            # do not need the last separator
            if (len(affiliation_list) > len(separator)):
                affiliation_list = affiliation_list[:-len(separator)]
            return affiliation_list
        return ''


    def __get_n_authors(self, author_list, n, separator, n_parts_author, before_last):
        """

        :param author_list:
        :param n:
        :param separator:
        :param n_parts_author:
        :param before_last:
        :return:
        """
        split_parts = author_list.replace(before_last, '').split(separator)
        if (n == 1):
            return separator.join(split_parts[:n_parts_author])
        if (len(before_last) == 0):
            before_last = ' '
        return separator.join(split_parts[:(n - 1) * n_parts_author]) + before_last + \
               separator.join(split_parts[(n - 1) * n_parts_author:n * n_parts_author])


    def __get_author_list_shorten(self, author_list, num_authors, format, m, n):
        """
        Formats	First Author	Second Author..	Before Last	    shorten
        A	        As in db	    As in db	    and	            first author, et al.
        G	        lastname f. i.	lastname f. i.	                first author, et al.
        H	        lastname	    lastname	    and	            display requested number of authors
        I	        lastname f. i.	f. i. lastname	and	            first author, and xx colleagues
        L	        lastname, f. i.	lastname, f. i.	and	            first author, and xx colleagues
        N	        lastname, f. i.	lastname, f. i.		            first author, and xx colleagues
        l	        lastname, f. i.	lastname, f. i.	&	            first author, et al.
        M	        lastname	    lastname	and	                first author, et al.
        m	        lastname	    lastname	&	                first author, et al.
        n	        lastname	    +
        a	        lastname
        g	        lastname, f.i.	lastname, f.i.	and	            first author, and xx colleagues
        h	        lastname	    lastname	    and	            first author \emph{et al.}

        n.m: Maximum number of entries in field (optional).
        If the number of authors in the list is larger than n, the list will be truncated and returned as
        "author1, author2, ..., authorm, et al.". If m is not specified, n.1 is assumed.

        :param author_list:
        :param num_authors:
        :param format:
        :param m:
        :param n:
        :return:
        """
        format_etal = u'{}, et al.'
        format_n_authors = u'{} and {}'
        format_with_n_colleagues = u'{}, and {} colleagues'
        format_escape_emph = u'{} \emph{{et al.}}'
        format_plus = u'{}+'

        if (num_authors <= n) or (num_authors <= m):
            return author_list
        if (format == 'A'):
            # in db we have LastName, FirstName (or FirstInitial.) MiddleInitial.
            # hence the first part is the LastName
            return format_etal.format(self.__get_n_authors(author_list, n, u',', 2, u', and'))
        if (format == 'G'):
            # return LastName et. al. - list is separated by a space
            return format_etal.format(self.__get_n_authors(author_list, n, u' ', 2, u''))
        if (format == 'M'):
            # return n authors (LastName) et. al. - list is separated by a comma
            return format_etal.format(self.__get_n_authors(author_list, n, u',', 1, u', and'))
        if (format == 'm'):
            # return n authors (LastName) et. al. - list is separated by a space
            return format_etal.format(self.__get_n_authors(author_list, n, u',', 1, u', \&'))
        if (format == 'H'):
            # return the asked number of authors - list is separated by space,
            # there is an and before the last author
            authors = author_list.split(' ')
            if (m == 1):
                return authors[0]
            else:
                authors.remove('and')
                return format_n_authors.format(' '.join(authors[:m-1]), authors[m])
        if (format == 'I') or (format == 'L') or (format == 'N') or (format == 'g'):
            # return LastName and count list is separated by a comma
            authors = author_list.split(',')
            return format_with_n_colleagues.format(authors[0], num_authors-1)
        if (format == 'l'):
            # return n author(s) et. al. - list is separated by a comma
            return format_etal.format(self.__get_n_authors(author_list, n, u',', 2, u' \&'))
        if (format == 'h'):
            authors = author_list.split(' ')
            return format_escape_emph.format(authors[0])
        if (format == 'n'):
            authors = author_list.split(' ')
            return format_plus.format(authors[0])
        if (format == 'a'):
            # return first authors Lastname only
            # this is already done at the CSL level so just return what was passed in
            return format_etal.format(self.__get_n_authors(author_list, n, u',', 2, u', \&'))
        return author_list


    def __get_author_list(self, format, index):
        """

        :param format:
        :param index:
        :return:
        """
        authors = self.from_cls.get(format)[index]
        count = self.author_count.get(format)[index]
        # see if author list needs to get shorten
        # n.m: Maximum number of entries in author field (optional).
        # If the number of authors in the list is larger than n, the list will be truncated to m entries.
        # If.m is not specified, n.1 is assumed.
        matches = self.REGEX_AUTHOR.findall(format)
        if (len(matches) >= 1) and (len(matches[0][0]) > 0):
            shorten = matches[0][0].split('.')
            if (len(shorten) > 1):
                return self.__get_author_list_shorten(authors, count, matches[0][1], int(str(shorten[0])), int(str(shorten[1])))
            else:
                return self.__get_author_list_shorten(authors, count, matches[0][1], int(str(shorten[0])), 1)
        return authors


    def __get_keywords(self, a_doc):
        """

        :param a_doc:
        :return:
        """
        if ('keyword') in a_doc:
            separator = ', '
            keyword_list = ''
            for keyword in a_doc['keyword']:
                keyword_list += keyword + separator
            # do not need the last separator
            if (len(keyword_list) > len(separator)):
                keyword_list = keyword_list[:-len(separator)]
            return keyword_list
        return ''

    
    def __add_clean_pub_raw(self, a_doc):
        """
        parse pub_raw and eliminate tags
        
        :param a_doc: 
        :return: 
        """
        pub_raw = ''.join(a_doc.get('pub_raw', ''))
        # proceed only if necessary
        if ('<' in pub_raw) and ('>' in pub_raw):
            for key in self.REGEX_PUB_RAW:
                pub_raw = key.sub(self.REGEX_PUB_RAW[key], pub_raw)
        return pub_raw


    def __get_publication(self, format, a_doc):
        """

        :param format:
        :param a_doc:
        :return:
        """
        format = format[-1]
        if (format == 'J'):
            # returns the journal name
            return a_doc.get('pub', '')
        if (format == 'j'):
            # returns an AASTeX macro for the journal if available, otherwise
            # returns the journal name
            journalMacros = dict([(k, v) for k, v in current_app.config['EXPORT_SERVICE_AASTEX_JOURNAL_MACRO']])
            return journalMacros.get(a_doc.get('pub', '').replace('The ', ''), a_doc.get('pub', ''))
        if (format == 'Q'):
            # returns the full journal information
            return self.__add_clean_pub_raw(a_doc)
        if (format == 'q'):
            # returns the journal abbreviation
            abbreviation = get_pub_abbreviation(a_doc.get('pub', ''), numBest=1, exact=True)
            if (len(abbreviation) > 0):
                return abbreviation[0][1].strip('.')
            return ''
        return ''


    def __encode(self, text, name):
        """

        :param text:
        :param name:
        :return:
        """
        if (self.export_format == adsFormatter.unicode):
            return text
        if (self.export_format == adsFormatter.html):
            return cgi.escape(text)
        if (self.export_format == adsFormatter.latex):
            if (name == 'author'):
                return encode_laTex_author(text)
            # do not encode publication since it could be the macro
            if (name == 'pub'):
                return text
            return encode_laTex(text)
        return text


    def __add_in(self, result, field, value):
        """

        :param result:
        :param field:
        :param value:
        :return:
        """
        if (len(value) > 0):
            return result.replace(field[1], self.__encode(value, field[2]))
        else:
            precede = r'(\\?[\(|\{|\[|\"]?(\\\\[a-z]{2}\s)?[\\|\s|,|-]?'
            succeed = r'[\\|,]?[\)|\}|\]|\"]?[\\|,]?)'
            return re.sub(precede + field[1] + succeed, '', result)


    def __get_doc(self, index):
        """

        :param index: index to the docs structure returned from solr
        :return:
        """
        result = self.custom_format
        a_doc = self.from_solr['response'].get('docs')[index]
        for field in self.parsed_spec:
            if (field[2] == 'title') or (field[2] == 'page') or (field[2] == 'lastpage') or \
               (field[2] == 'doi') or (field[2] == 'comment'):
                result = self.__add_in(result, field, ''.join(a_doc.get(field[2], '')))
            elif (field[2] == 'author'):
                result = self.__add_in(result, field, self.__get_author_list(field[1], index))
            elif (field[2] == 'doctype'):
                result = self.__add_in(result, field, self.__get_doc_type(a_doc.get(field[2], '')))
            elif (field[2] == 'date'):
                result = self.__add_in(result, field, self.__format_date(a_doc.get(field[2], ''), field[1][-1]))
            elif (field[2] == 'aff'):
                result = self.__add_in(result, field, self.__get_affiliation_list(a_doc))
            elif (field[2] == 'keyword'):
                result = self.__add_in(result, field, self.__get_keywords(a_doc))
            elif (field[2] == 'url'):
                result = self.__add_in(result, field, self.__format_url(a_doc.get('bibcode', ''), field[1][-1]))
            elif (field[2] == 'abstract') or (field[2] == 'copyright') or (field[2] == 'bibcode') or \
                 (field[2] == 'volume') or (field[2] == 'year'):
                result = self.__add_in(result, field, a_doc.get(field[2], ''))
            elif (field[2] == 'pub') or (field[2] == 'pub_raw'):
                result = self.__add_in(result, field, self.__get_publication(field[1], a_doc))
            elif (field[2] == 'citation_count'):
                result = self.__add_in(result, field, str(a_doc.get(field[2], '')))
        return self.__format_line_wrapped(result, index)


    def get(self):
        """
        
        :return: result of formatted records in a dict
        """
        num_docs = 0
        results = []
        if (self.status == 0):
            if len(self.header):
                results.append(self.header + '\n')
            num_docs = self.get_num_docs()
            for index in range(num_docs):
                results.append(self.__get_doc(index))
            results.append('\n' + self.footer)
        result_dict = {}
        result_dict['msg'] = 'Retrieved {} abstracts, starting with number 1.'.format(num_docs)
        result_dict['export'] = ''.join(result for result in results)
        return result_dict
