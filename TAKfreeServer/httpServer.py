from flask import Flask, request, send_file #import main Flask class and request object
import zipfile
from werkzeug.datastructures import FileStorage
import os
import sqlite3
from pathlib import Path, PurePath, PosixPath
import sys
import string
import random
import datetime
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR)))
from constants import vars
from SQLcommands import sql

sql = sql()
const = vars()
dir = dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir)
path = PurePath(dir, 'DataPackages')
print(path)
if Path(path).exists()==True:
    pass
elif Path(path).exists()==False:
    os.mkdir(path)

sqliteServer = sqlite3.connect(const.DATABASE)
cursor = sqliteServer.cursor()

cursor.execute(sql.CREATEDPTABLE)
cursor.close()
sqliteServer.commit()

sqliteServer.close()
app = Flask(__name__) #create the Flask app

@app.route('/Marti/api/version/config', methods=const.HTTPMETHODS)
def versionConfig():
    if request.method == const.GET:
        return const.VERSIONJSON

@app.route('/Marti/api/clientEndPoints', methods=const.HTTPMETHODS)
def clientEndPoint():
    if request.method == const.GET:
        return const.versionInfo
    else:
        return 'c'

@app.route('/Marti/sync/missionupload', methods=const.HTTPMETHODS)
def upload():
    print(request.method)
    sqliteServer = sqlite3.connect(const.DATABASE)
    cursor = sqliteServer.cursor()
    if request.method == 'POST':
        hash = request.args.get('hash')
        print(type(hash))
        print(hash)
        letters = string.ascii_letters
        uid = ''.join(random.choice(letters) for i in range(4))
        uid = 'uid-'+str(uid)
        filename = request.args.get('filename')
        creatorUid=request.args.get('creatorUid')
        file = request.files.getlist('assetfile')
        print(file[0])
        file = file[0]
        path = Path(dir, const.DATAPACKAGEFOLDER, hash)
        if Path.exists(path)==True:
            pass
        elif Path.exists(path)==False:
            os.mkdir(path)
        file.save(os.path.join(path,filename))
        fileSize = int(Path(const.DATAPACKAGEFOLDER,hash,str(filename)).stat().st_size)

        cursor.execute(sql.MISSIONUPLOADCALLSIGN,(creatorUid,))
        Callsign = cursor.fetchone()
        cursor.execute(sql.INSERTDPINFO,(uid, filename, str(hash), str(Callsign), str(creatorUid), int(fileSize),))
        sqliteServer.commit()
        cursor.close()
        sqliteServer.close()
        return const.IP+':'+const.HTTPPORT+"/Marti/api/sync/metadata/"+hash+"/tool"
    else:
        return 'e'

@app.route('/Marti/api/sync/metadata/<hash>/tool', methods=const.HTTPMETHODS)
def theUploadPart2(hash):
    sqliteServer = sqlite3.connect(const.DATABASE)
    cursor = sqliteServer.cursor()
    if request.method == const.PUT:
        print(request.data)
        if request.data == b'private':
            cursor.execute("UPDATE DataPackages SET Privacy = 1 WHERE Hash = ?;", (hash,))
            sqliteServer.commit()
            cursor.close()
            sqliteServer.close()
            
        else:
            pass
        return 'a'
    elif request.method == const.GET:
        file_list=os.listdir(const.DATAPACKAGEFOLDER+'/'+str(hash))
        dir = PurePath('.')
        path = PurePath(dir, const.DATAPACKAGEFOLDER, str(hash), file_list[0])
        print(str(path))
        return send_file(str(path))

    else:
        return 'b'
@app.route('/Marti/sync/search', methods=const.HTTPMETHODS)
def retrieveData():
    keyword = request.args.get('keyword')
    Packages = getAllPackages()
    print(Packages)
    return str(Packages)
    
@app.route('/Marti/sync/content', methods=const.HTTPMETHODS)
def specificPackage():
    hash = request.args.get('hash')
    print(os.listdir(const.DATAPACKAGEFOLDER+'/'+str(hash)))
    file_list=os.listdir(const.DATAPACKAGEFOLDER+'/'+str(hash))

    print(const.DATAPACKAGEFOLDER+'\\'+hash+'\\'+file_list[0])
    dir = PurePath('.')
    path = PurePath(dir, const.DATAPACKAGEFOLDER, str(hash), file_list[0])
    print(str(path))
    return send_file(str(path))

@app.route('/Marti/api/version', methods=const.HTTPMETHODS)
def returnVersion():
    if request.method == const.GET:
        return const.versionInfo
    else:
        return 'f'

@app.route('/Marti/sync/missionquery', methods=const.HTTPMETHODS)
def checkPresent():
    hash = request.args.get('hash')
    present = getSpecific(hash)
    if present == False:
        return '404', 404
    else:
        return const.IP+':'+const.HTTPPORT+"/Marti/api/sync/metadata/"+hash+"/tool"


def getSpecific(hash):
    sqliteServer = sqlite3.connect(const.DATABASE)
    cursor = sqliteServer.cursor()
    cursor.execute(sql.ROWBYHASH,(hash,))
    data = cursor.fetchall()

    if len(data)> 0:
        return True
    
    else:
        return False

def getAllPackages():
    sqliteServer = sqlite3.connect(const.DATABASE)
    cursor = sqliteServer.cursor()
    cursor.execute(sql.SELECTALLDP)
    data = cursor.fetchall()
    PackageDict = {"resultCount":len(data), "results":[]}
    for i in data:
        singlePackage = {"UID":str(i[1]), "Name": str(i[2]), "Hash": str(i[3]), "PrimaryKey":str(i[0]), "SubmissionDateTime": str(i[4]),"SubmissionUser": str(i[5]), "CreatorUid": str(i[6]), "Keywords": (i[7]), "MIMEType": str(i[8]), "Size": int(i[9])}
        PackageDict["results"].append(singlePackage)
    return PackageDict

def startup():
    app.run(host=const.IP, port=const.HTTPPORT, debug=const.HTTPDEBUG)

if __name__ == "__main__":
    app.run(host=const.IP, port=const.HTTPPORT, debug=const.HTTPDEBUG)
    
