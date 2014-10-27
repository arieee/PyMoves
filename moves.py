#!/Usr/bin/env python
# -*- coding:utf-8 -*-

# A python class for easy access to the Moves App data. Created by Joost Plattel [http://github.com/jplattel]

import requests
import pprint
import datetime
import sys
from collections import defaultdict

# At first, we should execute this func to complete authorization
def authorization():
        m = Moves()

        print "AUTHORIZATION"
        print "reqeust url for get access token"
        print "At first you access the URL, input PIN code and then get code from redirect URL"
        print m.request_url()

        print "get access token"
        tempCode = u"" # INPUT code got by above redirect URL
        if tempCode: print m.auth(tempCode) # After you get tempCode, get access_token and write it on USERINFO


def test(date = datetime.datetime.today().strftime("%Y%m%d")):
        m = Moves()

        pp = pprint.PrettyPrinter()
 
        print "\n\n#CONFIRM JSON DATA STURACTURE OF MOVES API#"
        print "\nget summary"
        pp.pprint(m.get_summary(date))

        print "\nget profile"
        pp.pprint(m.get_profile())

        print "\nget activity"
        pp.pprint(m.get_activity(date))

        print "\nget places"
        pp.pprint(m.get_places(date))
 
        print "\n\nMY CODE TEST"
        print "differenceSec func TEST"
        print differenceSec("20140509T234025+0900","20140511T024025+0900","20140510")

        print "\nPlace class TEST"
        p = Place(date)
        print "\ngetPlaceSec method (home) TEST"
        print p.getPlaceSec("home"),p.getPlaceSec("home")/60,p.getPlaceSec("home")/60/60
        print "\ngetPlaceSec method (lab) TEST"
        print p.getPlaceSec("lab"),p.getPlaceSec("lab")/60,p.getPlaceSec("lab")/60/60
        print "\ngetPlaceSec method (office) TEST"
        print p.getPlaceSec("office"),p.getPlaceSec("office")/60,p.getPlaceSec("office")/60/60
        
        print "\nSummary class TEST"
        s = Summary(date)
        print "\ngetActivitySec (transport) method TEST"
        print s.getActivitySec("transport")
        print "\ngetActivitySec (walking) method TEST"
        print s.getActivitySec("walking")
        print "\ngetActivitySec (running) method TEST"
        print s.getActivitySec("running")
        print "\ngetActivityMeter (running) method TEST"
        print s.getActivityMeter("running")

        print "\nfetchAllData TEST"
        print 'startTime="20141020",endTime="20141022"'
        print "date\thomeS\tlabS\tofficeS\ttransS\twalkS\trunS\ttsM\twalkM\trunM"
        fetchAllData(startTime="20141020",endTime="20141022")

# func for fething all data
def fetchAllData(startTime=None,endTime=None):
        m = Moves()
        
        if not startTime:
                startTime = m.get_profile[u"profile"][u"firstDate"].encode("utf8")
        if not endTime:
                endTime = datetime.datetime.today().strfitme("%Y%m%d")

        startDateTime = datetime.datetime.strptime(startTime,"%Y%m%d")
        endDateTime = datetime.datetime.strptime(endTime,"%Y%m%d")



        for plusDays in range((endDateTime-startDateTime).days):
                date = (startDateTime + datetime.timedelta(days=plusDays)).strftime("%Y%m%d")

                p = Place(date)
                placeOutput = [p.getPlaceSec(pName) for pName in ["home","lab","office"]]
        
                s = Summary(date)
                activitySecOutput = [s.getActivitySec(aName) for aName in ["transport","walking","running"]]
                activityMeterOutput = [s.getActivityMeter(aName) for aName in ["transport","walking","running"]]

                print "\t".join(map(str,[date] + placeOutput + activitySecOutput + activityMeterOutput))


# func for calcurating diffrence total seconds
def differenceSec(startTime,endTime,date):
        endTime = datetime.datetime.strptime(endTime,"%Y%m%dT%H%M%S+0900")
        startTime = datetime.datetime.strptime(startTime,"%Y%m%dT%H%M%S+0900")
        todaybegin = datetime.datetime.strptime(date,"%Y%m%d")
        tomorrowbegin = todaybegin + datetime.timedelta(days=1)
        if todaybegin > startTime:
                startTime = todaybegin
        if todaybegin + datetime.timedelta(days=1) < endTime:
                endTime = tomorrowbegin
        diff = endTime - startTime
        return diff.total_seconds()


