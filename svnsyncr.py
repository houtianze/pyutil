import sys
import os
import os.path
import subprocess as sub
import re
import urllib
import inspect

def lineno():
	""" Returns the current line number in our program. """
	return inspect.currentframe().f_back.f_lineno

def pt(msg):
	""" print with trace info """
	print (msg + '\nLine: ' + str(inspect.currentframe().f_back.f_lineno))

def usage():
	print('Svn simple batch script.\n\n'
		'Usage: ' + os.path.basename(sys.argv[0])
		+ ' <ToPath> <FromRepo>\n'
		'  <ToPath>    The destination repo path (to be created).\n'
		'  <FromRepo>  The source repo URL.\n'
	)

def main():
	if len(sys.argv) != 3:
		usage()
		return 1
	else:
		dest_path = sys.argv[1]
		# urllib doesn't produce the 'file:' prefix, and converts 'C:' to 'C|',
		# not sure who is more standardised.
		dest_url = 'file:' + urllib.pathname2url(os.path.abspath(sys.argv[1])).replace('|', ':')
		src_path = urllib.url2pathname(sys.argv[2])
		src_url = sys.argv[2]

		if os.system('svn --version > nul') != 0:
			pt('Error: Can\'t fork svn! Did you have subversion installed?\nAbort.')
			return 1

		if os.system('svnadmin create ' + dest_path) != 0:
			pt('Error: Can\'t create dest repo!\nAbort.')
			return 1

		if os.system('echo @echo off > ' + dest_path + '/hooks/pre-revprop-change.bat') != 0:
			pt('Error: Can\'t create the pre-revprop-change.bat!\nAbort.')
			return 1

		if os.system('svnsync init ' + dest_url + ' ' + src_url) != 0:
			pt('Error: Can\'t init the destination repo with the source repo!\Abort.')
			return 1

		if os.system('svnsync sync ' + dest_url) != 0:
			pt('Error: Can\'t sync the destination url!\Abort.')
			return 1
# end of the main() function

main()

