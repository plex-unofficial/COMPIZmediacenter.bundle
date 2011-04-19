# -*- coding: utf-8 -*-
#
#First ALPHA release on 05-06-2009
#Version 0.3
#
# This Plug-In is using the great web site / media portal www.COMPIZ.de
# All rights stay with COMPITZ
# I just did this plug-in to navigate the COMPIZ web site.
#
# COMPIZ.de wurde nicht fuer den Gebrauch am PC erstellt. Sondern fuer den PCH mit SYABAS-Browse
# Mehr Infos zu Compiz: http://www.popcornforum.de/showthread.php?tid=5702
# Kontakt: admin@compiz.de
#
# We use FRAMEWORK #1 because we need support for ID/PW secured web pages
#
#

from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *
from  htmlentitydefs import entitydefs
import urllib
import urllib2
import re
import base64

PLUGIN_PREFIX   = "/video/COMPIZmediacenter"
ROOT_URL        = "http://www.compiz.de"
ZDF_URL         = 'http://www.compiz.de/pch/mediathek/'
TRAILER_URL     = 'http://www.compiz.de/trailer/'
ARTE_URL        = 'http://www.compiz.de/arte/'
ARD_URL         = 'http://www.compiz.de/ard/'

CACHE_INTERVAL  = 3600

Protected 	= "No"
Username 	= 'nmt'
Password 	= 'nmt'
MainArt         = "%s/:/resources/%s" % (PLUGIN_PREFIX, "background-art.png")
MainThumb       = "%s/:/resources/%s" % (PLUGIN_PREFIX, "thumb-art.jpg")
SecondSelection = ""
SecondSelectionLogo = ""
zaehler         = 1

#This list had to be 'hard' coded as there was no desc. available for the links ... only img.
Sendernamen = [ 	"ZDF Mediathek",
                        "Filmtrailer",
                        "Podcasts",
                        "ARD Mediathek BETA",
                        "Verkehrsinfo BETA",
                        "FLaSH HOURS",
                        "COMPIZstoxx",
                        "Google Maps",
                        "SopCast ALPHA",
                        "arte.TV +7",
                        "3sat mediathek",
                        "more IPTV Channels",
                        "Spieltag Tabellen",
                        "CompizZEN",
                        "Hangman",
                        "(experimental) Video On Demand",
                        "Wetter",
                        "Die Bundekanzlerin",
                        "Die Bahn",
                        "Merkel"
                        ]

TrailerNames = [        "Alle Trailer",
                        "Jetzt im Kino",
                        "Bald im Kino",
                        "Neue Trailer"
                        ]

FrontPage = []
SecondPage= []
ThirdPage = []

Log('(PLUG-IN) Finished importing libraries & setting global variables')

####################################################################################################
def Start():

        # Add the MainMenu prefix handler
        Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, L('COMPIZmediacenter'), 'thumb-art.jpg', 'background-art.jpg')

        # Set up view groups
        Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
        Plugin.AddViewGroup("Info", viewMode="InfoList", mediaType="items")

        # Set the default cache time
        HTTP.SetCacheTime(3400)

        # Set the default MediaContainer attributes
        MediaContainer.title1 = 'COMPIZmediacenter'
        MediaContainer.content = 'List'
        MediaContainer.art = MainArt

        Log('(PLUG-IN) Finished initiallizing the plug-in')

####################################################################################################


def MainMenu(sender = None, Hallo = None):

        global FrontPage
        global SecondPage
        global ThirdPage
        global MainArt
        global MainThumb

        Log('(PLUG-IN) **==> ENTER Main Menu')
        if MainThumb == None:
                MainArt         = "%s/:/resources/%s" % (PLUGIN_PREFIX, "background-art.png")
                MainThumb       = "%s/:/resources/%s" % (PLUGIN_PREFIX, "thumb-art.jpg")

        dir = MediaContainer(art = MainArt, title1="COMPIZmediacenter", viewGroup="List")

        # Get the items for the FRONT page ... all WEB-PAGES & Thumbs
        if len(FrontPage) == 0:
                FrontPage = LoadFP()

        for item in FrontPage:
                TVID, URL, THUMB, TITLE = item
                # DirectoryItem( key, title, subtitle=None, summary=None, thumb=None, art=None, **kwargs)
                dir.Append(Function(DirectoryItem(LevelOneMenu,
                                                  title = TITLE,
                                                  subtitle= TITLE,
                                                  summary = None,
                                                  thumb = THUMB,
                                                  art= MainArt)
                                    , url = URL,
                                    tvid = TVID)
                           )
        Log('(PLUG-IN) <==** EXIT Main Menu')
        return dir

def LevelOneMenu(sender, url, tvid):

        global MainArt
        global MainThumb
        global FrontPage
        global Protected
        global Username
        global Password

        Log('(PLUG-IN) **==> ENTER Level One Menu')
        if MainThumb == None:
                MainArt         = "%s/:/resources/%s" % (PLUGIN_PREFIX, "background-art.png")
                MainThumb       = "%s/:/resources/%s" % (PLUGIN_PREFIX, "thumb-art.jpg")

        # Who did call us ... what was selected on Front Page
        wer = sender.itemTitle

        # Create a container
        dir = MediaContainer(title1="COMPIZmediacenter", title2=wer, viewGroup="List")

        #### Need to process each page indiviually ... depending what was selected on front page
        if wer == Sendernamen[0]:

                Log("(PLUG-IN) **==> ENTER: %s Menu" % (Sendernamen[0]))

                SecondPage = ZDF(url)

                for item in SecondPage:
                        URL, ALT, THUMB = item
                        # DirectoryItem( key, title, subtitle=None, summary=None, thumb=None, art=None, **kwargs)
                        dir.Append(Function(DirectoryItem(LevelTwoMenu,
                                                          title = ALT,
                                                          subtitle= ALT,
                                                          summary = None,
                                                          thumb = THUMB,
                                                          art= MainArt
                                                          ),
                                            url = URL,
                                            papa = wer,
                                            alt = ALT,
                                            thumb = THUMB
                                            )
                                   )
                #dSearchDirectoryItem(self, key, title, prompt, subtitle=None, summary=None, thumb=None, art=None, **kwargs):
                dir.Append(Function(SearchDirectoryItem(Search,
                                                        title=L("Suche ..."),
                                                        prompt=L("Suche in der ZDF Mediathek"),
                                                        subtitle = ALT,
                                                        summary = None,
                                                        thumb=R('search.png'),
                                                        art = MainArt
                                                        ),
                                    papa = wer,
                                    alt = ALT,
                                    thumb = THUMB,
                                    art = MainArt
                                    )
                           )

                Log("(PLUG-IN) <==** EXIT: %s Menu" % (Sendernamen[0]))

                return dir

        elif wer == Sendernamen[1]:

                Log("(PLUG-IN) **==> ENTER: %s Menu" % (Sendernamen[1]))

                # Test if we need ID - PW ... and get it
                check = getURL(TRAILER_URL, False)
                #Log(check)

                # Do we need to add the AUTHENTICATION header
                if check[1] <> {None:None}:
                        Log('(PLUG-IN) Needed Authentication TrailerStreams')
                        TRAILERStream = XML.ElementFromURL(TRAILER_URL, isHTML=True, values=None, headers=check[1], cacheTime=None, encoding="Latin-1", errors="ignore")
                else:
                        TRAILERStream = XML.ElementFromURL(TRAILER_URL, isHTML=True, values=None,  cacheTime=None, encoding="Latin-1", errors="ignore")

                TRAILERStreamString = cleanHTML(urllib2.urlopen(check[0]).read())

                Title = TRAILERStream.xpath('//title/text()')
                THUMB = TRAILER_URL + TRAILERStream.xpath('//center/img')[0].get('src')

                streamlist = TRAILERStream.xpath('//a')
                anzahl_streams = len(streamlist)
                ThirdPage = []

                for stream in range(0,anzahl_streams-1):

                        StreamSet = streamlist[stream]

                        URL = StreamSet.get('href')
                        TITLE = TrailerNames[stream]
                        SUBTITLE = "powered by previewnetworks.com"
                        SUMMARY = None
                        THUMB = StreamSet.xpath('//img')[stream+1].get('src')
                        if URL <> "":

                                dir.Append(Function(DirectoryItem(LevelTwoMenu,
                                                                  title = TITLE,
                                                                  subtitle= SUBTITLE,
                                                                  summary = None,
                                                                  thumb = TRAILER_URL + THUMB,
                                                                  art= MainArt
                                                                  ),
                                                    url = URL,
                                                    papa = wer,
                                                    alt = SUBTITLE,
                                                    thumb = TRAILER_URL + THUMB
                                                    )
                                           )

                Log("(PLUG-IN) <==** EXIT: %s Menu" % (Sendernamen[1]))

                return dir

        elif wer == Sendernamen[3]:

                Log("(PLUG-IN) **==> ENTER: %s Menu" % (Sendernamen[3]))

                SecondPage = ARD(url)

                for item in SecondPage:
                        URL, ALT, THUMB = item
                        #Log('**************** %s' % ALT.decode('Latin-1'))
                        # DirectoryItem( key, title, subtitle=None, summary=None, thumb=None, art=None, **kwargs)
                        dir.Append(Function(DirectoryItem(LevelTwoMenu,
                                                          title = cleanGerman(ALT, 'Latin-1', 'Latin-1'), #.decode('utf-8'), #.decode('Latin-1'), #.decode('utf-8'),
                                                          subtitle= None,
                                                          summary = None,
                                                          thumb = THUMB,
                                                          art= MainArt
                                                          ),
                                            url = URL,
                                            papa = wer,
                                            alt = ALT,
                                            thumb = THUMB
                                            )
                                   )

                # ARD Search is NOT working at www.compitz.de as of 05-07-09
                #SearchDirectoryItem(self, key, title, prompt, subtitle=None, summary=None, thumb=None, art=None, **kwargs):
                #dir.Append(Function(SearchDirectoryItem(Search,
                                                        #title=L("Suche ..."),
                                                        #prompt=L("Suche in der ZDF Mediathek"),
                                                        #subtitle = ALT,
                                                        #summary = None,
                                                        #thumb=R('search.png'),
                                                        #art = MainArt
                                                        #),
                                    #papa = wer,
                                    #alt = ALT,
                                    #thumb = THUMB,
                                    #art = MainArt
                                    #)
                           #)

                Log("(PLUG-IN) <==** EXIT: %s Menu" % (Sendernamen[3]))

                return dir


        elif wer == Sendernamen[9]:

                Log("(PLUG-IN) **==> ENTER: %s Menu" % (Sendernamen[9]))

                # Test if we need ID - PW ... and get it
                check = getURL(ARTE_URL, False)
                #Log(check)

                # Do we need to add the AUTHENTICATION header
                if check[1] <> {None:None}:
                        Log('(PLUG-IN) Needed Authentication ARTEStreams')
                        ARTEStreams = XML.ElementFromURL(ARTE_URL, isHTML=True, values=None, headers=check[1], cacheTime=None, encoding="Latin-1", errors="ignore")
                else:
                        ARTEStreams = XML.ElementFromURL(ARTE_URL, isHTML=True, values=None,  cacheTime=None, encoding="Latin-1", errors="ignore")

                ARTEStreamsString = cleanHTML(urllib2.urlopen(check[0]).read())

                Title = ARTEStreams.xpath('//title/text()')[0]
                THUMB = ARTEStreams.xpath('//body/font/img')[0].get('src')
                SenderTHUMB = THUMB
                Subtitle = str(ARTEStreams.xpath('//body/font/font/text()')[0])

                streamlistdescription = GetValues("<!--online bis<br>",ARTEStreamsString) #How Long is it ONLINE ?
                streamlisttitle = ARTEStreams.xpath('//*[@class="item_title"]') #Titles 10 streams in .text()
                streamlistthumbs =  GetValues("src=",ARTEStreamsString) # The THUMB URLs
                streamlisturl = GetValues("<a href=",ARTEStreamsString) #Finding the stream URLs

                anzahl_streams = len(streamlisttitle)
                ThirdPage = []
                ThirdPagePart1 = []

                ## This page is VERY badly composed ==> the normal XPATH does not work ... thus the 'strange' parsing

                #sender, url, papa, alt, thumb
                dir = LevelTwoMenu( sender, url = ARTE_URL, papa = wer, alt = Subtitle, thumb = SenderTHUMB)

                Log("(PLUG-IN) <==** EXIT: %s Menu" % (Sendernamen[9]))

                return dir


        else:

                Log("(PLUG-IN) Level One Menu:  We did NOT catch this !")

                return dir

        return None



