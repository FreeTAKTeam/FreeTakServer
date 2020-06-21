import datetime
import logging
import os
import random
import sqlite3
import string
import sys
import traceback
import xml.etree.ElementTree as ET
import zipfile
from logging.handlers import RotatingFileHandler
from pathlib import Path, PurePath

from FreeTAKServer.controllers.configuration.DataPackageServerConstants import DataPackageServerConstants
from FreeTAKServer.controllers.configuration.SQLcommands import SQLcommands
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants

from flask import Flask, request, send_file
from flask.logging import default_handler
from werkzeug.datastructures import FileStorage



sql = SQLcommands()
const = DataPackageServerConstants()
log =LoggingConstants()

app = Flask(__name__) #create the Flask app

file_dir = os.path.dirname(os.path.realpath(__file__))
dp_directory = PurePath(file_dir, const.DATAPACKAGEFOLDER)

# Set up logging
if not Path(log.LOGDIRECTORY).exists():
    print(f"Creating directory at {log.LOGDIRECTORY}")
    os.makedirs(log.LOGDIRECTORY)
app.logger.removeHandler(default_handler)
formatter = logging.Formatter(log.LOGFORMAT)
file_handler = RotatingFileHandler(
    log.HTTPLOG,
    maxBytes=log.MAXFILESIZE,
    backupCount=log.BACKUPCOUNT
)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.ERROR)
app.logger.addHandler(file_handler)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)
app.logger.addHandler(console_handler)
app.logger.setLevel(logging.DEBUG)

@app.route("/Marti/vcm", methods=[const.GET])
def get_all_video_links():
    # This is called when the user selects the Download button in the Videos window. It
    # expects an XML listing of all known feeds, so the user can pick and choose which ones
    # to store locally
    try:
        with sqlite3.connect(const.DATABASE) as db:
            cursor = db.cursor()
            cursor.execute(sql.GETALLVIDEOS)
            feeds = cursor.fetchall()
            app.logger.info(f"Found {len(feeds)} video feeds in {const.DATABASE}")
            if len(feeds) == 0:
                return ("No video feeds found", 500)
            all_feeds = ""
            for feed in feeds:
                # 'feed' is a tuple with one element, so we only append that
                all_feeds += feed[0].decode("utf-8")
            return f"<videoConnections>{all_feeds}</videoConnections>"
    except:
        app.logger.error(traceback.format_exc())
        return "Error", 500


@app.route("/Marti/vcm", methods=[const.POST])
def insert_video_link():
    db = sqlite3.connect(const.DATABASE)
    cursor = db.cursor()
    try:
        xml_root = ET.fromstring(request.data.decode("utf-8"))
        for xml_feed in xml_root:
            protocol = xml_feed.find("protocol").text
            alias = xml_feed.find("alias").text
            uid = xml_feed.find("uid").text
            address = xml_feed.find("address").text
            port = xml_feed.find("port").text
            rover_port = xml_feed.find("roverPort").text
            ignore_klv = xml_feed.find("ignoreEmbeddedKLV").text
            preferred_mac = xml_feed.find("preferredMacAddress").text
            path = xml_feed.find("path").text
            buf = xml_feed.find("buffer").text
            timeout = xml_feed.find("timeout").text
            rtsp_reliable = xml_feed.find("rtspReliable").text
            # Check that no other feeds with the same UID have been received
            cursor.execute(sql.GETVIDEOSWITHUID, (uid,))
            if len(cursor.fetchall()) > 0:
                app.logger.info(f"Already received feed with UID={uid} (alias = {alias})")
                continue  # Ignore this feed if there are duplicates
            app.logger.info(f"Inserting video feed into database: {request.data.decode('utf-8')}")
            cursor.execute(
                sql.INSERTVIDEO,
                (ET.tostring(xml_feed), protocol, alias, uid, address, port, rover_port,
                 ignore_klv, preferred_mac, path, buf, timeout, rtsp_reliable)
            )
        return "Okay", 200
    except:
        app.logger.error(traceback.format_exc())
        return "Error", 500
    finally:
        db.commit()
        db.close()


@app.route('/Marti/api/version/config', methods=[const.GET])
def versionConfig():
    return const.VERSIONJSON


@app.route('/Marti/api/clientEndPoints', methods=[const.GET])
def clientEndPoint():
    return const.versionInfo


@app.route('/Marti/sync/missionupload', methods=[const.POST])
def upload():
    with sqlite3.connect(const.DATABASE) as db:
        cursor = db.cursor()
        file_hash = request.args.get('hash')
        app.logger.info(f"Data Package hash = {str(file_hash)}")
        letters = string.ascii_letters
        uid = ''.join(random.choice(letters) for i in range(4))
        uid = 'uid-'+str(uid)
        filename = request.args.get('filename')
        creatorUid = request.args.get('creatorUid')
        file = request.files.getlist('assetfile')[0]
        directory = Path(dp_directory, file_hash)
        if not Path.exists(directory):
            os.mkdir(directory)
        file.save(os.path.join(directory, filename))
        fileSize = Path(directory, filename).stat().st_size
        callsign = str(FlaskFunctions().getSubmissionUser(creatorUid)) # fetchone() gives a tuple, so only grab the first element
        cursor.execute(sql.INSERTDPINFO, (uid, filename, file_hash, callsign, creatorUid, fileSize))
        cursor.close()
        db.commit()
    return IP+':'+const.HTTPPORT+"/Marti/api/sync/metadata/"+file_hash+"/tool"


