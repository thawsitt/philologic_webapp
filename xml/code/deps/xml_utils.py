import re
import xml.etree.ElementTree as ET
from xml.dom import minidom

# xml_utils.py (v1) Apr 09, 2018
# ------------------------------
# Utility (helper) functions used in main.py for writing XML output file.
# This module uses Python 3.
# Written by Thawsitt Naing (thawsitt@cs.stanford.edu).


class XMLUtils:
    def __init__(self, utils):
        self.utils = utils
        self.column_names = self.utils.getColumnNames()
        self.ignored_metadata_fields = self.utils.getIgnoredMetadataFields()

    def getXMLStr(self, text, footnotes, metadata, filename):
        root = self.getXMLTemplate()
        self.populateTeiHeader(root, metadata, filename)
        self.populateText(root, text, footnotes, metadata, filename)
        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
        return xmlstr

    def getXMLTemplate(self):
        root = ET.Element('root')

        # TEI Header
        teiHeader = ET.SubElement(root, 'teiHeader')
        fileDesc = ET.SubElement(teiHeader, 'fileDesc')

        # Title Statement
        titleStmt = ET.SubElement(fileDesc, 'titleStmt')
        title = ET.SubElement(titleStmt, 'title')
        recordID = ET.SubElement(titleStmt, 'recordID')
        transcription = ET.SubElement(titleStmt, 'transcription')
        respStmt = ET.SubElement(titleStmt, 'respStmt')
        resp = ET.SubElement(respStmt, 'resp')
        name = ET.SubElement(respStmt, 'name')
        note = ET.SubElement(respStmt, 'note')
        date = ET.SubElement(note, 'date')
        problems = ET.SubElement(note, 'problems')

        # Source Description
        sourceDesc = ET.SubElement(fileDesc, 'sourceDesc')
        baseText = ET.SubElement(sourceDesc, 'baseText')
        textNeeded = ET.SubElement(sourceDesc, 'textNeeded')
        noKnownText = ET.SubElement(sourceDesc, 'noKnownText')
        fragment = ET.SubElement(sourceDesc, 'fragment')
        ocrNote = ET.SubElement(sourceDesc, 'ocrNote')
        msDesc = ET.SubElement(sourceDesc, 'msDesc')
        bibl = ET.SubElement(sourceDesc, 'bibl')
        sourceNote = ET.SubElement(sourceDesc, 'sourceNote')

        source = ET.SubElement(msDesc, 'source')
        sourceOther = ET.SubElement(msDesc, 'sourceOther')
        _source = ET.SubElement(msDesc, '_source')

        edition = ET.SubElement(bibl, 'edition')
        editionOther = ET.SubElement(bibl, 'editionOther')
        _edition = ET.SubElement(bibl, '_edition')

        # Profile Description
        profileDesc = ET.SubElement(teiHeader, 'profileDesc')
        langUsage = ET.SubElement(profileDesc, 'langUsage')
        languageNote = ET.SubElement(profileDesc, 'languageNote')
        langUsage = ET.SubElement(profileDesc, 'langUsage')
        creation = ET.SubElement(profileDesc, 'creation')
        textDesc = ET.SubElement(profileDesc, 'textDesc')
        domain = ET.SubElement(textDesc, 'domain')
        genNotes = ET.SubElement(profileDesc, 'genNotes')

        # child nodes of 'creation'
        year = ET.SubElement(creation, 'year')
        origDate = ET.SubElement(creation, 'origDate')
        dateNotes = ET.SubElement(creation, 'dateNotes')
        origPlace = ET.SubElement(creation, 'origPlace')
        diocese = ET.SubElement(creation, 'diocese')
        diocese_id = ET.SubElement(creation, 'diocese_id')
        province = ET.SubElement(creation, 'province')
        country = ET.SubElement(creation, 'country')
        _allPlace = ET.SubElement(creation, '_allPlace')
        geo = ET.SubElement(creation, 'geo')
        placeNotes = ET.SubElement(creation, 'placeNotes')
        orgName = ET.SubElement(creation, 'orgName')
        persName = ET.SubElement(creation, 'persName')
        altName = ET.SubElement(creation, 'altName')
        _issuingAuthority = ET.SubElement(creation, '_issuingAuthority')
        regnalYears = ET.SubElement(creation, 'regnalYears')
        delegated = ET.SubElement(creation, 'delegated')
        classNotes = ET.SubElement(creation, 'classNotes')

        # Text
        text = ET.SubElement(root, 'text')
        body = ET.SubElement(text, 'body')

        return root

    # ---------------------------------------------
    # Helper Functions
    # ---------------------------------------------

    # def getTitleFromFileName(self, filename):
    #     #record_id = re.findall(r'^(.*?)_', filename)[0]
    #     name = re.findall(r'^(?:.*?)_(.*?)_(?:.*?)\.txt$', filename)[0]
    #     title = '{}'.format(name)
    #     return title

    # def getDateText(self, metadata):
    #     date_text = metadata['Year']
    #     if metadata['Month']:
    #         date_text += '-{}'.format(str(int(metadata['Month'])).zfill(2))
    #     if metadata['Day']:
    #         date_text += '-{}'.format(str(int(metadata['Day'])).zfill(2))
    #     return date_text


    def populateTeiHeader(self, root, metadata, filename):
        self.populateFileDesc(root, metadata, filename)
        self.populateProfileDesc(root, metadata, filename)

    def populateFileDesc(self, root, metadata, filename):
        title = root.find('teiHeader/fileDesc/titleStmt/title')
        title.text = metadata['Place']


        recordID = root.find('teiHeader/fileDesc/titleStmt/recordID')
        recordID.text = '{}'.format(str(int(metadata['RecordID'])).zfill(4))



    def populateProfileDesc(self, root, metadata, filename):

        # "Year" field is text-based: e.g. "1210x1215", "1300 (ca.)"
        # "Year_Sort" field is always a 4-digit number and used for sorting.
        origDate = root.find('teiHeader/profileDesc/creation/origDate')
        origDate.text = metadata['Year']

        if metadata['Circa'] == 'Yes':
            origDate.set('precision', 'circa')

        year = root.find('teiHeader/profileDesc/creation/year')
        year.text = metadata['Year_Sort']

        origPlace = root.find('teiHeader/profileDesc/creation/origPlace')
        origPlace.text = metadata['Place']

        diocese = root.find('teiHeader/profileDesc/creation/diocese')
        diocese.text = metadata['Diocese']

        diocese_id = root.find('teiHeader/profileDesc/creation/diocese_id')
        diocese_id.text = metadata['Jurisdiction_ID']

        province = root.find('teiHeader/profileDesc/creation/province')
        province.text = metadata['Province']

        country = root.find('teiHeader/profileDesc/creation/country')
        country.text = metadata['CountryModern']

        allPlaceValues = set()
        allPlaceValues.add(metadata['Place'])
        allPlaceValues.add(metadata['Diocese'])
        allPlaceValues.add(metadata['Province'])
        allPlaceValues.add(metadata['CountryModern'])
        allPlaceValues = [x for x in allPlaceValues if x is not None]
        _allPlace = root.find('teiHeader/profileDesc/creation/_allPlace')
        _allPlace.text = ' '.join(allPlaceValues)

        classification = root.find('teiHeader/profileDesc/textDesc/domain')
        classification.text = metadata['Classification']

        langUsage = root.find('teiHeader/profileDesc/langUsage')
        langUsage.text = metadata['Language']

        # Issuing Authority
        persName = root.find('teiHeader/profileDesc/creation/persName')
        persName.text = metadata['IssuingAuthority']

        altName = root.find('teiHeader/profileDesc/creation/altName')
        altName.text = metadata['IssuingAuthorityAlt']

        _issuingAuthority = root.find('teiHeader/profileDesc/creation/_issuingAuthority')
        issuingAuthValues = []
        issuingAuthValues.append(metadata['IssuingAuthority'])
        issuingAuthValues.append(metadata['IssuingAuthorityAlt'])
        issuingAuthValues = [x for x in issuingAuthValues if x is not None]
        _issuingAuthority.text = ', '.join(issuingAuthValues)

        # Source and Edition
        source = root.find('teiHeader/fileDesc/sourceDesc/msDesc/source')
        source.text = metadata['Source']
        sourceOther = root.find('teiHeader/fileDesc/sourceDesc/msDesc/sourceOther')
        sourceOther.text = metadata['SourceOther']
        _source = root.find('teiHeader/fileDesc/sourceDesc/msDesc/_source')
        _source.text = '; '.join([x for x in [metadata['Source'], metadata['SourceOther']] if x is not None])

        edition = root.find('teiHeader/fileDesc/sourceDesc/bibl/edition')
        edition.text = metadata['Edition']
        editionOther = root.find('teiHeader/fileDesc/sourceDesc/bibl/editionOther')
        editionOther.text = metadata['EditionOther']
        _edition = root.find('teiHeader/fileDesc/sourceDesc/bibl/_edition')
        _edition.text = '; '.join([x for x in [metadata['Edition'], metadata['EditionOther']] if x is not None])


    def populateText(self, root, text, footnotes, metadata, filename):
        body = root.find('text/body')
        meta = ET.SubElement(body, 'div')
        head = ET.SubElement(meta, 'head')
        metadata_body = ET.SubElement(meta, 'metadata')
        head.text = 'Metadata'

        # Metadata
        for key in self.column_names:
            # Exclude igored metadata fields and those with empty values
            if (key not in self.ignored_metadata_fields) and metadata[key]:
                p = ET.SubElement(metadata_body, 'p')
                p.text = '{}: {}'.format(key, metadata[key])

        # Text
        section_names = text['section_names']
        all_text = ET.SubElement(body, 'div')
        head = ET.SubElement(all_text, 'head')
        head.text = 'Text'

        for section in section_names:
            div = ET.SubElement(all_text, 'div')
            head = ET.SubElement(div, 'head')
            head.text = section

            for line in text[section]:
                p = ET.SubElement(div, 'p')
                p.text = line

        # FootNotes
        div = ET.SubElement(all_text, 'div')
        head = ET.SubElement(div, 'head')
        head.text = 'Footnotes'

        for line in footnotes:
            p = ET.SubElement(div, 'p')
            p.text = line
