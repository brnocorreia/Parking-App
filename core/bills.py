from datetime import datetime


class Bills():

    def calculate_total(self, entrance_time: datetime, exit_time: datetime) -> float:
        time_parked = (entrance_time - exit_time).total_seconds() / 60
        total_bill = time_parked * 0.2 * -1
            
        return total_bill

bills = Bills()
