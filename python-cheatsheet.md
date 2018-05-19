# OO

## Basic Modern Class

    class ClassName(object):

        def __init__(self, foo):
            self.foo = foo

        @classmethod
        def bar(cls, arg):
            ...

## Super Call

    def foo(self, bar):
        return super(MyClass, self).foo(bar)
        
## Recursive Subclass Map

    @classmethod
    def subclass_map(cls):
        map = {c.__name__: c for c in cls.__subclasses__()}
        for subclass in map.values():
            map.update(subclass.subclass_map())
        return map


# HTTP

## HEAD request

    request = urllib2.Request(url)
    request.get_method = lambda : 'HEAD'
    response = urllib2.urlopen(request)
    print response.info()['Last-Modified']

## Slurp page

    url = 'http://www.sno.phy.queensu.ca/~phil/exiftool/'
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    data = response.read()

# Installing Modules

## PIP

    http://www.pip-installer.org/en/latest/installing.html
    curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | sudo python
    
    sudo -H python -m ensurepip

## SciPy

    http://fonnesbeck.github.com/ScipySuperpack/


# Date/Time

## Sleep

    time.sleep(seconds)

## Now

    dt = datetime.datetime.now()

## Time some code

    t1 = datetime.datetime.now()
    xxx
    t2 = datetime.datetime.now()
    print '{:0.1f}s'.format((t2 - t1).total_seconds())

## Convert RFC-style date/time to datetime

    modification_time = datetime.datetime(*email.utils.parsedate(urllib2_response.info()['Last-Modified'])[:6])
    
## Convert ISO timestamp to datetime

    datetime.datetime.strptime("2008-09-03T20:56:35.450686Z", "%Y-%m-%dT%H:%M:%S.%fZ")

## Touch file modification with datetime

    timestamp = time.mktime(some_datetime.timetuple())
    os.utime(file_path, (timestamp, timestamp))

## Get file modification timestamp as datetime

    datetime.datetime.fromtimestamp(os.stat(path).st_mtime)

## Time delta between datetimes

    t1 = datetime.datetime.now()
    ...
    age_seconds = (datetime.datetime.now() - t1).seconds

## Human Readable Timestamp

    datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

## Datetime instance to Unix Timestamp

    import datetime
    date = datetime.datetime.utcfromtimestamp(0)

    def unix_time_millis(dt):
        return (dt - epoch).total_seconds() * 1000.0

## Unix timestamp to UTC and Local Time

    import datetime
    utcdatetime = datetime.datetime.utcfromtimestamp(unix_timestamp)
    localdatetime = datetime.datetime.fromtimestamp(unix_timestamp)

## Get Computer's UTC Offset

    http://stackoverflow.com/a/3168394/182781

# Exceptions

## Raise Exception

    raise Exception('foo')

## Less noisy exception errors

    try:
        ...
    except Exception as e:
        print ''.join(traceback.format_exception(*sys.exc_info())[1:-2])
        print ANSIColor.wrap(str(e), color=ANSIColor.red)


# Shell Command

    status = subprocess.call(['git', 'status', '--porcelain', self.path])
    status = subprocess.check_call(['git', 'status', '--porcelain', self.path])
    output = subprocess.check_output(['git', 'status', '--porcelain', self.path])

