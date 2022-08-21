from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import random

class Experiment:
    db = "experiment_db"
    def __init__(self,data):
        self.id = data['id']
        self.treatment = data['treatment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

###################################### 
# CREATE METHODS 
###################################### 

    @classmethod
    def save(cls, data):
        query = "INSERT INTO experiments (treatment, user_id) VALUES (%(treatment)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)


    @classmethod
    def treatment_assignment(cls,data):
        query = "SELECT * FROM experiments WHERE user_id = %(user_id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        if result:
            print('USER ALREADY IN A TREATMENT GROUP', result)
            return cls(result[0])
        else:
            print('ASSIGN USER NEW TREATMENT GROUP', result)
            randNum = random.randint(1,100)
            # Test setup as a three way test split:
            # Treatment A has a 50% chance, Treatment B has a 25% chance, and Treatment C has a 25%
            if randNum <=50:
                treatment = "TreatmentA"
            elif randNum >= 51 and randNum <=75:
                treatment = "TreatmentB"
            elif randNum >= 76:
                treatment = "TreatmentC"
            print("RANDNUM IS:", randNum)
            print("TREATMENT GROUP:", treatment)
            data = {
                'treatment' : treatment,
                'user_id' : session['user_id']
            }
            cls.save(data)
            return data


###################################### 
# READ METHODS 
###################################### 

    @classmethod
    def get_one_experiment_by_id(cls,data):
        query = "SELECT * FROM experiments WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

