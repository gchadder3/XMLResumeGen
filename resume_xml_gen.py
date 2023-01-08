"""
resume_xml_parse.py -- resume parser

Last updated: 10/8/22 (gchadder3)
"""

import argparse
import os
import xml.etree.ElementTree as ET
import re

def fieldSanitize(str):
    # Replace ampersand escapes with the real-deal (&), and then 
    # strip out left and right whitespace.
    return re.sub(r'&amp;', r'&', str).lstrip().rstrip()

htmlStartText_1 = """<html>

<body>
"""

htmlEndText_1 = """
</body>

</html>
"""

if __name__ == '__main__':
    # Parse the arguments from the command line.
    parser = argparse.ArgumentParser(
        description='Parse an XML resume file and format and output a resume from it.')
    parser.add_argument('infile', nargs='?',
        default='resume_xml.xml', 
        help='XML file containing the resume information (default="resume_xml.xml")')
    parser.add_argument('-f', '--format', 
        choices=['plaintext_1', 'ats_1', 'html_1'], 
        default='plaintext_1',     
        help='resume output format (default="plaintext_1")')
    args = parser.parse_args()   
    inFileName = 'resume_xml.xml'  # set the default in XML file
    if args.infile is not None:
        inFileName = args.infile
    outFormat = 'plaintext_1'      # set the format ('plaintext_1', 'ats_1', 'html_1')
    if args.format is not None:
        outFormat = args.format

    # Command args debugging...
    # print(args)
    # exit()

    # Give an error if the file we're trying to load is missing.
    if not os.path.exists(inFileName):
        print("ERROR: File '%s' is not found." % inFileName)
        exit()
        
    # Set some formatting parameters.
    plaintext_1_tabIndent = False
    
    # Extract the tree from the file.
    tree = ET.parse(inFileName)
    # tree = ET.parse('Resume MindMap_scratch.mm')
    
    # Get the root element from the tree.
    root = tree.getroot()

    # If HTML, create initial boiler-plate...
    if outFormat == 'html_1':
        print(htmlStartText_1)
       
    # Heading section...
    hinfo = root.find('./heading-info')
    if hinfo == None:
        raise LookupError('No <heading-info> tag found in file.')
    if outFormat == 'html_1':
        print('<div id="heading-info">')
    # For each child element...
    for hitem in hinfo:
        theField = fieldSanitize(hitem.text)
        if hitem.tag == 'name':
            if outFormat == 'plaintext_1':
                print(theField)
            elif outFormat == 'ats_1':
                print('NAME: %s' % theField)
            elif outFormat == 'html_1':
                html_temp = """<p align=center style='text-align:center; margin:0px'><b>%s</b></p>"""
                print(html_temp % theField)                
        elif hitem.tag == 'phone-number':
            if outFormat == 'plaintext_1':
                print(theField)
            elif outFormat == 'ats_1':
                print('PHONE: %s' % theField)
            elif outFormat == 'html_1':
                html_temp = """<p align=center style='text-align:center; margin:0px'>%s</p>"""
                print(html_temp % theField)
        elif hitem.tag == 'email':
            if outFormat == 'plaintext_1':
                print(theField)
            elif outFormat == 'ats_1':
                print('EMAIL: %s' % theField)
            elif outFormat == 'html_1':
                html_temp = """<p align=center style='text-align:center; margin:0px'>%s</p>"""
                print(html_temp % theField)
        elif hitem.tag == 'location':
            if outFormat == 'plaintext_1':
                print(theField)
            elif outFormat == 'ats_1':
                print('LOCATION: %s' % theField)
            elif outFormat == 'html_1':
                html_temp = """<p align=center style='text-align:center; margin:0px'>%s</p>"""
                print(html_temp % theField)
        elif hitem.tag == 'linkedin-url':
            if outFormat == 'plaintext_1':
                print(theField)
            elif outFormat == 'ats_1':
                print('LINKEDIN: %s' % theField)
            elif outFormat == 'html_1':
                html_temp = """<p align=center style='text-align:center; margin:0px'>%s</p>"""
                print(html_temp % theField)
        elif hitem.tag == 'github-url':
            if outFormat == 'plaintext_1':
                print(theField)
            elif outFormat == 'ats_1':
                print('GITHUB: %s' % theField)
            elif outFormat == 'html_1':
                html_temp = """<p align=center style='text-align:center; margin:0px'>%s</p>"""
                print(html_temp % theField)
    if outFormat == 'html_1':
        print('</div>')
    
    # Objective section...
    obj = root.find('./objective')
    if obj is not None and not('hide' in obj.attrib and obj.attrib['hide'].lower() == 'true'):
