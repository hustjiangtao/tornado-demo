# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Upload"""


from handlers.base_handler import BaseHandler
from handlers.base_handler import authenticated

from database.upload import upload_db

from lib.system_code import SUCCESS
from lib.system_code import PARAMS_MISS
from lib.utils import random_string


class UploadHandler(BaseHandler):

    """upload handler"""

    @authenticated
    def post(self):
        files = self.request.files.get('file', None)
        new_name = self.get_body_argument('newName', None)
        document = self.get_body_argument('document', None)

        code = SUCCESS
        data = None

        if not files:
            code = PARAMS_MISS
        else:
            file_objs = [self.save_file(file, new_name=new_name, document=document)
                         for file in files]

            if not document:
                map(upload_db.add_upload, file_objs)

            self.finish('\n'.join([obj.get('url') for obj in file_objs]))
            return

            # data = {
            #     "file_paths": file_paths,
            # }

        self.render_json(code=code, data=data)

    @authenticated
    def delete(self):
        pass

    @authenticated
    def put(self):
        _id = self.get_json_argument('id', None)
        name = self.get_json_argument('name', None)

        code = SUCCESS
        data = None

        if not all([_id, name]):
            code = PARAMS_MISS
        else:
            update_item = {
                "name": name,
            }
            result = upload_db.update_upload(_id=_id, item=update_item)
            if result:
                data = {
                    "result": True,
                }

        self.render_json(code=code, data=data)

    @authenticated
    def get(self):
        _id = self.get_json_argument('id', None)
        upload = upload_db.get_upload_by_id(_id=_id)
        if upload:
            upload = {
                "name": upload.get('name') or '',
                "create_time": upload.get('create_time'),
            }
        else:
            upload = {}
        data = {
            "upload": upload,
        }
        self.render('upload/upload.html', data=data)

    @authenticated
    def options(self):
        self.write('POST,PUT,GET')

    # @staticmethod
    def save_file(self, file, new_name=None, document=None):
        """
        save file to upload dir
        :param file: tornado.httputil.HTTPFile
        :param new_name: new file name if provide
        :param document: change document dir if provide
        :return: file_path
        """
        from tornado.httputil import HTTPFile
        if not isinstance(file, HTTPFile):
            return {}

        name = file.get('filename')
        body = file.get('body')
        content_type = file.get('content_type')

        if not all([name, body, content_type]):
            return {}

        import os
        from datetime import date
        if document:
            upload_dir = os.path.join('/var/www/document', f'{date.today().year}')
        else:
            upload_dir = os.path.join(self.application.settings.get('static_path'),
                                      'upload', f'{date.today().year}')
        if not os.path.exists(upload_dir):
            os.mkdir(upload_dir)
            from lib.utils import do_warning
            do_warning(f'mkdir: {upload_dir}')

        sign = random_string(6)
        file_name = f'{sign}_{name if not new_name else new_name}'
        file_path = os.path.join(upload_dir, file_name)
        with open(file_path, 'wb+') as f_temp:
            f_temp.write(body)

        new_file_path = self.static_url(f'upload/{date.today().year}/{file_name}',
                                        include_host=True, include_version=False)

        file_obj = {
            "name": name,
            "new_name": new_name,
            "size": len(body),
            "content_type": content_type,
            "url": new_file_path,
        }

        return file_obj
