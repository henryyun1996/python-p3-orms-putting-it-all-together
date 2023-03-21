import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        dog_table = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """

        CURSOR.execute(dog_table)

    @classmethod
    def drop_table(cls):
        dog_table = """
            DROP TABLE IF EXISTS dogs
        """

        CURSOR.execute(dog_table)

    def save(self):
        dog_table = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """

        CURSOR.execute(dog_table, (self.name, self.breed))

        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]

    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog

    @classmethod
    def get_all(cls):
        dog_table = """
            SELECT *
            FROM dogs
        """

        all = CURSOR.execute(dog_table).fetchall()

        cls.all = [cls.new_from_db(row) for row in all]
        return cls.all

    @classmethod
    def find_by_name(cls, name):
        dog_table = """
            SELECT *
            FROM dogs
            WHERE name = ?
            LIMIT 1
        """

        dog = CURSOR.execute(dog_table, (name,)).fetchone()

        return cls.new_from_db(dog)

    @classmethod
    def find_by_id(cls, id):
        dog_table = """
            SELECT *
            FROM dogs
            WHERE id = ?
            LIMIT 1
        """

        dog = CURSOR.execute(dog_table, (id,)).fetchone()

        return cls.new_from_db(dog)