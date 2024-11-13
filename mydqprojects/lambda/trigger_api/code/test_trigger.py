import unittest
import trigger 
 
class TestFunction(unittest.TestCase):
 
    def setUp(self):
        pass

    def test_get_parameter(self):
        self.assertEqual(trigger.get_parameter('STATE_MACHINE_NAME'),
                         'airports-input-state-machine')

if __name__ == '__main__':
    unittest.main()
