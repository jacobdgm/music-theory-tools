# Music Theory Tools

A collection of functions useful for analyzing musical relationships.

## array_notation.py

A tool for exploring interval ratios in microtonal music, array_notation.py takes a given ratio and decomposes it into its prime factors, returning it in array notation - as a list of powers of successive prime numbers.

For example, since 3/2 is equal to 2^-1 * 3^1, its array notation is [-1, 1].
For example, since 7/8 is equal to 2^-3 * 7^1, its array notation is [-3, 0, 0, 1].

array_notation.py searches for prime factors only up to 53.

## set\_class\_tools.py

This collection of functions was originally written as part of a term paper for a Mathematical Models for Music Analysis graduate seminar I took in the fall of 2019. 

<hr>

The functions in set_class_tools have been constructed to work in set-class universes of any size. The universe size, set by default to 12, can be adjusted by changing the value of ​`univ`​ after starting the program.

A number of common set classes have been included in the program: the ​`triad`, the `pentatonic` scale, and the ​`diatonic` scale (encoded versions of two pieces of music, addressed later in this paper, have also been included for demonstration purposes). The aggregate for the current universe size can be generated using the function ​`aggregate()​`:

```
>>> triad
[0, 3, 7]
>>> pentatonic
[0, 2, 4, 7, 9]
>>> diatonic
[0, 1, 3, 5, 6, 8, 10]
 >>> aggregate()
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
>>> univ = 7
>>> aggregate()
[0, 1, 2, 3, 4, 5, 6]
```

A maximally distributed scale of a given cardinality can be generated using the function `max_distributed()​` (all examples are shown as though the program has continued to run from the previous example: here, `univ` begins at a value of 7):

```
>>> max_distributed(3) [0, 2, 4]
>>> univ = 12
>>> max_distributed(5) [0, 2, 4, 7, 9]
```

Functions have been included to transpose, invert and retrograde series of pitches. `transpose()​` takes a series of pitches and an index by which to transpose them:

```
>>> transpose([0, 2, 4, 5, 4], 1) [1, 3, 5, 6, 5]
>>> transpose([0, 7, 4, 0], -2) [10, 5, 2, 10]
```

`invert()​` takes a series of pitches and an optional index around which to invert them. If no index is provided, the pitches are inverted around an index of 0:

```
>>> invert(triad) [0, 9, 5]
>>> invert(triad, 7) [7, 4, 0]
```

`retrograde()​` takes a series of pitches and returns them in reversed order:

```
>>> retrograde([1, 2, 3, 4])
[4, 3, 2, 1]
```

set_class_tools can perform multiplicative transformations on series of pitches. ​`m()​` takes a series of pitches and a multiplier. If the multiplier shares common multiples with univ, set_class_tools will print a warning message but will complete the calculation:

```
>>> m([0, 1, 2, 3], 7)
[0, 7, 2, 9]
>>> m([0, 1, 2, 3], 4)
Warning: index and univ are not coprime [0, 4, 8, 0]
```

`complement()​` returns all pitches in the universe that are not in a given set. `​vector()​` returns a given set’s interval vector.

```
>>> complement(diatonic) [2, 4, 7, 9, 11]
>>> vector(diatonic)
[2, 5, 4, 3, 6, 1]
>>> vector(triad) [0, 0, 1, 1, 1, 0]
```


set_class_tools contains a number of tools to generate set classes. ​`SC()​` reduces the input to a single set and returns it in least right-packed form—below, it returns the prime form of the major scale, and lists the notes of a familiar folk song. `​SCs_card_range()​` returns all set classes within a specified range of cardinalities.

```
>>> SC([0, 2, 4, 5, 7, 9, 11])
[0, 1, 3, 5, 6, 8, 10]
>>> twinkle
[0, 0, 7, 7, 9, 9, 7, 5, 5, 4, 4, 2, 2, 0] >>> SC(twinkle)
[0, 2, 4, 5, 7, 9]
>>> SCs_card_range(2, 3)
[[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6],
[0, 1, 2], [0, 1, 3], [0, 1, 4], [0, 1, 5], [0, 1, 6], [0, 2, 4], [0, 2, 5], [0, 2, 6], [0, 2, 7], [0, 3, 6], [0, 3, 7], [0, 4, 8]]
```

set_class_tools includes a number of functions for comparing set classes. `​are_z_related()​` returns True​ if the two given sets have the same interval vector. Robert Morris’ SIM and ASIM comparisons can be evaluated using the `​sim()​` and ​`asim()​` functions. `emb()​` returns how many times a set can be embedded in a second set. By default, ​`emb()​` searches all inversions and transpositions of the first set, but these deeper searches can be turned off by including additional arguments.

```
>>> are_z_related([0, 1, 3, 7], [0, 1, 4, 6])
True
>>> are_z_related(triad, diatonic)
False
>>> sim(triad, diatonic) 18
>>> asim(triad, diatonic) 0.75
>>> emb(triad, diatonic)
6
>>> emb(triad, diatonic, check_inversions = False)
3
>>> emb([0, 4, 8], [0, 2, 4, 6, 8, 10], check_inversions = False,
check_transpositions = False)
1
```

### Deficiency Searches

