# !/usr/bin/python
import subprocess
try:
    from OpenSSL import crypto
except ImportError:
    subprocess.run(["pip3", "install", "pyopenssl"], capture_output=True)
from OpenSSL import crypto
import os
import getopt
import sys
import random
from shutil import copyfile
import uuid
from jinja2 import Template
import socket
import zipfile
import shutil
import pathlib
from FreeTAKServer.controllers.configuration.MainConfig import MainConfig

try:
    import requests
except ImportError:
    subprocess.run(["pip3", "install", "requests"], capture_output=True)
import hashlib


def _utc_time_from_datetime(date):
    fmt = '%y%m%d%H%M'
    if date.second > 0:
        fmt += '%S'
    if date.tzinfo is None:
        fmt += 'Z'
    else:
        fmt += '%z'
    return date.strftime(fmt)


def revoke_certificate(username, revoked_file=None, ca_pem = MainConfig.CA, ca_key = MainConfig.CAkey, crl_file = MainConfig.CRLFile, user_cert_dir=MainConfig.certsPath, crl_path=MainConfig.CRLFile):
    """
    Function to create/update a CRL with revoked user certificates
    :param ca_pem: The path to your CA PEM file
    :param ca_key: The Path to your CA key file
    :param revoked_file: Path to JSON file to be used as a DB for revocation
    :param crl_file: Path to CRL file
    :param user_cert_dir: Path to director containing all issued user PEM files
    :param username: the username to Revoke
    :param crl_path: The path to your previous CRL file to be loaded and updated
    :return: bool
    """

    import os
    import json
    from OpenSSL import crypto
    from datetime import datetime
    data = {}
    certificate = crypto.load_certificate(crypto.FILETYPE_PEM, open(ca_pem, mode="rb").read())
    private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, open(ca_key, mode="r").read())
    if crl_path and os.path.exists(crl_path):
        crl = crypto.load_crl(crypto.FILETYPE_PEM, open(crl_path, mode="rb").read())
    else:
        crl = crypto.CRL()
        if revoked_file and os.path.exists(revoked_file):
            with open(revoked_file, 'r') as json_file:
                data = json.load(json_file)

    for cert in os.listdir(user_cert_dir):
        if cert.lower() == f"{username.lower()}.pem":
            with open(MainConfig.certsPath+'/'+cert, 'rb') as cert:
                revoked_cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert.read())
            data[str(revoked_cert.get_serial_number())] = username
            break

    for key in data:
        revoked_time = _utc_time_from_datetime(datetime.utcnow())
        revoked = crypto.Revoked()
        revoked.set_serial(format(int(key), "02x").encode())
        revoked.set_rev_date(bytes(revoked_time, encoding='utf8'))
        crl.add_revoked(revoked)
    crl.sign(certificate, private_key, b"sha256")
    if revoked_file:
        with open(revoked_file, 'w+') as json_file:
            json.dump(data, json_file)

    with open(crl_file, 'wb') as f:
        f.write(crl.export(cert=certificate, key=private_key, digest=b"sha256"))

    delete = 0
    with open(ca_pem, "r") as f:
        lines = f.readlines()
    with open(ca_pem, "w") as f:
        for line in lines:
            if delete:
                continue
            elif line.strip("\n") != "-----BEGIN X509 CRL-----":
                f.write(line)
            else:
                delete = 1

    with open(ca_pem, "ab") as f:
        f.write(crl.export(cert=certificate, key=private_key, digest=b"sha256"))


def send_data_package(server: str, dp_name: str = "user.zip") -> bool:
    """
    Function to send data package to server
    :param server: Server address where the package will be uploaded
    :param dp_name: Name of the zip file to upload
    :return: bool
    """
    file_hash = hashlib.sha256()
    block_size = 65536
    with open(dp_name, 'rb') as f:
        fb = f.read(block_size)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(block_size)

    with open(dp_name, 'rb') as f:
        s = requests.Session()
        r = s.post(f'http://{server}:8080/Marti/sync/missionupload?hash={file_hash.hexdigest()}'
                   f'&filename={dp_name}'
                   f'&creatorUid=atakofthecerts',
                   files={"assetfile": f.read()},
                   headers={'Expect': '100-continue'})
        if r.status_code == 200:
            p_r = s.put(f'http://{server}:8080/Marti/api/sync/metadata/{file_hash.hexdigest()}/tool')
            return True
        else:
            print("Something went wrong uploading DataPackage!")
            return False