def LevelTwoMenu(sender, url, papa, alt, thumb):


        global FrontPage
        global SecondPage
        global ThirdPage
        global MainArt
        global MainThumb
        global SecondSelection
        global SecondSelectionLogo
        global zaehler

        Log('(PLUG-IN) **==> ENTER: Level Two Menu')

        if MainThumb == None:
                MainArt         = "%s/:/resources/%s" % (PLUGIN_PREFIX, "background-art.png")
                MainThumb       = "%s/:/resources/%s" % (PLUGIN_PREFIX, "thumb-art.jpg")

        # Get the items for the FRONT page ... all WEB-PAGES & Thumbs
        if len(FrontPage) == 0:
                FrontPage = LoadFP()

        URL = url
        ALT = alt
        THUMB = thumb

        # Who did call us ... what was selected on ZDF Channel list
        TopLevel = papa
        SecondLevel = url
        Section = sender.itemTitle
        SectionTitel = Section.title()
        #Log(url, papa, alt)
        #Log(thumb, Section)

        if papa == Sendernamen[0]:

                Log("(PLUG-IN) ENTERED Level Two Menu for: %s" % (papa))

                HeadLine, ThirdPage, NextPage = ZDFStreams(ZDF_URL+SecondLevel)

                if str(Section.title()[0:5]) == str('Seite'):

                        SectionTitel = str(str(int(Section.title().split()[1])-1) + ' von ' + str(Section.title().split()[3]))

                else:
                        SecondSelection = Section.title() + ' Startseite'
                        SecondSelectionLogo = THUMB

                dir = MediaContainer(title1 = SectionTitel, title2 = HeadLine, viewGroup = "Info")

                for item in ThirdPage:
                        URL, DATE, TITLE, SUBTITLE, DURATION, DESCRIPTION, THUMB= item
                        # DirectoryItem( key, title, subtitle=None, summary=None, thumb=None, art=None, **kwargs)
                        # VideoItem(self, key, title, subtitle=None, summary=None, duration=None, thumb=None, art=None, **kwargs):
                        # The foolowing code can be used if we want a BIG list of all the streams and SINGLE click to have them started.
			#ML(URL)
                        #URL = URL.replace('rtsp://','http://') # CHANGE Protocol header to make the streams work ...
			if URL[-3:] == "wmv":
				#URL = "http://www.plexapp.com/player/silverlight.php?stream=" + URL + "&width=688&height=384" # + "#foo.wvx"
				WEBVIDEO = True

			#if URL[-3:] == "wmv": URL = URL + "?MSWMExt=.asf"
			#ML(URL)
                        TITLE = TITLE.encode('Latin-1').decode('utf-8')

                        SUMMARY = u"""
                        Vom:      %s

                        Dauer:    %s

                        %s""" % (DATE,DURATION, DESCRIPTION)

                        SUMMARY = cleanGerman(SUMMARY) #DESCRIPTION.decode('utf-8')
			ML(URL)
			if WEBVIDEO == True:
				#class RTMPVideoItem(WebVideoItem):
				#def __init__(self, url, clip=None, width=640, height=480, live=False, title=None, subtitle=None, summary=None, duration=None, thumb=None, art=None, **kwargs):
				#dir.Append(RTMPVideoItem(url      = URL,
							 #clip     = "",
							 #width    = 640,
							 #height   = 480,
							 #live     = False,
							 #title    = TITLE,
							 #subtitle = SUBTITLE,
							 #summary  = SUMMARY,
							 #duration = DurationToInt(DURATION),
							 #thumb    = THUMB,
							 #art      = MainArt
							#)
					   #)

				#class WindowsMediaVideoItem(WebVideoItem):
				#def __init__(self, url, width=720, height=576, title=None, subtitle=None, summary=None, duration=None, thumb=None, art=None, **kwargs):
				#688&height=384
				dir.Append(WindowsMediaVideoItem(url      = URL,
								 width    = 688,
								 height   = 384,
								 title    = TITLE,
								 subtitle = SUBTITLE,
								 summary  = SUMMARY,
								 duration = DurationToInt(DURATION),
								 thumb    = THUMB,
								 art      = MainArt
								 )
					   )

				WEBVIDEO = False

			else:

				dir.Append(VideoItem(   URL,
							TITLE,
							subtitle = SUBTITLE,
							summary = SUMMARY,
							duration = DurationToInt(DURATION),
							thumb = THUMB,
							art = MainArt
							)
					   )

                # Add any NAVIGATION pages if nessesary
                if NextPage <> None:

                        LEFT = []
                        RIGHT = []
                        HOME = []
                        BACK = []

                        for item in NextPage:

                                URL, TVID, THUMB = item

                                if TVID == 'HOME':
                                        HOME = [URL, TVID, THUMB]
                                elif TVID == 'RIGHT':
                                        RIGHT = [URL, TVID, THUMB]
                                elif TVID == 'LEFT':
                                        LEFT = [URL, TVID, THUMB]
                                elif TVID == 'BACK':
                                        BACK = [URL, TVID, THUMB]
                                else:
                                        dir.Append(Function(DirectoryItem(LevelTwoMenu,
                                                                          title = "Other Page",
                                                                          subtitle= None,
                                                                          summary = None,
                                                                          thumb = THUMB,
                                                                          art = MainArt
                                                                          ),
                                                            url = URL,
                                                            papa = papa,
                                                            alt = ALT,
                                                            thumb = MainThumb
                                                            )
                                                   )

                        # Add Pages

                        if LEFT <> []:

                                # Check if we have to PREP Logo & Title for first video-stream page ... coming back from page 2 or later.
                                if int(HeadLine.split(' -- Seite ')[1].split('/')[0].rstrip()) == 2:

                                        TITLE = SecondSelection
                                        THUMB = SecondSelectionLogo

                                else:
                                        TITLE = str('Seite '+ str(int(HeadLine.split(' -- Seite ')[1].split('/')[0].rstrip()) - 1) +' von ' + HeadLine.split(' -- Seite ')[1].split('/ ')[1])
                                        THUMB = SecondSelectionLogo
                                        Log('(PLUG-IN) ^^^ELSE^^ %s' % THUMB)

                                dir.Append(Function(DirectoryItem(LevelTwoMenu,
                                                                  title = TITLE,
                                                                  subtitle= None,
                                                                  summary = None,
                                                                  thumb = THUMB,
                                                                  art = MainArt
                                                                  ),
                                                    url = fixURL(LEFT[0]),
                                                    papa = papa,
                                                    alt = SecondSelection,
                                                    thumb = SecondSelectionLogo
                                                    )
                                           )

                        if HOME <> []:

                                dir.Append(Function(DirectoryItem(MainMenu,
                                                                  title = "COMPIZmediacenter",
                                                                  subtitle= None,
                                                                  summary = None,
                                                                  thumb = MainThumb,
                                                                  art = MainArt
                                                                  )
                                                    )
                                           )
                                dir.noHistory = True

                        if BACK <> []:

                                TVID, URL, THUMB, TITLE = FrontPage[0]
                                dir.Append(Function(DirectoryItem(LevelOneMenu,
                                                                  title = TITLE,
                                                                  subtitle= TITLE,
                                                                  summary = None,
                                                                  thumb = THUMB,
                                                                  art = MainArt
                                                                  ),
                                                    url = URL,
                                                    tvid = TVID
                                                    )
                                           )
                                dir.noHistory = True

                        if RIGHT <> []:

                                TITLE = str('Seite '+ str(int(HeadLine.split(' -- Seite ')[1].split('/')[0].rstrip()) +1) +' von ' + HeadLine.split(' -- Seite ')[1].split('/ ')[1])

                                dir.Append(Function(DirectoryItem(LevelTwoMenu,
                                                                  title = TITLE,
                                                                  subtitle= None,
                                                                  summary = None,
                                                                  thumb = SecondSelectionLogo,
                                                                  art = MainArt
                                                                  ),
                                                    url = fixURL(RIGHT[0]),
                                                    papa = papa,
                                                    alt = SecondSelection,
                                                    thumb = SecondSelectionLogo)
                                           )


                Log("(PLUG-IN) <==** EXIT Level Two Menu for: %s" % (papa))

                return dir

        elif papa == Sendernamen[1]:

                Log("(PLUG-IN) ENTERED Level Two Menu for: %s" % (papa))

                HeadLine, ThirdPage, NextPage = TrailerStreams(TRAILER_URL+SecondLevel)

                if str(Section.title()[0:5]) == str('Seite'):

                        SectionTitel = str(str(int(Section.title().split()[1])-1) + ' von ' + str(Section.title().split()[3]))

                else:
                        SecondSelection = Section.title() + ' Startseite'
                        SecondSelectionLogo = THUMB

                dir = MediaContainer(title1 = SectionTitel, title2 = alt, viewGroup = "Info")

                for item in ThirdPage:

                        URL, DATETEXT, DATE, TITLE, DESCRIPTION, THUMB = item
                        #Log('URL %s, DATETEXT %s, DATE %s, TITLE %s, DESCRIPTION %s, THUMB %s' % (URL, DATETEXT, DATE, TITLE, DESCRIPTION, THUMB))
                        # DirectoryItem( key, title, subtitle=None, summary=None, thumb=None, art=None, **kwargs)
                        # VideoItem(self, key, title, subtitle=None, summary=None, duration=None, thumb=None, art=None, **kwargs):
                        # The foolowing code can be used if we want a BIG list of all the streams and SINGLE click to have them started.

                        SUMMARY = ((
                                '%s: %s     \n\n'+
                                '%s') % (DATETEXT,DATE, DESCRIPTION)
                                   )
                        SUMMARY = SUMMARY.decode('utf-8')
                        #Log('SUMMARY %s' % type(SUMMARY))
                        dir.Append(VideoItem(   URL, #.replace('rtsp://','http://'), # CHANGE Protocol header to make the streams work ...
                                                TITLE.decode('utf-8'),
                                                #subtitle = SUBTITLE.encode('Latin-1').decode('utf-8'),
                                                summary = SUMMARY,
                                                duration = None,
                                                thumb = THUMB,
                                                art = MainArt
                                                )
                                   )

                # Add any NAVIGATION pages if nessesary
                if NextPage <> None:

                        LEFT = []
                        RIGHT = []
                        HOME = []
                        BACK = []

                        for item in NextPage:

                                URL, TVID, THUMB = item

                                if TVID == 'HOME':
                                        HOME = [URL, TVID, THUMB]
                                elif ((TVID == 'RIGHT') or (TVID == 'PGDN')):
                                        RIGHT = [URL, TVID, THUMB]
                                elif ((TVID == 'LEFT') or (TVID == 'PGUP')):
                                        LEFT = [URL, TVID, THUMB]
                                elif TVID == 'BACK':
                                        BACK = [URL, TVID, THUMB]
                                else:
                                        dir.Append(Function(DirectoryItem(LevelTwoMenu,
                                                                          title = "Other Page",
                                                                          subtitle= None,
                                                                          summary = None,
                                                                          thumb = THUMB,
                                                                          art = MainArt
                                                                          ),
                                                            url = URL,
                                                            papa = papa,
                                                            alt = ALT,
                                                            thumb = MainThumb
                                                            )
                                                   )

                        # Add Pages

                        if LEFT <> []:


                                TITLE = 'vorherige Seite'
                                THUMB = SecondSelectionLogo
                                Log('(PLUG-IN) ^^^ELSE^^ %s' % THUMB)

                                dir.Append(Function(DirectoryItem(LevelTwoMenu,
                                                                  title = TITLE,
                                                                  subtitle= None,
                                                                  summary = None,
                                                                  thumb = THUMB,
                                                                  art = MainArt
                                                                  ),
                                                    url = fixURL(LEFT[0]),
                                                    papa = papa,
                                                    alt = SecondSelection,
                                                    thumb = SecondSelectionLogo
                                                    )
                                           )

                        if HOME <> []:

                                dir.Append(Function(DirectoryItem(MainMenu,
                                                                  title = "COMPIZmediacenter",
                                                                  subtitle= None,
                                                                  summary = None,
                                                                  thumb = MainThumb,
                                                                  art = MainArt
                                                                  )
                                                    )
                                           )
                                dir.noHistory = True

                        if BACK <> []:

                                TVID, URL, THUMB, TITLE = FrontPage[1]
                                dir.Append(Function(DirectoryItem(LevelOneMenu,
                                                                  title = TITLE,
                                                                  subtitle= TITLE,
                                                                  summary = None,
                                                                  thumb = THUMB,
                                                                  art = MainArt
                                                                  ),
                                                    url = URL,
                                                    tvid = TVID
                                                    )
                                           )
                                dir.noHistory = True

                        if RIGHT <> []:

                                TITLE = "naechste Seite"

                                dir.Append(Function(DirectoryItem(LevelTwoMenu,
                                                                  title = TITLE,
                                                                  subtitle= None,
                                                                  summary = None,
                                                                  thumb = SecondSelectionLogo,
                                                                  art = MainArt
                                                                  ),
                                                    url = fixURL(RIGHT[0]),
                                                    papa = papa,
                                                    alt = SecondSelection,
                                                    thumb = SecondSelectionLogo)
                                           )


                Log("(PLUG-IN) <==** EXIT Level Two Menu for: %s" % (papa))

                return dir


        if papa == Sendernamen[3]:

                Log("(PLUG-IN) ENTERED Level Two Menu for: %s" % (papa))

                if SecondLevel[0:7] == 'http://':
                        URL = SecondLevel
                else:
                        URL = ARD_URL+SecondLevel

                HeadLine, ThirdPage, NextPage = ARDStreams(URL)

                if str(Section.title()[0:5]) == str('Seite'):

                        SectionTitel = str(str(int(Section.title().split()[1])-1) + ' von ' + str(Section.title().split()[3]))

                else:
                        SecondSelection = Section.title() + ' Startseite'
                        SecondSelectionLogo = THUMB

                dir = MediaContainer(title1 = TopLevel, title2 = HeadLine, viewGroup = "Info", art = THUMB)

                for item in ThirdPage:
                        URL, DATE, DURATION, DESCRIPTION, THUMB= item
                        DESCRIPTION = cleanGerman(DESCRIPTION.decode('utf-8'),'utf-8','utf-8')
                        # DirectoryItem( key, title, subtitle=None, summary=None, thumb=None, art=None, **kwargs)
                        # VideoItem(self, key, title, subtitle=None, summary=None, duration=None, thumb=None, art=None, **kwargs):
                        # The foolowing code can be used if we want a BIG list of all the streams and SINGLE click to have them started.

                        URL = URL.replace('rtsp://','http://') # CHANGE Protocol header to make the streams work ...

                        TITLE = DESCRIPTION
                        #Log('********* %s' % DESCRIPTION)
                        DESCRIPTION = DESCRIPTION
                        SUMMARY = u"""
                        Vom:      %s

                        Dauer:    %s

                        %s""" % (DATE,DURATION, DESCRIPTION)

                        SUMMARY = cleanGerman(SUMMARY, 'utf-8', 'utf-8') #DESCRIPTION.decode('utf-8')

                        #dir.Append(VideoItem(   URL,
                                                #TITLE,
                                                #subtitle = HeadLine,
                                                #summary = SUMMARY,
                                                #duration = DurationToInt(DURATION),
                                                #thumb = THUMB,
                                                #art = MainArt
                                                #)
                                   #)

			#class WindowsMediaVideoItem(WebVideoItem):
			#def __init__(self, url, width=720, height=576, title=None, subtitle=None, summary=None, duration=None, thumb=None, art=None, **kwargs):
			#688&height=384
			dir.Append(WindowsMediaVideoItem(url      = URL,
							 width    = 688,
							 height   = 384,
							 title    = TITLE,
							 subtitle = HeadLine,
							 summary  = SUMMARY,
							 duration = DurationToInt(DURATION),
							 thumb    = THUMB,
							 art      = MainArt
							 )
				   )

                # Add any NAVIGATION pages if nessesary
                # Get the items for the FRONT page ... all WEB-PAGES & Thumbs
                if len(FrontPage) == 0:
                        FrontPage = LoadFP()

                #Find the NEXT page if any

                if NextPage <> None:

                        LEFT = []
                        RIGHT = []
                        HOME = []
                        BACK = []

                        for item in NextPage:

                                URL, TVID, THUMB = item

                                if TVID == 'HOME':
                                        HOME = [URL, TVID, THUMB]
                                elif TVID == 'PGUP':
                                        RIGHT = [URL, TVID, THUMB]
                                elif TVID == 'PGDN':
                                        LEFT = [URL, TVID, THUMB]
                                elif TVID == 'BACK':
                                        BACK = [URL, TVID, THUMB]
                                else:
                                        #LevelOneMenu(sender, url, tvid)
                                        #LevelTwoMenu(sender, url, papa, alt, thumb):
                                        dir.Append(Function(DirectoryItem(LevelTwoMenu,
                                                                                title = "other Page",
                                                                                subtitle= None,
                                                                                summary = None,
                                                                                thumb = THUMB,
                                                                                art = MainArt
                                                                                ),
                                                                url = fixurl(URL),
                                                                papa = papa,
                                                                alt = TITLE,
                                                                thumb = THUMB
                                                                )
                                                       )

                        # Add Pages

                        if LEFT <> []:

                                ## Check if we have to PREP Logo & Title for first video-stream page ... coming back from page 2 or later.
                                #if int(HeadLine.split(' -- Seite ')[1].split('/')[0].rstrip()) == 2:

                                TITLE = "vorherige Seite"
                                THUMB = SecondSelectionLogo

                                #LevelOneMenu(sender, url, tvid)
                                #LevelTwoMenu(sender, url, papa, alt, thumb):

                                try:
                                        zaehler = int(ALT.split('Seite: ')[1])
                                except:
                                        zaehler = zaehler - 1

                                if zaehler == 1:
                                        AltTitle = "Startseite: " + Sendernamen[9]

                                else:
                                        AltTitle = "Seite: " + str(zaehler)

                                dir.Append(Function(DirectoryItem(LevelTwoMenu,
                                                                  title = TITLE,
                                                                  subtitle= None,
                                                                  summary = None,
                                                                  thumb = LEFT[2],
                                                                  art = MainArt
                                                                  ),
                                                    url = LEFT[0],
                                                    papa = Sendernamen[3],
                                                    alt = AltTitle,
                                                    thumb = LEFT[2]
                                                    )
                                           )
                                # DirectoryItem( key, title, subtitle=None, summary=None, thumb=None, art=None, **kwargs)

                        if HOME <> []:

                                dir.Append(Function(DirectoryItem(MainMenu,
                                                                  title = "COMPIZmediacenter",
                                                                  subtitle= None,
                                                                  summary = None,
                                                                  thumb = MainThumb,
                                                                  art = MainArt
                                                                  )
                                                    )
                                           )
                                dir.noHistory = True

                        if BACK <> []:

                                TVID, URL, THUMB, TITLE = FrontPage[3]
                                dir.Append(Function(DirectoryItem(LevelTwoMenu,
                                                                  title = "Startseite: " + str(TITLE), #"Startseite: " +
                                                                  subtitle= TITLE,
                                                                  summary = None,
                                                                  thumb = THUMB,
                                                                  art = MainArt
                                                                  ),
                                                        url = ARD_URL,
                                                        papa = Sendernamen[3],
                                                        alt = "Startseite: " + str(TITLE),
                                                        thumb = THUMB
                                                    )
                                           )
                                dir.noHistory = True
                                zaehler = 1

                        if RIGHT <> []:

                                TITLE = u"naechste Seite"
                                #navilist  = GetValues("<a tvid=",ARDStreamsString)
                                #pageURL = navilist[0]

                                try:
                                        zaehler = int(ALT.split('Seite: ')[1])
                                except:
                                        zaehler = zaehler + 1

                                dir.Append(Function(DirectoryItem(LevelTwoMenu,
                                                                  title = TITLE , #TITLE,
                                                                  subtitle= None,
                                                                  summary = None,
                                                                  thumb = RIGHT[2],
                                                                  art = MainArt
                                                                  ),
                                                        url = RIGHT[0],
                                                        papa = Sendernamen[3],
                                                        alt = "Seite: " + str(zaehler) ,
                                                        thumb = THUMB                                                    )
                                           )


                Log("(PLUG-IN) <==** EXIT Level Two Menu for: %s" % (papa))

                return dir

        elif papa == Sendernamen[9]:

                Log("(PLUG-IN) ENTERED Level Two Menu for: %s" % (papa))

                 # Who did call us ... what was selected on Front Page
                wer = sender.itemTitle

                # Test if we need ID - PW ... and get it
                check = getURL(URL, False)
                #Log(check)

                # Do we need to add the AUTHENTICATION header
                if check[1] <> {None:None}:
                        Log('(PLUG-IN) Needed Authentication ARTEStreams')
                        ARTEStreams = XML.ElementFromURL(URL, isHTML=True, values=None, headers=check[1], cacheTime=None, encoding="Latin-1", errors="ignore")
                else:
                        ARTEStreams = XML.ElementFromURL(URL, isHTML=True, values=None,  cacheTime=None, encoding="Latin-1", errors="ignore")

                ARTEStreamsString = cleanHTML(urllib2.urlopen(check[0]).read())

                Title = ARTEStreams.xpath('//title/text()')[0]
                THUMB = ARTEStreams.xpath('//body/font/img')[0].get('src')
                SenderTHUMB = THUMB
                Subtitle = str(ARTEStreams.xpath('//body/font/font/text()')[0])

                streamlistdescription = GetValues("<!--online bis<br>",ARTEStreamsString) #How Long is it ONLINE ?
                streamlisttitle = ARTEStreams.xpath('//*[@class="item_title"]') #Titles 10 streams in .text()
                streamlistthumbs =  GetValues("src=",ARTEStreamsString) # The THUMB URLs
                streamlisturl = GetValues("<a href=",ARTEStreamsString) #Finding the stream URLs

                anzahl_streams = len(streamlisttitle)
                ThirdPage = []
                ThirdPagePart1 = []

                ## This page is VERY badly composed ==> the normal XPATH does not work ... thus the 'strange' parsing

                #sender, url, papa, alt, thumb
                #dir = LevelTwoMenu( sender, url = None, papa = wer, alt = Subtitle, thumb = SenderTHUMB)
                dir = MediaContainer(title1 = Sendernamen[9], title2 = alt, viewGroup = "Info")


                for stream in range(0,anzahl_streams):

                        StreamSetURL = streamlisturl[stream+1]
                        StreamSetIMG = streamlistthumbs[stream+2]
                        StreamSetTitle = streamlisttitle[stream]
                        StreamSetDescription = streamlistdescription[stream+1]

                        try:
                                TITLE = StreamSetTitle.text_content().encode('Latin-1').decode('utf-8')
                        except:
                                TITLE = "T"
                                Log(TITLE)
                                #Log(StreamSetTitle.text_content())
                                Log(type(StreamSetTitle.text_content()))
                                Log(StreamSetTitle.text_content().encode('Latin-1'))

                        #Log(TITLE)
                        try:
                                URL = StreamSetURL #StreamSetURL.get('href')
                        except:
                                URL = None
                        #Log(URL)
                        try:
                                THUMB = StreamSetIMG #.text_content().encode('Latin-1')
                        except:
                                THUMB =" "
                        #Log(THUMB)
                        try:
                                Subtitle = StreamSetDescription #.text_content().encode('Latin-1')
                                try:
                                        Subtitle = "Online bis: " + Subtitle.split('--')[0].split('T')[0] + "   " + Subtitle.split('--')[0].split('T')[1]
                                except:
                                        Subtitle = "S"
                        except:
                                Subtitle = "S"
                        #Log(Subtitle)

                        if URL <> "":

                                dir.Append(Function(DirectoryItem(PlayArteVideo,
                                                                  title = TITLE,
                                                                  subtitle= Subtitle,
                                                                  summary = None,
                                                                  thumb = THUMB,
                                                                  art= MainArt
                                                                  ),
                                                    url = ARTE_URL + URL,
                                                    papa = wer,
                                                    alt = Subtitle,
                                                    thumb = SenderTHUMB
                                                    )
                                           )

                # Add any NAVIGATION pages if nessesary
                # Get the items for the FRONT page ... all WEB-PAGES & Thumbs
                if len(FrontPage) == 0:
                        FrontPage = LoadFP()

                #Find the NEXT page if any
                pagelist = ARTEStreams.xpath('//a[@tvid] ')
                anzahl_pageitems = len(pagelist)
                #Log('Page Items %s' % anzahl_pageitems)

                NextPage = []

                for page in range(0,anzahl_pageitems):

                        PageSet = pagelist[page]

                        URL = PageSet.get('href')
                        TVID = PageSet.get('tvid')
                        try:
                                THUMB = PageSet.find('img').get('src')
                                THUMB = ROOT_URL + THUMB.split('..')[1]

                        except:
                                THUMB = R("background-art.png")

                        #Log('THUMB in Page: %s' % THUMB)

                        NextPage = NextPage + [(URL, TVID, THUMB)]

                if NextPage <> None:

                        LEFT = []
                        RIGHT = []
                        HOME = []
                        BACK = []

                        for item in NextPage:

                                URL, TVID, THUMB = item

                                if TVID == 'HOME':
                                        HOME = [URL, TVID, THUMB]
                                elif TVID == 'PGDN':
                                        RIGHT = [URL, TVID, THUMB]
                                elif TVID == 'PGUP':
                                        LEFT = [URL, TVID, THUMB]
                                elif TVID == 'BACK':
                                        BACK = [URL, TVID, THUMB]
                                else:
                                        #LevelOneMenu(sender, url, tvid)
                                        #LevelTwoMenu(sender, url, papa, alt, thumb):
                                        dir.Append(Function(DirectoryItem(LevelTwoMenu,
                                                                                title = "other Page",
                                                                                subtitle= None,
                                                                                summary = None,
                                                                                thumb = THUMB,
                                                                                art = MainArt
                                                                                ),
                                                                url = fixurl(URL),
                                                                papa = papa,
                                                                alt = TITLE,
                                                                thumb = THUMB
                                                                )
                                                       )

                        # Add Pages

                        if LEFT <> []:

                                ## Check if we have to PREP Logo & Title for first video-stream page ... coming back from page 2 or later.
                                #if int(HeadLine.split(' -- Seite ')[1].split('/')[0].rstrip()) == 2:

                                TITLE = "vorherige Seite"
                                THUMB = SecondSelectionLogo

                                #LevelOneMenu(sender, url, tvid)
                                #LevelTwoMenu(sender, url, papa, alt, thumb):

                                try:
                                        zaehler = int(ALT.split('Seite: ')[1])
                                except:
                                        zaehler = zaehler - 1

                                if zaehler == 1:
                                        AltTitle = "Startseite: " + Sendernamen[9]

                                else:
                                        AltTitle = "Seite: " + str(zaehler)

                                dir.Append(Function(DirectoryItem(LevelTwoMenu,
                                                                  title = TITLE,
                                                                  subtitle= None,
                                                                  summary = None,
                                                                  thumb = LEFT[2],
                                                                  art = MainArt
                                                                  ),
                                                    url = ARTE_URL + LEFT[0],
                                                    papa = Sendernamen[9],
                                                    alt = AltTitle,
                                                    thumb = LEFT[2]
                                                    )
                                           )
                                # DirectoryItem( key, title, subtitle=None, summary=None, thumb=None, art=None, **kwargs)

                        if HOME <> []:

                                dir.Append(Function(DirectoryItem(MainMenu,
                                                                  title = "COMPIZmediacenter",
                                                                  subtitle= None,
                                                                  summary = None,
                                                                  thumb = MainThumb,
                                                                  art = MainArt
                                                                  )
                                                    )
                                           )
                                dir.noHistory = True

                        if BACK <> []:

                                TVID, URL, THUMB, TITLE = FrontPage[9]
                                #Log('BACK URL: %s' % URL)
                                dir.Append(Function(DirectoryItem(LevelTwoMenu,
                                                                  title = "Startseite: " + str(TITLE), #"Startseite: " +
                                                                  subtitle= TITLE,
                                                                  summary = None,
                                                                  thumb = THUMB,
                                                                  art = MainArt
                                                                  ),
                                                        url = ARTE_URL,
                                                        papa = Sendernamen[9],
                                                        alt = "Startseite: " + str(TITLE),
                                                        thumb = THUMB
                                                    )
                                           )
                                dir.noHistory = True
                                zaehler = 1

                        if RIGHT <> []:

                                TITLE = u"naechste Seite"
                                navilist  = GetValues("<a tvid=",ARTEStreamsString)
                                pageURL = navilist[0]

                                try:
                                        zaehler = int(ALT.split('Seite: ')[1])
                                except:
                                        zaehler = zaehler + 1

                                dir.Append(Function(DirectoryItem(LevelTwoMenu,
                                                                  title = TITLE , #TITLE,
                                                                  subtitle= None,
                                                                  summary = None,
                                                                  thumb = RIGHT[2],
                                                                  art = MainArt
                                                                  ),
                                                        url = ARTE_URL+RIGHT[0],
                                                        papa = Sendernamen[9],
                                                        alt = "Seite: " + str(zaehler) ,
                                                        thumb = THUMB                                                    )
                                           )

                Log("(PLUG-IN) <==** EXIT Level Two Menu for: %s" % (papa))

                return dir



        else:

                Log("(PLUG-IN) Level Two Menu: We did NOT catch this ! %s" % papa)

                return dir

        return dir


        #### Need to process each page indiviually ... depending what was selected on front page


