#! /usr/bin/env python

# Requires feedparser, icalendar, pytz

import sys
from datetime import datetime
try:
    import feedparser
    from pytz import timezone
    from icalendar import Calendar, Event
except:
    print "Please make sure you have installed the following modules:"
    print "Feedparser \t http://pypi.python.org/pypi/feedparser/"
    print "Pytz \t\t http://pypi.python.org/pypi/pytz/"
    print "iCalendar \t http://pypi.python.org/pypi/icalendar/"
    raise
    sys.exit(0)

calName = "calendars/menuRU.ics"
print "Exporting calendar: "+calName

# CROUS restaurants: http://www.crous-grenoble.fr/article-27-mg-3-mh-25-ms-1-menu-de-la-semaine.htm
chautagne = "http://www.crous-grenoble.fr/rss-menu-7.htm"

cal = Calendar()

menuRSS = feedparser.parse(chautagne)
for item in menuRSS["entries"]:
    title = item["title_detail"]["value"].split()
    jour = title[0]
    service = title[1]
    date = datetime.strptime(title[2], "%d/%m/%Y")
    item["summary_detail"]["value"] = item["summary_detail"]["value"].replace('<br />\n', '\\n')

    ev = Event()

    if not ((jour=="Vendredi" and service=="soir") or jour=="Samedi" or jour=="Dimanche"):
        ev.add('summary', 'menu RU')
        if service == "midi":
            ev.add('dtstart', datetime(date.year,date.month,date.day,11,30,0,tzinfo=timezone("Europe/Paris")))
            ev.add('dtend', datetime(date.year,date.month,date.day,13,0,0,tzinfo=timezone("Europe/Paris")))
        elif service == "soir":
            ev.add('dtstart', datetime(date.year,date.month,date.day,18,30,0,tzinfo=timezone("Europe/Paris")))
            ev.add('dtend', datetime(date.year,date.month,date.day,20,0,0,tzinfo=timezone("Europe/Paris")))

        ev.add('description', item["summary_detail"]["value"])
        cal.add_component(ev)

f = open(calName, 'wb')
f.write(cal.to_ical())
f.close()

print "Done!"
