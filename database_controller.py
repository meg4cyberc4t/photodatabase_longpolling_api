import pymysql
import pymysqlpool


selectCursor = pymysql.cursors.DictCursor



class Folders:
    def __init__(self, pool):
        self.pool = pool

    def create(self, title: str, description: str):
        connection = self.pool.get_connection()
        with connection.cursor(cursor=selectCursor) as cursor:
            sql = "INSERT INTO photo_database_folders VALUES(NULL, %s, %s) RETURNING id"
            cursor.execute(sql, (title, description))
            result = cursor.fetchone()
        self.pool.put_connection(connection)
        return result

    def edit(self, id: str, title: str, description: str) -> None:
        connection = self.pool.get_connection()
        if (len(title) > 0):
            with connection.cursor(cursor=selectCursor) as cursor:
                sql = "UPDATE photo_database_folders SET  title = %s WHERE id = %s"
                cursor.execute(sql, (title, id))
        if (len(description) > 0):
            with connection.cursor(cursor=selectCursor) as cursor:
                sql = "UPDATE photo_database_folders SET  description = %s WHERE id = %s"
                cursor.execute(sql, (description, id))
        self.pool.put_connection(connection)
        return

    def delete(self, id: str) -> None:
        connection = self.pool.get_connection()
        with connection.cursor(cursor=selectCursor) as cursor:
            sql = "DELETE FROM photo_database_links WHERE folder_id = %s"
            cursor.execute(sql, (id))
            sql = "DELETE FROM photo_database_folders WHERE id = %s"
            cursor.execute(sql, (id))
        self.pool.put_connection(connection)
        return
    
    def get(self, id: str):
        connection = self.pool.get_connection()
        with connection.cursor(cursor=selectCursor) as cursor:
            sql = "SELECT * FROM photo_database_folders WHERE id = %s"
            cursor.execute(sql, (id))
            result = cursor.fetchone()
            sql = "SELECT * FROM photo_database_images WHERE id IN (SELECT photo_id FROM `vsa11` WHERE folder_id = %s)"
            cursor.execute(sql, (id))
            if (result != None):
                result.update({"photos": cursor.fetchall()})
        self.pool.put_connection(connection)
        return result

    def getImagesIds(self, id: str):
        connection = self.pool.get_connection()
        with connection.cursor(cursor=selectCursor) as cursor:
            sql = "SELECT * FROM photo_database_links WHERE folder_id = %s"
            cursor.execute(sql, (id))
            result = cursor.fetchall() 
        self.pool.put_connection(connection)
        return result

    def getAll(self):
        connection = self.pool.get_connection()
        with connection.cursor(cursor=selectCursor) as cursor:
            sql = "SELECT * FROM photo_database_folders"
            cursor.execute(sql)
            result = cursor.fetchall()
        self.pool.put_connection(connection)
        return result

    def addImage(self, image_id: str, folder_id: str):
        return self.__addToFolder(image_id=image_id, folder_id=folder_id)
    
    def removeImage(self, image_id: str, folder_id: str) -> None:
        return self.__removeImageFromFolder(image_id=image_id, folder_id=folder_id)

    def __removeImageFromFolder(self, image_id: str, folder_id: str) -> None:
        connection = self.pool.get_connection()
        with connection.cursor(cursor=selectCursor) as cursor:
            sql = "DELETE FROM photo_database_links WHERE folder_id = %s AND image_id = %s"
            cursor.execute(sql, (folder_id, image_id))
            result = cursor.fetchone()
        self.pool.put_connection(connection)
        return result
    
    def __addToFolder(self, image_id: str, folder_id: str):
        connection = self.pool.get_connection()
        with connection.cursor(cursor=selectCursor) as cursor:
            sql = "INSERT INTO photo_database_links VALUES(NULL, %s, %s) RETURNING id"
            cursor.execute(sql, (folder_id, image_id))
            result = cursor.fetchone()
        self.pool.put_connection(connection)
        return result


class Images:
    def __init__(self, pool):
            self.pool = pool

    def create(self, title: str, description: str, path: str):
        connection = self.pool.get_connection()
        with connection.cursor(cursor=selectCursor) as cursor:
            sql = "INSERT INTO photo_database_images VALUES(NULL, %s, %s) RETURNING id"
            cursor.execute(sql, (title, path))
            result = cursor.fetchone()
        self.pool.put_connection(connection)
        return result

    def edit(self, id: str, title: str, description: str) -> None:
        connection = self.pool.get_connection()
        with connection.cursor(cursor=selectCursor) as cursor:
            sql = "UPDATE photo_database_images SET  title = %s WHERE id = %s"
            cursor.execute(sql, (title, description, id))
        self.pool.put_connection(connection)
        return

    def delete(self, id: str) -> None:
        connection = self.pool.get_connection()
        with connection.cursor(cursor=selectCursor) as cursor:
            sql = "DELETE FROM photo_database_links WHERE image_id = %s"
            cursor.execute(sql, (id))
            sql = "DELETE FROM photo_database_images WHERE id = %s"
            cursor.execute(sql, (id))
        self.pool.put_connection(connection)
        return
    
    def get(self, id: str):
        connection = self.pool.get_connection()
        with connection.cursor(cursor=selectCursor) as cursor:
            sql = "SELECT * FROM photo_database_images WHERE id = %s"
            cursor.execute(sql, (id))
            result = cursor.fetchone()
        self.pool.put_connection(connection)
        return result
    
    def getAll(self):
        connection = self.pool.get_connection()
        with connection.cursor(cursor=selectCursor) as cursor:
            sql = "SELECT * FROM photo_database_images"
            cursor.execute(sql)
            result = cursor.fetchall()
        self.pool.put_connection(connection)
        return result
    
    def addToFolder(self, image_id: str, folder_id: str):
        return self.__addToFolder(image_id=image_id, folder_id=folder_id)
    
    def removeFromFolder(self, image_id: str, folder_id: str) -> None:
        return self.__removeImageFromFolder(image_id=image_id, folder_id=folder_id)

    def __removeImageFromFolder(self, image_id: str, folder_id: str) -> None:
            connection = self.pool.get_connection()
            with connection.cursor(cursor=selectCursor) as cursor:
                sql = "DELETE FROM photo_database_links WHERE folder_id = %s AND image_id = %s"
                cursor.execute(sql, (folder_id, image_id))
                result = cursor.fetchone()
            self.pool.put_connection(connection)
            return result
        
    def __addToFolder(self, image_id: str, folder_id: str):
        connection = self.pool.get_connection()
        with connection.cursor(cursor=selectCursor) as cursor:
            sql = "INSERT INTO photo_database_links VALUES(NULL, %s, %s) RETURNING id"
            cursor.execute(sql, (folder_id, image_id))
            result = cursor.fetchone()
        self.pool.put_connection(connection)
        return result
   

class DatabaseController:
    def __init__(self, config) -> None:
        self.pool = pymysqlpool.ConnectionPool(size=20, name='pool', **config)
        self.folders = Folders(self.pool)
        self.images = Images(self.pool)

    def getUnion(self):
        connection = self.pool.get_connection()
        with connection.cursor(cursor=selectCursor) as cursor:
            sql = 'SELECT * FROM vsa11'
            cursor.execute(sql)
            result = cursor.fetchall()
        self.pool.put_connection(connection)
        return result