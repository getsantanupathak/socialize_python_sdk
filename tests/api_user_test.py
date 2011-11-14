try:
    from local_settings import version, host, key, secret, user_id , app_id, delete_app, api_user_id
except:
    print 'unable to load local settings using-> settings.py'
    from settings import version, host, key, secret, user_id , app_id, delete_app ,api_user_id

from socialize.client import Partner
from tests.base import SocializeTest

class ApiUserTest(SocializeTest):

    '''
        find()
    '''   
    def test_init(self):
        '''
            ** test init api_user by api_user_id
        '''
        api_user = self.partner.api_user(api_user_id)
        self.assertEqual( int(api_user.id) , api_user_id)
        self.assertTrue( len(api_user.device_id) > 0)

    def test_find(self):
        '''
            ** test get list of api_users by app_id
        '''
        api_users = self.partner.api_users(app_id =5)
        meta,collection = api_users.find()
        
        for item in collection:
            self.assertNotEqual( int(item.id) , 0)
            self.assertNotEqual( len(item.device_id) , 0)
            print item

    def test_findOne(self):
        ''' 
            ** test get single api_user_id object
        '''
        app_id = 5
        user_id = 210
        api_users = self.partner.api_users(app_id=app_id)

        api_client = api_users.findOne(api_user_id = user_id)

        self.assertEqual( int(api_client.id), user_id)
        self.assertNotEqual( len(api_client.device_id) , 0)
        
        print api_client.to_dict()

    def test_ban_user(self):
        '''
            ** test ban user from single app
        '''

        app_id = 5
        user_id = 5
        api_users = self.partner.api_users(app_id=app_id)

        api_client = api_users.findOne(api_user_id = user_id)

        resp = api_client.ban(app_id)
        self.assertTrue(resp)
