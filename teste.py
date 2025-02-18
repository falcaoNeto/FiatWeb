from BD.bdPinecone import pc


inndex_name = "carrosfiat"
index = pc.Index(inndex_name)
for ids in index.list(namespace='ns1'):
    print(ids)
response = index.fetch(ids=[str(19)], namespace="ns1")
mentada = response["vectors"]["19"]["metadata"]["dados"]
print(mentada)