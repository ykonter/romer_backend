import connection
import f_connect
import pandas
from fuzzywuzzy import fuzz
import util


frame = []

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
        d = util.cleanse_dict(data.to_dict())
        d['index'] = str(i)
        #f_connect.new_entry(d, "/people")
        f_connect.set(str(i), d, "/people")

def fetch_parent_lineage(strands):
    global frame
    appended_anything = False

    new_strands = strands[:]
    # print('starting with {}'.format(new_strands))

    for strand in strands:
        strand_head = strand[-1]
        p1 = frame.loc[strand_head]['p1']
        p2 = frame.loc[strand_head]['p2']

        if p1 or p2:
            new_strands = [std for std in new_strands if std != strand]  # remove current strand for replacement
            if p1:
                l=strand[:]
                l.append(p1)
                new_strands.append(l)
            if p2:
                l=strand[:]
                l.append(p2)
                new_strands.append(l)

            #  some debug code
            #  print('{} minus {} to subs with -> {}'.format(strands, strand, new_strands))
            appended_anything = True

    if appended_anything:
        new_strands = fetch_parent_lineage(new_strands)  # loop deeper

    return new_strands


if __name__ == "__main__":
    # fetch excel from server
    converters = {"Telefoonnummer":str}
    frame = connection.retrieve_file_as_xlsx(file_name="Contact Information (Responses)", local_name="fresh_list.xlsx", converters=converters)
    print(frame)
    frame['p1'] = ''
    frame['p1_c'] = ''
    frame['p2'] = ''
    frame['p2_c'] = ''
    frame['lineage']=''
    frame['partner_index'] = ''
    frame['parnter_c'] = ''
    short = frame[['Achternaam', 'Voornamen', 'Achternaam.1', u'Voornamen.1', 'Achternaam.2', 'Voornamen.2']]
    print(short)

    for i, row in frame.iterrows():
        # print('** parent 1 **')
        parent_name_dict = row[['Achternaam.1', 'Voornamen.1']].to_dict()
        partner_name_dict = row[['Voornamen Partner', 'Achternaam Partner']].to_dict()
        names = [str(v) for v in parent_name_dict.values()]
        p_names = [str(v) for v in partner_name_dict.values()]
        parent_name_blob = ' '.join(names)  # all parents names seperated by spaces
        p_name_blob = ' '.join(p_names)
        res1 = fuzzy_lookup(frame[['Achternaam', 'Voornamen', 'Roepnaam']], parent_name_blob)
        res1p = fuzzy_lookup(frame[['Achternaam', 'Voornamen', 'Roepnaam']], p_name_blob)

        if res1:
            frame.set_value(i, 'p1', res1['num'])
            frame.set_value(i, 'p1_c', res1['match'])

        if res1p:
            frame.set_value(i, 'partner_index', res1p['num'])
            frame.set_value(i, 'parnter_c', res1p['match'])


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
    # temp turn off upload
    # dump_frame_to_firebase(subset)

    # enhanche frame with lineage
    for index, person in frame.iterrows():
        all_lines = fetch_parent_lineage([[index]])
        lens = [len(line) for line in all_lines]
        longest_ones = [line for line in all_lines if len(line) == max(lens)]
        chosen = []
        placed = False
        if len(longest_ones) == 1:  # one result
            chosen = list( reversed(longest_ones[0]))
            placed = True
        else:
            for long in longest_ones:
                if fuzz.ratio("Romer", frame.loc[long[-1]]) > 70:
                    chosen = list(reversed(long))
                    placed = True
                    break
        # no match to romer, remains ambigious, choose any
        if not placed:
            chosen = list(reversed(longest_ones[0]))
        frame.set_value(index, 'lineage', chosen)

    print(frame)
    frame.columns = [c if c != 'Land' else 'GeboorteLand' for c in frame.columns]
    frame.columns = [c if c != 'Land.1' else 'Land' for c in frame.columns]
    subset = frame[['Voornamen', 'Achternaam', 'Email', 'Telefoonnummer',
                    'Geboren', 'Plaats', 'GeboorteLand', 'Roepnaam', 'p1', 'p2', 'lineage', 'Adres en huisnummer',
                    'Postcode', 'Land', 'partner_index', 'parnter_c']]
    # temp turn off upload
    print(subset)
    dump_frame_to_firebase(subset)
    for i, vals in frame.iterrows():
        d = dict([(str(iter), str(val)) for iter, val in enumerate(vals['lineage'])])
        print(d)
        f_connect.set('lin', d, "/people/{}".format(i))

