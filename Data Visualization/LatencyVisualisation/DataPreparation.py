from traceback import print_exc

class DataPreparation(object):
    def __init__(self):
        super()

    def transform_data_into_graph(self, data):
        categorized_data = self._compute_category_and_amount(data)
        dimensionlised_data = self._put_data_into_dimensions(categorized_data)
        data_as_graph = self._to_graph_format(dimensionlised_data)
        return data_as_graph

    def transform_empty_data_into_graph(self, data):
        empty_data_as_graph = self._to_graph_format(data)
        return empty_data_as_graph

    def _compute_category_and_amount(self, data):
        categs_and_amounts = []
        for val in data:
            temp = {}
            temp[val['slot']] = val['value']
            temp['time'] = val['time']
            categs_and_amounts.append(temp)
        return categs_and_amounts

    def _put_data_into_dimensions(self, data):
        category_axis = []
        amount_of_category = []
        time_axis = []
        # TODO: If the returned array empty, prevent that returning an error. Btw, when a db is created, then error isnot thrown
        for data_point in data:
            for key, value in data_point.items():
                if key == 'time':
                    time_axis.append(data_point[key])
                else:
                    category_axis.append(key)
                    amount_of_category.append(value)
        return [category_axis, amount_of_category]

    def _to_graph_format(self, data):
        # This function takes a list of two lists that consists of values for x- and y-axis respectively and inserts those values into the graph.
        # Length check
        if (len(data) != 2):  # !1
            print_exc()
            raise Exception
        # content length check
        if (len(data[0]) != len(data[1])):
            print_exc()
            raise Exception
        return {
            'data':
            [
                dict(
                    x=data[0],  # latency category
                    y=data[1],  # amount of bins
                    type="bar",
                    text=None,
                    marker=dict(
                        size=12,
                        opacity=0.8
                    )
                )
            ],
            'layout':
            {
                'title': 'Latency Visualisation',
                'xaxis': {
                    'title': 'Latencies'
                },
                'yaxis': {
                    'title': 'Number of latencies'
                },
                'zaxis': {
                    'title': 'time'
                }
            }
        }
