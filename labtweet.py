#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tweepy_basic
import moves
import datetime,os,sys

def maketweet(date=None):
    api = tweepy_basic.setup()
    if date == None:
        today = datetime.datetime.today().strftime("%Y%m%d")
        date = today
    p = moves.Place(date)
    labtime = p.getPlaceSec("lab")
    tweet = "@arieee0 {}のラボ滞在時間は{:.0f}時間{:.0f}分です".format(date[4:6]+"/"+date[6:8],labtime/60/60,labtime - (int(labtime)/60)*60)
    if int(labtime) == 0:
        tweet += " 明日はラボに行きましょう"
    elif int(labtime) < 60*60*3:
        tweet += " 何しに行ったんでしょうか…"
    elif int(labtime) < 60*60*12:
        tweet += " 研究は進みましたか？"
    else:
        tweet += " まさかラボに泊まってないですよね？"
    api.update_status(tweet)
    print "Made tweet:{}".format(tweet)

if __name__ == "__main__":
    os.chdir('/home/ysuzuki/MyApplication/movesapp')
    if len(sys.argv) > 1:
        date = sys.argv[1]
        maketweet(date)
    else:
        maketweet()
    #maketweet("20140508")
