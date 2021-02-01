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

def generate_zip(server_address: str = None, server_filename: str = "pubserver.p12",
                     user_filename: str = "user.p12", cert_password: str = MainConfig.password) -> None:
    """
    A Function to generate a Client connection Data Package (DP) from a server and user p12 file in the current
    working directory.
    :param server_address: A string based ip address or FQDN that clients will use to connect to the server
    :param server_filename: The filename of the server p12 file default is pubserver.p12
    :param user_filename: The filename of the server p12 file default is user.p12
    :param cert_password: The password for the certificate files

    """
    pref_file_template = Template("""<?xml version='1.0' standalone='yes'?>
    <preferences>
        <preference version="1" name="cot_streams">
            <entry key="count" class="class java.lang.Integer">1</entry>
            <entry key="description0" class="class java.lang.String">FreeTAKServer_{{ server }}</entry>
            <entry key="enabled0" class="class java.lang.Boolean">false</entry>
            <entry key="connectString0" class="class java.lang.String">{{ server }}:8089:ssl</entry>
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
                                     user_filename=user_filename, cert_password=cert_password)
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
    print("Generating Data Package: " + username + ".zip")
    copyfile(MainConfig.p12Dir, "./" + folder + "/" + server_filename)
    copyfile("./" + user_filename, "./" + folder + "/" + user_filename)
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
    print(f"Generating Main Data Package: {username}_DP.zip")
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

    def generate_ca(self) -> None:
        """
        Generate a CA certificate
        """
        if not os.path.exists(self.cakeypath):
            print("Cannot find CA locally so generating one")
            ca_key = crypto.PKey()
            ca_key.generate_key(crypto.TYPE_RSA, 2048)
            cert = crypto.X509()
            cert.get_subject().CN = "CA"
            cert.set_serial_number(0)
            cert.set_version(2)
            cert.gmtime_adj_notBefore(0)
            cert.gmtime_adj_notAfter(31536000)
            cert.set_issuer(cert.get_subject())
            cert.add_extensions([crypto.X509Extension(b'basicConstraints', False, b'CA:TRUE'),
                                 crypto.X509Extension(b'keyUsage', False, b'keyCertSign, cRLSign')])
            cert.set_pubkey(ca_key)
            cert.sign(ca_key, "sha256")

            f = open(self.cakeypath, "wb")
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, ca_key))
            f.close()
            print("CA key Stored Here: " + self.cakeypath)

            f = open(self.capempath, "wb")
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
            f.close()
            print("CA pem Stored Here: " + self.capempath)
        else:
            print("CA found locally, not generating a new one")

    def _generate_key(self, keypath: str) -> None:
        """
        Generate a new certificate key
        :param keypath: String based filepath to place new key, this should have a .key file extention
        """
        if os.path.exists(keypath):
            print("Certificate file exists, aborting.")
            print(keypath)
        else:
            print("Generating Key...")
            self.key.generate_key(crypto.TYPE_RSA, 2048)
            f = open(keypath, "wb")
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, self.key))
            f.close()
            print("Key Stored Here: " + keypath)

    def _generate_certificate(self, cn: str = "Server", pempath: str = MainConfig.pemDir, p12path: str = MainConfig.p12Dir) -> None:
        """
        Create a certificate and p12 file
        :param cn: Common Name for certificate
        :param pempath: String filepath for the pem file created
        :param p12path: String filepath for the p12 file created
        """
        if os.path.exists(pempath):
            print("Certificate File Exists, aborting.")
            print(pempath)
            return None
        cakey = crypto.load_privatekey(crypto.FILETYPE_PEM, open(self.cakeypath).read())
        capem = crypto.load_certificate(crypto.FILETYPE_PEM, open(self.capempath, 'rb').read())
        serialnumber = random.getrandbits(64)
        chain = (capem,)
        cert = crypto.X509()
        cert.get_subject().CN = cn
        cert.set_serial_number(serialnumber)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(315360000)
        cert.set_issuer(capem.get_subject())
        cert.set_pubkey(self.key)
        cert.set_version(2)
        cert.sign(cakey, "sha256")
        print('cert genned')
        p12 = crypto.PKCS12()
        p12.set_privatekey(self.key)
        p12.set_certificate(cert)
        p12.set_ca_certificates(tuple(chain))
        p12data = p12.export(passphrase=bytes(self.CERTPWD, encoding='UTF-8'))
        with open(p12path, 'wb') as p12file:
            p12file.write(p12data)
            print("P12 Stored Here: " + p12path)

        if os.path.exists(pempath):
            print("Certificate File Exists, aborting.")
            print(pempath)
        else:
            f = open(pempath, "wb")
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
            f.close()
            print("PEM Stored Here: " + pempath)

    def bake(self, cn: str, cert: str = "user") -> None:
        """
        Wrapper for creating certificate and all files needed
        :param cn: Common Name of the the certificate
        :param cert: Type of cert being created "user" or "server"
        """
        import os
        keypath = f"./{cn}.key"
        pempath = f"./{cn}.pem"
        p12path = f"./{cn}.p12"
        self._generate_key(keypath)
        self._generate_certificate(cn, pempath, p12path)
        os.remove(keypath)
        if cert.lower() == "server":
            copyfile(keypath, keypath + ".unencrypted")

    def bake_startup(self, cn: str = 'Server') -> None:
        self.generate_ca()
        self._generate_key(MainConfig.keyDir)
        print('key generated')
        self._generate_certificate(cn, MainConfig.pemDir, MainConfig.p12Dir)
        copyfile(MainConfig.keyDir, MainConfig.unencryptedKey)

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
        print("Copying ./" + server_name + ".key to :" + MainConfig.keyDir)
        copyfile("./" + server_name + ".key", MainConfig.keyDir)
        print("Done")
        print("Copying ./" + server_name + ".key to :" + MainConfig.unencryptedKey)
        copyfile("./" + server_name + ".key", MainConfig.unencryptedKey)
        print("Done")
        print("Copying ./" + server_name + ".pem to :" + MainConfig.pemDir)
        copyfile("./" + server_name + ".pem", MainConfig.pemDir)
        print("Done")
        """print("Copying ./ca.pem to :" + MainConfig.CA)
        copyfile("./ca.pem", MainConfig.CA)"""
        print("Done")

    def generate_auto_certs(self, ip: str, copy: bool = False) -> None:
        """
        Generate the basic files needed for a new install of FTS
        :param ip: A string based ip address or FQDN that clients will use to connect to the server
        :param copy: Whether to copy server files to FTS expected locations
        """
        self.bake("pubserver", "server")
        self.bake("user", "user")
        if copy is True:
            self.copy_server_certs()
        generate_zip(server_address=ip)

if __name__ == '__main__':
    """if True:
        AtakOfTheCerts().bake("testcert")
        generate_zip(user_filename='testcert.p12')"""
    VERSION = "0.3.5"
    help_txt = "This Python script is to be used to generate the certificate files needed for \n" \
               "FTS Version 1.3 and above to allow for SSL/TLS connections between Server and \n" \
               "Client.\n\n" \
               "This script works in the current working directory (the folder you are \n" \
               "currently in)\n\n" \
               "The .p12 files generated will need to be copied to ATAK clients\n" \
               "the default password set on the .p12 files is atakatak\n" \
               "The Server .key and .pem file will ne needed on the FTS server as per the MainConfig.py\n" \
               "The ca.pem is also needed for the MainConfig.py\n" \
               "the default password set on the .p12 files is atakatak, this can be overridden\n\n" \
               "Arguments:\n" \
               "-h --help : to open help\n" \
               "-v --version : to print the version number of the script\n" \
               "-p --password : to change the password for the p12 files from the default atakatak\n" \
               "-a --automated : to run the script in a headless mode to auto generate ca,server and user certs " \
               "for a fresh install\n" \
               "-c --copy : Use this in conjunction with -a to copy the server certs needed into the default location for FTS\n" \
               "-i --ip : The IP address of the server that clients will be accessing it on\n\n"
    AUTO = False
    COPY = False
    IP = False
    CERTPWD = "atakatak"
    cmd_args = sys.argv
    arg_list = cmd_args[1:]
    stort_opts = "avhci:p:"
    long_opts = ["automated", "version", "help", "copy", "ip", "password"]
    args, values = getopt.getopt(arg_list, stort_opts, long_opts)
    for current_arg, current_val in args:
        if current_arg in ("-h", "--help"):
            print(help_txt)
            exit(1)
        if current_arg in ("-v", "--version"):
            print(VERSION)
            exit(1)
        if current_arg in ("-p", "--password"):
            CERTPWD = current_val
        if current_arg in ("-a", "--automated"):
            AUTO = True
        if current_arg in ("-c", "--copy"):
            COPY = True
        if current_arg in ("-i", "--ip"):
            IP = current_val

    with AtakOfTheCerts() as aotc:
        aotc.generate_ca()
    if AUTO:
        if IP is False:
            IP = str(input("Enter IP address or FQDN that clients will use to connect to FTS: "))
        with AtakOfTheCerts() as aotc:
            aotc.generate_auto_certs(copy=COPY, ip=IP)
    else:
        server_p12 = None
        users_p12 = []
        server_question = input("Would you like to generate a server certificate? y/n ")
        if server_question.lower() == "y":
            with AtakOfTheCerts(CERTPWD) as aotc:
                IP = str(input("Enter IP address or FQDN that clients will use to connect to FTS: "))
                aotc.bake(cn=IP, cert="server")
                server_p12 = "./" + IP + ".p12"
            copy_question = input("Would you like to copy the server certificate files where needed for FTS? y/n ")
            if server_question.lower() == "y":
                aotc.copy_server_certs(server_name=IP)
        user_question = input("Would you like to generate a user certificate? y/n ")
        if user_question.lower() == "y":
            while True:
                with AtakOfTheCerts(CERTPWD) as aotc:
                    cn = input("Username: ")
                    if len(cn) == 0:
                        break
                    aotc.bake(cn, cert="user")
                    users_p12.append("./" + cn + ".p12")
                    cont = input("Generate another? y/n ")
                    if cont.lower() != "y":
                        break
            generate_zip_question = input(
                "Would you like to generate Data Packages for each user just created? y/n ")
            if generate_zip_question.lower() == "y":
                while server_p12 is None:
                    server_p12 = input("Enter path to server p12 file e.g ./pubserver.p12 : ")
                while IP is False:
                    IP = str(input("Enter IP address or FQDN that clients will use to connect to FTS: "))
                for user in users_p12:
                    generate_zip(server_address=IP, server_filename=server_p12, user_filename=user)