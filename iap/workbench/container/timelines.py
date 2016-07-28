
class TimelinesManager:
    '''
    Manages multiple timelines.
    '''

    def __init__(self):
        self.timelines = {}

    def set_timescales(self, timescales):
        for i in range(len(timescales)):
            self.timelines[timescales[i]] = Timeline(i, timescales[i])

    def get_timescale_id(self, timescale):
        return self.timelines[timescale].id

    def add_timeline(self, timescale, timeline):
        self.timelines[timescale].timeline = list(timeline)

    def get_timeline(self, timescale):
        return list(self.timelines[timescale])

class Timeline:
    '''
    Represents single timeline. 
    Used to transfer from index to label and label to index.
    '''

    def __init__(self, id, timescale):
        self.id = id
        self.timescale = timescale
        self.timeline= []