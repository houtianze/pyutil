import os
import sys
import subprocess as sub
import re
import inspect

def lineno():
	""" Returns the current line number in our program. """
	return inspect.currentframe().f_back.f_lineno

def pt(msg):
	""" print with trace info """
	print (msg + '\nLine: ' + str(inspect.currentframe().f_back.f_lineno))

def usage():
	print('Verify a file signature and retrieve the key from '
		'a keyserver if the key ID is not found in user\'s keyring.\n\n'
		'Usage: ' + os.path.basename(sys.argv[0])
		+ ' <sig>\n'
		'  <sig>  The signature file.'
	)

def main():
	if len(sys.argv) != 2:
		usage()
		return 1
	else:
		if os.system('gpg --version > nul') != 0:
			pt('Error: Can\'t fork gpg! Did you have GnuPG installed?\nAbort.')
			return 1

		p = sub.Popen('gpg --verify ' + sys.argv[1]
				, stdout=sub.PIPE, stderr=sub.PIPE
			)
		stdoutdata, stderrdata = p.communicate()
		print stdoutdata
		print stderrdata

		# signature verification succeeded
		if p.returncode == 0:
			return 0
		else:
			# signature verification failed, check about the failure reason
			m = re.search(r'(?im)^gpg:\s*Signature.*?ID\s*([0-9a-fA-F]+)\s*$', stderrdata)
			# can't find the key ID in the gpg error output, can't continue
			if m is None or m.group(1) is None:
				pt('Error: Signature verification failed weirdly!\nAbort.')
				return 1
			else:
				# the key ID is found , save it.
				keyid = m.group(1)
				# check if the error is due to 'public key not found' error.
				m = re.search(r'(?im)^gpg:.*?public\s*key\s*not\s*found\s*$', stderrdata)
				# no, the error is not 'public key not found', abort.
				if m is None:
					pt('Error: Signature verification failed weirdly!\nAbort.')
					return 1
				# good, the error is 'public key not found', continue
				else:
					# try to receive the publick key from the keyserver
					if os.system('gpg --recv-keys 0x' + keyid) != 0:
						# shoot, i can't retrieve the keys, abort.
						pt('Error: Can\'t retrieve the public key ID ' + keyid
							+ '! Is this computer connected to the internet?\nAbort.'
						)
						return 1
					else:
						# good, key received, try to re-verify the signature.
						print '\n==== Re-verify the signature using the key just retrieved. ===\n'
						if os.system('gpg --verify ' + sys.argv[1]) != 0:
							# shoot, still can't verify the signature, i give up
							pt('Error: Can\'t verify the signagure even after'
								' receiving the public key.\nI don\'t know what else'
								' I can do to verify the signature. I give up.'
							)
							return 1
							# yeah, finally, we are done, report this with a '0' code
						else:
							return 0
# end of the main() function

main()

