import connection
import f_connect
import pandas
from fuzzywuzzy import fuzz

def fuzzy_lookup(test_frame, text_blob):
    """blob is ' '-seperated names to lookup fuzzaly
    """
    all_words = text_blob.split()  # get list of all submitted names
    print(all_words)
    for i, row in test_frame.iterrows():
        parent_string = ' '.join(row.to_dict().values())
        print(text_blob + ' =?= ' + parent_string)
        fuzz_val = fuzz.token_set_ratio(text_blob, parent_string)
        print(parent_string, text_blob, fuzz_val)
        if fuzz_val > 80:
            print('match')
            res = dict()
            res['num'] = i
            res['match'] = fuzz_val
            return res
    return []

def dump_frame_to_firebase(input_frame):
    for i, data in input_frame.iterrows():
        d = data.to_dict()
        d['index'] = i
        d2=dict()
        for key, value in d.items():
            d2[key] = str(value)
        print(d2)
        print('')
        f_connect.new_entry(d2, "/people")

if __name__ == "__main__":
    # fetch excel from server
    frame = connection.retrieve_file_as_xlsx(file_name="Contact Information (Responses)", local_name="fresh_list.xlsx")
    print(frame)
    frame['p1'] = ''
    frame['p1_c'] = ''
    frame['p2'] = ''
    frame['p2_c'] = ''
    short = frame[['Achternaam', 'Voornamen', 'Achternaam.1', u'Voornamen.1', 'Achternaam.2', 'Voornamen.2']]
    print(short)

    for i, row in frame.iterrows():
        # print('** parent 1 **')
        parent_name_dict = row[['Achternaam.1', 'Voornamen.1']].to_dict()
        names = [str(v) for v in parent_name_dict.values()]
        parent_name_blob = ' '.join(names)  # all parents names seperated by spaces
        res1 = fuzzy_lookup(frame[['Achternaam', 'Voornamen', 'Roepnaam']], parent_name_blob)

        if res1:
            frame.set_value(i, 'p1', res1['num'])
            frame.set_value(i, 'p1_c', res1['match'])


        # print('** parent 2 **')
        parent_name_dict = row[['Achternaam.2', 'Voornamen.2']].to_dict()
        names = [str(v) for v in parent_name_dict.values()]
        parent_name_blob = ' '.join(names)  # all parents names seperated by spaces
        res2 = fuzzy_lookup(frame[['Achternaam', 'Voornamen', 'Roepnaam']], parent_name_blob)

        if res2:
            frame.set_value(i, 'p2', res2['num'])
            frame.set_value(i, 'p2_c', res2['match'])
            # frame['p2'] = res1['num']
            #  frame['p2_c'] = res1['match']

    print(frame[['Voornamen', 'p1', 'p2']])
    subset = frame[['Voornamen', 'Achternaam', 'Email', 'Telefoonnummer',
    'Geboren', 'Plaats', 'Land', 'Roepnaam', 'p1', 'p2']]
    dump_frame_to_firebase(subset)
