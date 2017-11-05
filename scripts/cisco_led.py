#!/usr/bin/python

#Importing modules
import paramiko
import sys
import time
import urllib2
import urllib

#setting parameters like host IP, username, passwd and number of iterations to gather cmds

queryIP = sys.argv[1]
queryUser = sys.argv[2]
queryPass = sys.argv[3]

HOST = queryIP
USER = queryUser
PASS = queryPass
ITERATION = 1

#A function that logins and execute commands
def fn():
  client1=paramiko.SSHClient()
  #Add missing client key
  client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  #connect to switch
  client1.connect(HOST,username=USER,password=PASS)
  print "SSH connection to %s established" %HOST
  #Gather commands and read the output from stdout
  stdin, stdout, stderr = client1.exec_command('led flash 30\n')
  print stdout.read()
  client1.close()
  print "Logged out of device %s" %HOST

#for loop to call above fn x times. Here x is set to 3
for x in xrange(ITERATION):
  fn()
  print "%s Iteration/s completed" %(x+1)
  print "********"
  time.sleep(5) #sleep for 5 seconds

