from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Pie:

    db_name = "pypie_schema"

    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.filling = data['filling']
        self.crust = data['crust']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.users_who_voted = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM pies"
        results = connectToMySQL(cls.db_name).query_db(query)
        return results

    @classmethod 
    def create_pie(cls, data):
        query = "INSERT INTO pies (name, filling, crust, user_id) VALUES (%(name)s, %(filling)s, %(crust)s, %(user_id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM pies WHERE id = %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update_pie(cls, data):
        query = "UPDATE pies SET name = %(name)s, filling = %(filling)s, crust = %(crust)s WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def vote(cls, data):
        query = "INSERT INTO votes (user_id, pie_id) VALUES (%(user_id)s, %(pie_id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results
    
    @classmethod
    def remove_vote(cls, data):
        query = "DELETE FROM votes WHERE user_id = %(user_id)s AND pie_id = %(pie_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def get_all_voted_pies(cls, data):
        pies_voted = []
        query = "SELECT pie_id FROM votes JOIN users ON users.id = user_id WHERE user_id = %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        for result in results:
            pies_voted.append(result['pie_id'])
        return pies_voted

    @classmethod
    def show_all_pies(cls):
        query = "SELECT pies.name, users.first_name, pies.id, COUNT(votes.pie_id) AS votes FROM pies "\
        "LEFT JOIN users ON users.id = pies.user_id "\
        "LEFT JOIN votes ON pies.id = votes.pie_id "\
        "GROUP by pies.id "\
        "ORDER BY COUNT(votes.pie_id) DESC;"
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results)
        return results
    # @classmethod
    # def show_all_pies(cls):
    #     query = "SELECT * FROM pies "\
    #     "LEFT JOIN users ON users.id = pies.user_id "\
    #     "LEFT JOIN votes ON votes.pie_id = pies.id "\
    #     "LEFT JOIN users AS users2 ON users2.id = votes.user_id "\
    #     "ORDER BY pies.created_at DESC"

    #     results = connectToMySQL(cls.db_name).query_db(query)
    #     all_pies = []

    #     for result in results:
    #         new_pie = True
    #         vote_user_data = {
    #             "id": result['users2.id'],
    #             "first_name": result['users2.first_name'], 
    #             "last_name": result['users2.last_name'],
    #             "email": result['users2.email'],
    #             "password": result['users2.password'],
    #             "created_at": result['users2.created_at'],
    #             "updated_at": result['users2.updated_at']
    #         }
    #         if len(all_pies) > 0 and all_pies[len(all_pies) -1].id == result['id']:
    #             all_pies[len(all_pies) -1].users_who_voted.append(user.User(vote_user_data))
    #             new_pie = False

    #         if new_pie:
    #             pie = cls(result)
    #             creator_data = {
    #                 "id": result['users.id'],
    #                 "first_name": result['first_name'], 
    #                 "last_name": result['last_name'],
    #                 "email": result['email'],
    #                 "password": result['last_name'],
    #                 "created_at": result['created_at'],
    #                 "updated_at": result['updated_at']
    #                 }
    #             pie.creator = user.User(creator_data)

    #             if result['users2.id'] is not None:
    #                 pie.users_who_voted.append(user.User(vote_user_data))
    #             all_pies.append(pie)
    #     return all_pies
        
    @classmethod
    def destroy_pie(cls, data):
        query = "DELETE FROM pies WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @staticmethod
    def validate_pie(pie):
        is_valid = True
        if len(pie['name']) < 1:
            is_valid = False
            flash("Name field can not be left blank","pie")
        if len(pie['filling']) < 1:
            is_valid = False
            flash("Filling field can not be left blank","pie")
        if len(pie['crust']) < 1:
            is_valid = False
            flash("Crust field can not be left blank","pie")
        return is_valid

    @classmethod
    def get_pie_and_user(cls, data):
        query = "SELECT * FROM pies LEFT JOIN users ON users.id = pies.user_id WHERE pies.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

