from SPARQLWrapper import SPARQLWrapper, JSON

# GraphDB의 SPARQL Endpoint URL 설정
# endpoint_url_insert = "http://jeonsuhyeong-ui-MacBookPro.local:7200/repositories/Diabete/statements"
endpoint_url = "http://jeonsuhyeong-ui-MacBookPro.local:7200/repositories/Diabete"

# sparql_query = """
# PREFIX Untitled: <http://www.semanticweb.org/wjchoi/ontologies/2023/9/untitled-ontology-27#>
# PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
# INSERT DATA {
# Untitled:temp_patient5 Untitled:hasAgeof 25 .
# Untitled:temp_patient5 rdf:type Untitled:정상간 .
# }
# """
# # SPARQLWrapper를 사용하여 쿼리 실행
# sparql = SPARQLWrapper(endpoint_url_insert)
# sparql.setQuery(sparql_query)
# print(sparql)
# sparql.method = "POST"
# sparql.setReturnFormat('json')
# sparql.queryType = "INSERT"
# try:
#     sparql.query()
#     print("SPARQL 쿼리가 성공적으로 실행되었습니다.")
# except Exception as e:
#     print(f"오류 발생: {e}")
#
# exit()
# SPARQL 쿼리 설정 (예제 쿼리)
query = """
PREFIX Untitled: <http://www.semanticweb.org/wjchoi/ontologies/2023/9/untitled-ontology-27#>

SELECT ?property ?value
WHERE {
  Untitled:patient_3 ?property ?value .
}
"""

"""
SELECT ?individual ?class
WHERE {
  ?individual rdf:type owl:NamedIndividual .
  ?individual rdf:type ?class .
}
"""

# SPARQLWrapper를 사용하여 쿼리 실행
sparql = SPARQLWrapper(endpoint_url)
sparql.setQuery(query)
sparql.setReturnFormat(JSON)
print(sparql)
# exit()
results = sparql.query().convert()
print(results)

# 결과 출력
for result in results["results"]["bindings"]:
    a = result['property']['value']
    subject = result["value"]["value"]
    print(a)
    print(subject)
