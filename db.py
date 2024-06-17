from google.cloud import datastore

def connect():
    return datastore.Client()

def insert_data(health_activities):
    client = connect()
    for activity in health_activities:
        key = client.key('HealthActivity')
        entity = datastore.Entity(key)
        entity.update({
            'question': activity['question'],
            'preference': activity['preference']
        })
        client.put(entity)

def fetch_all_data(filters=None):
    client = connect()
    query = client.query(kind='HealthActivity')

    if filters:
        if 'id' in filters:
            key = client.key('HealthActivity', int(filters['id']))
            entity = client.get(key)
            if entity:
                return [{
                    'id': entity.key.id,
                    'question': entity.get('question', None),
                    'preference': entity.get('preference', None)
                }]
            else:
                return []
        if 'preference' in filters:
            query.add_filter('preference', '=', filters['preference'])

    results = list(query.fetch())
    activities = []
    for result in results:
        activity = {
            'id': result.key.id,  # Include ID for update/delete operations
            'question': result.get('question', None),
            'preference': result.get('preference', None)
        }
        activities.append(activity)
    return activities

def update_data(id, data):
    client = connect()
    key = client.key('HealthActivity', id)
    entity = client.get(key)
    if not entity:
        return False
    entity.update({
        'question': data.get('question', entity['question']),
        'preference': data.get('preference', entity['preference'])
    })
    client.put(entity)
    return True

def delete_data(id):
    client = connect()
    key = client.key('HealthActivity', id)
    entity = client.get(key)
    if not entity:
        return False
    client.delete(key)
    return True
