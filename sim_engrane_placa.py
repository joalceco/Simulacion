import numpy as np

class Engrane():

    def __init__(self, id):
        self.id = id;
        self.arrival_time=0
        self.enter_queque_time=0
        self.exit_queque_time=0
        self.enter_supervisor_time=0
        self.exit_supervisor_time=0

    def __repr__(self):
        return "Engrane {} entro {:6.2f}, supervision {:6.2f}, salio {:6.2f}".format(self.id, self.arrival_time,self.enter_supervisor_time, self.exit_supervisor_time)

class Placa():

    def __init__(self, id):
        self.id = id;
        self.arrival_time=0
        self.enter_queque_time=0
        self.exit_queque_time=0
        self.enter_supervisor_time=0
        self.exit_supervisor_time=0

    def __repr__(self):
        return "Placa {} entro {:6.2f}, supervision {:6.2f}, salio {:6.2f}".format(self.id, self.arrival_time,self.enter_supervisor_time, self.exit_supervisor_time)

class Event():
    NEW_ENGRANE_ARRIVAL = 1
    NEW_PLACA_ARRIVAL = 2
    RECTIFICADO_EXIT = 3
    PRENSA_EXIT = 4
    LAVADO_EXIT_1 = 5
    LAVADO_EXIT_2 = 6
    EMPACADO_EXIT_1 = 7
    EMPACADO_EXIT_2 = 8

    def __init__(self, time, event_type, piece):
        self.time=time
        self.event_type=event_type
        self.piece = piece

    def __repr__(self):
        if self.event_type==self.NEW_ENGRANE_ARRIVAL:
            return "{:6.2f} - Entro engrane {}".format(self.time, self.piece.id)
        elif self.event_type==self.NEW_PLACA_ARRIVAL:
            return "{:6.2f} - Entro placa {}".format(self.time, self.piece.id)
        elif self.event_type==self.RECTIFICADO_EXIT:
            return "{:6.2f} - Termino rectificado de engrane {}".format(self.time, self.piece.id)
        elif self.event_type==self.PRENSA_EXIT:
            return "{:6.2f} - Termino prensa de placa {}".format(self.time, self.piece.id)
        elif self.event_type==self.LAVADO_EXIT_1:
            return "{:6.2f} - Termino lavado 1".format(self.time)
        elif self.event_type==self.LAVADO_EXIT_2:
            return "{:6.2f} - Termino lavado 2".format(self.time)
        elif self.event_type==self.EMPACADO_EXIT_1:
            return "{:6.2f} - Termino empacado 1".format(self.time)
        elif self.event_type==self.EMPACADO_EXIT_2:
            return "{:6.2f} - Termino empacado 2".format(self.time)
        else:
            return "{:6.2f} - Evento Desconocido".format(self.time)

    
        
def getTime(event):
    return event.time       