def LevelThreeMenu(sender, url):

        global MainArt
        global MainThumb

        Log('(PLUG-IN) **==> ENTER Level Three Menu')

        if MainThumb == None:
                MainArt         = "%s/:/resources/%s" % (PLUGIN_PREFIX, "background-art.png")
                MainThumb       = "%s/:/resources/%s" % (PLUGIN_PREFIX, "thumb-art.jpg")

        URL = url
        DATE = date
        SUBTITLE = subtitle
        DURATION = duration
        DESCRIPTION = description
        THUMB = thumb

        dir = MediaContainer(title1=sender.title2, title2=sender.itemTitle, viewGroup="Info")
        dir.Append(VideoItem(URL, title = DATE, subtitle=SUBTITLE, summary=DESCRIPTION, duration=DURATION, thumb=THUMB, art = R("background-art.png")))

        Log('(PLUG-IN) <==** EXIT Level Three Menu')

        return dir

def Search(sender, query, papa, alt, thumb, art, page=1):

        Log('(PLUG-IN) **==> ENTER Search for ZDF Streams')

        dir = MediaContainer(viewGroup='Details', title1 = alt, title2='Such Ergebnis')

        query = query.replace(' ', '+')

        URL = 'pch.php?s='+query

        dir = LevelTwoMenu(sender, URL, papa, alt, thumb)

        Log('(PLUG-IN) <==** EXIT Search for ZDF Streams')

        return dir


