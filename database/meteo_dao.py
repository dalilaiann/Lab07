from database.DB_connect import DBConnect
from model.situazione import Situazione


class MeteoDao():

    @staticmethod
    def get_all_situazioni_mese(mese):
        """ritorna tutte le situazioni del mese indicato e riferite ai primi 15 giorni dello stesso"""
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s 
                        WHERE MONTH(s.Data)=%s and DAY(s.Data)<=15
                        ORDER BY s.Data ASC"""

            cursor.execute(query, (mese,))
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_umidita_media(mese):
        """Ritorna la località e l'umidità media del mese indicato"""
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ SELECT s.Localita, SUM(s.Umidita)/COUNT(s.Data) as media
                        FROM situazione s 
                        WHERE MONTH(s.Data)=%s
                        group by s.Localita"""

            cursor.execute(query, (mese,))
            for row in cursor:
                result.append(f"{row["Localita"]}: {row["media"]}")

            cursor.close()
            cnx.close()
        return result


if __name__ == '__main__':
    print(MeteoDao.get_all_situazioni_mese(2))




