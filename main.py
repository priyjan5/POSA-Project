import elasticsearch
from pprint import pprint

tor_network ={
    'private_network1':
    {
        'DAs':
        [
            {
                'Nickname': 'DA1',
                'Fingerprint': 'FG',
                'V3ident': 'V3',
                'ORPort': 0,
                'DIRPort': 7000,
                'ControlPort':5601
            },

            {
                'Nickname': 'DA2',
                'Fingerprint': 'FG',
                'V3ident': 'V3',
                'ORPort': 0,
                'DIRPort': 7000,
                'ControlPort':5601
            }
        ],

        'Relays':
        [
           {
                'Nickname': 'Relay1',
                'Fingerprint': 'FG',
                'V3ident': 'V3',
                'ORPort': 0,
                'DIRPort': 7000,
                'ControlPort':5601
            },

            {
                'Nickname': 'Relay2',
                'Fingerprint': 'FG',
                'V3ident': 'V3',
                'ORPort': 0,
                'DIRPort': 7000,
                'ControlPort':5601
            }

        ]
    }
}



#Take user network paramaters from webapp

#Generate torrc files for all boxes



#Spawn boxes using openstack API



#Publish tor_network json to ES

es = elasticsearch.Elasticsearch('172.16.106.155')
es.index(
       index="tor_network",
       doc_type='tor_network',
       id=2,
       body = tor_network
       )

pprint(tor_network)
