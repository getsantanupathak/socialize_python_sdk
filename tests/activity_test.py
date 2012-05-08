import sys, os
cmd_folder = os.path.dirname(os.path.abspath(__file__)[-len('tests')])
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
from datetime import datetime
try:
    from local_settings import version, host, key, secret, user_id , app_id, delete_app, api_user_id
except:
    print 'Failed to load local_settings.py. Switching to settings.py'
    from settings import version, host, key, secret, user_id , app_id, delete_app , api_user_id

from socialize.client import Partner
from base import SocializeTest

class ActivityTest(SocializeTest):
    '''
        find()
    '''   
    def test_init(self):
        '''
            ** test init activity by app_id
            nosetests -s -v tests.activity_test:ActivityTest.test_init

        '''
        comment = self.partner.comment(app_id)
        self.assertEqual(comment.activity_type , 'comment')
        self.assertEqual(comment.app_id , app_id)

    def untest_delete_comment(self):
        '''
            nosetests -s -v tests.activity_test:ActivityTest.test_delete_comment  
            ## Note: comment 's filtered by api , so we can't delete same comment twice.
        '''
        comment = self.partner.comment(app_id)
        delete_comment_id=3
        self.assertTrue( comment.deleteComment(3))
        

    def untest_invalid_delete_activities(self):
        '''
            ** nosetests -s -v tests.activity_test:ActivityTest.test_invalid_delete_activities
        '''
        for item in ['comment','view','like','share']:
            activity = self.partner.activities(app_id, item)
            meta, collection = activity.find()


            if item != 'comment':
                one_activity = collection[0]                
                self.assertRaises(Exception, one_activity.delete )


    def test_comment_find(self):
        '''
            ** test get list of comment by app_id
        '''
        comment = self.partner.comment(app_id)
        meta, collection = comment.find()
        
        for item in collection:
            self.assertNotEqual(int(item.id) , 0)
            self.assertEqual(comment.activity_type , 'comment')
            self.assertEqual(comment.app_id , app_id)
            print item

    def test_view_find(self):
        '''
            ** test get list of view by app_id
        '''
        view = self.partner.view(app_id)
        meta, collection = view.find()
        
        for item in collection:
            self.assertNotEqual(int(item.id) , 0)
            self.assertEqual(view.activity_type , 'view')
            print item
    
    def test_share_find(self):
        '''
            ** nosetests -s -v tests.activity_test:ActivityTest.test_share_find

        '''
        share = self.partner.share(app_id)
        meta, collection = share.find()
        
        for item in collection:
            self.assertNotEqual(int(item.id) , 0)
            self.assertEqual(item.activity_type , 'share')
            print item.medium
            self.assertNotEqual(item.medium['id'], None)
            self.assertNotEqual(item.medium['medium'], None)

    def test_like_find(self):
        '''
            ** test get list of like by app_id
        '''
        like = self.partner.like(app_id)
        meta, collection = like.find()
        
        for item in collection:
            self.assertNotEqual(int(item.id) , 0)
            self.assertEqual(like.activity_type , 'like')
            print item

    def test_comment_find_order_by_date(self):
        '''
            nosetests -s -v tests.activity_test:ActivityTest.test_comment_find_order_by_date    
            ** test get list of comment by app_id order by created
        '''
        comment = self.partner.comment(app_id)
        params= {'order_by':'-created', 'limit':100}
        meta, collection = comment.find(params)

        prev_created = datetime.strptime('2999-01-01T00:00:00','%Y-%m-%dT%H:%M:%S')

        self.assertTrue( len(collection) <=100)
        self.assertTrue( len(collection) >= 2 )
        for item in collection:
            self.assertNotEqual(int(item.id) , 0)
            self.assertEqual(comment.activity_type , 'comment')
            self.assertTrue( prev_created >= item.created)
            prev_created = item.created
            self.assertFalse( item.deleted)
            print item