def generate_zip(server_address: str = None, server_filename: str = "pubserver.p12", user_filename: str = "user.p12",
                 cert_password: str = "atakatak", ssl_port: str = "8089") -> None:
    """
    A Function to generate a Client connection Data Package (DP) from a server and user p12 file in the current
    working directory.
    :param server_address: A string based ip address or FQDN that clients will use to connect to the server
    :param server_filename: The filename of the server p12 file default is pubserver.p12
    :param user_filename: The filename of the server p12 file default is user.p12
    :param cert_password: The password for the certificate files
    :param ssl_port: The port used for SSL CoT, defaults to 8089
    """
    pref_file_template = Template("""<?xml version='1.0' standalone='yes'?>
    <preferences>
        <preference version="1" name="cot_streams">
            <entry key="count" class="class java.lang.Integer">1</entry>
            <entry key="description0" class="class java.lang.String">FreeTAKServer_{{ server }}</entry>
            <entry key="enabled0" class="class java.lang.Boolean">false</entry>
            <entry key="connectString0" class="class java.lang.String">{{ server }}:{{ port }}:ssl</entry>
        </preference>
        <preference version="1" name="com.atakmap.app_preferences">
            <entry key="displayServerConnectionWidget" class="class java.lang.Boolean">true</entry>
            <entry key="caLocation" class="class java.lang.String">/storage/emulated/0/atak/cert/{{ server_filename }}</entry>
            <entry key="caPassword" class="class java.lang.String">{{ cert_password }}</entry>
            <entry key="clientPassword" class="class java.lang.String">{{ cert_password }}</entry>
            <entry key="certificateLocation" class="class java.lang.String">/storage/emulated/0/atak/cert/{{ user_filename }}</entry>
        </preference>
    </preferences>
    """)

    manifest_file_template = Template("""<MissionPackageManifest version="2">
       <Configuration>
          <Parameter name="uid" value="{{ uid }}"/>
          <Parameter name="name" value="FreeTAKServer_{{ server }}"/>
          <Parameter name="onReceiveDelete" value="true"/>
       </Configuration>
       <Contents>
          <Content ignore="false" zipEntry="{{ folder }}/fts.pref"/>
          <Content ignore="false" zipEntry="{{ folder }}/{{ server_filename }}"/>
          <Content ignore="false" zipEntry="{{ folder }}/{{ user_filename }}"/>	  
       </Contents>
    </MissionPackageManifest>
    """)

    manifest_file_parent_template = Template("""<MissionPackageManifest version="2">
           <Configuration>
              <Parameter name="uid" value="{{ uid }}"/>
              <Parameter name="name" value="FreeTAKServer_{{ server }}_DP"/>
           </Configuration>
           <Contents>
              <Content ignore="false" zipEntry="{{ folder }}/{{ internal_dp_name }}.zip"/>
           </Contents>
        </MissionPackageManifest>
        """)
    username = user_filename[:-4]
    random_id = uuid.uuid4()
    new_uid = uuid.uuid4()
    folder = "5c2bfcae3d98c9f4d262172df99ebac5"
    parentfolder = "80b828699e074a239066d454a76284eb"
    if MainConfig.UserConnectionIP == "0.0.0.0":
        hostname = socket.gethostname()
        server_address = socket.gethostbyname(hostname)
    else:
        server_address = MainConfig.UserConnectionIP
    pref = pref_file_template.render(server=server_address, server_filename=server_filename,
                                     user_filename=user_filename, cert_password=cert_password,
                                     port=str(MainConfig.SSLCoTServicePort))
    man = manifest_file_template.render(uid=random_id, server=server_address, server_filename=server_filename,
                                        user_filename=user_filename, folder=folder)
    man_parent = manifest_file_parent_template.render(uid=new_uid, server=server_address,
                                                      folder=parentfolder,
                                                      internal_dp_name=f"{username.replace('./', '')}")
    if not os.path.exists("./" + folder):
        os.makedirs("./" + folder)
    if not os.path.exists("./MANIFEST"):
        os.makedirs("./MANIFEST")
    with open('./' + folder + '/fts.pref', 'w') as pref_file:
        pref_file.write(pref)
    with open('./MANIFEST/manifest.xml', 'w') as manifest_file:
        manifest_file.write(man)
    copyfile(MainConfig.p12Dir, "./" + folder + "/" + server_filename)
    copyfile(MainConfig.certsPath + "/" + user_filename, "./" + folder + "/" + user_filename)
    zipf = zipfile.ZipFile(f"{username}.zip", 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk('./' + folder):
        for file in files:
            zipf.write(os.path.join(root, file))
    for root, dirs, files in os.walk('./MANIFEST'):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()
    shutil.rmtree("./MANIFEST")
    shutil.rmtree("./" + folder)
    # Create outer DP...because WinTAK
    if not os.path.exists("./" + parentfolder):
        os.makedirs("./" + parentfolder)
    if not os.path.exists("./MANIFEST"):
        os.makedirs("./MANIFEST")
    with open('./MANIFEST/manifest.xml', 'w') as manifest_parent:
        manifest_parent.write(man_parent)
    copyfile(f"./{username}.zip", f"./{parentfolder}/{username}.zip")
    zipp = zipfile.ZipFile(str(pathlib.PurePath(pathlib.Path(MainConfig.clientPackages), pathlib.Path(f"{username}.zip"))), 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk('./' + parentfolder):
        for file in files:
            name = str(pathlib.PurePath(pathlib.Path(root), pathlib.Path(file)))
            zipp.write(name)
    for root, dirs, files in os.walk('./MANIFEST'):
        for file in files:
            zipp.write(os.path.join(root, file))
    zipp.close()
    shutil.rmtree("./MANIFEST")
    shutil.rmtree("./" + parentfolder)
    os.remove(f"./{username}.zip")


class AtakOfTheCerts:
    def __init__(self, pwd: str = MainConfig.password) -> None:
        """
        :param pwd: String based password used to secure the p12 files generated, defaults to atakatak
        """
        self.key = crypto.PKey()
        self.CERTPWD = pwd
        self.cakeypath = MainConfig.CAkey
        self.capempath = MainConfig.CA

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return None

    def generate_ca(self, expiry_time_secs: int = 31536000) -> None:
        """
        Generate a CA certificate
        """
        if not os.path.exists(self.cakeypath):
            print("Cannot find CA locally so generating one")
            if not os.path.exists(os.path.dirname(self.cakeypath)):
                print("the directory for storing certificates doesn't exist.")
                print("Creating one at " + os.path.dirname(self.cakeypath))
                os.makedirs(os.path.dirname(self.cakeypath))
            ca_key = crypto.PKey()
            ca_key.generate_key(crypto.TYPE_RSA, 2048)
            cert = crypto.X509()
            cert.get_subject().CN = "CA"
            cert.set_serial_number(0)
            cert.set_version(2)
            cert.gmtime_adj_notBefore(0)
            cert.gmtime_adj_notAfter(expiry_time_secs)
            cert.set_issuer(cert.get_subject())
            cert.add_extensions([crypto.X509Extension(b'basicConstraints', False, b'CA:TRUE'),
                                 crypto.X509Extension(b'keyUsage', False, b'keyCertSign, cRLSign')])
            cert.set_pubkey(ca_key)
            cert.sign(ca_key, "sha256")

            f = open(self.cakeypath, "wb")
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, ca_key))
            f.close()

            f = open(self.capempath, "wb")
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
            f.close()

            # append empty crl
            crl = crypto.CRL()
            crl.sign(cert, ca_key, b"sha256")

            with open(MainConfig.CRLFile, 'wb') as f:
                f.write(crl.export(cert=cert, key=ca_key, digest=b"sha256"))

            delete = 0
            with open(self.capempath, "r") as f:
                lines = f.readlines()
            with open(self.capempath, "w") as f:
                for line in lines:
                    if delete:
                        continue
                    elif line.strip("\n") != "-----BEGIN X509 CRL-----":
                        f.write(line)
                    else:
                        delete = 1

            with open(self.capempath, "ab") as f:
                f.write(crl.export(cert=cert, key=ca_key, digest=b"sha256"))

        else:
            print("CA found locally, not generating a new one")

    def _generate_key(self, keypath: str) -> None:
        """
        Generate a new certificate key
        :param keypath: String based filepath to place new key, this should have a .key file extention
        """
        if os.path.exists(keypath):
            print("Certificate file exists, aborting.")
        else:
            print("Generating Key...")
            self.key.generate_key(crypto.TYPE_RSA, 2048)
            f = open(keypath, "wb")
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, self.key))
            f.close()

    def _generate_certificate(self, common_name: str, p12path: str, pempath: str = MainConfig.pemDir,
                              expiry_time_secs: int = 31536000) -> None:
        """
        Create a certificate and p12 file
        :param cn: Common Name for certificate
        :param pempath: String filepath for the pem file created
        :param p12path: String filepath for the p12 file created
        :param expiry_time_secs: length of time in seconds that the certificate is valid for, defaults to 1 year
        """
        if not os.path.exists(pempath):
            ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, open(self.cakeypath).read())
            ca_pem = crypto.load_certificate(crypto.FILETYPE_PEM, open(self.capempath, 'rb').read())
            serial_number = random.getrandbits(64)
            chain = (ca_pem,)
            cert = crypto.X509()
            cert.get_subject().CN = common_name
            cert.set_serial_number(serial_number)
            cert.gmtime_adj_notBefore(0)
            cert.gmtime_adj_notAfter(expiry_time_secs)
            cert.set_issuer(ca_pem.get_subject())
            cert.set_pubkey(self.key)
            cert.set_version(2)
            cert.sign(ca_key, "sha256")
            p12 = crypto.PKCS12()
            p12.set_privatekey(self.key)
            p12.set_certificate(cert)
            p12.set_ca_certificates(tuple(chain))
            p12data = p12.export(passphrase=bytes(self.CERTPWD, encoding='UTF-8'))
            with open(p12path, 'wb') as p12file:
                p12file.write(p12data)

            if os.path.exists(pempath):
                print("Certificate File Exists, aborting.")
            else:
                f = open(pempath, "wb")
                f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
                f.close()
        else:
            pass
    def bake(self, common_name: str, cert: str = "user", expiry_time_secs: int = 31536000) -> None:
        """
        Wrapper for creating certificate and all files needed
        :param common_name: Common Name of the the certificate
        :param cert: Type of cert being created "user" or "server"
        :param expiry_time_secs: length of time in seconds that the certificate is valid for, defaults to 1 year
        """
        keypath = MainConfig.certsPath+f"/{common_name}.key"
        pempath = MainConfig.certsPath+f"/{common_name}.pem"
        p12path = MainConfig.certsPath+f"/{common_name}.p12"
        self._generate_key(keypath)
        self._generate_certificate(common_name=common_name, pempath=pempath, p12path=p12path, expiry_time_secs=expiry_time_secs)
        if cert.lower() == "server":
            copyfile(keypath, keypath + ".unencrypted")

    @staticmethod
    def copy_server_certs(server_name: str = "pubserver") -> None:
        """
        copy all the server files with of a given name to the FTS server cert location
        :param server_name: Name of the server/IP address that was used when generating the certificate
        """
        """python37_fts_path = MainConfig.MainPath
        python38_fts_path = MainConfig.MainPath
        if os.path.exists(python37_fts_path):
            dest = python37_fts_path
        elif os.path.exists(python38_fts_path):
            dest = python38_fts_path
        else:
            print("Cannot Find FreeTAKServer install location, cannot copy")
            return None
        if not os.path.exists(dest + "/Certs"):
            os.makedirs(dest + "/Certs")"""
        copyfile("./" + server_name + ".key", MainConfig.keyDir)
        copyfile("./" + server_name + ".key", MainConfig.unencryptedKey)
        copyfile("./" + server_name + ".pem", MainConfig.pemDir)

    def generate_auto_certs(self, ip: str, copy: bool = False, expiry_time_secs: int = 31536000) -> None:
        """
        Generate the basic files needed for a new install of FTS
        :param ip: A string based ip address or FQDN that clients will use to connect to the server
        :param copy: Whether to copy server files to FTS expected locations
        :param expiry_time_secs: length of time in seconds that the certificate is valid for, defaults to 1 year
        """
        self.bake("pubserver", "server", expiry_time_secs)
        self.bake("user", "user", expiry_time_secs)
        if copy is True:
            self.copy_server_certs()
        generate_zip(server_address=ip)
