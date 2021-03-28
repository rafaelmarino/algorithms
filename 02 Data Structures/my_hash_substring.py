# python3

def read_input():
    # prompts for 2 inputs and strip right whitespaces
    # returns tuple of 2 character vectors
    return (input().rstrip(), input().rstrip())

def print_occurrences(output):
    print(' '.join(map(str, output)))

def PolyHash(s, prime, multiplier):
    # Polyhash works on both the pattern and the strings
    # computes a cum sum of hashes per string mod p
    hash = 0
    for c in reversed(s):
        hash = (hash * multiplier + ord(c)) % prime
    return hash

def PrecomputeHashes(text, len_pattern, prime, multiplier):
    # calculates a hash for a substring of length equal to length(pattern)
    # at each character of the text, using polynomial string hashing
    H = [None] * (len(text) - len_pattern + 1)
    S = text[len(text) - len_pattern:]  # len of text - len pattern until end
    H[len(text) - len_pattern] = PolyHash(S, prime, multiplier)
    y = 1
    for i in range(len_pattern):
        y = (y * multiplier) % prime
    for i in range(len(text) - len_pattern - 1, -1, -1):
        H[i] = (multiplier * H[i+1] + ord(text[i]) - y * ord(text[i + len_pattern])) % prime
    return H

def Rabin_Karp(pattern, text):
    result = []
    # prime and multiplier are elements of a particular hash function
    # they have to be predefined for the hash fuction to be deterministic
    prime = 1610612741
    multiplier = 263
    p_hash = PolyHash(pattern, prime, multiplier)
    H = PrecomputeHashes(text, len(pattern), prime, multiplier)

    for i in range(len(text) - len(pattern) + 1):
        if p_hash == H[i] and text[i:i + len(pattern)] == pattern:
            result.append(i)

    return result

def get_occurrences(pattern, text):
    return [
        i
        for i in range(len(text) - len(pattern) + 1)
        if text[i:i + len(pattern)] == pattern
    ]

if __name__ == '__main__':
    # star operator unpacks a tuple or a list of elements to be read
    # as function arguments
    print_occurrences(Rabin_Karp(*read_input()))

