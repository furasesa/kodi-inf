import unittest
from kodiinf import Kodi, Inf

class KodiInfTest (unittest.TestCase):
    #basic unittest
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_kodi_connection (self):
        k = Kodi("localhost:8080","","",True)
        # self.assertTrue(k.checkConnection())




if __name__ == "__main__" :
    unittest.main()