## sudo authenticate

    def validate_sudo():
        pwd = ''
        for i in range(5):
            sp = subprocess.Popen(['sudo', '-S', '-v'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            sp.communicate(pwd + '\n')
            if sp.returncode == 0:
                return True
            pwd = getpass.getpass()
        return False

## relaunch with sudo

    @classmethod
    def ensure_superuser(cls):
        if os.getuid() != 0:
            print 'Relaunching with sudo...'
            os.execv('/usr/bin/sudo', ['/usr/bin/sudo'] + sys.argv)

# Context Manager for `with` Statement

    @contextlib.contextmanager
    def chdir_to_path(self, path):
        oldwd = os.getcwd()
        os.chdir(path)
        try:
            yield
        except:
            os.chdir(oldwd)
            raise

        os.chdir(oldwd)
    
    def foo(self):
        with self.chdir_to_path(self.path):
            foo


# Logging

## Basic Logging Setup

    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    logging.debug('foo')
    logging.warning('foo')
    logging.error('foo')

Based on args:

    if self.args.verbose:
        logging.basicConfig(level=logging.DEBUG)


# Files

## Slurp File Contents

    with open('x.txt') as x: f = x.read()
    with open('x.txt') as x: f = x.readlines()

## Walking File System Trees

    for dirpath, dirnames, filenames in os.walk(path, topdown=True):
        ...

## Get directory contents

    contents = os.listdir(path)


# Autopep

    pep8 file.py

## diff

    autopep8 -d --ignore E501 file.py

## in-place

    autopep8 -i --ignore E501 file.py


# Regex

## Single match

    match = re.search(r'pattern', string)
    print match.group(1)

## Iterate

    for match in re.finditer(r'pattern', string)
        print match.group(1)

## Replace

    re.sub(r'pattern', replace, string)


# String Manipulations

## Split string into lines

    str.splitlines()

## Convert camel case to underscore

    def underscore_to_camel_case(underscore_value):
        return re.sub(r'(\w)_(\w)', lambda match: match.group(1) + match.group(2).upper(), underscore_value)

    def camel_case_to_underscore(camelcase_value):
        return re.sub(r'([a-z])([A-Z])', lambda match: match.group(1) + '_' + match.group(2).lower(), camelcase_value)

# String Formatting

## Fixed-width aligned placeholder

    'foo [{:<5}] bar'.format(value)

## Parameter-defined, fixed-width placeholder

    'foo [{1:<{0}}] bar'.format(field_width, value)

# Empty a list in-place

    del list[:]

http://docs.python.org/2/tutorial/datastructures.html#the-del-statement


# Iterate over a dictionary's keys and values

    for k, v in globals().items():
        ...


# Iterate over a collection with an index

    for index, item in enumerate(iterable):
        ...


# Version Number Sorting

    versions = [tuple(map(int, (i.split('.')))) for i in version_strings]
    sorted(versions, cmp)

Support in pkg_resources (http://stackoverflow.com/questions/11887762/compare-version-strings):

    import pkg_resources
    pkg_resources.parse_version('1.2.3') < pkg_resources.parse_version('4.5.6')


# Dictionary get with fallback

    dict.get(key, default)


# Object get with fallback

    getattr(object, key, default)


# Iterate over slices

    for i in range(0, len(items), 50):
        x = items[i:i + 50]


# Encoding / Unicode / Charsets

## Decode Hex Chars

    'cafebabe'.decode('hex')
    binascii.unhexlify('cafebabe')
    binascii.a2b_hex('cafebabe')

## Encode Hex Chars

    binascii.b2a_hex(binary)
    binascii.hexlify(binary)

# Shell Script Inline Python script

    python <<EOF
    from IPython.external.mathjax import install_mathjax
    install_mathjax()
    EOF


# Get file system path to current file

    os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# Plist parsing with plistlib

    data = plistlib.readPlistFromString(stdoutdata)

# XML with ElementTree

    import xml.etree.ElementTree

## Parse File

    tree = xml.etree.ElementTree.parse(path)
    
## Parse String

    tree = xml.etree.ElementTree.fromstring(xml_string)

# PyObjc

## Loading Frameworks - old

http://quickies.seriot.ch/index.php?id=180

    import objc

    objc.loadBundle("InstantMessage", globals(),
                    bundle_path=objc.pathForFramework(u'/System/Library/Frameworks/InstantMessage.framework'))

    service = IMService.serviceWithName_('AIM')
    print service.peopleWithScreenName_('pikswiss')


## Loading Frameworks - Since Mac OS X 10.5

    from AddressBook import *

    book = ABAddressBook.sharedAddressBook()
    print book.me()

## Replace otool on OS X Systems without Xcode

The `macholib` module can replace otool for some purposes, for example getting a binary's UUID:

Replace

    otool -l /Applications/Foo.app/Contents/MacOS/Foo | grep uuid

with

    python -c 'import macholib.MachO, uuid, sys; binary = macholib.MachO.MachO(sys.argv[1]); uuid_command, = [c[1] for c in binary.headers[0].commands if type(c[1]) == macholib.mach_o.uuid_command]; print uuid.UUID(bytes=uuid_command.uuid)' /Applications/Foo.app/Contents/MacOS/Foo

or

    python - /Applications/Foo.app/Contents/MacOS/Foo <<-EOF
        import macholib.MachO, uuid, sys
        binary = macholib.MachO.MachO(sys.argv[1])
        uuid_command, = [c[1] for c in binary.headers[0].commands if type(c[1]) == macholib.mach_o.uuid_command]
        print uuid.UUID(bytes=uuid_command.uuid)
    EOF

# C API

## Print description of an object in an embedded Python 3 interpreter when attached with LLDB:

    call (char *)PyUnicode_AsUTF8((void *)PyObject_Repr($arg2))