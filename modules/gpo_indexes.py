from colorama import Fore, Style

# Class used to define index storage object.
class GPO_Indexes:
    def __init__(self):
        self.html_start=[]
        self.html_end=[]
        self.title_start=[]
        self.title_end=[]
        self.status_anchor=[]
        self.effective_anchor=[]
    def __str__(self):
        return f'''
            Master:
            html_start indexes are {self.html_start}
            html_end indexes are {self.html_end}
            title_start indexes are {self.title_start}
            title_end indexes are {self.title_end}
            status_anchor indexes are {self.status_anchor}
            effective_anchor indexes are {self.effective_anchor}
        '''
    def print_index_counts(self):
        print(f'''
            Counts:
            html_start - {len(self.html_start)}
            html_end - {len(self.html_end)}
            title_start - {len(self.title_start)}
            title_end - {len(self.title_end)}
            status_anchor - {len(self.status_anchor)}
            effective_anchor - {len(self.effective_anchor)}
        ''')
    def validate_indexes(self):
        error_out = ""
        
        gpo_num = len(self.html_start)
        for indx in [self.html_end, self.title_start, self.title_end, self.status_anchor, self.effective_anchor]:
            if len(indx)!=gpo_num:
                error_out = "\r"+Style.BRIGHT+Fore.RED+"Indexing experienced an error.\n"+Style.RESET_ALL+"It appears the file might be corrupted.\nThere is not a matching number of indexes!"        
        return error_out

    def construct_master_index(self, thread_list):
        for thread in thread_list:
            for indx in thread.html_start:
                self.html_start.append(indx)
            for indx in thread.html_end:
                self.html_end.append(indx)
            for indx in thread.title_start:
                self.title_start.append(indx)
            for indx in thread.title_end:
                self.title_end.append(indx)
            for indx in thread.status_anchor:
                self.status_anchor.append(indx)
            for indx in thread.effective_anchor:
                self.effective_anchor.append(indx)