from colorama import Fore, Style
import threading, sys, time, re, modules.gpo_indexes as gpo_indexes

# Class for threads to index file
class indx_thread(threading.Thread):
    def __init__(self, read_material, read_start, read_end, thread_name):
        threading.Thread.__init__(self)
        #Each thread will track it's own found indices and data
        self.name = thread_name
        self.read_material = read_material
        self.read_start = read_start
        self.read_end = read_end
        self.html_start = []
        self.html_end = []
        self.title_start = []
        self.title_end = []
        self.status_anchor = []
        self.effective_anchor = []
    def __str__(self):
        return f'''
            html_start indexes are {self.html_start}
            html_end indexes are {self.html_end}
            title_start indexes are {self.title_start}
            title_end indexes are {self.title_end}
            status_anchor indexes are {self.status_anchor}
            effective_anchor indexes are {self.effective_anchor}
        '''
    def run(self):       
        for indx, content in enumerate(self.read_material[self.read_start:self.read_end]):
            if(content=="<"):
                # Search for opening HTML tags of interest
                if(self.read_material[(self.read_start+indx):(self.read_start+indx)+6]=="<html " and self.read_material[(self.read_start+indx)-1:(self.read_start+indx)+6]!="\"<html "):
                    self.html_start.append((self.read_start+indx))
                elif(self.read_material[(self.read_start+indx):(self.read_start+indx)+7]=="<title>" and self.read_material[(self.read_start+indx)-1:(self.read_start+indx)+8]!="\"<title>\""):
                    self.title_start.append((self.read_start+indx)+7)
                # Determine the status of each GPO
                elif(self.read_material[(self.read_start+indx):(self.read_start+indx)+56]=="<tr><td scope=\"row\">GPO Status</td><td>Enabled</td></tr>"):
                    self.status_anchor.append("enabled    ")
                elif(self.read_material[(self.read_start+indx):(self.read_start+indx)+70]=="<tr><td scope=\"row\">GPO Status</td><td>All settings disabled</td></tr>"):
                    self.status_anchor.append("disabled   ")
                elif(self.read_material[(self.read_start+indx):(self.read_start+indx)+71]=="<tr><td scope=\"row\">GPO Status</td><td>User settings disabled</td></tr>"):
                    self.status_anchor.append("computer   ")
                elif(self.read_material[(self.read_start+indx):(self.read_start+indx)+75]=="<tr><td scope=\"row\">GPO Status</td><td>Computer settings disabled</td></tr>"):
                    self.status_anchor.append("user       ")
                elif(self.read_material[(self.read_start+indx):(self.read_start+indx)+35]=="<tr><td scope=\"row\">GPO Status</td>"):
                    self.status_anchor.append((self.read_start+indx))
                # Determine if the GPO is ineffective
                elif(("<b>The settings in this GPO can only apply to the following groups, users, and computers:</b>") in self.read_material[(self.read_start+indx):(self.read_start+indx)+93] and ("<tr><td>None</td></tr>" in self.read_material[(self.read_start+indx):(self.read_start+indx)+250])):
                    self.effective_anchor.append("ineffective")
                elif(("<b>The settings in this GPO can only apply to the following groups, users, and computers:</b>") in self.read_material[(self.read_start+indx):(self.read_start+indx)+93]):
                    self.effective_anchor.append((self.read_start+indx))
                # Search for closing HTML tags of interest.
                elif(self.read_material[(self.read_start+indx):(self.read_start+indx)+7]=="</html>" and self.read_material[(self.read_start+indx):(self.read_start+indx)+8]!="</html>\""):
                    self.html_end.append((self.read_start+indx))
                elif(self.read_material[(self.read_start+indx):(self.read_start+indx)+8]=="</title>" and self.read_material[(self.read_start+indx)-1:(self.read_start+indx)+9]!="\"</title>\"" and self.read_material[(self.read_start+indx-1):(self.read_start+indx)+9]!="\"</title>\\"):
                    self.title_end.append((self.read_start+indx))

# Index GPOReport
def concurrent_index_file(filecontent):
    thread_count = 3
    thread_divisible = int((len(filecontent)/thread_count))
    thread_pool = []

    for count in range(thread_count):
        if(count!=thread_count-1):
            thread_pool.append(indx_thread(filecontent, (thread_divisible*count), ((thread_divisible*(count+1))-1), "thread"+str(count)))
        else:
            thread_pool.append(indx_thread(filecontent, (thread_divisible*count), len(filecontent), "thread"+str(count)))
    
    # Push threads to the background and start
    for thread in thread_pool:
        thread.setDaemon(True)
        thread.start()
    
    # Print feedback to indicate processing.
    counter = 0
    options = [
        "\r"+Style.BRIGHT+Fore.BLUE+"."+"   "+Style.RESET_ALL,
        "\r"+Style.BRIGHT+Fore.BLUE+"."+Fore.GREEN+".  "+Style.RESET_ALL,
        "\r"+Style.BRIGHT+Fore.BLUE+"."+Fore.GREEN+"."+Fore.RED+". "+Style.RESET_ALL,
        "\r"+Style.BRIGHT+Fore.BLUE+"."+Fore.GREEN+"."+Fore.RED+"."+Fore.WHITE+"."+Style.RESET_ALL]
    while(threading.active_count() > 1):
        if(counter==4):
            counter=0
        print(options[counter], end="")
        time.sleep(0.05)
        counter+=1

    Indexes = gpo_indexes.GPO_Indexes()
    Indexes.construct_master_index(thread_pool)
    return Indexes

# Check for Errors - Exit in the case of error
def review_validation(validate, start):
    if(validate):
        print("\r"+validate)
        sys.exit()
    else:
        print(Style.BRIGHT+Fore.GREEN+f'\rParsing the GPO Report took{time.time() - start : .2f} seconds.'+Style.RESET_ALL)
