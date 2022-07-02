from .db_connection import DB_Conn
from .database_operations import DB_Operations
from traceback import print_exc

class DB_Ops_Read_Criteria(DB_Operations):

    def __init__(self):
        self.client = DB_Conn.get_client()

    def read_criteria(self, db_name, measurement):
        data = {}
        c_query, p_query, i_query = self._set_crit_queries(measurement)

        try:
            unique_cpus = self.client.query(c_query, database=db_name)
            unique_intervals = self.client.query(i_query, database=db_name)
            unique_priorities = self.client.query(p_query, database=db_name)
        except Exception:
            print_exc()
            raise Exception

        cpus, priorities, intervals = self._extract_crit(unique_cpus, unique_intervals, unique_priorities)

        data['cpu'] = cpus
        data['priority'] = priorities
        data['interval'] = intervals

        return data
    
    def _set_crit_queries(self, measurement):
        cpu = "SHOW TAG VALUES FROM " + measurement + " WITH KEY = \"cpu\""
        priority = "SHOW TAG VALUES FROM " + measurement + " WITH KEY = \"priority\""
        interval = "SHOW TAG VALUES FROM " + measurement + " WITH KEY = \"interval\""

        return [cpu, priority, interval]

    def _extract_crit(self, u_cpus, u_intervals, u_priorities):
        cpus = [c['value'] for c in list(u_cpus.get_points())]
        priorities = [c['value'] for c in list(u_priorities.get_points())]
        intervals = [c['value'] for c in list(u_intervals.get_points())]
        
        return [cpus, priorities, intervals]