class Simulation():

    EMPTY = 0
    BUSY = 1
    FULL = 2

    def __init__(self, simulation_time=10000, debug=False):
        self.simulation_time = simulation_time
        self.clock=0
        self.events=[]
        self.queue_engrane=[]
        self.queue_placa=[]
        self.rejected_engrane=[]
        self.rejected_placa=[]
        self.exits=[]
        self.empacado_state_1 = self.EMPTY
        self.empacado_state_2 = self.EMPTY
        self.lavado_state_1 = self.EMPTY
        self.lavado_state_2 = self.EMPTY
        self.rectificado_state = self.EMPTY
        self.prensa_state = self.EMPTY
        self.debug=debug
        
        self.prepare_entries()

    def prepare_entries(self):
        time = 0
        id = 1
        while True:
            time += np.random.normal(13,2)
            engrane = Engrane(id)
            id+=1
            engrane.arrival_time = time
            self.events.append(Event(time,Event.NEW_ENGRANE_ARRIVAL, engrane))
            if time > self.simulation_time:
                self.events.pop()
                break
        time = 0
        id=1
        while True:
            time += np.random.exponential(12)
            placa = Placa(id)
            id+=1
            placa.arrival_time = time
            self.events.append(Event(time,Event.NEW_PLACA_ARRIVAL, placa))
            if time > self.simulation_time:
                self.events.pop()
                break
        self.events.sort(key=getTime)

    def next_event(self):
        event = self.events.pop(0);
        self.clock = event.time 
        return event


    def run(self):
        pieza_rectificado = ""
        pieza_prensa = ""
        pieza_lavado_1 = ""
        pieza_lavado_2 = ""
        pieza_empacado_1 = ""
        pieza_empacado_2 = ""
        iteration = 0
        while self.events:
            iteration+=1
            event = self.next_event()
            self.clock = event.time

            if self.debug:
                print()
                print("Iteración número {}".format(iteration))
                print("Reloj {}".format(self.clock))
                print("{} engranes, {} placas".format(len(self.queue_engrane),len(self.queue_placa)))
                print(">"+str(event))
                for evento in sim.events[:5]:
                    print(evento)
            
            if event.event_type == event.NEW_ENGRANE_ARRIVAL:
                event.piece.enter_queque_time = self.clock
                if len(self.queue_engrane) < 30:
                    self.queue_engrane.append(event.piece)
                else:
                    self.rejected_engrane.append(event.piece)
            elif event.event_type == event.NEW_PLACA_ARRIVAL:
                event.piece.enter_queque_time = self.clock
                if len(self.queue_placa) < 30:
                    self.queue_placa.append(event.piece)
                else:
                    self.rejected_placa.append(event.piece)
            elif event.event_type == event.RECTIFICADO_EXIT:
                self.rectificado_state = self.FULL
                event.piece.exit_rectificado_time=self.clock
                pieza_rectificado = event.piece
            elif event.event_type == event.PRENSA_EXIT:
                self.prensa_state = self.FULL
                event.piece.exit_prensa_time=self.clock
                pieza_prensa = event.piece
                # self.exits.append(event.client)
            elif event.event_type == event.LAVADO_EXIT_1:
                self.lavado_state_1 = self.FULL
                event.piece.exit_lavado_time=self.clock
                pieza_lavado_1 = event.piece
            elif event.event_type == event.LAVADO_EXIT_2:
                self.lavado_state_2 = self.FULL
                event.piece.exit_lavado_time=self.clock
                pieza_lavado_2 = event.piece
            elif event.event_type == event.EMPACADO_EXIT_1:
                self.empacado_state_1 = self.EMPTY
                event.piece.exit_empacado_time=self.clock
                self.exits.append(event.piece)
            elif event.event_type == event.EMPACADO_EXIT_2:
                self.empacado_state_2 = self.EMPTY
                event.piece.exit_empacado_time=self.clock
                self.exits.append(event.piece)

            if self.empacado_state_1 == self.EMPTY and self.lavado_state_1 == self.FULL:
                self.empacado_state_1 = self.BUSY
                self.lavado_state_1 = self.EMPTY
                next_piece = pieza_lavado_1
                if type(next_piece).__name__ == "Engrane":
                    busy_time = np.random.uniform(4.0, 6.0) + np.random.exponential(3)
                else:
                    busy_time = np.random.uniform(5.0, 9.0) + np.random.exponential(3)
                next_piece.enter_empacado_time = self.clock
                self.events.append(Event(self.clock+busy_time, Event.EMPACADO_EXIT_1, next_piece))
                self.events.sort(key=getTime)
            if self.empacado_state_1 == self.EMPTY and self.lavado_state_2 == self.FULL:
                self.empacado_state_1 = self.BUSY
                self.lavado_state_2 = self.EMPTY
                next_piece = pieza_lavado_2
                if type(next_piece).__name__ == "Engrane":
                    busy_time = np.random.uniform(4.0, 6.0) + np.random.exponential(3)
                else:
                    busy_time = np.random.uniform(5.0, 9.0) + np.random.exponential(3)
                next_piece.enter_empacado_time = self.clock
                self.events.append(Event(self.clock+busy_time, Event.EMPACADO_EXIT_1, next_piece))
                self.events.sort(key=getTime)
            if self.empacado_state_2 == self.EMPTY and self.lavado_state_1 == self.FULL:
                self.empacado_state_2 = self.BUSY
                self.lavado_state_1 = self.EMPTY
                next_piece = pieza_lavado_1
                if type(next_piece).__name__ == "Engrane":
                    busy_time = np.random.uniform(4.0, 6.0) + np.random.exponential(3)
                else:
                    busy_time = np.random.uniform(5.0, 9.0) + np.random.exponential(3)
                next_piece.enter_empacado_time = self.clock
                self.events.append(Event(self.clock+busy_time, Event.EMPACADO_EXIT_1, next_piece))
                self.events.sort(key=getTime)
            if self.empacado_state_2 == self.EMPTY and self.lavado_state_2 == self.FULL:
                self.empacado_state_2 = self.BUSY
                self.lavado_state_2 = self.EMPTY
                next_piece = pieza_lavado_2
                if type(next_piece).__name__ == "Engrane":
                    busy_time = np.random.uniform(4.0, 6.0) + np.random.exponential(3)
                else:
                    busy_time = np.random.uniform(5.0, 9.0) + np.random.exponential(3)
                next_piece.enter_empacado_time = self.clock
                self.events.append(Event(self.clock+busy_time, Event.EMPACADO_EXIT_1, next_piece))
                self.events.sort(key=getTime)
            if self.lavado_state_1 == self.EMPTY and self.rectificado_state == self.FULL:
                self.lavado_state_1 = self.BUSY
                self.rectificado_state = self.EMPTY
                next_piece = pieza_rectificado
                pieza_rectificado = ""
                busy_time = 10 + np.random.exponential(3)
                next_piece.enter_lavado_time = self.clock
                self.events.append(Event(self.clock+busy_time, Event.LAVADO_EXIT_1, next_piece))
                self.events.sort(key=getTime)
            if self.lavado_state_2 == self.EMPTY and self.rectificado_state == self.FULL:
                self.lavado_state_2 = self.BUSY
                self.rectificado_state = self.EMPTY
                next_piece = pieza_rectificado
                busy_time = 10 + np.random.exponential(3)
                next_piece.enter_lavado_time = self.clock
                self.events.append(Event(self.clock+busy_time, Event.LAVADO_EXIT_2, next_piece))
                self.events.sort(key=getTime)
            if self.lavado_state_1 == self.EMPTY and self.prensa_state == self.FULL:
                self.lavado_state_1 = self.BUSY
                self.prensa_state = self.EMPTY
                next_piece = pieza_prensa
                busy_time = 10 + np.random.exponential(3)
                next_piece.enter_lavado_time = self.clock
                self.events.append(Event(self.clock+busy_time, Event.LAVADO_EXIT_1, next_piece))
                self.events.sort(key=getTime)
            if self.lavado_state_2 == self.EMPTY and self.prensa_state == self.FULL:
                self.lavado_state_2 = self.BUSY
                self.prensa_state = self.EMPTY
                next_piece = pieza_prensa
                busy_time = 10 + np.random.exponential(3)
                next_piece.enter_lavado_time = self.clock
                self.events.append(Event(self.clock+busy_time, Event.LAVADO_EXIT_2, next_piece))
                self.events.sort(key=getTime)
            if self.rectificado_state == self.EMPTY and len(self.queue_engrane)>0:
                self.rectificado_state = self.BUSY
                next_piece = self.queue_engrane.pop(0)
                busy_time = np.random.normal(13.0,2.0) + np.random.exponential(3)
                next_piece.enter_rectificado_time = self.clock
                self.events.append(Event(self.clock+busy_time, Event.RECTIFICADO_EXIT, next_piece))
                self.events.sort(key=getTime)
            if self.prensa_state == self.EMPTY and len(self.queue_placa)>0:
                self.prensa_state = self.BUSY
                next_piece = self.queue_placa.pop(0)
                busy_time = np.random.exponential(3.0) + np.random.exponential(3)
                next_piece.enter_prensa_time = self.clock
                self.events.append(Event(self.clock+busy_time, Event.PRENSA_EXIT, next_piece))
                self.events.sort(key=getTime)

            if self.clock > self.simulation_time:
                break

sim = Simulation(simulation_time=10000, debug=False)

print("")
sim.run()
print("")

timeinsystem_engrane = 0
engranes=0
for piece in sim.exits[:10]:
    if type(piece).__name__ == "Placa":
        timeinsystem_engrane += (piece.exit_empacado_time - piece.arrival_time)
        engranes+=1
    # print(piece)
print(timeinsystem_engrane/engranes)

