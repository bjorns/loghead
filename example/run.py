from sys import stderr
from time import sleep
import kuvio

def main():
	kuvio.init('example/config/jsonout.yaml')
	while True:
		kuvio.debug("Hello, world!");
		kuvio.info("Hello, world!");
		kuvio.notice("Hello, world!");
		kuvio.warning("Hello, world!");
		kuvio.error("Hello, world!");
		stderr.write('\n')
		sleep(1)

if __name__ == '__main__':
	main()