def LoadFP():

        global FrontPage
        global ROOT_URL
        global Protected

        global MainArt
        global MainThumb

        Log('(PLUG-IN) **==> ENTER Load FIRST Page COMPIZMediacenter')

        if MainThumb == None:
                MainArt         = "%s/:/resources/%s" % (PLUGIN_PREFIX, "background-art.png")
                MainThumb       = "%s/:/resources/%s" % (PLUGIN_PREFIX, "thumb-art.jpg")

        # Get the MAIN Page
        Log("(PLUG-IN) Try ROOT_URL: %s" % (ROOT_URL))

        # Check if URL needs ID / PW
        check = getURL(ROOT_URL, False)

        # Do we need to add the AUTHENTICATION header
        #def ElementFromURL(url, isHTML=False, values=None, headers={}, cacheTime=None, encoding="utf8", errors="strict"):
        if check[1] <> {None:None}:
                Log('(PLUG-IN) Needed Authentication')
                toppage = XML.ElementFromURL(ROOT_URL, isHTML = True, values = None, headers = check[1], cacheTime=None, encoding="utf8", errors="ignore")

        else:
                toppage = XML.ElementFromURL(ROOT_URL, isHTML = True, values=None, headers={}, cacheTime=None, encoding="utf8", errors="ignore")

        # Select all the TV Stations (each station is FRAMED with "<a>...</a>"
        senderlist = toppage.xpath('//a')

        # How many did we get?
        anzahl_sender = len(senderlist)
        Log("(PLUG-IN) Anzahl Sender: %s" % (anzahl_sender))

        FrontPage = []
        # Get the TVID, URL, and THUMB for each 'station'
        for sender in range(0,anzahl_sender-1):

                SenderSet = senderlist[sender+1]

                # We have to TRY each attribute as not all stations have all attributes.
                try:
                        #Interesting that the GET function ONLY works on lowercase "tvid" even if the web-page uses uppercase "TVID"
                        TVID = SenderSet.get('tvid')
                except:
                        TVID = ""

                try:
                        URL = SenderSet.get('href')
                except:
                        URL = ""

                try:
                        # The THUMB url (src) is in the next section <img> and thus we need to find this first before we can GET the src-info.
                        THUMB = ROOT_URL+SenderSet.find('img').get('src')
                except:
                        THUMB = R("background-art.png")

                try:
                        TITLE = Sendernamen[sender]
                except:
                        TITLE = "COMPIZmediathek"

                FrontPage = FrontPage + [(TVID,URL,THUMB,TITLE)]

        Log('(PLUG-IN) <==** EXIT Load FIRST Page COMPIZMediacenter')

        return FrontPage

