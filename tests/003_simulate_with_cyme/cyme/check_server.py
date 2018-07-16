def main():
    import urllib2
    try:
        response = urllib2.urlopen("http://localhost:63712/ping").read()
        response = response.decode('utf-8')
    except:
        response = 'bad request'
    if response in 'pinged':
        print('The Server is up')
        return 0
    else:
        print('The server is not up yet')
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(main())
    