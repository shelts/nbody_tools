import os

#This program releases N-Body aside from copying version.xml and updating versions.

version = raw_input("Enter release version.\n")

Linux64Tag = "x86_64-pc-linux-gnu"   
Linux64MTTag = "x86_64-pc-linux-gnu__mt" 

#Linux32Tag = "i686-pc-linux-gnu"
#Linux32MTTag = "i686-pc-linux-gnu__mt"

MacTag = "x86_64-apple-darwin"
MacMTTag = "x86_64-apple-darwin__mt"

Windows64Tag = "windows_x86_64"
Windows64MTTag = "windows_x86_64__mt"

#Windows32Tag = "windows_intelx86"
#Windows32MTTag = "windows_intelx86__mt"

#tagList = [Linux64Tag, Linux64MTTag, Linux32Tag, Linux32MTTag, MacTag, MacMTTag, Windows64Tag, Windows64MTTag, Windows32Tag, Windows32MTTag]

tagList = [Linux64Tag, Linux64MTTag, MacTag, MacMTTag, Windows64Tag, Windows64MTTag]


os.system("mkdir /boinc/milkyway/apps/milkyway_nbody/" + version)
cdir = os.curdir

crypt_prog = "/boinc/milkyway/bin/crypt_prog"
private_key = "/boinc/milkyway/keys/code_sign_private"
public_key = "/boinc/milkyway/keys/code_sign_public"

for tag in tagList:

    os.system("mkdir /boinc/milkyway/apps/milkyway_nbody/" + version +"/" + tag)
    
    binary = "milkyway_nbody_" + version + "_" + tag
    dest = "/boinc/milkyway/apps/milkyway_nbody/" + version + "/" + tag + "/milkyway_nbody_" + version + "_" + tag
    
    if (tag.startswith("windows")):
        binary = binary + ".exe"
        dest = dest + ".exe"

    sig = dest + ".sig"

    os.system("sudo chown boinc:boinc " + binary)
    os.system("sudo cp " + binary + " " + dest)
    os.system("sudo -u boinc " + crypt_prog + " -sign " + dest + " " + private_key + " > " + sig)
    os.system("sudo chown boinc:boinc " + sig)
    os.system("sudo -u boinc " + crypt_prog + " -verify " + dest + " " + sig + " " + public_key)
