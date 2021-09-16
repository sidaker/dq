class Pants:

    def __init__(self, p_color, p_waist_size, p_length, p_price):
        self.color = p_color
        self.waist_size  = p_waist_size
        self.length = p_length
        self.price = p_price

    def discount(self, disc):
      return self.price * (1 - disc)

    def change_price(self, new_price):
      self.price = new_price


class SalesPerson():
    def __init__(self,fname,lname,eid,sal):
        self.first_name = fname
        self.last_name  = lname
        self.employee_id = eid
        self.salary = sal
        self.pants_sold = []
        self.total_sales = 0

    def sell_pants(self,pants):
        self.pants_sold.append(pants)

    def display_sales(self):
        for pt in self.pants_sold:
            print(f'color: {pt.color}, waist_size: {pt.waist_size}, length: {pt.length}, price: {pt.price}')


    def calculate_sales(self):
        for pt in self.pants_sold:
            self.total_sales += pt.price
        return self.total_sales

    def calculate_commission(self, comm):
        return self.total_sales * comm


def check_results():
    pants_one = Pants('red', 35, 36, 15.12)
    pants_two = Pants('blue', 40, 38, 24.12)
    pants_three = Pants('tan', 28, 30, 8.12)

    salesperson = SalesPerson('Amy', 'Gonzalez', 2581923, 40000)

    assert salesperson.first_name == 'Amy'
    assert salesperson.last_name == 'Gonzalez'
    assert salesperson.employee_id == 2581923
    assert salesperson.salary == 40000
    assert salesperson.pants_sold == []
    assert salesperson.total_sales == 0

    salesperson.sell_pants(pants_one)
    salesperson.pants_sold[0] == pants_one.color

    salesperson.sell_pants(pants_two)
    salesperson.sell_pants(pants_three)

    assert len(salesperson.pants_sold) == 3
    assert round(salesperson.calculate_sales(),2) == 47.36
    assert round(salesperson.calculate_commission(.1),2) == 4.74

    print('Great job, you made it to the end of the code checks!')

check_results()

pants_one = Pants('red', 35, 36, 15.12)
pants_two = Pants('blue', 40, 38, 24.12)
pants_three = Pants('tan', 28, 30, 8.12)

salesperson = SalesPerson('Amy', 'Gonzalez', 2581923, 40000)

salesperson.sell_pants(pants_one)
salesperson.sell_pants(pants_two)
salesperson.sell_pants(pants_three)

salesperson.display_sales()              
