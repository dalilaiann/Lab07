from database.meteo_dao import MeteoDao
import copy

from model.situazione import Situazione


class Model:
    def __init__(self):
        self._soluzione_ottima=[]
        self._costoTot=-1

    def get_Umidita_Media(self, mese):
        """Ritorna l'umidità media del mese passato come parametro"""
        return MeteoDao.get_umidita_media(mese)

    def calcola_sequenza(self, mese):
        """Calcola sequenza ottima per il mese indicato"""
        self._soluzione_ottima=[]
        self._costoTot=-1
        rimanenti=MeteoDao.get_all_situazioni_mese(mese)
        self._ricorsione([], rimanenti)
        return self._soluzione_ottima, self._costoTot

    def trova_candidati(self, parziale, rimanenti):
        """Restituisce solo le entry corrispondenti al giorno da determinare (pari alla lunghezza della sol parziale)"""
        candidates=[]
        for c in rimanenti:
            if c.data.day==len(parziale)+1:
                candidates.append(c)
        return candidates

    def is_admisibile(self, parziale, candidato):
        """verifica se la nuova entry genera una soluzione ammissibile"""
        counter=0
        for e in parziale:
            if e.localita==candidato.localita:
                counter+=1

        #controllo num giornate
        if counter>=6:
            return False

        #controllo giorni permanenza
        if len(parziale)==0:
            return True

        if len(parziale)<3:
            if parziale[0].localita!=candidato.localita:
                return False
            else:
                return True
        else:
            if (parziale[-1].localita!=parziale[-2].localita or
                parziale[-1].localita!=parziale[-3].localita or
                parziale[-2].localita!=parziale[-3].localita):
                if parziale[-1].localita!=candidato.localita:
                   return False
                return True
            else:
                return True

    def calcola_costo(self, parziale):
        """calcola il costo totale della sequenza"""
        costo=parziale[0].umidita+parziale[1].umidita

        for i in range(2,len(parziale)):
            costo+=parziale[i].umidita
            if parziale[i].localita!=parziale[i-1].localita:
                costo+=100
            elif parziale[i].localita!=parziale[i-2].localita:
                costo+=100

        return costo


    def _ricorsione(self, parziale, rimanenti):
        """esegue meccanismo di ricosione"""
        if len(parziale)==15:
            #controllo che sol sia ottima
            costo=self.calcola_costo(parziale)
            if self._costoTot==-1 or costo<self._costoTot:
                self._costoTot=costo
                self._soluzione_ottima=copy.deepcopy(parziale)

        else:
            candidates=self.trova_candidati(parziale, rimanenti)
            for i in range(len(candidates)):
                if self.is_admisibile(parziale, candidates[i]):
                    parziale.append(candidates[i])
                    self._ricorsione(parziale, rimanenti)
                    parziale.pop()


if __name__ == '__main__':
    istanza = Model()
    print(istanza.calcola_sequenza(2))









