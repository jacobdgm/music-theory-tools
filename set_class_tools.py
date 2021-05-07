"""
mt_tools: a collection of tools for musical set-theory analysis prepared
by Jacob deGroot-Maggetti as part of MUTH 538 final paper
"""

from math import gcd
from itertools import combinations, permutations

univ = 12 #size of pitch class 'univ'erse


"""
Some useful sets and melodies, and generators for other specific sets:
"""

triad = [0, 3, 7]
pentatonic = [0, 2, 4, 7, 9]
diatonic = [0, 1, 3, 5, 6, 8, 10]

twinkle = [0, 0, 7, 7, 9, 9, 7, 5, 5, 4, 4, 2, 2, 0]
klavierstuck_iii = [9, 11, 2, 8, 10, 9, 8, 11, 5, 3, 2, 4, (8, 7), 6, 5,
                    4, 10, 2, (3, 11), (8, 5, 9), (1, 10), 4, 5, 6, 3,
                    7, 4, (11, 8, 10), 0, 9, (7, 1, 4), 8, 5, 3, 6,
                    11, 4, 3, 2, (1, 10), 8, 7, 0, 9, 11]

def aggregate():
    """Return a list of all set classes in univ."""
    return [x for x in range(univ)]

def max_distributed(card, u = univ):
    """Return maximally distributed scale of given cardinality."""
    if card > univ:
        print("Warning: cardinality > universe size")
    return [int(x * (u / card)) for x in range(card)]


"""
Operations on melodies and sets:
"""

def transpose(patt, index):
    """Transpose patt upwards by index."""
    return [(patt[x] + index) % univ for x in range(len(patt))]

def invert(patt, index = 0):
    """Invert patt around index."""
    return [(index - note) % univ for note in patt]

def retrograde(patt):
    """Return patt in reversed order."""
    return [x for x in reversed(patt)]

def m(patt, index):
    """Multiply pitches of patt by index."""
    #if index and universe size share common factors, print warning
    if (gcd(index, univ) == 1) == False:
        print("Warning: index and univ are not coprime")
    return [(note * index) % univ for note in patt]

def complement(patt):
    """Return all notes not in patt."""
    return [pc for pc in range(univ) if pc not in patt]

def vector(patt):
    """Return interval vector as list of counts."""
    if len(patt) != len(set(patt)):
        print("Error: patt contains duplicate notes")
        return []
    length = len(patt)
    half_univ = (univ)//2
    vector_list = []
    for x in range(half_univ):
        vector_list.append(0)
    #compare all pairs of notes in patt
    for a in range(length-1):
        for b in range(a+1, length):
            interval = (patt[b] - patt[a]) % univ
            #count ascending or descending interval, whichever is smaller
            if interval <= half_univ:
                vector_list[interval - 1] += 1
            else:
                interval = (patt[a] - patt[b]) % univ
                vector_list[interval - 1] += 1
    return vector_list
    
def intervals(patt, ordered=True):
    """
    Return a list of intervals between successive pitches in patt.
    If ordered == False, return unordered pitch-class intervals.
    """
    vector_list = []
    half_univ = (univ + 1) // 2
    for note in range(len(patt) - 1):
        ival = (patt[note + 1] - patt[note]) % univ
        if ordered == False:
            if ival > half_univ:
                ival = univ - ival
        vector_list.append(ival)
    return vector_list        

def all_transformations(patt):
    """Return all transpositions and inversions of patt."""
    tf_set = set()
    tp_list = [transpose(patt,level) for level in range(univ)]
    for tp in tp_list:
        tf_set.add(tuple(sorted(tp)))
        tf_set.add(tuple(sorted(invert(tp))))
    return sorted([list(tf) for tf in tf_set])

def modes(patt, fixed_pitch = True):
    """
    Return all modes of patt.

    if fixed_pitch == True, transpose all modes to the same starting
    pitch.
    """
    modes_list = [patt]
    for n in range(1, len(patt)):
        if fixed_pitch:
            mode = patt[n:] + patt[:n]
            modes_list.append(transpose(mode,
                                        (patt[0] - mode[0]) % univ))
        elif not fixed_pitch:
            modes_list.append(patt[n:] + patt[:n])
    return modes_list