def ZDF(sender):

        global Protected
        global Username
        global Password

        global MainArt
        global MainThumb

        Log('(PLUG-IN) **==> ENTER Load FIRST Page ZDF Mediathek')

        if MainThumb == None:
                MainArt         = "%s/:/resources/%s" % (PLUGIN_PREFIX, "background-art.png")
                MainThumb       = "%s/:/resources/%s" % (PLUGIN_PREFIX, "thumb-art.jpg")

        ZDFChannel = []

        ## Get the ZDF Page
        # Need to extract PW and ID for page access
        seite = sender
        split = seite.split('//')
        head = split[0]
        rest = split[1]
        split = rest.split(':')
        Username = split[0]
        rest = split[1]
        split = rest.split('@')
        Password = split[0]
        url2 = split[1]

        url = head+'//'+url2
        Log("(PLUG-IN) Try ZDF URL: %s" % (url))

        check = getURL(url, False)

        # Do we need to add the AUTHENTICATION header
        if check <> {None:None}:
                Log('(PLUG-IN) Needed Authentication ZDF-Top Page %s %s ' % (url,check[1]))
                # ElementFromURL(url, isHTML=False, values=None, headers={}, cacheTime=None, encoding="utf8", errors="strict"):
                ZDFpage = XML.ElementFromURL(url, isHTML=True, values=None, headers=check[1], cacheTime=None, encoding="utf8", errors="ignore")
        else:
                ZDFpage = XML.ElementFromURL(sender, True)

        # Select all the pre defined search pages (each page is FRAMED with "<a>...</a>"
        ZDFlist = ZDFpage.xpath('//a')

        # How many did we get?
        anzahl_seiten = len(ZDFlist)

        ZDFChannel = []
        # Get the URL, THUMB, and ALT description for each 'ZDF-Channel'
        for Seite in range(0,anzahl_seiten-1):

                SeitenSet = ZDFlist[Seite+1]

                # We have to TRY each attribute as not all stations have all attributes.
                try:
                        #Interesting that the GET function ONLY works on lowercase "tvid" even if the web-page uses uppercase "TVID"
                        URL = SeitenSet.get('href')
                except:
                        URL = ""

                try:
                        # The THUMB url (src) is in the next section <img> and thus we need to find this first before we can GET the src-info.
                        THUMB = SeitenSet.find('img').get('src')
                except:
                        THUMB = R("background-art.png")

                try:
                        # The description (alt) is in the next section <img> and thus we need to find this first before we can GET the src-info.
                        ALT = SeitenSet.find('img').get('alt')
                except:
                        try:
                                # Take care of the 'new' weekday selections
                                ALT = wochentag(URL)

                        except:
                                ALT = ""

                if ALT <> "":
                        ZDFChannel = ZDFChannel + [(URL,ALT,THUMB)]

        Log('(PLUG-IN) <==** EXIT Load FIRST Page ZDF Mediathek')

        return ZDFChannel