@app.route('/Marti/api/sync/metadata/<hash>/tool', methods=[const.PUT])
def putDataPackageTool(hash):
    if request.data == b'private':
        with sqlite3.connect(const.DATABASE) as db:
            cursor = db.cursor()
            cursor.execute("UPDATE DataPackages SET Privacy = 1 WHERE Hash = ?;", (hash,))
            cursor.close()
            db.commit()
    return "Okay", 200


@app.route('/Marti/api/sync/metadata/<hash>/tool', methods=[const.GET])
def getDataPackageTool(hash):
    file_list = os.listdir(str(dp_directory)+'/'+str(hash))
    path = PurePath(dp_directory, str(hash), file_list[0])
    app.logger.info(f"Sending data package from {str(path)}")
    return send_file(str(path))


@app.route('/Marti/sync/search', methods=[const.GET])
def retrieveData():
    keyword = request.args.get('keyword')
    packages = FlaskFunctions().getAllPackages()
    app.logger.info(f"Data packages in the database: {packages}")
    return str(packages)


@app.route('/Marti/sync/content', methods=const.HTTPMETHODS)
def specificPackage():
    hash = request.args.get('hash')
    app.logger.debug(os.listdir(str(dp_directory)+'/'+str(hash)))
    file_list = os.listdir(str(dp_directory)+'/'+str(hash))
    app.logger.debug(const.DATAPACKAGEFOLDER+'\\'+hash+'\\'+file_list[0])
    path = PurePath(dp_directory, str(hash), file_list[0])
    app.logger.debug(str(path))
    return send_file(str(path))


@app.route('/Marti/api/version', methods=[const.GET])
def returnVersion():
    return const.versionInfo


@app.route('/Marti/sync/missionquery', methods=const.HTTPMETHODS)
def checkPresent():
    hash = request.args.get('hash')
    if FlaskFunctions().hashIsPresent(hash):
        app.logger.info(f"Data package with hash {hash} exists")
        return IP+':'+const.HTTPPORT+"/Marti/api/sync/metadata/"+hash+"/tool"
    else:
        app.logger.info(f"Data package with hash {hash} does not exist")
        return '404', 404

class FlaskFunctions:

    def __init__(self):
        self.callsigns = []

    def hashIsPresent(self, hash):
        with sqlite3.connect(const.DATABASE) as db:
            cursor = db.cursor()
            cursor.execute(sql.ROWBYHASH, (hash,))
            data = cursor.fetchall()
            cursor.close()
            return len(data) > 0

    def getSubmissionUser(self, UID):
        with sqlite3.connect(const.DATABASE) as db:
            cursor = db.cursor()
            cursor.execute(sql.RETRIEVECALLSIGNFROMUID, (UID,))
            callsign = cursor.fetchone()
            cursor.close()
            return callsign
            
    def getAllPackages(self):
        with sqlite3.connect(const.DATABASE) as db:
            cursor = db.cursor()
            cursor.execute(sql.SELECTALLDP)
            data = cursor.fetchall()
            cursor.close()
            package_dict = {
                "resultCount": len(data),
                "results": []
            }
            for i in data:
                package_dict["results"].append({
                    "UID": i[1],
                    "Name": i[2],
                    "Hash": i[3],
                    "PrimaryKey": i[0],
                    "SubmissionDateTime": i[4],
                    "SubmissionUser": i[5],
                    "CreatorUid": i[6],
                    "Keywords": i[7],
                    "MIMEType": i[8],
                    "Size": i[9]
                })
            return package_dict

    def startup(self, ip, port, pipe):
        global IP, HTTPPORT, PIPE
        PIPE = pipe
        IP = ip
        HTTPPORT = port
            # Make sure the data package directory exists
        if not Path(dp_directory).exists():
            app.logger.info(f"Creating directory at {str(dp_directory)}")
            os.makedirs(str(dp_directory))

        # Create the relevant database tables
        with sqlite3.connect(const.DATABASE) as db:
            cursor = db.cursor()
            cursor.execute(sql.CREATEDPTABLE)
            cursor.execute(sql.CREATEVIDEOTABLE)
            cursor.execute(sql.CREATEUSERTABLE)
            db.commit()
            cursor.close()
            
        app.run(host=IP, port=HTTPPORT, debug=const.HTTPDEBUG)

if __name__ == "__main__":
    pass
    
