from asyncio import wait_for
from multiprocessing.connection import wait
from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

@patch('core.management.commands.wait_for_db.Command.check') ## --> patched_check
class Commandtest(SimpleTestCase):
    ''' Test commands '''
    
    def test_wait_for_db(self, patched_check):
        ''' Tests waiting for database until it is ready'''
        patched_check.return_value = True
        
        call_command('wait_for_db')  ## call the function checking it exists
        
        patched_check.assert_called_once_with(databases=['default'])
        ## check that the command in the decorator
        ## is called using the 'default' parameter

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep,patched_check):
        ''' Tests for database when getting OperationalError.'''
        patched_check.side_effect = [Psycopg2Error] * 2 +  \
            [OperationalError] * 3 + [True]
            
        call_command('wait_for_db')
        
        self.assertEqual(patched_check.call_count,6)
        patched_check.assert_called_with(databases=['default'])
        
        
