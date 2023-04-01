from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests
import PyPDF2
import io
import re
import csv
from datetime import datetime

url= "https://tim.blog/2018/09/20/all-transcripts-from-the-tim-ferriss-show/"

req = Request(url)
html_page = urlopen(req)
bs = BeautifulSoup(html_page, "lxml")
title_link = {}
urls = []
transcript = []
pattern = re.compile('#')
for link in bs.find_all('a',text=pattern, attrs={'data-wpel-link' : True}):
  title_link[link.string] = link.get('href')
  urls.append(link.get('href'))

now = datetime.now().strftime("%d-%m-%Y-%H:%M:%S")

with open(f'content-{now}.csv', mode='w') as csv_file:
  fieldnames = ['title', 'url', 'content']
  writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
  writer.writeheader()

  for author, url in title_link.items():
    if url.endswith('.pdf'):
      print("page is pdf file")

      output = io.BytesIO()
      output.write(requests.get(url).content)
      output.seek(0)
      pdf_reader = PyPDF2.PdfFileReader(output)
      # Get the number of pages in the PDF
      num_pages = pdf_reader.numPages
      # Initialize a variable to store the text
      pdf_text = ""

      # Iterate through each page
      for page in range(num_pages):
          # Extract the text from the page
          pdf_text += pdf_reader.getPage(page).extractText()
      
      print("author, url", author, url)

      writer.writerow({'title': author, 'url': url, 'content': pdf_text})

    elif url.endswith('.mp3') or url.endswith('manifesto') or url.endswith('freedom/'):
      print("skipping these")
    else:
      response = requests.get(url)
      soup = BeautifulSoup(response.text, 'html.parser')
      content = []
      blockquote = soup.find('blockquote')
      if blockquote:
        next_element = blockquote.find_next_sibling()
        while next_element:
          if next_element.name == "p":
            content.append(next_element.get_text())
          elif next_element.name == "div" and "jp-relatedposts" in next_element["class"]:
            break
          next_element = next_element.find_next_sibling()
        if content:
          title = soup.find('title').text
          print("url---->",title, url)
          writer.writerow({'title': title, 'url': url, 'content': ''.join(content)})