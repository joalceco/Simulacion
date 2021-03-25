import numpy as np

class Client():

    def __init__(self, id):
        self.id = id;
        self.arrival_time=0
        self.enter_queque_time=0
        self.exit_queque_time=0
        self.enter_supervisor_time=0
        self.exit_supervisor_time=0

    def __repr__(self):
        return "{} entro {:6.2f}, supervision {:6.2f}, salio {:6.2f}".format(self.id, self.arrival_time,self.enter_supervisor_time, self.exit_supervisor_time)

class Event():
    NEW_CUSTOMER_ARRIVAL = 1
    SUPERVISOR_EXIT = 2

    def __init__(self, time, event_type, client):
        self.time=time
        self.event_type=event_type
        self.client = client

    def __repr__(self):
        if self.event_type==self.NEW_CUSTOMER_ARRIVAL:
            return "{:6.2f} - Entro al sistema la Pieza {}".format(self.time, self.client.id)
        elif self.event_type==self.SUPERVISOR_EXIT:
            return "{:6.2f} - Pieza {} salio de supervision".format(self.time, self.client.id)
        else:
            return "{:6.2f} - Evento Desconocido".format(self.time)

    
        
def getTime(event):
    return event.time       

class Simulation():

    EMPTY = 0
    BUSY = 1

    def __init__(self, simulation_time=10000):
        self.simulation_time = simulation_time
        self.clock=0
        self.events=[]
        self.queue=[]
        self.exits=[]
        self.supervisor_state = self.EMPTY
        self.prepare_entries()

    def prepare_entries(self):
        time = 0
        id = 1
        while True:
            time += np.random.exponential(5)
            client = Client(id)
            id+=1
            client.arrival_time = time
            self.events.append(Event(time,Event.NEW_CUSTOMER_ARRIVAL, client))
            if time > self.simulation_time:
                self.events.pop()
                break

    def next_event(self):
        event = self.events.pop(0);
        if event.event_type == event.NEW_CUSTOMER_ARRIVAL:
            self.clock = event.time 
        return event


    def run(self):
        while self.events:
            event = self.next_event()
            self.clock = event.time
            if event.event_type == event.NEW_CUSTOMER_ARRIVAL:
                event.client.enter_queque_time = self.clock
                self.queue.append(event.client)
            elif event.event_type == event.SUPERVISOR_EXIT:
                self.supervisor_state = self.EMPTY
                event.client.exit_supervisor_time=self.clock
                self.exits.append(event.client)

            if self.supervisor_state == self.EMPTY and len(self.queue)>0:
                self.supervisor_state = self.BUSY
                next_client = self.queue.pop(0)
                busy_time = np.random.normal(4.0, 0.5)
                next_client.enter_supervisor_time = self.clock
                self.events.append(Event(self.clock+busy_time, Event.SUPERVISOR_EXIT, next_client))
                self.events.sort(key=getTime)
            if self.clock > self.simulation_time:
                break

sim = Simulation(simulation_time=10000)
sim.run()


timeinsystem = 0
for piece in sim.exits:
    timeinsystem += (piece.exit_supervisor_time - piece.arrival_time)
    print(piece)
print(timeinsystem/len(sim.exits))

