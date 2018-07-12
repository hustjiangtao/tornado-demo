# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from handlers.base_handler import BaseHandler
from handlers.base_handler import authenticated

from database.demo import demo_db

from lib.system_code import SUCCESS
from lib.system_code import PARAMS_MISS


class UploadHandler(BaseHandler):

    """upload handler"""

    @authenticated
    def post(self):
        files = self.request.files.get('file', None)
        new_name = self.request.files.get('newName', None)

        code = SUCCESS
        data = None

        if not files:
            code = PARAMS_MISS
        else:
            file_paths = [self.save_file(file, new_name=new_name) for file in files]
            self.finish('\n'.join(file_paths))
            return

            # data = {
            #     "file_paths": file_paths,
            # }

        self.render_json(code=code, data=data)
        return

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
            result = demo_db.update_demo(_id=_id, item=update_item)
            if result:
                data = {
                    "result": True,
                }

        self.render_json(code=code, data=data)
        return

    @authenticated
    def get(self):
        _id = self.get_json_argument('id', None)
        demo = demo_db.get_demo_by_id(_id=_id)
        if demo:
            demo = {
                "name": demo.get('name') or '',
                "create_time": demo.get('create_time'),
            }
        else:
            demo = {}
        data = {
            "demo": demo,
        }
        self.render('upload/upload.html', data=data)

    @authenticated
    def options(self):
        self.write('POST,PUT,GET')
        return

    # @staticmethod
    def save_file(self, file, new_name=None):
        """
        save file to upload dir
        :param file: tornado.httputil.HTTPFile
        :param new_name: new file name if provide
        :return: file_path
        """
        from tornado.httputil import HTTPFile
        if not isinstance(file, HTTPFile):
            return None

        name = file.get('filename')
        body = file.get('body')
        content_type = file.get('content_type')

        if not all([name, body, content_type]):
            return None

        import os
        from datetime import date
        upload_dir = os.path.join(self.application.settings.get('static_path'), 'upload')
        file_dir = os.path.join(upload_dir, f'{date.today().year}')
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)

        file_name = f'{name if not new_name else new_name}.{content_type.split("/")[-1]}'
        file_path = os.path.join(file_dir, file_name)
        with open(file_path, 'wb+') as f:
            f.write(body)

        server_host = f'{self.request.protocol}://{self.request.host}'
        new_file_path = server_host + os.path.join(self.static_url('upload'), f'{date.today().year}', file_name)

        return new_file_path
