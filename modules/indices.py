class Indices:

    def __init__(self):
        self.start_indices=[]
        self.end_indices=[]
        self.gpo_statuses=[]
        self.names = []
        self.ineffective=[]

    def __repr__(self):
        return f"{self.start_indices}\n{self.end_indices}\n{self.gpo_statuses}\n{self.names}\n{self.ineffective}"

    # Decorator to count how many indices exist for each class element
    def CountCalls(func):
        def wrapper(*args, **kwargs):
            wrapper.count += 1
            return func(*args, **kwargs)
        wrapper.count = 0
        return wrapper
    
    # Decorator to count which type of index is being parsed.
    def ParseCount(func):
        def wrapper(*args, **kwargs):
            wrapper.count += 1
            if(wrapper.count > 5):
                wrapper.count = 1
            return func(*args, **kwargs)
        wrapper.count = 0
        return wrapper
    
    @CountCalls
    def append_start(self, index_value):
        self.start_indices.append(index_value)

    @CountCalls
    def append_end(self, index_value):
        self.end_indices.append(index_value)

    @CountCalls
    def append_status(self, status_value):
        self.gpo_statuses.append(status_value)

    @CountCalls
    def append_name(self, name):
        self.names.append(name)

    @CountCalls
    def append_ineffective(self, ibool):
        self.ineffective.append(ibool)

    @ParseCount
    def parse_index(self, attribute):
        # Closing HTML tags
        if (self.parse_index.count)==5 and isinstance(attribute, int):
            self.append_end(attribute)
        elif (self.parse_index.count) == 4 and isinstance(attribute, bool):
            self.append_ineffective(attribute)
        # GPO Status
        elif (self.parse_index.count)==3 and isinstance(attribute, str):
            self.append_status(attribute)
        # Title Tags
        elif (self.parse_index.count)==2 and isinstance(attribute, str):
            self.append_name(attribute)
        # Opening HTML Tags    
        elif (self.parse_index.count)==1 and isinstance(attribute, int):
            self.append_start(attribute)
        else:
            print(f"{self.parse_index.count} {type(attribute)} {attribute}")

    def return_indices(self):
        return self.start_indices, self.end_indices, self.gpo_statuses, self.names, self.ineffective
