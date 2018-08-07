# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Album"""


from handlers.base_handler import BaseHandler
from handlers.base_handler import authenticated

from database.upload import upload_db

from lib.system_code import SUCCESS
from lib.system_code import PARAMS_MISS


class AlbumHandler(BaseHandler):

    """Album handler"""

    @authenticated
    def post(self):
        """add api"""
        pass

    @authenticated
    def delete(self):
        """delete api"""
        pass

    @authenticated
    def put(self):
        """update api"""
        pass

    @authenticated
    def get(self, *args):
        """get albums or a single ablum"""
        if not args:
            albums = upload_db.get_all_upload_dir_with_url()
            data = {
                "albums": albums,
            }
            self.render('album/albums.html', data=data)
        else:
            album_id = args[0]
            album = upload_db.get_upload_by_dir(upload_dir=album_id)
            data = {
                "album": album
            }
            self.render('album/album.html', data=data)

    @authenticated
    def options(self):
        self.write('GET')
