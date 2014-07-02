import MySQLdb
import urllib2
from time import sleep
from bs4 import BeautifulSoup as bf
import urllib

lang = "JavaScript" # could be Python, JavaScript, C, C++, Shell, CSS, Java, VimL,Ruby, PHP
p = 1 #indicates page number


def checkLink():

    global p
    url = """https://github.com/search?l=JavaScript&o=desc&p=%(page)s&q=%(location)s&ref=advsearch&type=Users"""
    url2 = """https://github.com/"""
    data = {"page": p, "location": "location%3AIndia"} #location can be set here insted of India, any desired location could be entered.
    site = (url % data)
    print site
    print "\n\n"
    try:
        data = urllib2.urlopen(site, data=None, timeout=60)
        tag = bf(data.read())
        user = tag.findAll('div',{'class': 'user-list-info'})
        mydb = MySQLdb.connect(host='localhost',
                                user='root',
                                passwd='password',
                                db='gitcrawler')# change the database information
        cursor = mydb.cursor()
        for r in user:
            username = r.find('a').string
            locate = r.find('li')
            location = locate.text
            date = r.findAll('li')[2:3]
            fullname = r.contents[2:3]
            name = str(fullname)[9:-8]
            site2 = (url2+username)
            userpage = urllib2.urlopen(site2,data=None, timeout=60)
            userinfo = bf(userpage.read())
            information = userinfo.findAll('a', {'class': 'url'}, text=True)
            link = None
            for x in information:
                link = ''.join(x.findAll(text=True))
            print link
            joining_date = "Not Available"
            for n in date:
                joindate = n.findAll('span')[1:]
                for s in joindate:
                    joining_date = ''.join(s.findAll(text=True))
            email = r.findAll('a')[1:2]
            mail = None
            for q in email:
                mail = q.get('data-email')
                mail = urllib.unquote(mail).decode('utf8')
                print "---------------------------------------------------------------------------"
                print '|%s | %s | %s | %s | %s | %s |' % (location, username, joining_date, mail, name, link)
            try:
                len(mail)# change the name of table in insert query as per language.
                cursor.execute('''INSERT INTO javascript(username, language, currentlocation, email, joining_date, name, link) VALUES(%s, %s, %s, %s, %s, %s, %s)''', (username, lang, location, mail, joining_date, name,link))
            except TypeError:
                cursor.execute('''INSERT INTO javascript(username, language, currentlocation, email, joining_date, name, link) VALUES(%s, %s, %s, %s, %s, %s, %s)''', (username, lang, location, mail, joining_date, name, link))
        mydb.commit()
        cursor.close()
        p += 1
    except urllib2.HTTPError, e:
        print "Http error to many request , sleeping for 10 seconds..."
        print e
        sleep(10)


while p < 101:
    checkLink()


__author__ = 'niklaus'
