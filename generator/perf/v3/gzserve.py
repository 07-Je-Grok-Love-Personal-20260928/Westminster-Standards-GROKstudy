import sys,gzip,os,http.server,functools
class H(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        path=self.translate_path(self.path)
        if os.path.isdir(path): path=os.path.join(path,'index.html')
        if not os.path.isfile(path) or 'gzip' not in self.headers.get('Accept-Encoding',''): return super().send_head()
        ct=self.guess_type(path)
        if not any(ct.startswith(x) for x in ('text/','application/javascript','application/json','image/svg')): return super().send_head()
        data=gzip.compress(open(path,'rb').read(),6)
        self.send_response(200);self.send_header('Content-Type',ct);self.send_header('Content-Encoding','gzip');self.send_header('Content-Length',str(len(data)));self.end_headers()
        import io;return io.BytesIO(data)
    def log_message(self,*a):pass
port,root=int(sys.argv[1]),sys.argv[2]
http.server.ThreadingHTTPServer(('127.0.0.1',port),functools.partial(H,directory=root)).serve_forever()
