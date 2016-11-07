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
                'ControlPort':5601,
                'IP':''
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
                'ControlPort':5601,
                'ExitPolicy':''
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


valid_after = r"""(valid-after ([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2}):([0-9]{2}))\n(fresh-until ([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2}):([0-9]{2}))\n(valid-until ([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2}):([0-9]{2}))\n"""

#Take user network paramaters from webapp


dir-source DAzeiwa 71332F494F6AB32F55DB530B652C92C8A71AE0BB 172.16.106.155 172.16.106.155 9898 7000

/^[a-z\-]/

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
