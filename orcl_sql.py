import re
import json
import cx_Oracle
from ansible.module_utils.basic import AnsibleModule

def sql_execute(sql_host, sql_username, sql_password, sql_db, sql_queries):
    my_dsn = str(sql_host) + "/" + str(sql_db)
    connection = cx_Oracle.connect(dsn=my_dsn, user=sql_username, password=sql_password)
    cursor = connection.cursor()
    r = {}
    for i,query in enumerate(sql_queries):
        query_cmd = query['query']
        query_var = query['query_var']
        r[query_var] = {}
        r[query_var]['query'] = query_cmd
        try:
            cursor.execute(str(query_cmd))
            try:
                columns = [col[0] for col in cursor.description]
                cursor.rowfactory = lambda *args: dict(zip(columns, args))
                payload = cursor.fetchall()
                r[query_var]['return'] = dict_convert(payload)
            except:
                r[query_var]['return'] = {}
                pass;
        except:
            r[query_var]['return'] = cursor.fetchall()
            r[query_var]['state'] = 'failed'
    connection.commit() # the commit after all queries makes sure, that all or none of the data is persisted
    connection.close()
    return r

def dict_convert(list):
    for obj in list:
        for keigh in obj.keys():
            try:
                temp = re.sub('\'','"',obj[keigh])
                keigh_obj = json.loads(temp)
                obj[keigh] = keigh_obj
            except:
                pass;
    return list
  
def run_module():
    module_args = dict(
        hostname=dict(type='str', required=True),
        database=dict(type='str', required=True),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True),
        queries=dict(type='list', required=True)
    )
    result = dict(
        changed=False,
        original_message='',
        message='',
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    if module.check_mode:
        module.exit_json(**result)
    hostname = module.params['hostname']
    username = module.params['username']
    password = module.params['password']
    database = module.params['database']
    queries  = module.params['queries']

    sql_return = sql_execute(hostname, username, password, database, queries)

    result['sql_return'] = sql_return
    result['stdout'] = json.dumps(sql_return)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
