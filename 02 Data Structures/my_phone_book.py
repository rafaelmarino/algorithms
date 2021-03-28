# python3

class Query:
    def __init__(self, query):
        self.type = query[0]
        self.number = int(query[1])
        if self.type == 'add':
            self.name = query[2]

def read_queries():
    n = int(input())
    return [Query(input().split()) for i in range(n)]

def write_responses(result):
    print('\n'.join(result))

def process_queries(queries):
    result = []
    # Keep list of all existing (i.e. not deleted yet) contacts.
    contacts = []
    for cur_query in queries:
        if cur_query.type == 'add':
            # if we already have contact with such number,
            # we should rewrite contact's name
            for contact in contacts:
                if contact.number == cur_query.number:
                    contact.name = cur_query.name
                    break
            else:  # otherwise, just add it
                contacts.append(cur_query)
        elif cur_query.type == 'del':
            for j in range(len(contacts)):
                if contacts[j].number == cur_query.number:
                    contacts.pop(j)
                    break
        else:
            response = 'not found'
            for contact in contacts:
                if contact.number == cur_query.number:
                    response = contact.name
                    break
            result.append(response)
    return result

def faster_process_queries(queries):
    result = []
    # Keep list of all existing (i.e. not deleted yet) contacts.
    size = 10 ** 7
    contacts = [None] * size
    # Hashing integers according to lecture formula
    for cur_query in queries:
        # hash an integer per query_i.number
        index = ((34 * cur_query.number + 2) % 10000019) % size
        if cur_query.type == 'add':
            # if we already have contact with such number,
            # we should rewrite contact's name
            if contacts[index] != None:  # if true, query added before
                contacts[index].name = cur_query.name
            else:  # otherwise, add the query OBJECT
                contacts[index] = cur_query
        elif cur_query.type == 'del':
            if contacts[index] != None:
                contacts[index] = None
        else:
            response = 'not found'
            if contacts[index] != None:
                response = contacts[index].name
            result.append(response)
    return result

if __name__ == '__main__':
    write_responses(faster_process_queries(read_queries()))

# key thought in direct addressing: having a direct place to look an item at
# (the index), is a an O(1) search vs O(n) if you have to scan for a key value