from LogCorona.utlis import extract_field_name, extract_log_id, extract_peoples_data

HTML_ELEMENT = 'a3b1ffb6-568f-4f07-9f57-09e072c8bded_first_name'
INVALID_HTML_ELEMENT = 'a3b1ffb6-568f-4f07-9f57-09e072c8bded'
EMPTY_VALUE = ''

INVALID_HTML_ELEMENT_FOR_LOG = '1_a3b1ffb6-568f-4f07-9f57-09e072c8bded'

REQUEST_FORM = {'b03a5b31-69e6-41a1-9269-262b3d7ab166': 'True',
                'b03a5b31-69e6-41a1-9269-262b3d7ab166_first_name': 'asd',
                'b03a5b31-69e6-41a1-9269-262b3d7ab166_last_name': 'asd',
                'b03a5b31-69e6-41a1-9269-262b3d7ab166_location_name': 'd',
                'b03a5b31-69e6-41a1-9269-262b3d7ab166_date': '2021-01-10',
                'b03a5b31-69e6-41a1-9269-262b3d7ab166_comment': 'asd',
                '609ea804-93ea-482a-a643-82597b72b1c3_first_name': 'אסף',
                '609ea804-93ea-482a-a643-82597b72b1c3_last_name': 'לב',
                '609ea804-93ea-482a-a643-82597b72b1c3_location_name': 'sadfsdf',
                '609ea804-93ea-482a-a643-82597b72b1c3_date': '2020-10-12',
                '609ea804-93ea-482a-a643-82597b72b1c3_comment': 'שדגשדגשגד', 'Delete': 'Delete'}

EXTRACT_LOG_RESULT = ({'b03a5b31-69e6-41a1-9269-262b3d7ab166': {'b03a5b31-69e6-41a1-9269-262b3d7ab166': 'True',
                                                                'first_name': 'asd',
                                                                'last_name': 'asd', 'location_name': 'd',
                                                                'date': '2021-01-10',
                                                                'comment': 'asd'},
                       '609ea804-93ea-482a-a643-82597b72b1c3_first_name': {
                           '609ea804-93ea-482a-a643-82597b72b1c3_first_name': 'אסף'},
                       '609ea804-93ea-482a-a643-82597b72b1c3_last_name': {
                           '609ea804-93ea-482a-a643-82597b72b1c3_last_name': 'לב'},
                       '609ea804-93ea-482a-a643-82597b72b1c3_location_name': {
                           '609ea804-93ea-482a-a643-82597b72b1c3_location_name': 'sadfsdf'},
                       '609ea804-93ea-482a-a643-82597b72b1c3_date': {
                           '609ea804-93ea-482a-a643-82597b72b1c3_date': '2020-10-12'},
                       '609ea804-93ea-482a-a643-82597b72b1c3_comment': {
                           '609ea804-93ea-482a-a643-82597b72b1c3_comment': 'שדגשדגשגד'},
                       'Delete': {'Delete': 'Delete'}}, ['b03a5b31-69e6-41a1-9269-262b3d7ab166'])


class TestUtils:
    @staticmethod
    def test_extract_field_name_valid_input():
        assert extract_field_name(HTML_ELEMENT) == 'first_name'

    @staticmethod
    def test_extract_field_name_invalid_input():
        assert extract_field_name(INVALID_HTML_ELEMENT) == INVALID_HTML_ELEMENT

    @staticmethod
    def test_extract_field_name_empty_value():
        assert extract_field_name(EMPTY_VALUE) == EMPTY_VALUE

    @staticmethod
    def test_extract_log_id_valid_input():
        assert extract_log_id(HTML_ELEMENT) == 'a3b1ffb6-568f-4f07-9f57-09e072c8bded'

    @staticmethod
    def test_extract_log_id_invalid_input():
        assert extract_log_id(INVALID_HTML_ELEMENT_FOR_LOG) == '1'

    @staticmethod
    def test_extract_log_id_empty_value():
        assert extract_log_id(EMPTY_VALUE) == ''

    @staticmethod
    def test_extract_peoples_data_valid():
        assert extract_peoples_data(REQUEST_FORM) == EXTRACT_LOG_RESULT
