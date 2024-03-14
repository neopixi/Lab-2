import pandas as pd
import xml.etree.ElementTree as ET

df = pd.read_csv('books.csv', delimiter=';', encoding='windows-1251')
df['Цена поступления'] = pd.to_numeric(df['Цена поступления'], errors='coerce')

long_titles_count = df[df['Название'].str.len() > 30].shape[0]
print(long_titles_count)

def search_books_by_author(author, limit=5):
    result = df[df['Автор'].str.contains(author, case=False, na=False)]
    result = result[result['Цена поступления'] <= 150]
    result = result.head(limit)
    return result

print(search_books_by_author(input("Введите автора: "), limit=10)) # ! Ждет ввода с клавиатуры !

bibliographic_references = df.sample(n=20).apply(lambda x: f"{x['Автор']}. {x['Название']} - {x['Дата поступления'].split(' ')[0]}", axis=1)
bibliographic_references.to_csv('bibliographic_references.txt', index_label='№', header=False)

print("\n\n\nXML: ")
with open('currency.xml', 'r', encoding='windows-1251') as file:
    xml_data = file.read()
root = ET.fromstring(xml_data)

currency_dict = {}

for valute in root.findall('Valute'):
    name = valute.find('Name').text
    value_str = valute.find('Value').text
    value = float(value_str.replace(',', '.'))
    
    currency_dict[name] = value

for name, value in currency_dict.items():
    print(f"{name}: {value}")