#        objchoice = obj.find('data-science-option')
#        objchoice = obj.find('general-option')
        objchoice = obj.find('current-job-option')
        headingStr = obj.attrib['sectionname'].upper()
        theField = fieldSanitize(objchoice.text)
        print('')
        if outFormat == 'plaintext_1':
            print('%s: %s' % (headingStr, theField))
        elif outFormat == 'ats_1':
            print('%s: %s' % (headingStr, theField))
        elif outFormat == 'html_1':
            print('<div id="objective">')
            print('<p><u>%s</u>: %s</p>' % (headingStr, theField))
            print('</div>') 
            
    # Summary section...
    summary = root.find('./summary')
    if summary is not None and not('hide' in summary.attrib and summary.attrib['hide'].lower() == 'true'):
        headingStr = summary.attrib['sectionname'].upper()
        print('')
        if outFormat == 'plaintext_1':
            print('%s:' % headingStr)
        elif outFormat == 'ats_1':
            print('%s:' % headingStr)            
        elif outFormat == 'html_1':
            print('<div id="summary">')
            print('<p style="margin-bottom:0px"><u>%s</u>:</p>' % headingStr)  
            print('<p style="margin:0px">', end='')            
        firstsumitem = True
        for sumitem in summary.iter('summary-item'):
            if not firstsumitem:
                print(' ', end='')
            print(fieldSanitize(sumitem.text), end='')
            firstsumitem = False
        if outFormat == 'plaintext_1':
            print('')
        elif outFormat == 'ats_1':
            print('')            
        elif outFormat == 'html_1':
            print('</p>')        
            print('</div>') 
            
    # Qualifications / Technical Skills section...
    qualskills = root.find('./qualifications-skills')
    if qualskills is not None and not('hide' in qualskills.attrib and qualskills.attrib['hide'].lower() == 'true'):
        headingStr = qualskills.attrib['sectionname'].upper()
        print('')
        if outFormat == 'plaintext_1':
            print('%s:' % headingStr)
        elif outFormat == 'ats_1':
            print('TECHNICAL SKILLS:')            
        elif outFormat == 'html_1':
            print('<div id="qualifications-skills">')
            print('<p style="margin-bottom:0px"><u>%s</u>:</p>' % headingStr)
            print('<ul style="margin-top:0px">')
        # For each child element...
        for qelem in qualskills:
            if qelem.tag == 'qual-skill-item':
                qelemText = fieldSanitize(qelem.text)
                if outFormat == 'plaintext_1':
                    if plaintext_1_tabIndent:
                        print('\t', end='')
                    print('* %s' % qelemText, end='')
                elif outFormat == 'ats_1': 
                    print('* %s' % qelemText, end='')
                elif outFormat == 'html_1':
                    print('<li style="margin-top:0px">%s' % qelemText, end='')           
            elif qelem.tag == 'qual-skill-list': 
                className = fieldSanitize(qelem.find('qual-skill-class').text)
                if outFormat == 'plaintext_1':
                    if plaintext_1_tabIndent:
                        print('\t', end='')                
                    print('* %s: ' % className, end='')
                elif outFormat == 'ats_1': 
                    print('* %s: ' % className, end='')
                elif outFormat == 'html_1':
                    print('<li style="margin-top:0px">%s: ' % className, end='')            
                firstqitem = True
                for qitem in qelem.iter('qual-skill-item'):
                    if not firstqitem:
                        print(', ', end='')
                    print(fieldSanitize(qitem.text), end='')
                    firstqitem = False
            if outFormat == 'plaintext_1':
                print('')
            elif outFormat == 'ats_1':
                print('')                
            elif outFormat == 'html_1':
                print('</li>')                
        if outFormat == 'html_1':
            print('</ul>')        
            print('</div>')      

    # Work experience section...
    wexper = root.find('./work-experience')
    if wexper == None:
        raise LookupError('No <work-experience> tag found in file.')
    if wexper is not None and not('hide' in wexper.attrib and wexper.attrib['hide'].lower() == 'true'):        
        headingStr = wexper.attrib['sectionname'].upper()    
        print('')
        if outFormat == 'plaintext_1':
            print('%s:' % headingStr)
        elif outFormat == 'ats_1':
            print('%s:' % headingStr)            
        elif outFormat == 'html_1':
            print('<div id="work-experience">')
            print('<p style="margin:0px"><u>%s</u>:</p>' % headingStr)
        firstexpitem = True
        # For each experience-item...        
        for expitem in wexper.iter('experience-item'):  
            start_date = fieldSanitize(expitem.find('start-date').text)
            end_date = fieldSanitize(expitem.find('end-date').text)
            job_title = fieldSanitize(expitem.find('job-title').text)
            org = fieldSanitize(expitem.find('organization').text)
            loc = fieldSanitize(expitem.find('location').text)
            desc = expitem.find('description')
            if desc is not None:
                desc = fieldSanitize(desc.text)
            if not firstexpitem:
                print('')
            if outFormat == 'plaintext_1':
                print('%s-%s' % (start_date, end_date), end='')
                print('\t', end='')
                print(job_title, end='')
                print(', ', end='')
                print(org, end='')
                print(', ', end='')
                print(loc)
                for ritem in expitem.iter('role-item'):
                    if plaintext_1_tabIndent:
                        print('\t', end='')
                    print('* ', end='')
                    print(fieldSanitize(ritem.text))
                if desc is not None:
                    print(desc)
            elif outFormat == 'ats_1':
                print('COMPANY: %s' % org)
                print('LOCATION: %s' % loc)
                print('JOB TITLE: %s' % job_title)
                print('START DATE: %s' % start_date)
                print('END DATE: %s' % end_date)
                print('DESCRIPTION:')
                for ritem in expitem.iter('role-item'):
                    print('* ', end='')
                    print(fieldSanitize(ritem.text))   
            elif outFormat == 'html_1':
                print('<div class="experience-item">')
                print('<p style="margin:0px">%s-%s <b>%s, %s, %s</b></p>' % (start_date, end_date, job_title, org, loc))
                print('<ul style="margin-top:0px">')
                for ritem in expitem.iter('role-item'):
                    theField = fieldSanitize(ritem.text)
                    print('<li style="margin-top:0px">%s</li>' % theField)
                print('</ul>')
                if desc is not None:
                    print('<p style="margin-top:0px">%s</p>' % desc)            
                print('</div>')
            firstexpitem = False            
        if outFormat == 'html_1':
            print('</div>')

    # Education section...
    edu = root.find('./education')
    if edu is not None and not('hide' in edu.attrib and edu.attrib['hide'].lower() == 'true'):
        headingStr = edu.attrib['sectionname'].upper()
        print('')    
        if outFormat == 'plaintext_1':
            print('%s:' % headingStr)
        elif outFormat == 'ats_1':
            print('%s:' % headingStr)           
        elif outFormat == 'html_1':
            print('<div id="education">')
            print('<p style="margin:0px"><u>%s</u>:</p>' % headingStr)
        firsteduitem = True            
        # For each education-item...
        for editem in edu.iter('education-item'):
            inst = editem.find('institution')
            if inst == None:
                raise LookupError('No <institution> tag found in <education-item>.')
            inst = fieldSanitize(inst.text)
            
            deg = editem.find('degree')
            if deg is not None:
                deg = fieldSanitize(deg.text)
                
            maj = editem.find('major')
            if maj is not None:
                maj = fieldSanitize(maj.text)
                
            grad_year = editem.find('completion-year')
            if grad_year is not None:
                grad_year = fieldSanitize(grad_year.text)
                
            if outFormat == 'plaintext_1':
                print(inst, end='')
                if deg is not None:
                    print(', ', end='')
                    print(deg, end='')
                    if maj is not None:
                        print(' in ', end='')
                        print(maj, end='')
                if grad_year is not None:
                    print(', ', end='')
                    print(grad_year, end='')
                print('')
                for mitem in editem.iter('more-info'):
                    if plaintext_1_tabIndent:
                        print('\t', end='')
                    print('* ', end='')
                    print(fieldSanitize(mitem.text), end='')
                    print('')
            elif outFormat == 'ats_1':
                if not firsteduitem:
                    print('')            
                if deg is not None:
                    print('DEGREE: ', end='')
                    print(deg, end='')
                    if maj is not None:
                        print(' in ', end='')
                        print(maj, end='')
                    print('')
                print('SCHOOL: %s' % inst)            
                if grad_year is not None:
                    print('GRADUATION YEAR: %s' % grad_year)
            elif outFormat == 'html_1':
                print('<p style="margin:0px">%s' % inst, end='')
                if deg is not None:
                    print(', ', end='')
                    print(deg, end='')
                    if maj is not None:
                        print(' in ', end='')
                        print(maj, end='')
                if grad_year is not None:
                    print(', ', end='')
                    print(grad_year, end='')                 
                print('</p>')
                numMores = sum(1 for _ in editem.iter('more-info'))
                if numMores > 0:
                    print('<ul style="margin:0px">')
                    for mitem in editem.iter('more-info'):
                        theField = fieldSanitize(mitem.text)
                        print('<li style="margin:0px">%s</li>' % theField)
                    print('</ul>')
            firsteduitem = False                    
        if outFormat == 'html_1':
            print('</div>')
            
    # Special coursework section...
    speccoursework = root.find('./special-coursework')
    if speccoursework is not None and not('hide' in speccoursework.attrib and speccoursework.attrib['hide'].lower() == 'true'):
        headingStr = speccoursework.attrib['sectionname'].upper()
        print('')
        if outFormat == 'plaintext_1':
            print('%s:' % headingStr)
        elif outFormat == 'ats_1':
            print('%s:' % headingStr)           
        elif outFormat == 'html_1':
            print('<div id="special-coursework">')
            print('<p style="margin-bottom:0px"><u>%s</u>:</p>' % headingStr)  
            print('<p style="margin:0px">', end='')            
        firstcwitem = True
        for cwitem in speccoursework.iter('coursework-item'):
            if not firstcwitem:
                print(', ', end='')
            print(fieldSanitize(cwitem.text), end='')
            firstcwitem = False
        if outFormat == 'plaintext_1':
            print('')
        elif outFormat == 'ats_1':
            print('')            
        elif outFormat == 'html_1':
            print('</p>')        
            print('</div>') 
                     
    # Cerfications section...
    certifs = root.find('./certifications')
    if certifs is not None and not('hide' in certifs.attrib and certifs.attrib['hide'].lower() == 'true'):
        headingStr = certifs.attrib['sectionname'].upper()
        print('')
        if outFormat == 'plaintext_1':
            print('%s (see LinkedIn page for validations):' % headingStr)
        elif outFormat == 'ats_1':
            print('%s:' % headingStr)           
        elif outFormat == 'html_1':
            print('<div id="certifications">')
            print('<p style="margin-bottom:0px"><u>%s</u> (see LinkedIn page for validations):</p>' % headingStr)           
            print('<p style="margin:0px">', end='')            
        firstcitem = True
        for citem in certifs.iter('certification-item'):
            if not firstcitem:
                print(', ', end='')
            print(fieldSanitize(citem.text), end='')
            firstcitem = False
        if outFormat == 'plaintext_1':
            print('')
        elif outFormat == 'ats_1':
            print('')            
        elif outFormat == 'html_1':
            print('</p>')        
            print('</div>') 
            
    # Additional info section...
    addinfo = root.find('./additional-info')
    if addinfo is not None and not('hide' in addinfo.attrib and addinfo.attrib['hide'].lower() == 'true'):
        headingStr = addinfo.attrib['sectionname'].upper()
        theField = fieldSanitize(addinfo.text)
        print('')
        if outFormat == 'plaintext_1':
            print('%s: %s' % (headingStr, theField))
        elif outFormat == 'ats_1':
            print('%s: %s' % (headingStr, theField))            
        elif outFormat == 'html_1':
            print('<div id="additional-info">')
            print('<p><u>%s</u>: %s</p>' % (headingStr, theField))
            print('</div>')           
                
    # If HTML, create end boiler-plate...
    if outFormat == 'html_1':
        print(htmlEndText_1)       