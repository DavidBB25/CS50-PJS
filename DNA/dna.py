import csv
import sys


def main():

    # TODO: Check for command-line usage
    command_line_usage()

    # TODO: Read database file into a variable
    data = databasevar()

    # TODO: Read DNA sequence file into a variable
    dnaseq = dnaseqvar()

    # TODO: Find longest match of each STR in DNA sequence
    DSTR = {
        "AGATC": longest_match(dnaseq, "AGATC"),
        "TTTTTTCT": longest_match(dnaseq, "TTTTTTCT"),
        "AATG": longest_match(dnaseq, "AATG"),
        "TCTAG": longest_match(dnaseq, "TCTAG"),
        "GATA": longest_match(dnaseq, "GATA"),
        "TATC": longest_match(dnaseq, "TATC"),
        "GAAA": longest_match(dnaseq, "GAAA"),
        "TCTG": longest_match(dnaseq, "TCTG"),
    }

    # TODO: Check database for matching profiles
    counters = {}
    for person in data:  # iterate through each person
        count = 0
        # print(person) # DEBUG
        for dnastr in DSTR:  # iterate through each str
            # print(dnastr) # DEBUG
            if dnastr in person.keys():  # if str is in person
                # print("^^^")
                # print(f"THIS IS THE VALUE OF THE CURRENT STR: {DSTR[dnastr]}") # DEBUG
                # print(f"THIS IS THE VALUE OF THE CURRENT PERSON STR: {person[dnastr]}") # DEBUG
                # check if the value of the str is equal to the value of the person str
                if DSTR[dnastr] == int(person[dnastr]):
                    count += 1
                    # print("yes") # DEBUG
                else:
                    continue

                counters[person["name"]] = count

    maxs = max(counters, key=counters.get)
    if counters[maxs] == len(data[0].keys()) - 1:
        print(maxs)
    else:
        print("No match.")

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


def command_line_usage():
    if len(sys.argv) != 3:
        print("Usage: database.csv sequence.txt")
        sys.exit(1)


def databasevar():
    rows = []
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
    return rows  # list of dicts


def dnaseqvar():
    rows = []
    with open(sys.argv[2]) as file:
        reader = file.read()
        return reader  # list


main()