def ZDFStreams(channel):

        global FrontPage
        global SecondPage
        global ThirdPage

        global Protected
        global Username
        global Password
        global MainArt
        global MainThumb

        Log('(PLUG-IN) **==> ENTER Load VIDEOITEM Page ZDF Mediathek')

        if MainThumb == None:
                MainArt         = "%s/:/resources/%s" % (PLUGIN_PREFIX, "background-art.png")
                MainThumb       = "%s/:/resources/%s" % (PLUGIN_PREFIX, "thumb-art.jpg")

        # Test if we need ID - PW ... and get it
        check = getURL(channel, False)

        # Do we need to add the AUTHENTICATION header
        if check[1] <> {None:None}:
                Log('(PLUG-IN) Needed Authentication ZDFStreams')
                ZDFStream = XML.ElementFromURL(channel, isHTML=True, values=None, headers=check[1], cacheTime=None, encoding="Latin-1", errors="ignore")
        else:
                ZDFStream = XML.ElementFromURL(channel, isHTML=True, values=None, cacheTime=None, encoding="Latin-1", errors="ignore")

        ZDFStreamString = cleanHTML(urllib2.urlopen(check[0]).read())

        Title = ZDFStream.xpath('//tr[1]/th[1]/text()')

        streamlist = ZDFStream.xpath('//tr')
        anzahl_streams = len(streamlist)
        ThirdPage = []
        HeadLine = Title[0][2:]

        for stream in range(0,anzahl_streams-1):

                StreamSet = streamlist[stream]

                URL = StreamSet.xpath('//td[2]')[stream].find('a').get('href')
                DATE = StreamSet.xpath('//td[3]/text()')[stream]
                TITLE = StreamSet.xpath("//td[2]/a/text()")[stream]
                SUBTITLE = StreamSet.xpath('//td[5]/text()')[stream]
                DURATION = cleanstring(StreamSet.xpath('//td[4]/text()')[stream])
                DESCRIPTION = cleanHTML(cleanstring(ZDFStreamString.split('<!--	<td align="left" >')[stream+1].split('</a>')[0]))
                THUMB = StreamSet.xpath('//td[1]/img')[stream].get('src')
                if URL <> "":

                        ThirdPage = ThirdPage + [(URL, DATE, TITLE, SUBTITLE, DURATION, DESCRIPTION, THUMB)]

        #Find the NEXT page if any
        pagelist = ZDFStream.xpath('//a[@tvid]')
        anzahl_pageitems = len(pagelist)

        NextPage = []

        for page in range(0,anzahl_pageitems):
                PageSet = pagelist[page]

                URL = PageSet.get('href')
                TVID = PageSet.get('tvid')
                try:
                        THUMB = PageSet.find('img').get('src')

                except:
                        THUMB = R("background-art.png")

                NextPage = NextPage + [(URL, TVID, THUMB)]

        Log('(PLUG-IN) <==** EXIT Load VIDEOITEM Page ZDF Mediathek')

        return (HeadLine,ThirdPage, NextPage)

def TrailerStreams(channel):

        Log("(PLUG-IN) In: %s" % (Sendernamen[1]))

        global FrontPage
        global SecondPage
        global ThirdPage

        global Protected
        global Username
        global Password
        global MainArt
        global MainThumb

        Log('(PLUG-IN) **==> ENTER Load VIDEOITEM Page Trailers')

        if MainThumb == None:
                MainArt         = "%s/:/resources/%s" % (PLUGIN_PREFIX, "background-art.png")
                MainThumb       = "%s/:/resources/%s" % (PLUGIN_PREFIX, "thumb-art.jpg")

        # Test if we need ID - PW ... and get it
        check = getURL(channel, False)

        # Do we need to add the AUTHENTICATION header
        if check[1] <> {None:None}:
                Log('(PLUG-IN) Needed Authentication TrailerStreams')
                TrailerStreams = XML.ElementFromURL(channel, isHTML=True, values=None, headers=check[1], cacheTime=None, encoding="Latin-1", errors="ignore")
        else:
                TrailerStreams = XML.ElementFromURL(channel, isHTML=True, values=None, cacheTime=None, encoding="Latin-1", errors="strict")

        TrailerStreamString = cleanHTML(urllib2.urlopen(check[0]).read())

        Title = TrailerStreams.xpath('//h1/text()')

        HeadLine = Title

        streamlist = TrailerStreams.xpath('//*[@class]')

        anzahl_streams = len(streamlist)
        ThirdPagePart1 = []
        ThirdPage = []

        # This page is VERY badly composed ==> the normal XPATH does not work ... thus the 'strange' parsing
        for stream in range(0,anzahl_streams-1,2):

                TITLE =  streamlist[stream].text_content().encode('Latin-1')
                BIGDESCRIPTION = streamlist[stream+1].text_content().encode('Latin-1')
                DESCRIPTION = str.split(BIGDESCRIPTION, 'Im Kino: ')[0]
                DATETEXT = "Im Kino:"
                DATE = str.split(BIGDESCRIPTION, 'Im Kino: ')[1]

                ThirdPagePart1 = ThirdPagePart1 + [(TITLE, DESCRIPTION, DATETEXT, DATE)]

        streamlistURL = TrailerStreams.xpath('//*[@href]')

        anzahl_streams = len(streamlistURL)

        streamlistIMG = TrailerStreams.xpath('//*[@src]')

        anzahl_streams = len(streamlistIMG)

        for stream in range(0,9):

                StreamSetURL = streamlistURL[stream]
                StreamSetIMG = streamlistIMG[stream]

                TITLE, DESCRIPTION, DATETEXT, DATE = ThirdPagePart1[stream]

                URL = StreamSetURL.get('href')
                THUMB = StreamSetIMG.get('src')

                if URL <> "":

                        ThirdPage = ThirdPage + [(URL, DATETEXT, DATE, TITLE, DESCRIPTION, THUMB)]

        #Find the NEXT page if any
        pagelist = TrailerStreams.xpath('//a[@tvid]')
        anzahl_pageitems = len(pagelist)

        NextPage = []

        for page in range(0,anzahl_pageitems):

                PageSet = pagelist[page]

                URL = PageSet.get('href')
                TVID = PageSet.get('tvid')
                try:
                        THUMB = PageSet.find('img').get('src')

                except:
                        THUMB = R("background-art.png")

                NextPage = NextPage + [(URL, TVID, THUMB)]

        Log('(PLUG-IN) <==** EXIT Load VIDEOITEM Page Trailer Mediathek')

        return (HeadLine,ThirdPage, NextPage)

def ArteStreams(channel):

        Log("(PLUG-IN) In: %s" % (Sendernamen[9]))

        global FrontPage
        global SecondPage
        global ThirdPage

        global Protected
        global Username
        global Password
        global MainArt
        global MainThumb

        Log('(PLUG-IN) **==> ENTER Load VIDEOITEM Page ARTE')

        if MainThumb == None:
                MainArt         = "%s/:/resources/%s" % (PLUGIN_PREFIX, "background-art.png")
                MainThumb       = "%s/:/resources/%s" % (PLUGIN_PREFIX, "thumb-art.jpg")

        # Test if we need ID - PW ... and get it
        check = getURL(channel, False)

        # Do we need to add the AUTHENTICATION header
        if check[1] <> {None:None}:
                Log('(PLUG-IN) Needed Authentication ArteStreams')
                ArteStreams = XML.ElementFromURL(channel, isHTML=True, values=None, headers=check[1], cacheTime=None, encoding="Latin-1", errors="ignore")
        else:
                ArteStreams = XML.ElementFromURL(channel, isHTML=True, values=None, cacheTime=None, encoding="Latin-1", errors="strict")

        ArteStreamString = cleanHTML(urllib2.urlopen(check[0]).read())

        Title = ARTEStreams.xpath('//title/text()')[0]
        THUMB = ARTEStreams.xpath('//body/font/img')[0].get('src')
        Subtitle = str(ARTEStreams.xpath('//body/font/font/text()')[0])

        streamlistdescription = GetValues("<!--online bis<br>",ARTEStreamsString) #How Long is it ONLINE ?
        streamlisttitle = ARTEStreams.xpath('//*[@class="item_title"]') #Titles 10 streams in .text()
        streamlistthumbs =  GetValues("src=",ARTEStreamsString) # The THUMB URLs
        streamlisturl = GetValues("<a href=",ARTEStreamsString) #Finding the stream URLs

        HeadLine = Title

        anzahl_streams = len(streamlisttitle)
        ThirdPage = []
        ThirdPagePart1 = []

        # This page is VERY badly composed ==> the normal XPATH does not work ... thus the 'strange' parsing
        for stream in range(0,anzahl_streams):

                StreamSetURL = streamlisturl[stream+1]
                StreamSetIMG = streamlistthumbs[stream+2]
                StreamSetTitle = streamlisttitle[stream]
                StreamSetDescription = streamlistdescription[stream+1]

                try:
                        TITLE = StreamSetTitle.text_content().encode('Latin-1').decode('utf-8')
                except:
                        TITLE = "T"
                        Log(TITLE)
                        #Log(StreamSetTitle.text_content())
                        Log(type(StreamSetTitle.text_content()))
                        Log(StreamSetTitle.text_content().encode('Latin-1'))

                #Log(TITLE)
                try:
                        URL = StreamSetURL #StreamSetURL.get('href')
                except:
                        URL = None
                #Log(URL)
                try:
                        THUMB = StreamSetIMG #.text_content().encode('Latin-1')
                except:
                        THUMB =" "
                #Log(THUMB)
                try:
                        Subtitle = StreamSetDescription #.text_content().encode('Latin-1')
                        try:
                                Subtitle = "Online bis: " + Subtitle.split('--')[0].split('T')[0] + "   " + Subtitle.split('--')[0].split('T')[1]
                        except:
                                Subtitle = "S"
                except:
                        Subtitle = "S"

                if URL <> "":

                        ThirdPage = ThirdPage + [(TITLE, Subtitle, THUMB, ARTE_URL + URL, wer)]

        # Add any NAVIGATION pages if nessesary
        # Get the items for the FRONT page ... all WEB-PAGES & Thumbs
        if len(FrontPage) == 0:
                FrontPage = LoadFP()

        #Find the NEXT page if any
        pagelist = ARTEStreams.xpath('//a[@tvid] ')
        anzahl_pageitems = len(pagelist)

        NextPage = []

        for page in range(0,anzahl_pageitems):

                PageSet = pagelist[page]

                URL = PageSet.get('href')
                TVID = PageSet.get('tvid')
                try:
                        THUMB = PageSet.find('img').get('src')
                        THUMB = ROOT_URL + THUMB.split('..')[1]

                except:
                        THUMB = R("background-art.png")

                NextPage = NextPage + [(URL, TVID, THUMB)]

        Log('(PLUG-IN) <==** EXIT Load VIDEOITEM Page Arte Mediathek')

        return (HeadLine,ThirdPage, NextPage)

