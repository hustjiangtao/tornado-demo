# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from database.base import BaseDB
from database.models.model_route import UploadModel


class UploadDB(BaseDB):
    """Upload DB"""

    def add_upload(self, item):
        """Add a upload
        # >>> {'name': 'jiangtao', 'new_name': 'new_jiangtao', 'size': 12333, 'content_type': 'image/png', 'url': 'http://www.baidu.com/123.png'}
        int
        """
        if not isinstance(item, dict):
            return False

        upload_model = UploadModel()
        upload_model.name = item.get('name')
        upload_model.new_name = item.get('new_name')
        upload_model.size = item.get('size')
        upload_model.content_type = item.get('content_type')
        upload_model.url = item.get('url')

        result = self.add(upload_model)
        if result:
            result = upload_model.id

        return result

    def update_upload(self, _id, item):
        """update a upload
        # >>> {'name': 'jiangtao', 'new_name': 'new_jiangtao', 'size': 12333, 'content_type': 'image/png', 'url': 'http://www.baidu.com/123.png'}
        True
        """
        if not _id or not isinstance(item, dict):
            return False

        query = self.db_session.query(UploadModel).filter_by(id=_id)
        upload = self.fetch_first(query)
        if not upload:
            return False

        upload.name = item.get('name')
        upload.new_name = item.get('new_name')
        upload.size = item.get('size')
        upload.content_type = item.get('content_type')
        upload.url = item.get('url')

        result = self.save(upload)

        return result

    def get_upload_by_id(self, _id):
        """get a upload
        # >>> 1
        {}
        """
        if not _id:
            return {}
        elif not isinstance(_id, int):
            _id = int(_id)

        query = self.db_session.query(UploadModel).filter_by(id=_id)
        upload = self.fetch_first(query)
        if upload:
            result = {
                "id": upload.id,
                "name": upload.name,
                "new_name": upload.new_name,
                "size": upload.size,
                "content_type": upload.content_type,
                "url": upload.url,
                "create_time": upload.create_time,
            }
        else:
            result = {}

        return result


upload_db = UploadDB()


if __name__ == '__main__':
    upload_db = UploadDB()
    print(upload_db.get_upload_by_id(1))
