from database.DB_connect import DBConnect
from model.arco import Arco
from model.order import Order


class DAO():
    @staticmethod
    def getAllStore():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []
        query = """select s.store_id as storeId
                    from stores s """

        cursor.execute(query)

        for row in cursor:
            result.append(row['storeId'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(store_id):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []
        query = """select *
                    from orders o 
                    where o.store_id = %s"""

        cursor.execute(query, (store_id,))

        for row in cursor:
            result.append(Order(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(store_id, k, idMap):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []
        query = """Select DISTINCT o1.order_id as o1, o2.order_id as o2, count(oi1.quantity+ oi2.quantity) as peso
                    from orders o1, orders o2, order_items oi1, order_items oi2 
                    where o1.store_id=  %s
                    and o1.store_id=o2.store_id 
                    and o1.order_date > o2.order_date
                    and oi1.order_id = o1.order_id
                    and oi2.order_id  = o2.order_id
                    and DATEDIFF(o1.order_Date, o2.order_date) < %s
                    group by o1.order_id, o2.order_id"""

        cursor.execute(query,(store_id,k))

        for row in cursor:
            result.append(Arco(idMap[row["o1"]], idMap[row["o2"]], row["peso"]))


        cursor.close()
        conn.close()
        return result
