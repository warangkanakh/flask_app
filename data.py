from selenium import webdriver
import os
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pymongo

title_list = []
authors_list = []
conference_list = []
volume_list = []
issue_list= []
page_list = []
year_list = []

title_update = []
year_update = []

#tci_format
def tci_format(element):
    
    article_split = element.split("\n")
    title = article_split[0]    
    authors = article_split[2]
    
    conference_reset = article_split[3].split(", ")
    issue = conference_reset[1]
    year = conference_reset[2]
    page = conference_reset[3]
    
    
    x = "." in conference_reset[0]
    
    
    if x:
        new_conference = conference_reset[0].replace(".",".,")
    else:
        new_conference = conference_reset[0].replace(" V",", V")
        
    new_split= new_conference.split(", ")
    conference =  new_split[0]
    volume =  new_split[1]
    
    title_list.append(title)
    authors_list.append(authors)
    conference_list.append(conference)
    volume_list.append(volume)
    issue_list.append(issue)
    page_list.append(page)
    year_list.append(year)

    title_update.append(title)
    year_update.append(year)

    
    return title_update,year_update

def update():
    #Set directory
    path = 'C:/Users/THIS PC/Desktop/internshipproject/flask_web/'
    os.chdir(path)


    myclient = pymongo.MongoClient("mongodb+srv://warangkana_kh:Sadaharu123@cluster0.h4ueo.mongodb.net/publication?retryWrites=true&w=majority")
    mydb = myclient["publication_db"]
    pub_db = mydb["publication"]
    user_db = mydb['user']


    pubdict = {}
    publist = []
    userdict = {}
    userlist = []



    for i in pub_db.find():
            pubdict = i
            publist.append(pubdict)

    for i in user_db.find():
            userdict = i
            userlist.append(userdict)



#tci_update
    all_element = []

    for i in userlist:
        thainame = i['thainame']
        thaisurname = i['thaisurname']
        try:
            tci = webdriver.Chrome(path+"chromedriver.exe")
            tci.get('https://tci-thailand.org/wp-content/themes/magazine-style/tci_search/advance_search.html')

            select_authors = tci.find_element(By.XPATH, '//*[@id="condition"]/div/div/select')
            select_authors = select_authors.send_keys("Author")

            authors_fullname = thainame+" "+thaisurname

            input_authors = tci.find_element(By.XPATH, '//*[@id="condition"]/div/div/input').send_keys(authors_fullname)
            tci.find_element(By.XPATH, '//*[@id="searchBtn"]').click()

            element_wait = WebDriverWait(tci, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="limit_num_page"]')))

            select_entry = tci.find_element(By.XPATH, '//*[@id="limit_num_page"]')
            select_entry = select_entry.send_keys("100")

    
            all_article = tci.find_element(By.XPATH, '//*[@id="search_result"]')
            #print(all_article.text)
            all_article_str = all_article.text
            #print(all_article_str)
            number = []
    
            document = all_article_str.replace('(','').replace(')','')
            #print(document)
            for word in document.split():
                if word.isdigit():
                    list_index = word
    
            list_index =int(list_index)
            list_index = list_index+1

            if list_index == 1:
                print("no result")
                #print(str(i)+". "+authors_fullname)
            elif list_index == 2:
                element =  tci.find_element(By.XPATH, '//*[@id="data-article"]/div/div')
                element_str = element.text
            #print(create_article(element_str))
                all_element.append(element_str)
                #print(str(i)+". "+authors_fullname)
                #print(str(j) + ". " +element_str)
            else:
                for j in range(1,list_index):
                    #print(i)
                    xpath = '//*[@id="data-article"]/div['+str(j)+']/div'
                    element =  tci.find_element(By.XPATH, xpath)
                    element_str = element.text 
                    #print(str(i)+". "+authors_fullname)
                    all_element.append(element_str)
                    #print(str(j) + ". " +element_str)
            
            tci.close()
        except:
            print("can't collect element")
            tci.close()



    for i in all_element:
        tci_format(i)


    if title_update:
        update_status = "updated"
    else:
        update_status = "no update"
    return update_status

# dict_update = {
#   "title": title_list,
#   "authors": authors_list,
#   "conference": conference_list,
#   "volume" : volume_list,
#   "issue" :issue_list,
#   "page" : page_list,
#   "year" : year_list,
# }