def matrix(prime_form):
    """Return a univ-tone matrix as a list of lists."""
    matrix = []
    inverted_form = invert(prime_form, prime_form[0])
    for position in range(univ):
        matrix.append(transpose(prime_form, inverted_form[position]))
    return matrix


"""
Tools for generating set classes:
"""

def SC(patt):
    """List the the pitches of patt as a set class in prime form."""
    #test all rotations of coll, save most left-packed version to
    #prime_form
    coll = sorted(set(patt)) #'coll'ection
    prime_form = coll
    test = []
    for r in range(len(coll)): #'r'otation
        test = coll[r:] + coll[:r]
        test_tp = transpose(test, 0 - test[0])
        if is_less_right_packed(test_tp, prime_form):
            prime_form = test_tp
    #also compare rotations of inverted(coll)
    coll_inv = sorted(invert(coll))
    for r in range(len(coll)): #'r'otation
        test = coll_inv[r:] + coll_inv[:r]
        test_tp = transpose(test, 0 - test[0])
        if is_less_right_packed(test_tp, prime_form):
            prime_form = test_tp
    return prime_form

def SCs_card_range(low, high):
    """List all set classes of cardinality between low and high."""
    SCs_list = []
    for card in range(low, high + 1):
        for combination in combinations(range(univ), card):
            prime_form = SC(combination)
            if prime_form not in SCs_list:
                SCs_list.append(prime_form)
    return SCs_list

def is_less_right_packed(a, b):
    """
    Return True if a is less right-packed than b, otherwise return False.

    a and b should be lists of the same length.
    """
    length = len(a)
    if len(b) != length:
        print("Warning: len(a) != len(b)")
    #work from end of a, b
    if a[-1] < b[-1]:
        return True
    elif a[-1] > b[-1]:
        return False
    #if ends of a and b are equal, check the next note forward
    elif length > 1:
        return is_less_right_packed(a[:-1], b[:-1])
    elif length == 1:
        return False


"""
Tools for comparing melodies, set classes:
"""

def are_z_related(a, b):
    """Return whether a and b have the same interval vector."""
    return vector(a) == vector(b)

def sim(a, b):
    """Return Morris' similarity index for sets a, b."""
    a_vect = vector(a)
    b_vect = vector(b)
    similarity = 0
    for interval in range(len(a_vect)):
        similarity += abs(a_vect[interval] - b_vect[interval])
    return similarity

def asim(a, b):
    """Return Morris' absolute similarity index for sets a, b."""
    ab_sim = sim(a, b)
    vector_sum = sum(vector(a)) + sum(vector(b))
    return ab_sim / vector_sum

def emb(a, b, check_transpositions = True, check_inversions = True):
    """Return the number of times a can be embedded in b."""
    counter = 0
    #set how many different transpositions to check
    if check_transpositions == True:
        tp_range = univ
    elif check_transpositions == False:
        tp_range = 1
    #transpose a to all necessary transpositions, check that all pitches
    #are in b
    for x in range(tp_range):
        tp_a = transpose(a, x)
        check = True
        for y in tp_a:
            if y not in b:
                check = False
                break
        if check == True:
            counter += 1
    #if necessary, check inverted form of a
    if check_inversions == True:
        counter += emb(invert(a), b, check_transpositions, False)
    return counter


"""
Tools for deficiency searches, a la David Lewin:
"""

def packed(mel):
    """
    Package melody so that each onset is represented as a list of all
    pitch classes making up the onset.
    """
    packed_mel = []
    for onset in mel:
        if type(onset) == int:
            packed_mel.append([onset])
        elif type(onset) == tuple:
            packed_mel.append([note for note in onset])
    return packed_mel

def flagged(patt):
    'Return a list of pitch classes and False flags.'
    fl_patt = []
    for pc in patt:
        fl_patt.append([pc, False])
    return fl_patt

