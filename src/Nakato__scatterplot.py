import json
import requests
import csv
import re
from prettytable import PrettyTable
import matplotlib.pyplot as plot
import pandas as pd 

from dateutil.parser import parse

table = PrettyTable()
table.field_names = ["File Name", "Author Name","Date"]

flst=[]
authorlst=[]
datelst=[]
datenumberlst=[]
shalst=[]
# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']
               
               
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    dictfiles[filename] = dictfiles.get(filename, 0) + 1
                    #collecting source files for rootbeer- IT HAS JAVA, Kotlin, cpp, c and cmake files
                    javafilename=re.match('\S+.java$', filename)
                    kotlinfile=re.match('\S+.kt$', filename)
                    cppfile=re.match('\S+.cpp$', filename)
                    cfile=re.match('\S+.c$', filename)
                    cmakefile=re.match('\S+.txt$', filename)
                    
                    #collecting authors
                    authornamejson=shaDetails['commit']['author']
                    authorname=authornamejson['name']
                    commitdate=authornamejson['date']
                    #dateweek=commitdate.week
                #   
                   # a_date = datetime.date(commitdate)
                    #week_number = a_date.isocalendar()[1]
                    #Get the week number of a_date


                    
                    if( javafilename or kotlinfile or cppfile or cfile or cmakefile):
                    
            
                    #if( javafilename):
                    #if( kotlinfile):
                    #if( cppfile):
                    #if( cfile):
                    #if( cmakefile):
                        
                        
                         #append values to lsts
                        flst.append(filename)
                        authorlst.append(authorname)
                        datelst.append(commitdate)
                        shalst.append(sha)
                        
                        date_series = pd.Series(datelst)
                        date_series = date_series.map(lambda x: parse(x))
                        datenumber= date_series.dt.isocalendar().week
                        # table.add_row([filename, authorname, commitdate ])
          #  print(datenumber)
                    
                     
                        #print(authorname)
                        #print(commitdate)
            list_of_tuples = list(zip(flst, authorlst,datenumber,sha)) 
    
# Assign data to tuples. 
            list_of_tuples  
            print(list_of_tuples )
  
  
      # Converting lists of tuples into 
      # pandas Dataframe. 
            df = pd.DataFrame(list_of_tuples,
                  columns = ['flename', 'author' ,'weekofyear','sha' ]) 
     
# Print data. 
            print(df)      
            
            
            df.plot.scatter(x='flename', y='weekofyear', title= "Scatter plot between two variables X and Y");

            plot.show(block=True);
            
             #print(table)             
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)
# GitHub repo
repo = 'scottyab/rootbeer' 

# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'


# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = [""]
#i have commented my token right here----Nakato
#printing the table data


dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)
print('Total number of files: ' + str(len(dictfiles)))

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = '../csv/file_' + file + '.csv'
rows = ["Filename", "Touches","Author","Date"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

bigcount = None
bigfilename = None
for filename, count in dictfiles.items():
    rows = [filename, count]
    writer.writerow(rows)
    if bigcount is None or count > bigcount:
        bigcount = count
        bigfilename = filename
fileCSV.close()
print('The file ' + bigfilename + ' has been touched ' + str(bigcount) + ' times.')
