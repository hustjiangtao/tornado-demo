# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Upload"""


from app.database.base import BaseDB
from app.database.models import UploadModel


class UploadDB(BaseDB):
    """Upload DB"""

    def add_upload(self, item):
        """Add a upload
        :param item: {
            'name': 'jiangtao',
            'new_name': 'new_jiangtao',
            'size': 12333,
            'content_type': 'image/png',
            'url': 'http://www.baidu.com/123.png'
            }
        """
        if not isinstance(item, dict):
            return False

        upload_model = UploadModel()
        upload_model.name = item.get('name')
        upload_model.new_name = item.get('new_name')
        upload_model.size = item.get('size')
        upload_model.content_type = item.get('content_type')
        upload_model.url = item.get('url')
        upload_model.upload_dir = item.get('upload_dir')

        result = self.add(upload_model)
        if result:
            result = upload_model.id

        return result

    def update_upload(self, _id, item):
        """update a upload
        :param _id: id
        :param item: {
            'name': 'jiangtao',
            'new_name': 'new_jiangtao',
            'size': 12333,
            'content_type': 'image/png',
            'url': 'http://www.baidu.com/123.png'
            }
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
        :param _id: id
        """
        if not _id:
            return {}
        if not isinstance(_id, int):
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
                "upload_dir": int(upload.upload_dir),
                "create_time": upload.create_time,
            }
        else:
            result = {}

        return result

    def get_all_upload_dir_with_url(self):
        """get all the upload dir"""
        dirs = self.db_session.query(UploadModel.upload_dir, UploadModel.url).all()
        group_urls = {}
        if dirs:
            for x in dirs:
                group_urls.setdefault(x[0], []).append(x[1])
        result = {x: group_urls.get(x) for x in sorted(group_urls, reverse=True)}

        return result

    def get_upload_by_dir(self, upload_dir):
        """get upload by upload_dir
        :param upload_dir: str
        """
        if not upload_dir:
            return []
        if not isinstance(upload_dir, str):
            upload_dir = str(upload_dir)

        urls = self.db_session.query(UploadModel.url).filter_by(upload_dir=upload_dir).all()
        if urls:
            result = [x[0] for x in urls]
        else:
            result = []

        return result


upload_db = UploadDB()


if __name__ == '__main__':
    upload_db = UploadDB()
    print(upload_db.get_upload_by_id(1))
