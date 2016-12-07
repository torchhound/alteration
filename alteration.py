import hashlib
import requests
import sqlite3
import argparse

def getArgs():
	parser = argparse.ArgumentParser(description="Detect website changes")
	parser.add_args("website", help="The website to either add or check")
	parser.add_args("-a", action="store_true", help="Add a website to the DB")
	parser.add_args("-c", action="store_true", help="Check a site against a previous record")
	return parser.parse_args(argv)

def getHash(website):
	try:
		hashObj = hashlib.md5(website)
		return hashObj.hexdigest()
	except Exception as e:
		print(e)
		return False

def requestSite(website):
	try:
		response = request.get(website)
		return response.content
	except requests.exceptions.RequestException as e:
		print("Requests error: {}".format(e))
		return False
	except Exception as e:
		print("Other error: {}".format(e))
		return False

def insertSite(website, webHash):
	try:
		conn = sqlite3.connect("alteration.db")
		cur = conn.cursor()
		#cur.execute("CREATE table IF NOT EXISTS")
		#values = [website, webHash]
		#cur.execute("INSERT INTO (website) (webHash) VALUES (?,?)", values)
		conn.commit()
		conn.close()
		return True
	except Exception as e:
		print(e)
		return False

def checkSite(website, webHash):
	try:
		conn = sqlite3.connect("alteration.db")
		cur = conn.cursor()#check if table exists then check latest hash value
		if :#does not exist
			return 3
		elif :#has changed
			return 2
		elif :#has not changed
			return 1
		conn.commit()
		conn.close()
		return False
	except Exception as e:
		print(e)
		return False

if __name__ == "__main__":
	args = getArgs()
	if args.a:
		if insertSite(args.website, getHash(requestSite(args.website))) == True:
			print("{} added".format(args.website))
		else:
			print("Something went wrong")
	elif args.c:
		if checkSite(args.website, getHash(requestSite(args.website))) == 1:
			print("{} has not changed".format(args.website))
		elif checkSite(args.website, getHash(requestSite(args.website))) == 2:
			print("{} has changed".format(args.website))
		elif checkSite(args.website, getHash(requestSite(args.website))) == 3:
			print("{} was not found in the database please add it with the -a flag".format(args.website))
		else:
			print("An unexpected error occured")
	else:
		print("An unknown error has occured")