def PlayArteVideo(sender, url, papa, alt, thumb):

        global FrontPage
        global SecondPage
        global ThirdPage
        global MainArt
        global MainThumb
        global SecondSelection
        global SecondSelectionLogo

        Log('(PLUG-IN) **==> ENTER: Play Arte Video')

        if MainThumb == None:
                MainArt         = "%s/:/resources/%s" % (PLUGIN_PREFIX, "background-art.png")
                MainThumb       = "%s/:/resources/%s" % (PLUGIN_PREFIX, "thumb-art.jpg")

        # Get the items for the FRONT page ... all WEB-PAGES & Thumbs
        if len(FrontPage) == 0:
                FrontPage = LoadFP()

        URL = url
        ALT = alt
        THUMB = thumb
        SenderTHUMB = thumb

        # Who did call us ... what was selected on Arte Video List list
        TopLevel = papa
        SecondLevel = url
        Section = sender.itemTitle
        SectionTitel = Section.title()

        # Test if we need ID - PW ... and get it
        check = getURL(URL, False)

        # Do we need to add the AUTHENTICATION header
        if check[1] <> {None:None}:
                Log('(PLUG-IN) Needed Authentication ArteStreams')
                ArteStreams = XML.ElementFromURL(URL, isHTML=True, values=None, headers=check[1], cacheTime=None, encoding="Latin-1", errors="ignore")
        else:
                ArteStreams = XML.ElementFromURL(URL, isHTML=True, values=None, cacheTime=None, encoding="Latin-1", errors="strict")

        ArteStreamString = cleanHTML(urllib2.urlopen(check[0]).read())

        Title = ArteStreams.xpath('//h1')[0].text_content().encode('Latin-1').decode('utf-8')

        THUMB = ArteStreams.xpath('//img')[1].get('src')

        Subtitle = Title #str(ARTEStreams.xpath('//body/font/font/text()')[0])

        dir = MediaContainer(art = SenderTHUMB, title1 = TopLevel, title2 = Title, viewGroup = "Info")

        streamlistdescription = ArteStreams.xpath('//*[@class="item_description"]')[0].text_content().encode('Latin-1').decode('utf-8')  #.text_content()  #[0].split('<br ')[0] #How Long is it ONLINE ?
        streamlist =  GetValues("href=",ArteStreamString) # The Stream URLs
        Low = streamlist[1].split(' VOD')[0].replace('rtsp','http')
	ML(Low)
        High = streamlist[2].split(' VOD')[0].replace('rtsp','http')

         # VideoItem(self, key, title, subtitle=None, summary=None, duration=None, thumb=None, art=None, **kwargs):
        # The foolowing code can be used if we want a BIG list of all the streams and SINGLE click to have them started.

        #dir.Append(VideoItem(   High,
                                #Title + " (720p)",
                                #subtitle = "HIGH Quality (720p)",
                                #summary = streamlistdescription, #.encode('Latin-1'),
                                #duration = None,
                                #thumb = THUMB,
                                #art = MainArt
                                #)
                   #)

	#class WindowsMediaVideoItem(WebVideoItem):
	#def __init__(self, url, width=720, height=576, title=None, subtitle=None, summary=None, duration=None, thumb=None, art=None, **kwargs):
	#688&height=384
	dir.Append(WindowsMediaVideoItem(url      = High,
					 width    = 688,
					 height   = 384,
					 title    = Title + " (720p)",
					 subtitle = "HIGH Quality (720p)",
					 summary  = streamlistdescription, #.encode('Latin-1'),
					 duration = None,
					 thumb    = THUMB,
					 art      = MainArt
					 )
		   )

        #dir.Append(VideoItem(   Low,
                                #Title +' (SD)',
                                #subtitle = "LOW Quality (SD)",
                                #summary = streamlistdescription, #.encode('Latin-1'),
                                #duration = None,
                                #thumb = THUMB,
                                #art = MainArt
                                #)
                   #)

	dir.Append(WindowsMediaVideoItem(url      = Low,
					 width    = 688,
					 height   = 384,
					 title    = Title + " (SD)",
					 subtitle = "LOW Quality (SD)",
					 summary  = streamlistdescription, #.encode('Latin-1'),
					 duration = None,
					 thumb    = THUMB,
					 art      = MainArt
					 )
		   )

        return dir

def ARD(sender):

        global Protected
        global Username
        global Password

        global MainArt
        global MainThumb

        Log('(PLUG-IN) **==> ENTER Load FIRST Page ARD Mediathek')

        if MainThumb == None:
                MainArt         = "%s/:/resources/%s" % (PLUGIN_PREFIX, "background-art.png")
                MainThumb       = "%s/:/resources/%s" % (PLUGIN_PREFIX, "thumb-art.jpg")

        ARDChannel = []


        # Test if we need ID - PW ... and get it
        check = getURL(ARD_URL, False)
        #Log(check)

        # Do we need to add the AUTHENTICATION header
        if check[1] <> {None:None}:
                Log('(PLUG-IN) Needed Authentication ARDStreams')
                ARDStreams = XML.ElementFromURL(ARD_URL, isHTML=True, values=None, headers=check[1], cacheTime=None, encoding="Latin-1", errors="ignore")
        else:
                ARDStreams = XML.ElementFromURL(ARD_URL, isHTML=True, values=None,  cacheTime=None, encoding="Latin-1", errors="ignore")

        ARDStreamsString = cleanHTML(urllib2.urlopen(check[0]).read())

        Title = ARDStreams.xpath('//h1/text()')[0]
        THUMB = GetValues('src=',ARDStreamsString)[1].split()[0]
        SenderTHUMB = ARD_URL + THUMB
        Subtitle = None

        #Log('*************** %s %s' % (Title, THUMB))

        # Select all the pre defined search pages (each page is FRAMED with "<a>...</a>"
        ARDlist = GetValues('href=',ARDStreamsString,'</a>') #How Long is it ONLINE ?

        # How many did we get?
        anzahl_seiten = len(ARDlist)
        #Log('*************** %s' % anzahl_seiten)

        ARDChannel = []
        # Get the URL, THUMB, and ALT description for each 'ARD-Channel'
        for Seite in range(1,anzahl_seiten-3):

                SeitenSet = ARDlist[Seite].replace('"','').split('>')

                # We have to TRY each attribute as not all stations have all attributes.
                try:
                        #Interesting that the GET function ONLY works on lowercase "tvid" even if the web-page uses uppercase "TVID"
                        URL = SeitenSet[0]
                        #Log('*************** %s' % URL)
                except:
                        URL = ""

                try:
                        # The THUMB url (src) is in the next section <img> and thus we need to find this first before we can GET the src-info.
                        THUMB = SenderTHUMB
                except:
                        THUMB = R("background-art.png")

                try:
                        # The description (alt) is in the next section <img> and thus we need to find this first before we can GET the src-info.
                        ALT = SeitenSet[1].decode('Latin-1')
                        #Log(ALT)
                except:
                        ALT = "Wie Bitte?"

                if ALT <> "":
                        #Log("""***************
                        #URL: %s
                        #ALT: %s
                        #THUMB: %s
                        #""" % (URL, ALT, THUMB))

                        ARDChannel = ARDChannel + [(URL,ALT,THUMB)]

        Log('(PLUG-IN) <==** EXIT Load FIRST Page ARD Mediathek')

        return ARDChannel

def ARDStreams(channel):

        global FrontPage
        global SecondPage
        global ThirdPage

        global Protected
        global Username
        global Password
        global MainArt
        global MainThumb

        Log('(PLUG-IN) **==> ENTER Load VIDEOITEM Page ARD Mediathek')

        if MainThumb == None:
                MainArt         = "%s/:/resources/%s" % (PLUGIN_PREFIX, "background-art.png")
                MainThumb       = "%s/:/resources/%s" % (PLUGIN_PREFIX, "thumb-art.jpg")

        # Test if we need ID - PW ... and get it
        check = getURL(channel, False)

        # Do we need to add the AUTHENTICATION header
        if check[1] <> {None:None}:
                Log('(PLUG-IN) Needed Authentication ARDStreams')
                ARDStream = XML.ElementFromURL(channel, isHTML=True, values=None, headers=check[1], cacheTime=None, encoding="Latin-1", errors="ignore")
        else:
                ARDStream = XML.ElementFromURL(channel, isHTML=True, values=None, cacheTime=None, encoding="Latin-1", errors="ignore")

        ARDStreamString = cleanHTML(urllib2.urlopen(check[0]).read())

        Title = ARDStream.xpath('//h2')

        streamlistURL = ARDStream.xpath('//a')
        streamlistIMG = ARDStream.xpath('//img')
        streamlistDES = GetValues('</a> <br>',ARDStreamString)
        streamlistDATE = GetValues('<br>',ARDStreamString)
        if channel.find('idx=') >=1:
                anzahl_streams = len(streamlistURL)-3
        else:
                anzahl_streams = len(streamlistURL)-2
        ThirdPage = []
        HeadLine = Title[0].text_content()  #[2:]

        for stream in range(0,anzahl_streams):

                StreamSetURL = streamlistURL[stream]
                StreamSetIMG = streamlistIMG[stream]

                try:
                        StreamSetDES = streamlistDES[stream+1]
                except:
                        StreamSetURL = ""

                zaehler = stream

                try:
                        StreamSetDATE = streamlistDATE[(zaehler+1)*2]
                except:
                        StreamSetURL = ""

                #Log(zaehler)

                if StreamSetURL <> "":
                        URL = StreamSetURL.get('href')
                        THUMB = StreamSetIMG.get('src') #.text_content() #.get('src')
                        DESCRIPTION = StreamSetDES.split('<br')[0].strip().decode('Latin-1').encode('utf-8')
                        DATE = StreamSetDATE.split(' | ')[0]
                        DURATION = StreamSetDATE.split(' | ')[1].split('min')[0]
                        if URL <> "":

                                ThirdPage = ThirdPage + [(URL, DATE, DURATION, DESCRIPTION, THUMB)]

        #Find the NEXT page if any
        pagelist = ARDStream.xpath('//a[@tvid]')
        anzahl_pageitems = len(pagelist)

        NextPage = []

        for page in range(0,anzahl_pageitems):
                PageSet = pagelist[page]

                URL = PageSet.get('href')
                TVID = PageSet.get('tvid')
                try:
                        THUMB = PageSet.find('img').get('src')

                except:
                        THUMB = R("background-art.png")

                NextPage = NextPage + [(URL, TVID, THUMB)]

        Log('(PLUG-IN) <==** EXIT Load VIDEOITEM Page ARD Mediathek')

        return (HeadLine,ThirdPage, NextPage)