class Summary:
        def __init__(self,date):
                m = Moves()
                summary_json = m.get_summary(date)
                self.date = summary_json[0][u'date']
                self.timehash = dict()
                self.dishash = dict()
                try:
                        for s in summary_json[0][u'summary']:
                                #print s
                                activity = s[u'activity']
                                duration = s[u'duration']
                                distance = s[u'distance']
                                self.timehash[activity] = duration
                                self.dishash[activity] = distance
                except:
                        pass

        def getActivitySec(self,activityName):
                if activityName in self.timehash:
                        return self.timehash[activityName]
                else:
                        return 0.0

        def getActivityMeter(self,activityName):
                if activityName in self.dishash:
                        return self.dishash[activityName]
                else:
                        return 0.0
                        

class Place:
        def __init__(self,date):
                m = Moves()
                places_json = m.get_places(date)
                self.timehash = dict()
                self.date = places_json[0][u'date']
                for p in places_json[0][u'segments']:
                        start = p[u'startTime']
                        end = p[u'endTime']
                        duration = differenceSec(start,end,self.date)
                        placeid = int(p[u'place'][u'id'])
                        
                        if placeid in self.timehash:
                                self.timehash[placeid] += duration
                        else:
                                self.timehash[placeid] = duration

                # relation dic placeName(ex.your home or your office) and ID (annotated by Moves)
                # you should make "PLACEINFO.tsv" forward
                self.placeIDdic = defaultdict(list)
                with open("PLACEINFO.tsv") as f:
                        for line in f:
                                placeName,ID = line.strip().split("\t")
                                self.placeIDdic[placeName].append(int(ID))

        def getPlaceSec(self,placeName):
                placeIDlist = self.placeIDdic[placeName]
                placeTime = 0.0
                for placeID in placeIDlist:
                        if placeID in self.timehash:
                                placeTime += self.timehash[placeID]
                return placeTime

# the basic class 
class Moves:
	def __init__(self):
                client_id,client_secret,redirect_url,oauth_url,api_base_url,access_token = open("USERINFO.tsv","r").read().strip().split("\n")
                self.client_id = client_id	   # Client ID, get this by creating an app
                self.client_secret = client_secret # Client Secret, get this by creating an app
                self.redirect_url = redirect_url  # Callback URL for getting an access token
                self.oauth_url = oauth_url
                self.api_base_url = api_base_url
                self.access_token = access_token

	# Generate an request URL
	def request_url(self):
		u = 'https://api.moves-app.com/oauth/v1/authorize?response_type=code'
		c = '&client_id=' + self.client_id
		s = '&scope=' + 'activity location' # Assuming we want both activity and locations
		url = u + c + s 
		return url # Open this URL for the PIN, then authenticate with it and it will redirect you to the callback URL with a request-code, specified in the API access.

	# Get access_token 
	def auth(self, request_token):
		c = '&client_id=' + self.client_id
		r = '&redirect_uri=' + self.redirect_url
		s = '&client_secret=' + self.client_secret
                url = self.oauth_url +'access_token?grant_type=authorization_code&code=' + request_token + c + s + r
		j = requests.post(url)
                print j.text
		token = j.json()['access_token']
		return token 
		
	# Standard GET and profile requests

	# Base request
	def get(self, endpoint):
		token = '?access_token=' + self.access_token
		return requests.get(self.api_url + endpoint + token).json()

	# /user/profile
	def get_profile(self):
		token = '?access_token=' + self.access_token
		root = '/user/profile'
		#return requests.get(self.api_url + root + token).json()
                return requests.get(self.api_base_url + root + token).json()

	# Summary requests

	# /user/summary/daily/<date>
	# /user/summary/daily/<week>
	# /user/summary/daily/<month>
	def get_summary(self, date):
		token = '?access_token=' + self.access_token
		return requests.get(self.api_base_url + '/user/summary/daily/' + date + token).json()

        # Activity requests
        # /user/activities/daily/<date>
        def get_activity(self, date):
                token = '?access_token=' + self.access_token
                return requests.get(self.api_base_url + '/user/activities/daily/' + date + token).json()

        # Places requests
        # /user/places/daily/<date>
        def get_places(self,date):
                token = '?access_token=' + self.access_token
                return requests.get(self.api_base_url + '/user/places/daily/' + date + token).json()

	# Range requests, max range of 7 days!

	# /user/summary/daily?from=<start>&to=<end>
	# /user/activities/daily?from=<start>&to=<end>
	# /user/places/daily?from=<start>&to=<end>
	# /user/storyline/daily?from=<start>&to=<end>
	def get_range(self, endpoint, start, end):
		export = requests.get(self.access_token, endpoint + '?from=' + start + '&to=' + end).json()
		return export


if __name__ == "__main__":
        #autorization()
        if len(sys.argv) > 1:
                date = sys.argv[1]
                test(date)
        else:
                test()

