class RequestPreparation(object):

    def __init__(self, DB_NAME, MEASUREMENT):
        super()
        self.DB_NAME = DB_NAME
        self.MEASUREMENT = MEASUREMENT

    def prepare_request(self, filters):
        non_none_filters = self._extract_selected_filters(filters)
        filter_query = self._compose_the_query(non_none_filters)
        params = {
            'db_name': self.DB_NAME,
            'measurement': self.MEASUREMENT,
            'query': filter_query
        }

        return params

    def _extract_selected_filters(self, filters):
        non_none_filters = []
        for filt in filters:
            for v in filt.values():
                if v is not None:
                    non_none_filters.append(filt)

        return non_none_filters


    def _compose_the_query(self, filters):
        # This block composes a query with chosen filter values
        filter_query = str('SELECT slot, value FROM ' + self.MEASUREMENT + ' WHERE ')
        for filt_ind in range(len(filters)):
            for key, val in filters[filt_ind].items():
                # This condition prevents that there is an 'AND' at the end of the query
                if filt_ind == len(filters)-1:
                    filter_query += "".join(["{}='{}'".format(key, val)])
                else:
                    filter_query += "".join(["{}='{}' AND ".format(key, val)])
        return filter_query
