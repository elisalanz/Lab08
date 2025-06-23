import copy

from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = []
        self._hoursBest = 0
        self._totCustomersBest = 0
        self._listNerc = []
        self._listEvents = []
        self.loadNerc()

        self.rec_level = 0

    def worstCase(self, nerc_value, maxY, maxH):
        self._solBest = []
        self._hoursBest = 0
        self._totCustomersBest = 0
        self._listEvents = []
        nerc = self.search_nerc(nerc_value)
        self.loadEvents(nerc)
        self.ricorsione([], maxY, maxH, self._listEvents)
        return self._solBest, self._hoursBest, self._totCustomersBest

    def search_nerc(self, nerc_value):
        for nerc in self._listNerc:
            if nerc.value == nerc_value:
                return nerc

    def constraint_satisfied(self, parziale, event,  maxY, maxH):
        const_1 = (self.tot_hours(parziale) + event.duration() <= maxH)
        const_2 = self.years_ok(parziale, event, maxY)
        return const_1 and const_2


    def ricorsione(self, parziale, maxY, maxH, remaining_events):
        self.rec_level+=1
        print(f"Rec level: {self.rec_level}")
        print(f"Parziale: {[single_parziale.id for single_parziale in parziale]}")
        print(f"Remaining_events: {[single_parziale.id for single_parziale in remaining_events]}")
        if len(remaining_events) == 0: # condizione finale
            return
        for event in remaining_events:
            print(f"Event ID: {event.id} - Dur: {event.duration()}")
            if self.constraint_satisfied(parziale, event, maxY, maxH):
                print(f"Selected event: {event.id} - Dur: {event.duration()}")
                parziale.append(event)
                tot_people_affected = self.tot_customers(parziale)
                if tot_people_affected > self._totCustomersBest:
                    # trova una soluzione migliore e aggiorna i dati
                    self._totCustomersBest = tot_people_affected
                    self._hoursBest = self.tot_hours(parziale)
                    self._solBest = copy.deepcopy(parziale)
                remaining_events.remove(event)
                self.ricorsione(parziale, maxY, maxH, remaining_events)
                parziale.pop() # backtracking
                print(f"Parziale: {[single_parziale.id for single_parziale in parziale]}")
        self.rec_level-=1
        print((f"Rec level: {self.rec_level}"))



    def tot_customers(self, parziale):
        tot_people_affected = 0
        for event in parziale:
            tot_people_affected += event.customers_affected
        return tot_people_affected


    def tot_hours(self, parziale):
        tot = 0
        if len(parziale) > 0:
            for event in parziale:
                tot += event.duration()
        return tot

    def years_ok(self, parziale, new_event, maxY):
        parziale_copied = copy.deepcopy(parziale)
        parziale_copied.append(new_event)
        max_year = 0
        min_year = 1000000
        if len(parziale_copied) <= 1:
            return True
        for event in parziale_copied:
            if event.date_event_began.year < min_year:
                min_year = event.date_event_began.year
            if event.date_event_finished.year > max_year:
                max_year = event.date_event_finished.year
        if (max_year - min_year) <= maxY:
            return True
        return False


    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()


    @property
    def listNerc(self):
        return self._listNerc