#############################################
#Utility Functions
#############################################


def getURL(URL, InstallDefault = False ):

# This function tries to get ID / PW from supplied URLs
# If needed it can also set the DEFAULT handler with these credentials
# making successive calls with no need to specify ID-PW

        global Protected
        global Username
        global Password

        Log('(PLUG-IN) **==> ENTER getURL')

        HEADER = {None:None}

        req = urllib2.Request(URL)

        try:
                Log('(PLUG-IN) Try URL: %s %s' % (URL,req))
                handle = urllib2.urlopen(req)

        except IOError, e:
                # here we *want* to fail
                pass
        else:
                # If we don't fail then the page isn't protected
                Protected = "No"
                Log('(PLUG-IN) URL is NOT protected')
                return (URL,HEADER)

        if not hasattr(e, 'code') or e.code != 401:
                # we got an error - but not a 401 error
                Log("(PLUG-IN) This page isn't protected by authentication.")
                Log('(PLUG-IN) But we failed for another reason. %s' % (e.code))
                return (None, None)

        authline = e.headers['www-authenticate']
        # this gets the www-authenticate line from the headers
        # which has the authentication scheme and realm in it

        authobj = re.compile(
                r'''(?:\s*www-authenticate\s*:)?\s*(\w*)\s+realm=['"]([^'"]+)['"]''',
                re.IGNORECASE)
        # this regular expression is used to extract scheme and realm
        matchobj = authobj.match(authline)

        if not matchobj:
                # if the authline isn't matched by the regular expression
                # then something is wrong
                Log('(PLUG-IN) The authentication header is badly formed.')
                Log('(PLUG-IN) Authline: %s' % (authline))
                Protected = "Yes"
                return None

        scheme = matchobj.group(1)
        REALM = matchobj.group(2)
        # here we've extracted the scheme
        # and the realm from the header
        if scheme.lower() != 'basic':
                Log('(PLUG-IN) This function only works with BASIC authentication.')
                Protected = "Yes"
                return None

        if InstallDefault:

                # Create an OpenerDirector with support for Basic HTTP Authentication...
                auth_handler = urllib2.HTTPBasicAuthHandler()
                auth_handler.add_password(realm=REALM,
                                          uri=URL,
                                          user=Username,
                                          passwd=Password)
                opener = urllib2.build_opener(auth_handler)
                # ...and install it globally so it can be used with urlopen.
                urllib2.install_opener(opener)

                # All OK :-)
                Protected = "Yes"
                Log('(PLUG-IN) ### Alles Ready ! via default Opener###')
                return (URL, HEADER)

        base64string = base64.encodestring('%s:%s' % (Username, Password))[:-1]
        authheader = "Basic %s" % base64string
        req.add_header("Authorization", authheader)
        HEADER = {"Authorization": authheader}

        try:
                handle = urllib2.urlopen(req)
        except IOError, e:
                # here we shouldn't fail if the username/password is right
                Log("(PLUG-IN) It looks like the username or password is wrong.")
                Protected = "Yes"
                return None

        # All OK :-)
        Protected = "Yes"

        Log('(PLUG-IN) <==** EXIT getURL')
        return (req,HEADER)

def wochentag(urldate):
# Exctract DATE from Video Item

        split = urldate.split('=')
        wd = split[1]

        if wd == "http://www.compiz.de/":

                wd = ""

        return wd

def fixURL(url):
# This will ENCODE an url to get rid of e.g. spaces in between.

        try:
                tempstr = RIGHT[0].split(':')
                url = tempstr[0] + ':' + urllib.quote(tempstr[1])

                return url
        except:
                return urllib.quote(url)

def cleanstring(mystr):

        str=mystr.replace("\\n", " ")
        while str.find("  ")>=0:
                str=str.replace("  ", " ")
        if str.startswith(" "):
                str=str[1:]
        if str.endswith(" "):
                str=str[:-1]
        return str

def cleanGerman(mystr, decodec = 'utf-8', encodec = 'Latin-1'):
# This is an attempt to get rid of " &auml; " etc within a string
# Still working on it ... any help appreicated.

        if encodec <> None:
                mystr = mystr.encode(encodec)
        Log('******%s' % mystr)

        mystr = mystr.replace('&auml;',"ä") # öüß
        mystr = mystr.replace('&ouml;',"ö") # ß
        mystr = mystr.replace('&uuml;',"ü") # öü
        mystr = mystr.replace('&szlig;',"ß") # öüß
        mystr = mystr.replace('&Auml;',"Ä") # öüß
        mystr = mystr.replace('&Ouml;',"Ö") # ß
        mystr = mystr.replace('&Uuml;',"Ü") # öü
        mystr = mystr.replace('&#034;','"') # öüß
        mystr = mystr.replace('\u00E9','é')
        mystr = mystr.replace('&#039;',"'") # öüß
        mystr = mystr.replace('&amp;','&')

        if decodec <> None:
                mystr = mystr.decode(decodec)
        #Log('******%s' % mystr)
        return mystr

def cleanHTML(text, skipchars=[], extra_careful=1):
# This is an attempt to get rid of " &auml; " etc within a string
# Still working on it ... any help appreicated.

        entitydefs_inverted = {}

        for k,v in entitydefs.items():
                entitydefs_inverted[v] = k

        _badchars_regex = re.compile('|'.join(entitydefs.values()))
        _been_fixed_regex = re.compile('&\w+;|&#[0-9]+;')

        # if extra_careful we don't attempt to do anything to
        # the string if it might have been converted already.
        if extra_careful and _been_fixed_regex.findall(text):
                return text

        if type(skipchars) == type('s'):
                skipchars = [skipchars]

        keyholder= {}
        for x in _badchars_regex.findall(text):
                if x not in skipchars:
                        keyholder[x] = 1
        text = text.replace('&','&amp;')
        text = text.replace('\x80', '&#8364;')
        for each in keyholder.keys():
                if each == '&':
                        continue

                better = entitydefs_inverted[each]
                if not better.startswith('&#'):
                        better = '&%s;'%entitydefs_inverted[each]

                text = text.replace(each, better)
        return text

def DurationToInt(mystr):
# This converts "00:00" to an INT with 1000ths of seconds for PLEX

        Duration = 0
        sekunden = 0
        minuten = 0
        stunden = 0
        tage = 0

        Multiplier = 1000

        # Transform a time string of "xx:xx:xx" format into a INT showing miliseconds
        str=mystr.split(':')
        try:
                sekunden = str.pop()

                #Log('(PLUG-IN) Sekunden: %s INT: %d' % (sekunden, int(sekunden)))
        except:
                Duration = 0
                return Duration

        try:
                minuten = str.pop()
                #Log('(PLUG-IN) minuten: %s INT: %d' % (minuten, int(minuten)))

        except:
                Duration = int(sekunden)  * Multiplier
                return Duration

        try:
                stunden = str.pop()
                #Log('(PLUG-IN) stunden: %s INT: %d' % (stunden, int(stunden)))

        except:
                Duration = int(minuten) * 60 * Multiplier + int(sekunden)  * Multiplier
                return Duration

        try:
                tage = str.pop()
                #Log('(PLUG-IN) tage: %s INT: %d' % (tage, int(tage)))
        except:
                Duration = int(stunden) * 60 * 60 * Multiplier + int(minuten) * 60 * Multiplier + int(sekunden)  * Multiplier
                return Duration

        Duration = int(tage) * 24 *60 * 60 * Multiplier + int(stunden) * 60 * 60 * Multiplier + int(minuten) * 60 * Multiplier + int(sekunden)  * Multiplier
        return Duration

def GetValues(key, doc, ende = None):
        #Look for values within a document and returns a LIST of items

        inhalt = []

        temp = doc.split(key)

        anzahl = len(temp)
        #Log('************************* %s %s' % (key,anzahl))

        for item in range(0,anzahl):

                try:
                        if ende == None:
                                ende = '>'

                        value = temp[item].split(ende)[0]

                        inhalt = inhalt + [value] #.append(value)
                        #Log('******* %s' % value)

                except:
                        Log('None')
                        None

        tag = inhalt
        #Log('LAST Value %s' % value)
        #Log(item)
        #Log(temp[item])
        #Log(temp[item])

        return  inhalt

def ML(Target):

	Log('***********************************************')
	temp = Target
	try:
		temp = tostring(temp)

	except:
		temp = temp

	try:
		Log('TYPE: %s' % type(temp))
	except:
		Log('TYPE: Error')

	try:
		Log('LEN: %d' %len(temp))
	except:
		Log('LEN: Error')

	try:
		Log('CONTENT: %s' % temp)
	except:
		Log('CONTENT: Error')

	Log('***********************************************')

	return
