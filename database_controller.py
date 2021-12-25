import pymysql
from datetime import datetime 

selectCursor = pymysql.cursors.DictCursor

def __parsingTime(time):
    return time.strftime('%Y-%m-%d %H:%M:%S')

class Folders:
    def __init__(self, connection):
        self.connection = connection

    def create(self, title: str, description: str):
        self.connection.ping()
        with self.connection.cursor(cursor=selectCursor) as cursor:
            now = __parsingTime(datetime.now())
            sql = "INSERT INTO photo_database_folders VALUES(NULL, %s, %s, %s, %s) RETURNING id"
            cursor.execute(sql, (title, description, now, now))
            result = cursor.fetchone()
        return result

    def edit(self, id: str, title: str, description: str) -> None:
        self.connection.ping()
        with self.connection.cursor(cursor=selectCursor) as cursor:
            now = __parsingTime(datetime.now())
            sql = "UPDATE title = %s, description = %s, last_edit_datatime = %s FROM photo_database_folders WHERE id = %s"
            cursor.execute(sql, (title, description, now, id))
        return

    def delete(self, id: str) -> None:
        self.connection.ping()
        with self.connection.cursor(cursor=selectCursor) as cursor:
            sql = "DELETE FROM photo_database_links WHERE folder_id = %s"
            self.cursor.execute(sql, (id))
            sql = "DELETE FROM photo_database_folders WHERE id = %s"
            self.cursor.execute(sql, (id))
        return
    
    def get(self, id: str):
        self.connection.ping()
        with self.connection.cursor(cursor=selectCursor) as cursor:
            sql = "SELECT * FROM photo_database_folders WHERE id = %s"
            cursor.execute(sql, (id))
            result = cursor.fetchone()
        return result

    def getAll(self):
        self.connection.ping()
        with self.connection.cursor(cursor=selectCursor) as cursor:
            sql = "SELECT * FROM photo_database_folders"
            cursor.execute(sql)
            result = cursor.fetchall()
        return result

    def addImage(self, image_id: str, folder_id: str):
        return self.__addToFolder(image_id=image_id, folder_id=folder_id)
    
    def removeImage(self, image_id: str, folder_id: str) -> None:
        return self.__removeImageFromFolder(image_id=image_id, folder_id=folder_id)

    def __removeImageFromFolder(self, image_id: str, folder_id: str) -> None:
        with self.connection.cursor(cursor=selectCursor) as cursor:
            sql = "DELETE FROM photo_database_links WHERE folder_id = %s AND image_id = %s"
            cursor.execute(sql, (folder_id, image_id))
            result = cursor.fetchone()
        return result
    
    def __addToFolder(self, image_id: str, folder_id: str):
        with self.connection.cursor(cursor=selectCursor) as cursor:
            sql = "INSERT INTO photo_database_links VALUES(NULL, %s, %s) RETURNING id"
            cursor.execute(sql, (folder_id, image_id))
            result = cursor.fetchone()
        return result


class Images:
    def __init__(self, connection):
            self.connection = connection

    def create(self, title: str, description: str, path: str):
        self.connection.ping()
        with self.connection.cursor(cursor=selectCursor) as cursor:
            now = __parsingTime(datetime.now())
            sql = "INSERT INTO photo_database_images VALUES(NULL, %s, %s, %s, %s, %s) RETURNING id"
            cursor.execute(sql, (title, description, path, now, now))
            result = cursor.fetchone()
        return result

    def edit(self, id: str, title: str, description: str) -> None:
        self.connection.ping()
        with self.connection.cursor(cursor=selectCursor) as cursor:
            now = __parsingTime(datetime.now())
            sql = "UPDATE title = %s, description = %s, last_edit_datatime = %s FROM photo_database_images WHERE id = %s"
            cursor.execute(sql, (title, description, now, id))
        return

    def delete(self, id: str) -> None:
        self.connection.ping()
        with self.connection.cursor(cursor=selectCursor) as cursor:
            sql = "DELETE FROM photo_database_links WHERE image_id = %s"
            self.cursor.execute(sql, (id))
            sql = "DELETE FROM photo_database_images WHERE id = %s"
            self.cursor.execute(sql, (id))
        return
    
    def get(self, id: str):
        self.connection.ping()
        with self.connection.cursor(cursor=selectCursor) as cursor:
            sql = "SELECT * FROM photo_database_images WHERE id = %s"
            cursor.execute(sql, (id))
            result = cursor.fetchone()
        return result
    
    def getAll(self):
        self.connection.ping()
        with self.connection.cursor(cursor=selectCursor) as cursor:
            sql = "SELECT * FROM photo_database_images"
            cursor.execute(sql)
            result = cursor.fetchall()
        return result
    
    def addToFolder(self, image_id: str, folder_id: str):
        return self.__addToFolder(image_id=image_id, folder_id=folder_id)
    
    def removeFromFolder(self, image_id: str, folder_id: str) -> None:
        return self.__removeImageFromFolder(image_id=image_id, folder_id=folder_id)

    def __removeImageFromFolder(self, image_id: str, folder_id: str) -> None:
            with self.connection.cursor(cursor=selectCursor) as cursor:
                sql = "DELETE FROM photo_database_links WHERE folder_id = %s AND image_id = %s"
                cursor.execute(sql, (folder_id, image_id))
                result = cursor.fetchone()
            return result
        
    def __addToFolder(self, image_id: str, folder_id: str):
        with self.connection.cursor(cursor=selectCursor) as cursor:
            sql = "INSERT INTO photo_database_links VALUES(NULL, %s, %s) RETURNING id"
            cursor.execute(sql, (folder_id, image_id))
            result = cursor.fetchone()
        return result
   

class DatabaseController:
    def __init__(self, config) -> None:
        self.connection = pymysql.connect(**config)
        self.folders = Folders(self.connection)
        self.images = Images(self.connection)

    def close(self):
        self.connection.close()

    def getUnion(self):
        self.connection.ping()
        with self.connection.cursor(cursor=selectCursor) as cursor:
            sql = 'SELECT * FROM vs10'
            cursor.execute(sql)
            result = cursor.fetchall()
        return result