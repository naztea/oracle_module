# oracle_module

This module will allow you to write oracle sql command straight into your playbook.
the return is a list of dictionaries with the column-name as key, and the row as value.
This module is quite easily adaptable to mssql and mysql, as the python modules are quite similar.
It does require the python module cx-Oracle(==8.2.1, tested). And it requires the Oracle instantclient, and libaio1 packages.

### install example for fedora/rhel
curl -o libaio-0.3.111-14.fc37.x86_64.rpm https://kojipkgs.fedoraproject.org//packages/libaio/0.3.111/14.fc37/x86_64/libaio-0.3.111-14.fc37.x86_64.rpm

sudo rpm -i libaio-0.3.111-14.fc37.x86_64.rpm

curl -o oracle-instantclient-basic-21.8.0.0.0-1.el8.x86_64.rpm https://download.oracle.com/otn_software/linux/instantclient/218000/oracle-instantclient-basic-21.8.0.0.0-1.el8.x86_64.rpm

sudo rpm -i oracle-instantclient-basic-21.8.0.0.0-1.el8.x86_64.rpm

### Example playbook
---

\- name: "Test oracle connection"

  hosts: localhost
  
  gather_facts: false
  
  tasks:

    - name: "Execute orcl_spl module"
    
      orcl_sql:
      
        hostname: "<ip/hostname>:<port>"
        
        database: "<database-name>"
        
        username: "<username>"
        
        password: "<password>"
        
        queries:
        
          - query_var: "first_query"
          
            query: |
            
              SELECT * FROM "table"
              
      register: sql

    - name: "Show return"
    
      ansible.builtin.debug:
      
        var: sql


### Example output
TASK [Show return] **************************************************************************************************************************************************************************************************************************
ok: [localhost] => {
    "sql": {
        "changed": false,
        "failed": false,
        "message": "",
        "original_message": "",
        "sql_return": {
            "first_query": {
                "query": "SELECT * FROM \"lb_tenants\"\n",
                "return": [
                    {
                        "comment": null,
                        "id": 1,
                        "name": "Dampfnudel",
                        "se_consumer": null,
                        "se_provider": false,
                        "status": "beauftragt"
                    }
                ]
            }
        },
        "stdout": "{\"db_lock\": {\"query\": \"SELECT * FROM \\\"lb_tenants\\\"\\n\", \"return\": [{\"name\": \"Dampfnudel\", \"status\": \"beauftragt\", \"id\": 1, \"se_provider\": false, \"comment\": null, \"se_consumer\": null}]}}",
        "stdout_lines": [
            "{\"db_lock\": {\"query\": \"SELECT * FROM \\\"lb_tenants\\\"\\n\", \"return\": [{\"name\": \"Dampfnudel\", \"status\": \"beauftragt\", \"id\": 1, \"se_provider\": false, \"comment\": null, \"se_consumer\": null}]}}"
        ],
        "warnings": [
            "Module did not set no_log for password"
        ]
    }
}
