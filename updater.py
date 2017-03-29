# PyWeather Updater - 0.5 beta
# (c) 2017, o355, GNU GPL 3.0


import sys
import json
import urllib.request
import codecs
import shutil
import configparser
reader = codecs.getreader("utf-8")
from colorama import Fore, Style, init
init()

config = configparser.ConfigParser()
config.read('storage//config.ini')

try:
    verbosity = config.getboolean('VERBOSITY', 'updater_verbosity')
    jsonVerbosity = config.getboolean('VERBOSITY', 'updater_jsonverbosity')
except:
    print("Couldn't load your config file. Make sure your spelling is correct.")
    print("Setting variables to default...")
    print("")
    verbosity = False
    jsonVerbosity = False
    
    
if (verbosity == True or jsonVerbosity == True):
    import logging
    logger = logging.getLogger('pyweather_updater_0.4.2beta')
    logger.setLevel(logging.DEBUG)
    logformat = '%(asctime)s | %(levelname)s | %(message)s'
    logging.basicConfig(format=logformat)

buildnumber = 50
buildversion = "0.5 beta"
if verbosity == True:
    logger.debug("buildnumber: %s ; buildversion: %s" %
                (buildnumber, buildversion))
print("Checking for updates. This shouldn't take that long.")
try:
    versioncheck = urllib.request.urlopen("https://raw.githubusercontent.com/o355/pyweather/master/updater/versioncheck.json")
    if verbosity == True:
        logger.debug("versioncheck: %s" % versioncheck)
except:
    if verbosity == True:
        logger.warn("Couldn't check for updates! Is there an internet connection?")
    print(Style.BRIGHT + Fore.RED + "Couldn't check for updates.")
    print("Make sure GitHub user content is unblocked, and you have an internet connection.")
    print("Error 54, updater.py")
    print("Press enter to exit.")
    input()
    sys.exit()
    
versionJSON = json.load(reader(versioncheck))
if jsonVerbosity == True:
    logger.debug("versionJSON: %s" % versionJSON)
if verbosity == True:
    logger.debug("Loaded versionJSON with reader %s" % reader)
version_buildNumber = float(versionJSON['updater']['latestbuild'])
version_latestVersion = versionJSON['updater']['latestversion']
version_latestURL = versionJSON['updater']['latesturl']
version_latestFileName = versionJSON['updater']['latestfilename']
if verbosity == True:
    logger.debug("version_buildNumber: %s ; version_latestVersion: %s"
                % (version_buildNumber, version_latestVersion))
    logger.debug("version_latestURL: %s ; verion_latestFileName: %s"
                % (version_latestURL, version_latestFileName))
version_latestReleaseDate = versionJSON['updater']['releasedate']
if verbosity == True:
    logger.debug("version_latestReleaseDate: %s" % version_latestReleaseDate)
if buildnumber >= version_buildNumber:
    if verbosity == True:
        logger.info("PyWeather is up to date.")
        logger.info("local build (%s) >= latest build (%s)"
                    % (buildnumber, version_buildNumber))
    print("")
    print(Style.BRIGHT + Fore.GREEN + "PyWeather is up to date!")
    print("You have version: " + Fore.CYAN + buildversion)
    print(Fore.GREEN + "The latest version is: " + Fore.CYAN + version_latestVersion)
    print(Fore.GREEN + "Press enter to exit.")
    input()
    sys.exit()

elif buildnumber < version_buildNumber:
    print("")
    if verbosity == True:
        logger.warn("PyWeather is NOT up to date.")
        logger.warn("local build (%s) < latest build (%s)"
                    % (buildnumber, version_buildNumber))
    print(Fore.RED + Style.BRIGHT + "PyWeather is not up to date! :(")
    print(Fore.RED + "You have version: " + Fore.CYAN + buildversion)
    print(Fore.RED + "The latest version is: " + Fore.CYAN + version_latestVersion)
    print(Fore.RED + "And it was released on: " + Fore.CYAN + version_latestReleaseDate)
    print("")
    print(Fore.RED + "Would you like to download the latest version?" + Fore.YELLOW)
    downloadLatest = input("Yes or No: ").lower()
    if verbosity == True:
        logger.debug("downloadLatest: %s" % downloadLatest)
    if downloadLatest == "yes":
        print("")
        if verbosity == True:
            logger.debug("Downloading latest version...")
        print(Fore.YELLOW + "Downloading the latest version of PyWeather...")
        try:
            with urllib.request.urlopen(version_latestURL) as update_response, open(version_latestFileName, 'wb') as update_out_file:
                if verbosity == True:
                    logger.debug("update_response: %s ; update_out_file: %s" %
                                 (update_response, update_out_file))
                shutil.copyfileobj(update_response, update_out_file)
        except:
            if verbosity == True:
                logger.warn("Couldn't download the latest version!")
                logger.warn("Is the internet online?")
            print(Fore.RED + "Couldn't download the latest version.")
            print("Make sure GitHub user content is unblocked, "
                    + "and you have an internet connection.")
            print("Error 55, updater.py")
            print("Press enter to exit.")
            input()
            sys.exit()
            
        if verbosity == True:
            logger.debug("Latest version was saved, filename: %s"
                        % version_latestFileName)
        print(Fore.YELLOW + "The latest version of PyWeather was downloaded " +
                    "to the base directory of PyWeather, and saved as " +
                    Fore.CYAN + version_latestFileName + Fore.YELLOW + ".")
        print("Press enter to exit.")
        input()
        sys.exit()
        
    elif downloadLatest == "no":
        if verbosity == True:
            logger.debug("Not downloading the latest version.")
        print(Fore.YELLOW + "Not downloading the latest version of PyWeather.")
        print("For reference, you can download the latest version of PyWeather at:")
        print(Fore.CYAN + version_latestURL)
        print(Fore.YELLOW + "Press enter to exit.")
        input()
        sys.exit()
    else:
        if verbosity == True:
            logger.warn("Input could not be understood!")
        print(Fore.GREEN + "Could not understand what you said.")
        print(Fore.GREEN + "Press enter to exit.")
        input()
        sys.exit()
else:
    if verbosity == True:
        logger.error("PW updater failed. Build comparison below.")
        try:
            logger.error("local build: %s ; updater build: %s"
                        % (buildnumber, version_buildNumber))
        except:
            logger.error("Variables are corrupted, or a typo was made.")
            logger.error("Trying to list variables 1 more time...")
            try:
                logger.error("buildnumber: %s" % buildnumber)
            except:
                logger.error("Variable buildnumber is corrupt.")
    print(Style.BRIGHT + Fore.RED + "PyWeather Updater ran into an error, and couldn't compare versions.")
    print(Fore.RED + "Error 53, updater.py")
    print("Press enter to exit.")
    input()
    sys.exit()