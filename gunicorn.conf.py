import multiprocessing

bind = "127.0.0.1:5959"
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = "access.log"
errorlog = "errors.log"
pidfile = "pidfile"
proc_name = "uuber.me"
