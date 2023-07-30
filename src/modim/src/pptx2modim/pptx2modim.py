# Extract information from pptx file and generates data in MODIM format

import argparse
import zipfile
import os
import time



class PPTX2MODIM:

    def __init__(self, pptxfile, modimdemodir):
        self.pptxfile = pptxfile
        self.modimdemodir = modimdemodir
        self.zip = None
        self.tmpdir = '.ppt/'

    def createdirs(self):
        if (not os.path.exists(self.modimdemodir)):
            os.makedirs(self.modimdemodir)
            os.makedirs(self.modimdemodir+'/img')
            os.makedirs(self.modimdemodir+'/actions')
            os.makedirs(self.modimdemodir+'/scripts')
        if (not os.path.exists(self.tmpdir)):
            os.makedirs(self.tmpdir)

    def getactioninfo(self,name):

        os.chdir(self.tmpdir)
        os.system('rm -rf ppt')
        time.sleep(0.1)

        id = int(name[5:]) # id of the slide

        self.zip.extract('ppt/slides/slide%d.xml' %id)
        self.zip.extract('ppt/slides/_rels/slide%d.xml.rels' %id)
        self.zip.extract('ppt/notesSlides/notesSlide%d.xml' %id)

        # extract text
        text = ''

        # first look for title in the notes
        fn = open('ppt/notesSlides/notesSlide%d.xml' %id) 
        for l in fn.readlines():
            p1 = l.find('TITLE')
            if (p1>=0):
                p2 = l[p1:].find('<')
                text = l[p1+5:p1+p2]
        fn.close()

        if text=='': # if not found extract text from slide
            fn = open('ppt/slides/slide%d.xml' %id) 
            for l in fn.readlines():
                p1 = l.find('<a:t>')
                p2 = l[p1:].find('</a:t>')
                text = l[p1+5:p1+p2]
            fn.close()


        # extract image
        image = ''

        # first look for title in the notes
        fn = open('ppt/notesSlides/notesSlide%d.xml' %id) 
        for l in fn.readlines():
            p1 = l.find('IMAGE')
            if (p1>=0):
                p2 = l[p1:].find('<')
                image = 'img/'+l[p1+5:p1+p2].strip()
        fn.close()

        if image=='':
            fn = open('ppt/slides/_rels/slide%d.xml.rels' %id) 
            for l in fn.readlines():
                p1 = l.find('image')
                if (p1>=0):
                    p2 = l[p1:].find('media')
                    p3 = l[p1+p2:].find('"')                
                    image = 'img/'+l[p1+p2+6:p1+p2+p3]
            fn.close()


        # extract TTS

        tts = ''

        fn = open('ppt/notesSlides/notesSlide%d.xml' %id) 
        for l in fn.readlines():
            p1 = l.find('TTS')
            if (p1>=0):
                p2 = l[p1:].find('<')
                tts = l[p1+4:p1+p2]
        fn.close()


        # extract buttons
        buttons = [] # example: [['yes','Yes'],['no','No']]
        btstr = ''
        fn = open('ppt/notesSlides/notesSlide%d.xml' %id) 
        for l in fn.readlines():
            p1 = l.find('BUTTONS')
            if (p1>=0):
                p2 = l[p1:].find('<')
                btstr = l[p1+8:p1+p2].strip()
        fn.close()
        if btstr!='':
            print btstr
            v1 = btstr.split(',')
            #print v1
            for b in v1:
                b = b.strip()
                p = b.find(' ')
                if p>0:
                    buttons.append([b[0:p].strip(),b[p:].strip()])


        print '\tTEXT_title %s' %text
        print '\tIMAGE %s' %image
        print '\tTTS %s' %tts
        print '\tBUTTONS %s' %buttons

        os.chdir('..')

        return [text,image,tts,buttons]


    def createaction(self,name,text,image,tts,buttons):
        fa = open(self.modimdemodir+'/actions/'+name,'w')
        if len(text)>0:
            fa.write('TEXT_title\n')
            fa.write('<*,*,*,*>: %s\n' %text)
            fa.write('----\n')
        if len(image)>0:
            fa.write('IMAGE\n')
            fa.write('<*,*,*,*>: %s\n' %image)
            fa.write('----\n')
        if len(tts)>0:
            fa.write('TTS\n')
            fa.write('<*,*,*,*>: %s\n' %tts)
            fa.write('----\n')
        if len(buttons)>0:
            fa.write('BUTTONS\n')
            for b in buttons:
                fa.write('%s\n' %b[0])
                fa.write('<*,*,*,*>: %s\n' %b[1])
            fa.write('----\n')
        fa.close()

    def getinfo(self):
        self.zip = zipfile.ZipFile(self.pptxfile)
        self.zip.printdir()
        l = self.zip.infolist()
        for zi in l:
            fn = str(zi.filename)
            # copy images
            if fn.startswith('ppt/media'):
                tk = fn.split('/')
                print '%s -> %s' %(fn,self.modimdemodir+'/img')
                #os.chdir(self.modimdemodir+'/img')
                self.zip.extract(zi)
                os.rename(fn, self.modimdemodir+'/img/'+tk[2])
            # prepare slides
            if fn.startswith('ppt/slides/slide'):
                tk = fn.split('/')
                an = tk[2].split('.')[0]
                print '\n%s -> %s' %(an,self.modimdemodir+'/actions')
                [text,image,tts,buttons] = self.getactioninfo(an)
                self.createaction(an,text,image,tts,buttons)

        self.zip.close()


# Main program

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("pptxfile", type=str, default='default.pptx',  help="Input pptx file")
    parser.add_argument("modimdemodir", type=str, default='default', help="MODIM demo output folder")

    args = parser.parse_args()

    print 'PPTX file: %s' %args.pptxfile
    print 'MODIM demo folder: %s' %args.modimdemodir

    p2m = PPTX2MODIM(args.pptxfile,args.modimdemodir)
    p2m.createdirs()
    p2m.getinfo()


