
from flask import Flask, render_template,request

import pymongo
import re
import flask_excel as excel



app = Flask(__name__)



myclient = pymongo.MongoClient("mongodb+srv://warangkana_kh:Sadaharu123@cluster0.h4ueo.mongodb.net/publication?retryWrites=true&w=majority")
mydb = myclient["publication_db"]
pub_db = mydb["publication"]
user_db = mydb['user']


pubdict = {}
publist = []
userdict = {}
userlist = []
year = {}
published_year = []


for i in pub_db.find():
        pubdict = i
        publist.append(pubdict)

for i in user_db.find():
        userdict = i
        userlist.append(userdict)

for i in range(1994,2021):
        published_year.append(i)

published_year.sort(reverse=True)

def userpublication(username):
    user = user_db.find_one({'name' : username})
    indexname = user['indexname']
    reg = indexname
    for i in publist:
        if re.findall(reg,i['authors']):
            user_dict = i
            userlist.append(user_dict)
    return userlist




@app.route("/")
def publication():
    #newlist = sorted(publist, key=lambda k: k['year'],reverse=True) 
    return render_template("index.html",publist = publist,userlist = userlist,published_year = published_year)

@app.route("/user")
def user():
    for i in user_db.find():
        userdict = i
        userlist.append(userdict)
    return render_template("user.html",userlist = userlist)

@app.route("/userpub/<username>")
def userpub(username):
    user = user_db.find_one({'name' : username})
    fullname = user['thainame'] + " " + user['thaisurname'] 
    thainame = user['thainame']   
    indexname = user['indexname']
    user_dict = {}
    user_pub = []
    reg = indexname
    for i in publist:
        if re.findall(reg,i['authors']):
            user_dict = i
            user_pub.append(user_dict)
        elif re.findall(thainame,i['authors']):
            user_dict = i
            user_pub.append(user_dict)
    return render_template("user_pub.html", user_pub = publist,userlist = userlist,fullname = fullname, name = username)





@app.route("/publication/<year>")
def yearpub(year):
    yeardict = {}
    yearlist = []
    str_year = str(year)

    for x in publist:
        if re.findall(str_year,str(x['year'])):
            yeardict = x
            yearlist.append(yeardict)
    return render_template("index.html",publist = yearlist,userlist = userlist,published_year = published_year)


@app.route("/search")
def searchpub():
    resultdict = {}
    resultlist = []
    keyword = request.query_string
    keyword = str(keyword)
    keyword = keyword.split('=')
    keyword = keyword[1]

   
    for i in publist:
        if re.findall(keyword,str(i)):
            resultdict = i
            resultlist.append(resultdict)
    return render_template("search.html",publist = resultlist,userlist = userlist,published_year = published_year)

@app.route("/update")
def updatepub():
    return "ยังไม่มีงานวิจัยที่ตีพิมพ์เพิ่ม"


    


@app.route('/download/<keyword>')
def download_data(keyword):
    keyword = str(keyword)
    titledict = {}
    titlelist = []
    authorsdict = {}
    authorslist = []
    conferencedict = {}
    conferencelist = []
    volumedict = {}
    volumelist = []
    issuedict = {}
    issuelist = []
    pagedict = {}
    pagelist = []
    yeardict = {}
    yearlist = []
    monthdict = {}
    monthlist = []
    for i in publist:
        try:
            user = user_db.find_one({'name' : keyword}) 
            indexname = user['indexname']
            indexname = str(indexname)
            if re.findall(indexname,i['authors']):
                titledict = i['title']
                titlelist.append(titledict)

                authorsdict = i['authors']
                authorslist.append(authorsdict)

                conferencedict = i['conference']
                conferencelist.append(conferencedict)

                volumedict = i['volume']
                volumelist.append(volumedict)

                issuedict = i['issue']
                issuelist.append(issuedict)

                pagedict = i['page']
                pagelist.append(pagedict)

                yeardict = i['year']
                yearlist.append(yeardict)

                monthdict = i['month']
                monthlist.append(monthdict)

        except:
            if keyword == "all" :
                titledict = i['title']
                titlelist.append(titledict)

                authorsdict = i['authors']
                authorslist.append(authorsdict)

                conferencedict = i['conference']
                conferencelist.append(conferencedict)

                volumedict = i['volume']
                volumelist.append(volumedict)

                issuedict = i['issue']
                issuelist.append(issuedict)

                pagedict = i['page']
                pagelist.append(pagedict)

                yeardict = i['year']
                yearlist.append(yeardict)

                monthdict = i['month']
                monthlist.append(monthdict)

            if re.findall(keyword,str(i['year'])):
                titledict = i['title']
                titlelist.append(titledict)

                authorsdict = i['authors']
                authorslist.append(authorsdict)

                conferencedict = i['conference']
                conferencelist.append(conferencedict)

                volumedict = i['volume']
                volumelist.append(volumedict)

                issuedict = i['issue']
                issuelist.append(issuedict)

                pagedict = i['page']
                pagelist.append(pagedict)

                yeardict = i['year']
                yearlist.append(yeardict)

                monthdict = i['month']
                monthlist.append(monthdict)
        
    d = {'title' :titlelist,'authors': authorslist,'conference':conferencelist,'volume':volumelist,'issue':issuelist,'page':pagelist,'year':yearlist,'month':monthlist}
    excel.init_excel(app)
    extension_type = "csv"
    filename = "Article_" + keyword + "." + extension_type     
    return excel.make_response_from_dict(d, file_type=extension_type, file_name=filename)


if __name__== "__main__":
    app.run()