from quest.annotations import (provided, provider)
from quest.decorators import (plugin)
from quest.types import DataType
from quest.system import System


System.register(
    DataType('timeline_data', 
             ['start_time', 'end_time'], 
             lambda data: 'Timeline: start @ {}, end @ {}'.format(data.start_time, data.end_time)
    )
)
System.register(
    DataType('event_data', 
             ['events'],
             lambda data: 'Events: {}'.format('\n\t' + '\n\t'.join(map(str, data.events)))
    )
)


@plugin(System)
def process_events_data(event_data:provider):
    event_data.events = event_data.events or []
    while True:
        item = yield
        if 'foo' in item['attrs']:
            event_data.events.append({'type': 'FOO-EVENT', 'origin': item})
        if 'time' in item:
            event_data.events.append({'type': 'TIME-EVENT', 'origin': item, 'value': item['time']})


@plugin(System)
def process_timeline_data(event_data:provided, timeline_data:provider):
    time_events = [e for e in event_data.events if e['type'] == 'TIME-EVENT']
    if not time_events:
        timeline_data.start_time = None
        timeline_data.end_time = None
    else:
        timeline_data.start_time = time_events[0]['value']
        timeline_data.end_time = time_events[-1]['value']


sys = System([
    dict(attrs=['foo']),
    dict(attrs=['foo'], time=0),
    dict(attrs=[], time=5),
    dict(attrs=['foo'], time=9)
])

data = sys.run()
print('\n'.join(map(str, data.values())))


