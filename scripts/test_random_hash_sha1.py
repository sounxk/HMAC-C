import binascii
import hashlib
import os
import random
import string
import subprocess
import sys
import time
import threading
import Queue

BIN_PATH = "./build/test_random_sha1"

NTHREADS = 2
NTESTS = 10
NBYTES = 20

global still_making_input
still_making_input = True
tests = Queue.Queue()
failures = list()


#
# Helper functions
#


def random_string(len):
  """ Returns a random string of length 'len' consisting of upper + lowercase letters and digits """
  ret = list()
  rand = random.Random()

  for i in xrange(len):
    ret.append("%.02x" % rand.randint(0, 255))

  return "".join(ret)

  #selector = string.ascii_uppercase + string.ascii_lowercase + string.digits
  #return ''.join(random.choice(selector) for _ in range(len))


def run_test(input_string, expected_output):
  """ Run the C test program, comparing the Python SHA1 implementation to the one in C """
  return subprocess.call([BIN_PATH, input_string, expected_output])


def run_in_thread(target_function):
  t = threading.Thread(target=target_function)
  t.start()
  t.join()


def run_tests():
  while (tests.empty() == False) or (still_making_input == True):
    try:
      inp, out = tests.get(True, 0)
      retcode = run_test(inp, out)
      if retcode != 0:
        failures.append([inp, out])
        sys.stdout.write("X")
      else:
        sys.stdout.write(".")
      sys.stdout.flush()
    except Queue.Empty:
      time.sleep(0.1)


def make_test_input():

  # Create input and expected output
  for i in xrange(NTESTS):
    test_input = random_string(NBYTES)
    #test_input = bytearray(random.getrandbits(8) for _ in xrange(8))
    sha = hashlib.sha1()
    sha.update(binascii.a2b_hex(test_input))
    test_output = sha.hexdigest()
    tests.put([test_input, test_output])

#
# Test driver
#
if __name__ == "__main__":

  # Read NTESTS from stdin 
  if len(sys.argv) > 1:
    if sys.argv[1].isdigit():
      NTESTS = int(sys.argv[1])

  # Read NTHREADS from stdin
  if len(sys.argv) > 2:
    if sys.argv[2].isdigit():
      NTHREADS = int(sys.argv[2])

  # Read NBYTES from stdin
  if len(sys.argv) > 3:
    if sys.argv[3].isdigit():
      NBYTES = int(sys.argv[3])


  # Tell user what is going to happen
  print("")
  str_threads = "thread"
  if NTHREADS > 1:
    str_threads += "s"
  print("Running tests on %d %s SHA1-hashing %d random %d-byte strings," % (NTHREADS, str_threads, NTESTS, NBYTES))
  print("comparing the results to the output of Python's hashlib.sha1().")
  print("")

  # Spawn thread to create test inputs in the background, instead of blocking here...
  t_mk_input = threading.Thread(target=make_test_input)
  t_mk_input.start()
 

  # Create new threads
  threadlist = list()
  for i in range(NTHREADS):
    threadlist.append(threading.Thread(target=run_tests))

  # Run all threads
  for i, thread in enumerate(threadlist):
    thread.start()

  # Wait for input-creation to complete
  t_mk_input.join()

  still_making_input = False

  # Wait for threads to complete
  for i, thread in enumerate(threadlist):
    thread.join()


  print(" ")
  print(" ")
  print("%d/%d tests succeeded." % (NTESTS - len(failures), NTESTS))
  print(" ")

  if len(failures) > 0:
    error_log = open("error_log.txt", "a")
    for fail_input, fail_output in failures:
      error_log.write("./build/test_random2 %s %s %s" % (fail_input, fail_output, os.linesep))
    error_log.close()
    


