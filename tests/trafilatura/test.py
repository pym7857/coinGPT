import trafilatura

html = trafilatura.fetch_url('https://blog.naver.com/tkdghks0222')
text = trafilatura.extract(html)
print(text)