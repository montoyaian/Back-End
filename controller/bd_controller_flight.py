from Classes.first_class import Firtsclass
from Classes.economic_class import Economiclass
from Classes.standart_class import Standartclass
from Classes.supplier import Supplier
import mysql.connector

DELETE_SUCCESS = {"message": "eliminacion completa"}




class DatabaseControllerFlight():
    """
    This class is used to connect to the database and execute queries
    """

    def __init__(self):
        """
        Constructor
        """
        
        self.connection = mysql.connector.connect(user='ian',password='ian1234',host='localhost',database='data_base',port='3306')
        self.cursor = self.connection.cursor()

    def insert_flight(self, flight: Firtsclass or Economiclass or Standartclass):
        self.connection = mysql.connector.connect(user='ian',password='ian1234',host='localhost',database='data_base',port='3306')
        self.cursor = self.connection.cursor()
        self.cursor.execute(
        """SELECT * FROM data_base.supplier WHERE id = %s""",
        (flight.id_agency,),
        )
        result = self.cursor.fetchone()
        if result:
            if flight.positions > 0:
                if isinstance(flight, Firtsclass):
                    self.cursor.execute(      """INSERT INTO  data_base.firts_class(
                Origin,
                Destination,
                Date,
                Positions,
                Hour,
                Id_agency,
                Premium_cost
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (
                flight.origin,
                flight.destination,
                flight.date,
                flight.positions,
                flight.hour,
                flight.id_agency,
                flight.premium_cost,
                ))
                    self.connection.commit()
                    self.connection.close()
                    flightj = {
                    "origin": flight.origin,
                    "destination": flight.destination,
                    "date": flight.date,
                    "positions": flight.positions,
                    "hour": flight.hour,
                    "id_agency": flight.id_agency,
                    "premium_cost": flight.premium_cost
                    }
                    return flightj

            
                elif isinstance(flight, Standartclass):
                    self.cursor.execute(      """INSERT INTO  data_base.standart_class(
                    Origin,
                    Destination,
                    Date,
                    Positions,
                    Hour,
                    Id_agency,
                    Standart_cost
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (
                    flight.origin,
                    flight.destination,
                    flight.date,
                    flight.positions,
                    flight.hour,
                    flight.id_agency,
                    flight.standart_cost,
                    ))
                    self.connection.commit()
                    self.connection.close()
                    flightj = {
                    "origin": flight.origin,
                    "destination": flight.destination,
                    "date": flight.date,
                    "positions": flight.positions,
                    "hour": flight.hour,
                    "id_agency": flight.id_agency,
                    "standart_cost": flight.standart_cost
                    }
                    return flightj    
            else:
                return{"error": "cantidad de puestos no aceptada"}
        else:
            return{"error":"proveedor no encontrado"}
   
    def insert_supplier(self, supplier:Supplier ):
    
        self.connection = mysql.connector.connect(user='ian',password='ian1234',host='localhost',database='data_base',port='3306')

        self.cursor = self.connection.cursor()
        self.cursor.execute("""INSERT INTO  data_base.supplier(
        Name,
        Contact,
        Description
        ) VALUES (%s,%s, %s)""",
        (
        supplier.name,
        supplier.contact,
        supplier.description,
        ))
        self.connection.commit()
        self.connection.close()
        supplierj = {
        "name": supplier.name,
        "contact": supplier.contact,
        "Description": supplier.description,
        }

        return supplierj      


     
    def edit_supplier(self,supplier:Supplier ):
    
        self.connection = mysql.connector.connect(user='ian',password='ian1234',host='localhost',database='data_base',port='3306')
        self.cursor = self.connection.cursor()
        self.cursor.execute("""SELECT * FROM data_base.supplier WHERE ID = %s""", (supplier.id,))
        result = self.cursor.fetchone()

        if not result :
            return {"error":"proveedor no encontrado"}

        self.cursor.execute("""UPDATE data_base.supplier SET 
        Name = %s,
        Contact = %s,
        Description = %s
        WHERE ID = %s""",
        (
        supplier.name,
        supplier.contact,
        supplier.description,
        supplier.id,
        ))
        self.connection.commit()
        self.connection.close()
        supplierj = {
        "id": supplier.id,
        "name": supplier.name,
        "contact": supplier.contact,
        "Description": supplier.description,
        }
        return supplierj

    def edit_flight(self, flight:Standartclass or Firtsclass):
        self.connection = mysql.connector.connect(user='ian',password='ian1234',host='localhost',database='data_base',port='3306')

        self.cursor = self.connection.cursor()
        self.cursor.execute(
        """SELECT * FROM data_base.supplier WHERE id = %s""",
        (flight.id_agency,),
        )
        result = self.cursor.fetchone()
        if result:
            if isinstance(flight, Standartclass):
                self.cursor.execute(
                """SELECT * FROM data_base.standart_class WHERE id = %s""",
                (flight.id,),
            )
                result = self.cursor.fetchone()
                if result:
                    self.cursor.execute(
                        """UPDATE data_base.standart_class SET
                        Origin=%s,
                        Destination=%s,
                        Date=strftime('%Y-%m-%d', %s),
                        Positions=%s,
                        Hour=%s,
                        Id_agency=%s,
                        Standart_cost=%s
                        WHERE id = %s""",
                        (
                            flight.origin,
                            flight.destination,
                            flight.date,
                            flight.positions,
                            flight.hour,
                            flight.id_agency,
                            flight.standart_cost,
                            flight.id,
                        ),
                    )
                    self.connection.commit()
                    self.cursor.execute(
                    """SELECT * FROM data_base.standart_class WHERE id = %s""",
                    (flight.id,),
                    )
                    updated_flight = self.cursor.fetchone()

                    updated_flight_dict = {
                        "id": updated_flight[0], 
                        "origin": updated_flight[1],
                        "destination": updated_flight[2],
                        "date": updated_flight[3],
                        "positions": updated_flight[4],
                        "hour": updated_flight[5],
                        "id_agency": updated_flight[6],
                        "standart_cost": updated_flight[7]
                    }
                    self.connection.close()
                    return updated_flight_dict
                else:
                    return{"error": "vuelo no encontrado"}
           
            elif isinstance(flight, Firtsclass):
                self.cursor.execute(
                """SELECT * FROM data_base.firts_class WHERE id = %s""",
                (flight.id,),
                )
                result = self.cursor.fetchone()
                if result:
                    self.cursor.execute(
                        """UPDATE data_base.firts_class SET
                        Origin=%s,
                        Destination=%s,
                        Date=strftime('%Y-%m-%d', %s),
                        Positions=%s,
                        Hour=%s,
                        Id_agency=%s,
                        premium_cost=%s
                        WHERE id = %s""",
                        (
                            flight.origin,
                            flight.destination,
                            flight.date,
                            flight.positions,
                            flight.hour,
                            flight.id_agency,
                            flight.premium_cost,
                            flight.id,
                        ),
                    )
                    self.connection.commit()
                    self.cursor.execute(
                    """SELECT * FROM data_base.firts_class WHERE id = %s""",
                    (flight.id,),
                    )
                    updated_flight = self.cursor.fetchone()

                    updated_flight_dict = {
                        "id": updated_flight[0],  
                        "origin": updated_flight[1],
                        "destination": updated_flight[2],
                        "date": updated_flight[3],
                        "positions": updated_flight[4],
                        "hour": updated_flight[5],
                        "id_agency": updated_flight[6],
                        "premium_cost": updated_flight[7]
                    }
                    self.connection.close()
                    return updated_flight_dict

            else:
                return{"error": "vuelo no encontrado"}
        else:
            return{"error": "proveedor no encontrado"}
                        
    def delete_flight(self, id: int, class_type: str):
        """
        Delete a flight from database
        """
        self.connection = mysql.connector.connect(user='ian',password='ian1234',host='localhost',database='data_base',port='3306')

        self.cursor = self.connection.cursor()
        class_type.lower()
        if (class_type == "firts class"):
            self.cursor.execute(
            """SELECT * FROM data_base.firts_class WHERE id = %s""",
            (id,),
            )
            result = self.cursor.fetchone()
            if result:
                self.cursor.execute("""DELETE FROM data_base.firts_class WHERE id = %s""", (id,))
                self.cursor.execute("""DELETE FROM data_base.Bookings WHERE Id_flight= %s AND Type_flight = 'firts class'""", (id,))
                self.cursor.execute("""DELETE FROM data_base.Offers WHERE Id_flight = %s""", (id,))
                self.connection.commit()
                self.connection.close()
                return DELETE_SUCCESS
            else:
                return{"error": "vuelo no encontrado"}            
        elif (class_type == "standart class"):
            self.cursor.execute(
            """SELECT * FROM data_base.firts_class WHERE id = %s""",
            (id,),
            )
            result = self.cursor.fetchone()
            if result:
                self.cursor.execute("""DELETE FROM data_base.standart_class WHERE id = %s""", (id,))
                self.cursor.execute("""DELETE FROM data_base.Bookings WHERE Id_flight= %s AND Type_flight = 'standart class'""", (id,))
                self.cursor.execute("""DELETE FROM data_base.Offers WHERE Id_flight = %s""", (id,))
                self.connection.commit()
                self.connection.close()
                return DELETE_SUCCESS
            else:
                {"error": "vuelo no encontrado"} 
        else:
            return {"error":"tipo de vuelo no encontrado"}
    
    def delete_supplier(self, id:int):
        """
        Delete a supplier from database
        """
        self.connection = mysql.connector.connect(user='ian',password='ian1234',host='localhost',database='data_base',port='3306')

        self.cursor = self.connection.cursor()
        
        self.cursor.execute(
        """SELECT * FROM data_base.supplier WHERE id = %s""",
        (id,),
        )
        result = self.cursor.fetchone()
        if result:
            self.cursor.execute("""DELETE FROM data_base.supplier  WHERE id = %s""", (id,))      
            self.cursor.execute("""DELETE FROM data_base.firts_class  WHERE ID_agency = %s""", (id,))
            self.cursor.execute("""DELETE FROM data_base.standart_class  WHERE ID_agency = %s""", (id,))
            self.connection.commit()
            self.connection.close()          
            return DELETE_SUCCESS
        else:
            return {"error":"proveedor no encontrado"}        
            
    def show_flight(self, table_name:str ):
        self.connection = mysql.connector.connect(user='ian',password='ian1234',host='localhost',database='data_base',port='3306')

        self.cursor = self.connection.cursor()
        try:
            if table_name == "all":
                self.cursor.execute('SELECT * FROM data_base.firts_class')
                rows = self.cursor.fetchall()
                self.cursor.execute('SELECT * FROM data_base.standart_class')
                rows += self.cursor.fetchall()
                self.connection.commit()
                self.connection.close()
                return rows 
            else:
                self.cursor.execute(
                    '''SELECT * FROM data_base.{}'''.format(table_name))
                rows = self.cursor.fetchall()
                self.connection.commit()
                self.connection.close()
                return rows
        except:
            return{"error":"tabla no valida"}

    def show_supplier(self):
        self.connection = mysql.connector.connect(user='ian',password='ian1234',host='localhost',database='data_base',port='3306')
        self.cursor = self.connection.cursor()
        self.cursor.execute('SELECT * FROM data_base.supplier')
        rows = self.cursor.fetchall()      
        return rows 
    
