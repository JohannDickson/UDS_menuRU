# Requires feedparser, icalendar, pytz

import feedparser, pytz, logging
from icalendar import Calendar, Event
from datetime import datetime

logfile = "logs/menuRU.log"
calName = "calendars/menuRU.ics"

logging.basicConfig(filename=logfile,level=logging.INFO) # level can be 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
logging.info("-----")
logging.info(datetime.now())
logging.info("Fetching this week's menu")

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
    
    logging.debug(item["title_detail"]["value"])
    logging.debug("---")
    logging.debug(item["summary_detail"]["value"])
    logging.debug("-----------------------------\r\n")

    ev = Event()

    if not ((jour=="Vendredi" and service=="soir") or jour=="Samedi" or jour=="Dimanche"):
        if service == "midi":
            ev.add('summary', 'menu RU')
            ev.add('dtstart', datetime(date.year,date.month,date.day,11,30,0,tzinfo=pytz.timezone("Europe/Paris")))
            ev.add('dtend', datetime(date.year,date.month,date.day,13,0,0,tzinfo=pytz.timezone("Europe/Paris")))
        elif service == "soir":
            ev.add('summary', 'menu RU')
            ev.add('dtstart', datetime(date.year,date.month,date.day,19,15,0,tzinfo=pytz.timezone("Europe/Paris")))
            ev.add('dtend', datetime(date.year,date.month,date.day,20,0,0,tzinfo=pytz.timezone("Europe/Paris")))

        ev.add('description', item["summary_detail"]["value"])

        cal.add_component(ev)

logging.info("Saving to file: "+calName)
f = open(calName, 'wb')
f.write(cal.to_ical())
f.close()

logging.info("Done")
