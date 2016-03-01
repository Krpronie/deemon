'''
Created on Dec 1, 2015

@author: gianko
'''
import urlparse
import sqlparse

fmt = "{:>5}  {:>5}  {:<5} {:<30}"

def serverconnect(context, server_conn):
    pass

def clientconnect(context, root_layer):
    pass


def mysqlproxy_is_running(context, proc):
    print fmt.format(*["SEL", "ST_CH", "METHD", "URL"])


"""
Return true if the request can be async.
"""
def is_async_request(context, request):
    host = request.headers["host"][0]
    
    # If request is for an external, let's send it async
    
    if host not in ["192.168.56.4"]:
        return True
    
    url = "{}{}".format(host, request.path)
    urlp = urlparse.urlparse(url)
    ext  = urlp.path.split(".")[-1]
    if ext in ["jpg", "gif", "png", "ico",
               "css", "woff2",
               "js"]:
        return True

    return False

"""
Do whatever you want with the queries, e.g., dynamic taint-analysis requests vs queries
"""
def process_queries(context, request, queries):
    host = request.headers["host"][0]
    url = "{}{}".format(host, request.path)
   
    sel   = 0
    st_ch = 0
    #print queries
    for q in queries:
        #print ">>", q, "<<"
        
        sql = sqlparse.parse(q)
        if sql[0].tokens[0].value.upper() in ["SELECT"]:
            sel += 1
        if sql[0].tokens[0].value.upper() in ["UPDATE", "INSERT", "CREATE", "ALTER", "DROP"]:
            st_ch += 1

    
    print fmt.format(*[sel, st_ch, request.method, url])


def request(context, flow):
    pass
    #print "handle request: {}{}".format(flow.request.host, flow.request.path)
    
    
def response(context, flow):
    pass
    #print "handle response: {}{}".format(flow.request.host, flow.request.path)
