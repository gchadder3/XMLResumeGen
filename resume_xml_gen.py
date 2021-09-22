"""
resume_xml_parse.py -- resume parser

Last updated: 9/22/21 (gchadder3)
"""

import argparse
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

htmlStartText_2 = """<html>

<head>
<meta http-equiv=Content-Type content="text/html; charset=windows-1252">
<meta name=Generator content="Microsoft Word 15 (filtered)">
<style>
<!--
 /* Font Definitions */
 @font-face
	{font-family:"Cambria Math";
	panose-1:2 4 5 3 5 4 6 3 2 4;}
@font-face
	{font-family:Consolas;
	panose-1:2 11 6 9 2 2 4 3 2 4;}
 /* Style Definitions */
 p.MsoPlainText, li.MsoPlainText, div.MsoPlainText
	{mso-style-link:"Plain Text Char";
	margin:0in;
	font-size:10.5pt;
	font-family:Consolas;}
span.PlainTextChar
	{mso-style-name:"Plain Text Char";
	mso-style-link:"Plain Text";
	font-family:Consolas;}
.MsoChpDefault
	{font-family:"Calibri",sans-serif;}
.MsoPapDefault
	{margin-bottom:8.0pt;
	line-height:107%;}
@page WordSection1
	{size:8.5in 11.0in;
	margin:1.0in 75.1pt 1.0in 75.05pt;}
div.WordSection1
	{page:WordSection1;}
-->
</style>

</head>

<body lang=EN-US style='word-wrap:break-word'>

<div class=WordSection1>
"""

htmlEndText_2 = """
</div>

</body>

</html>
"""

if __name__ == '__main__':
    # Parse the arguments from the command line.
    parser = argparse.ArgumentParser(description='Parse an XML resume file and format and output a resume from it.')
    parser.add_argument('-i', '--infile')
    parser.add_argument('-f', '--format')
    args = parser.parse_args()   
    inFileName = 'resume_xml.xml'  # set the default in XML file
    if args.infile is not None:
        inFileName = args.infile
    outFormat = 'plaintext_1'      # set the format ('plaintext_1', 'html_1', 'html_2')
    if args.format is not None:
        outFormat = args.format
    
    # Extract the tree from the file.
    tree = ET.parse(inFileName)
    # tree = ET.parse('Resume MindMap_scratch.mm')
    
    # Get the root element from the tree.
    root = tree.getroot()

    # If HTML, create initial boiler-plate...
    if outFormat == 'html_1':
        print(htmlStartText_1)
    elif outFormat == 'html_2':
        print(htmlStartText_2)
       
    # Heading section...
    hinfo = root.find('./heading-info')
    if hinfo == None:
        raise LookupError('No <heading-info> tag found in file.')
    if outFormat == 'html_1':
        print('<div id="heading-info">')
    for hitem in hinfo:
        if outFormat == 'html_1':
            if hitem.tag == 'name':
                html_temp = """<p align=center style='text-align:center; margin:0px'><b>%s</b></p>"""
            else:
                html_temp = """<p align=center style='text-align:center; margin:0px'>%s</p>"""     
        elif outFormat == 'html_2':
            if hitem.tag == 'name':
                html_temp = """<p class=MsoPlainText align=center style='text-align:center'><b><span style='font-size:12.0pt;font-family:"Times New Roman",serif'>%s</span></b></p>"""
            else:
                html_temp = """<p class=MsoPlainText align=center style='text-align:center'><span style='font-size:12.0pt;font-family:"Times New Roman",serif'>%s</span></p>"""
        theField = fieldSanitize(hitem.text)
        if outFormat == 'plaintext_1':
            print(theField)
        elif outFormat == 'html_1':
            print(html_temp % theField)
    if outFormat == 'html_1':
        print('</div>')
    
    # Objective section...
    obj = root.find('./objective')
    if obj is not None:
#        objchoice = obj.find('data-science-option')
        objchoice = obj.find('general-option')
        theField = fieldSanitize(objchoice.text)
        print('')
        if outFormat == 'plaintext_1':
            print('OBJECTIVE: %s' % theField)
        elif outFormat == 'html_1':
            print('<div id="objective">')
            print('<p><u>OBJECTIVE</u>: %s</p>' % theField)
            print('</div>') 
            
    # Summary section...
    summary = root.find('./summary')
    if summary is not None:
        print('')
        if outFormat == 'plaintext_1':
            print('SUMMARY:')
        elif outFormat == 'html_1':
            print('<div id="summary">')
            print('<p style="margin-bottom:0px"><u>SUMMARY</u>:</p>')  
            print('<p style="margin:0px">', end='')            
        firstsumitem = True
        for sumitem in summary.iter('summary-item'):
            if not firstsumitem:
                print(' ', end='')
            print(fieldSanitize(sumitem.text), end='')
            firstsumitem = False
        if outFormat == 'plaintext_1':
            print('')
        if outFormat == 'html_1':
            print('</p>')        
            print('</div>') 
            
    # Qualifications / Technical Skills section...
    qualskills = root.find('./qualifications-skills')
    if qualskills is not None:
        print('')
        if outFormat == 'plaintext_1':
            print('QUALIFICATIONS / TECHNICAL SKILLS:')
        elif outFormat == 'html_1':
            print('<div id="qualifications-skills">')
            print('<p style="margin-bottom:0px"><u>QUALIFICATIONS / TECHNICAL SKILLS</u>:</p>')
            print('<ul style="margin-top:0px">')
        # For each child element...
        for qelem in qualskills:
            if qelem.tag == 'qual-skill-item':
                qelemText = fieldSanitize(qelem.text)
                if outFormat == 'plaintext_1':
                    print('\t* %s' % qelemText, end='')
                elif outFormat == 'html_1':
                    print('<li style="margin-top:0px">%s' % qelemText, end='')           
            elif qelem.tag == 'qual-skill-list': 
                className = fieldSanitize(qelem.find('qual-skill-class').text)
                if outFormat == 'plaintext_1':
                    print('\t* %s: ' % className, end='')
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
            elif outFormat == 'html_1':
                print('</li>')                
        if outFormat == 'html_1':
            print('</ul>')        
            print('</div>')      

    # Work experience section...
    wexper = root.find('./work-experience')
    if wexper == None:
        raise LookupError('No <work-experience> tag found in file.')
    print('')
    if outFormat == 'plaintext_1':
#        print('EXPERIENCE:')
        print('RECENT EXPERIENCE:')
    elif outFormat == 'html_1':
        print('<div id="work-experience">')
#        print('<p style="margin:0px"><u>EXPERIENCE</u>:</p>')
        print('<p style="margin:0px"><u>RECENT EXPERIENCE</u>:</p>')
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
                print('\t* ', end='')
                print(fieldSanitize(ritem.text))
            if desc is not None:
                print(desc)
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
    if edu is not None:
        print('')    
        if outFormat == 'plaintext_1':
            print('EDUCATION:')
        elif outFormat == 'html_1':
            print('<div id="education">')
            print('<p style="margin:0px"><u>EDUCATION</u>:</p>')    
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
                    print('\t* ', end='')
                    print(fieldSanitize(mitem.text), end='')
                    print('')
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
        if outFormat == 'html_1':
            print('</div>')
            
    # Special coursework section...
    speccoursework = root.find('./special-coursework')
    if speccoursework is not None:
        print('')
        if outFormat == 'plaintext_1':
            print('SPECIALIZED COURSEWORK:')
        elif outFormat == 'html_1':
            print('<div id="special-coursework">')
            print('<p style="margin-bottom:0px"><u>SPECIALIZED COURSEWORK</u>:</p>')  
            print('<p style="margin:0px">', end='')            
        firstcwitem = True
        for cwitem in speccoursework.iter('coursework-item'):
            if not firstcwitem:
                print(', ', end='')
            print(fieldSanitize(cwitem.text), end='')
            firstcwitem = False
        if outFormat == 'plaintext_1':
            print('')
        elif outFormat == 'html_1':
            print('</p>')        
            print('</div>') 
                     
    # Cerfications section...
    certifs = root.find('./certifications')
    if certifs is not None:
        print('')
        if outFormat == 'plaintext_1':
            print('CERTIFICATIONS (see LinkedIn page for validations):')
        elif outFormat == 'html_1':
            print('<div id="certifications">')
            print('<p style="margin-bottom:0px"><u>CERTIFICATIONS</u> (see LinkedIn page for validations):</p>')  
            print('<p style="margin:0px">', end='')            
        firstcitem = True
        for citem in certifs.iter('certification-item'):
            if not firstcitem:
                print(', ', end='')
            print(fieldSanitize(citem.text), end='')
            firstcitem = False
        if outFormat == 'plaintext_1':
            print('')            
        elif outFormat == 'html_1':
            print('</p>')        
            print('</div>') 
            
    # Additional info section...
    addinfo = root.find('./additional-info')
    if addinfo is not None:
        theField = fieldSanitize(addinfo.text)
        print('')
        if outFormat == 'plaintext_1':
            print('ADDITIONAL INFORMATION: %s' % theField)
        elif outFormat == 'html_1':
            print('<div id="additional-info">')
            print('<p><u>ADDITIONAL INFORMATION</u>: %s</p>' % theField)
            print('</div>')           
                
    # If HTML, create end boiler-plate...
    if outFormat == 'html_1':
        print(htmlEndText_1)
    elif outFormat == 'html_2':
        print(htmlEndText_2)        