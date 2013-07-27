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


# Installing Modules

## PIP

    http://www.pip-installer.org/en/latest/installing.html
    curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | sudo python

## SciPy

    http://fonnesbeck.github.com/ScipySuperpack/


# Time

## Sleep

    time.sleep(seconds)

## Time some code

    t1 = datetime.datetime.now()
    xxx
    t2 = datetime.datetime.now()
    print '{:0.1f}s'.format((t2 - t1).total_seconds())


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


# Files

## Slurp File Contents

    with open('x.txt') as x: f = x.read()
    with open('x.txt') as x: f = x.readlines()

## Walking File System Trees

    for (dirpath, dirnames, filenames) in os.walk(args.root_path, topdown=True):
        ...


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


# Split string into lines

    str.splitlines()


# Empty a list in-place

    del list[:]

http://docs.python.org/2/tutorial/datastructures.html#the-del-statement


# Iterate over a dictionary's keys and values

    for k, v in globals().items():
        ...


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


# Shell Script Inline Python script

    python <<EOF
    from IPython.external.mathjax import install_mathjax
    install_mathjax()
    EOF


# Get file system path to current file

    os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

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
