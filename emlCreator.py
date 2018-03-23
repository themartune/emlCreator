# Python version of Perl EML Generator

# Read in list of addresses

# Content
    # Read in a book
    
# Mail
    # Randomly choose a sender from addresses
    # randomly pick a number of recipients from addresses
    # randomly choose a range of lines from our content
    # create eml files with a timestamp as part of the filename
    
import secrets
import time
import uuid
from time import strftime, gmtime

# import collections as coll
# import traceback
# import logging

# there is no "use strict" equivalent in Python! Ahhhhh!

# create mtUtils.py at some point

params = {
    'addressFile':        './devAddressExport.txt',
    'contentFile':        './MobyDick.txt',
    'emlCreationCount':   5,
    'maxRecipientCount':  3,
    'maxContentLines':    30
    }

  
def trim(myString):
    '''
    Trim Whitespace from each end of a given string
    ZuTun: 
        Add to mtUtils.py
        Is there a need for other optional characters?
    '''
    myString = myString.lstrip()
    myString = myString.rstrip()
    return myString


def readDataFile(dataFileName):
    '''Read in a file into an array and return the array'''
    data = []
    
    print(dataFileName)
    
    # add errorhandling
    try:
        fh = open(dataFileName, "r")
    except Exception as e: # catch any errors
        print('Could not open File ' + dataFileName, e)
        exit(1)

    for line in fh:
        if line.isspace() or '#' in line:
            continue
        line = trim(line)
        # print('.' + line + '.')
        data.append(line)
    fh.close()
    return data


def generateEmlFiles(addresses, content):
    '''Create EML files from the addresses and content'''
    
    # Check that addresses and content have data
    if not addresses:
        print("ERROR\tAddress list is empty")
        exit(1)
    elif not content:
        print("ERROR\tContent is empty")
        exit(1)
    
    emlCount = 0
    while emlCount < params['emlCreationCount']:
        # create sender
        sender = secrets.choice(addresses)
        
        #create recipients
        recipients = []
        recipientCount = secrets.randbelow(params['maxRecipientCount'] + 1)
        
        # guarantee at least one recipient
        if recipientCount == 0:
            recipientCount = 1

        for i in range(0, recipientCount):
            recipients.append(secrets.choice(addresses))
                
        # Get Time for email
        emlTime = int(time.time()*1000)
        emlFile = 'emlTest-' + str(emlTime) + '.eml'
        
        # create Message-ID
        messageId = str(uuid.uuid4()) + '@' + sender.split('@')[1]
        
        # generate content
        emlContent = []
        
        #add eml headers to emlContent
        emlContent.append( 'X-Sender: ' + sender )
        emlContent.append( 'From: ' + sender )
        emlContent.append( 'Mime-Version: 1.0' )
        emlContent.append( 'To: ' + ', '.join(recipients) )
        emlContent.append( 'Date: ' + strftime("%a, %d %b %Y %H:%M:%S +0000 (UTC)", gmtime()))
        emlContent.append( 'Message-ID: ' + messageId )
        emlContent.append( 'Subject: EML Test ' + str(emlTime) )
        emlContent.append( 'Content-Type: text/plain;' ) # charset=UTF-8'
        emlContent.append( 'Content-Transfer-Encoding: quoted-printable' )
        emlContent.append( '' ) # this is the separator between header and content
        
        # determine the number of lines of content
        contentLineCount = secrets.randbelow(params['maxContentLines'] + 1)
        
        # choose the starting point in our content and create content
        startContentLine = secrets.randbelow(len(content) - contentLineCount)
        for i in range(startContentLine, startContentLine + contentLineCount):
            emlContent.append(content[i])

        # create emlFile
        try:
            fh = open(emlFile, "w")
        except Exception as e: # catch any errors
            print('Could not open File ' + emlFile, e)
            exit(1)
        
        for line in emlContent:
            fh.write(line + '\n')
        
        fh.close()
        
        emlCount+=1

# Read addresses into an array
addresses = readDataFile(params['addressFile'])

# Read Content into an array
content = readDataFile(params['contentFile'])

# generate eml files
generateEmlFiles(addresses, content)


