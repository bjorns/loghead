import kuvio

def main():
	kuvio.init('example/config/jsonout.yaml')
	kuvio.info("Hello, world!");

if __name__ == '__main__':
	main()
