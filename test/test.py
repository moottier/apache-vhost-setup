import os, re, io, unittest, yaml
import make_apache_conf as MakeConf

class TestValidateInput(unittest.TestCase):
    FILE_NAME = "realFile.txt"
    NONEXIST_FILE_NAME = "nonexist.txt"

    @classmethod
    def setUpClass(cls):        
        with open(cls.FILE_NAME, "w+") as fin:
            fin.write("content")
        try:
            os.remove(cls.NONEXIST_FILE_NAME)
        except FileNotFoundError:
            pass

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.FILE_NAME)

    def testArgExists(self):
        self.assertTrue(MakeConf.validateInput(self.FILE_NAME))
        
class TestTextFileLineIterator(unittest.TestCase):
    FILE_NAME = '_lineItTest'
    LINE_1 = 'abcd\n'
    LINE_2 = 'efgh\n'

    @classmethod
    def setUpClass(cls):
        with open(cls.FILE_NAME, 'w+') as fout:
            fout.write(cls.LINE_1)
            fout.write(cls.LINE_2)
    
    @classmethod
    def tearDownClass(cls):
        os.remove(cls.FILE_NAME)

    def setUp(self):
        self.FILE = open(self.FILE_NAME, 'r')
        self.file_iter = MakeConf.TextFileLineIterator(self.FILE)

    def tearDown(self):
        self.FILE.close()

    def testReadlines(self):
        line_1 = next(self.file_iter)
        line_2 = next(self.file_iter)
        self.assertTrue(line_1 == self.LINE_1)
        self.assertTrue(line_2 == self.LINE_2)

class TestFileSubstitutor(unittest.TestCase):
    FILE_ITER = iter(['aabc', 'efgh', 'ijkl'])
    LINE_1_PATTERN = 'a'
    LINE_2_PATTERN = 'e{ blah }'
    LINE_3_PATTERN = 'e'

    @classmethod
    def setUpClass(cls):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass

    def testSubstituteTokens(self):
        finder = re.compile('({\s*.*?\s*})').findall
        mapper = lambda k: {'key':'val'}[k]        
        substitutor = MakeConf.TextFileSubstitutor(io.TextIOBase(), finder, mapper)

        test = '{key}, {key } asd {  key} {   key   }'
        new = substitutor.substitute_tokens(test)
        expected = 'val, val asd val val'

        self.assertTrue(new == expected)

    def testWrite(self):
        expected = '{key}, {key } asd {  key} {   key   }'
        
        fin = io.TextIOWrapper(io.BytesIO(expected.encode()))
        fout = io.TextIOWrapper(io.BytesIO())
        
        finder = lambda x: list()
        parser = mapper = lambda x: None
        substitutor = MakeConf.TextFileSubstitutor(fin, finder, mapper)
        
        substitutor._write_to_stream(fout)

        fout.seek(0)
        wrote = fout.readline()
        
        self.assertTrue(wrote == expected)
 
class TestMain(unittest.TestCase):
    def testMain(self):
        redirect_permanent =  "www.google.com"
        site               =  "www.andremottier.com"

        template           =  "<VirtualHost *:80>\n"
        template          +=  "    ServerName dev.andremottier.com\n"
        template          +=  "    Redirect permanent / {RedirectPermanent}\n"
        template          +=  "</VirtualHost>\n"

        yml                =  "www.andremottier.com:\n"
        yml               += f"    RedirectPermanent: {redirect_permanent}\n"
        yml               +=  "dev.andremottier.com:\n"
        yml               +=  "    RedirectPermanent: dev.google.com\n"

        expected           =  "<VirtualHost *:80>\n"
        expected          +=  "    ServerName dev.andremottier.com\n"
        expected          += f"    Redirect permanent / {redirect_permanent}\n"
        expected          +=  "</VirtualHost>\n"

        
        fin  = io.TextIOWrapper(io.BytesIO(template.encode()))
        fout = io.TextIOWrapper(io.BytesIO())
        yml  = yaml.safe_load(yml)

        MakeConf.TextFileSubstitutor(
            file_ = fin
            ,tk_finder = re.compile('({\s*.*?\s*})').findall
            ,tk_mapper = lambda match: yml[site][match]
        )._write_to_stream(fout)
        
        fout.seek(0)
        result = ''
        while True:
            line = fout.readline()
            if not line:
                break
            result += line

        self.assertTrue(expected == result)

if __name__ == '__main__':
    unittest.main()