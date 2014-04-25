import csv, re, cStringIO, codecs

#from pattern.web import abs, URL, DOM, plaintext, strip_between
#from pattern.web import NODE, TEXT, COMMENT, ELEMENT, DOCUMENT

from pattern.web import Wikipedia

#unicode writer
class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

# Creating the csv output file for writing into as well as defining the writer
output = open("congress-data.csv", "wb")
writer = UnicodeWriter(output)

# add header row
writer.writerow(["Name", "Congress", "House/Senate", "State", "Party", "Military", "Military Branch"])

# create Wikipedia search engine
engine = Wikipedia(license=None, throttle=5.0, language=None)

# for each year (82nd to 113th Congress)
for i in range(82, 113):
    # change from number to ordinal (12 to 12th)
    k = i%10
    print "%d%s United States Congress"%(i,"tsnrhtdd"[(i/10%10!=1)*(k<4)*k::4])
    
    congress_article = Wikipedia().search("%d%s United States Congress"%(i,"tsnrhtdd"[(i/10%10!=1)*(k<4)*k::4]))

    state_section = False
    
    for section in congress_article.sections:
        # Alabama to Wyoming
        if "Alabama" in section.title:
            state_section = True
        
        if state_section:
            print section.source
            #put in dom parser, loop through <li>, grab title element in <a> within <li>
            #congressman_article on title
            
            #for link in section.links:
            #    congressman_article = Wikipedia().search(link)
            #    print article.title
        
        if "Wyoming" in section.title:
            state_section = False
            break
        
    # for each Congressman

##    congressman_article = Wikipedia().search('John McCain')
##
##    # grab state, party, military info, somewhere in a table
##    for table in congressman_article.tables:
##        if "Military" in table.title:
##            #write military row
##            print "military"
##        if "Personal" in table.title:
##            #write party
##            print "Republican"
        