def patt_in_mel(fl_patt, p_mel, dfcy_rem = 0, first_onset = True):
    """
    A helper function for instance_check(). Takes a flagged pattern
    and a packaged mel.
    
    Return True if, starting at the beginning of mel, patt can be found
    in mel, within the allowable deficiency. Only return True if a pc
    of fl_patt can be found within the first onset.
    """
    if dfcy_rem < 0: #beyond maximum deficiency
        return False
    if len(p_mel) == 0: #end of melody
        return False
    
    #can any pcs of fl_patt can be found in first onset?
    match_in_onset = False
    for pc in fl_patt:
        for note in p_mel[0]:
            if note == pc[0]:
                pc[1] = True
                match_in_onset = True
    
    #have all pcs of fl_patt been found?
    all_pcs_matched = True
    for pc in fl_patt:
        if pc[1] == False:
            all_pcs_matched = False

    if all_pcs_matched:
        return True
    #don't return True if the beginning of the melody doesn't participate
    #in the instance
    elif first_onset and not match_in_onset:
        return False
    #if some pcs not yet found, advance to next onset of p_mel
    elif all_pcs_matched == False:
        if match_in_onset:
            return patt_in_mel(fl_patt, p_mel[1:], dfcy_rem, False)
        elif match_in_onset == False:
            return patt_in_mel(fl_patt, p_mel[1:], dfcy_rem - 1, False)           
                
def instance_check(patt, mel, dfcy = 0):
    """Call patt_in_mel()"""
    return patt_in_mel(flagged(patt), packed(mel), dfcy)

def find_instances(patt, mel, dfcy = 0):
    """
    Return a list of instances of a set class, along with the index
    of the first note of the instance.
    """
    instances_list = []
    for onset in range(len(mel)):
        for tf in all_transformations(patt):
            if instance_check(tf, mel[onset:], dfcy):
                instances_list.append([tf, onset])
    return instances_list
    
def find_instances_formatted(patt, mel, dfcy = 0):
    """Print the results of find_instances() in a cleaner layout"""
    for inst in find_instances(patt, mel, dfcy):
        print(inst[1], inst[0])

def explained_by_patt(patt, mel, dfcy = 0):
    """
    Return True if all notes of mel participate in an instance of patt
    """
    flags_list = []
    p_mel = packed(mel)
    for onset in p_mel:
        flags_list.append([False for note in onset])

    #advance onset-by-onset through the melody, checking for matches
    for onset in range(len(mel)):
        for tf in all_transformations(patt):

            #when match found, progress through melody in search of
            #participating notes
            if instance_check(tf, mel[onset:], dfcy):
                dfcy_counter = 0

                #search from current location until end of melody
                for x in range(onset, len(p_mel)):
                    in_onset_check = False
                    #change flags for all participating notes
                    for y in range(len(p_mel[x])):
                        if p_mel[x][y] in tf:
                            flags_list[x][y] = True
                            in_onset_check = True
                    #if matches in onset, increment deficiency counter
                    if in_onset_check == False:
                        dfcy_counter += 1
                        if dfcy_counter > dfcy:
                            break
    #return bool(no falses among melody flags)
    for onset in flags_list:
        if False in onset:
            return False
    return True

def deficiency_given_SCs(SC_list, mel, deficiency = 0):
    """Return all set classes that explain mel at given deficiency."""
    matching_SCs = []
    for SC in SC_list:
        if explained_by_patt(SC, mel, deficiency) == True:
            matching_SCs.append(SC)
    return matching_SCs

def exhaustive_search(SC_list, mel, deficiency):
    """
    Print all set classes that explain mel up to a given maximum deficiency.

    Searches set classes of cardinality ranging from card_low to
    card_high; for each set class that explains mel at the given
    deficiency, checks whether they can still explain the melody at
    lower deficiencies.
    """
    matching_SCs = []
    print("deficiency =", deficiency)
    working_list = deficiency_given_SCs(SC_list, mel, deficiency)
    for SC in working_list:
        print(SC)
        matching_SCs.append(SC)
    if len(matching_SCs) > 0 and deficiency > 0:
        exhaustive_search(matching_SCs, mel, deficiency - 1)

def covering_sets_by_count(SC_list, mel, deficiency):
    """
    Print all set classes that explain mel at the given deficiency in
    order of number of instances of the set class.
    """
    sufficient_SCs = deficiency_given_SCs(SC_list, mel, deficiency)
    instances_by_SC = []
    for SC in sufficient_SCs:
        instances_by_SC.append([SC, find_instances(SC, mel, deficiency)])
    instance_counts = set([len(inst) for [SC, inst] in instances_by_SC])
    for count in sorted(instance_counts, reverse = True):
        print(count)
        for SC in instances_by_SC:
            if len(SC[1]) == count:
                print(SC[0])