set_class_tools contains a number of tools for evaluating whether a given set class can be used to explain all the pitches in a given melody. Following David Lewin, a “deficiency” parameter has been included to allow for a given number of gaps in any instance of the set class (Lewin, 2007). Consider the first six notes of an ascending major scale. The set class [0, 2, 4] can be used to explain all the notes in this short melody: the first three notes are covered by the set class in its prime form, while the last three notes of the melody are explained by the set class transposed up five semitones. ​`explained_by_patt()​`, given the set class and the melody in question, returns ​`True`​.

```
>>> first_six = [0, 2, 4, 5, 7, 9]
>>> explained_by_patt([0, 2, 4], first_six)
True
```

If pitches 4 and 5, however, are reversed in the melody, ​`explained_by_patt()​` will return `False`​, since [0, 2, 4] cannot be found as three consecutive onsets. If `explained_by_patt()` is run with a deficiency of 1, however, the function will skip over up to one onset while searching for instances of the set class. In this case, the function will return ​`True`​: [0, 2, 4] is found, with 5 having been skipped over, and [5, 7, 9] will be found, with 4 having been skipped over:

```
>>> six_scrambled = [0, 2, 5, 4, 9, 7]
>>> explained_by_patt([0, 2, 4], six_scrambled)
False
>>> explained_by_patt([0, 2, 4], six_scrambled, dfcy = 1)
True
```

The ​`deficiency_given_SCs()​` function can be used to check multiple set classes against a given melody. Here, ​`deficiency_given_SCs()​` and ​`SCs_card_range()​` are used to search for all set classes of cardinality 3 or 4 that can explain all the notes in ​`six_scrambled` up to a maximum deficiency of 1:

```
>>> deficiency_given_SCs(SCs_card_range(3, 4), six_scrambled, deficiency = 1)
[[0, 2, 4], [0, 2, 5], [0, 1, 3, 5], [0, 2, 4, 7]]
```

`exhaustive_search()​` can be used to search for all set classes that can explain all the notes in a melody. All set classes that can explain the melody at a given maximum deficiency are then tested at increasingly strict maximum deficiencies until no set classes remain. `exhaustive_search()​` prints its output, rather than returning it.

```
>>> exhaustive_search(SCs_card_range(3, 4), six_scrambled, deficiency = 1)
deficiency = 1
[0, 2, 4]
[0, 2, 5]
[0, 1, 3, 5]
[0, 2, 4, 7]
deficiency = 0
[0, 2, 5]
[0, 1, 3, 5]
```

`find_instances()​` finds all instances of a given set class in a given melody at a given maximum deficiency. Instances are returned as list of pairs of pitch-class sets and the index of the first note that participates in that set. `find_instances_formatted()` can be used to unpack this list, printing each instance on its own line.

```
>>> find_instances([0, 2, 4], six_scrambled, dfcy = 1)
[[[0, 2, 4], 0], [[5, 7, 9], 2]]
>>> find_instances_formatted([0, 2, 4], six_scrambled, dfcy = 1)
0 [0, 2, 4]
2 [5, 7, 9]
```

Deficiency and instance searches can be conducted on “melodies” that include multiple notes sounding simultaneously. Simultaneities can be encoded by surrounding simultaneous notes in parentheses. If one or more notes in a given onset participate in an instance of the pitch-class set, deficiency is not incremented. For example, consider a melody with three onsets, one of which has two notes played in harmony: [0, (2, 3), 5]. This melody can be explained by the set class [0, 2, 5] at a maximum deficiency of 0: pitch-class 2 can be found in [0, 2, 5], pitch class 3 can be found in the set class' inversion [0, 3, 5], and in both cases, no onset has been skipped over. If pitch classes 2 and 3 are encoded sequentially, however—[0, 2, 3, 5]—a test at a maximum deficiency of 1 would fail, because one of the middle onsets needs to be skipped over.

```
>>> explained_by_patt([0, 2, 5], [0, (2, 3), 5], 0)
True
>>> find_instances_formatted([0, 2, 5], [0, (2, 3), 5], 0)
0 [0, 2, 5]
0 [0, 3, 5]
>>> explained_by_patt([0, 2, 5], [0, 2, 3, 5], 0)
False
```

Finally, `covering_sets_by_count()` can be used to find the optimal set class to explain a given melody, measured by how many instances of the set class can be found in the melody. Let's use `exhaustive_search()` to see which set classes of cardinality 4 can account for all the notes of the first phrase of Twinkle, Twinkle Little Star (included in variable `twinkle`):

```
>>> exhaustive_search(SCs_card_range(4, 4), twinkle, deficiency = 4)
deficiency = 4
[0, 2, 3, 7]
[0, 2, 4, 7]
[0, 2, 5, 7]
[0, 3, 5, 8]
deficiency = 3
[0, 2, 3, 7]
[0, 2, 4, 7]
[0, 3, 5, 8]
deficiency = 2
[0, 2, 3, 7]
[0, 2, 4, 7]
deficiency = 1
```

Both [0, 2, 3, 7] and [0, 2, 4, 7] can explain all the notes in the melody at a maximum deficiency of 2! But are there more instances of [0, 2, 3, 7], or of [0, 2, 4, 7]?

```
>>> covering_sets_by_count([[0, 2, 3, 7], [0, 2, 4, 7]], twinkle, deficiency = 2)
7
[0, 2, 4, 7]
5
[0, 2, 3, 7]
```

So it turns out you can find more instances of [0, 2, 4, 7] than [0, 2, 3, 7] in the first phrase of Twinkle, Twinkle Little Star.