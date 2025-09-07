from datetime import date


class GlobalUtils:

     @staticmethod
     def calculate_age(birthday: date):
          """
          A function to calculate user age by specifying the user birthday.
          :param birthday: That is given by the user.
          :return: Age of the user.
          """
          # get today's date
          today_date = date.today()
          # and day,month and year to variables
          t_day, t_month, t_year = today_date.day, today_date.month, today_date.year

          # assign day, month and year of user to variable
          user_b_day, user_b_month, user_b_year = birthday.day, birthday.month, birthday.year

          # calculate age
          age = t_year - user_b_year

          # check if today's month is less than to its birth month
          if t_month < user_b_month:
               age -= 1

          # otherwise check today's month if equal to user's birthmonth
          elif t_month == user_b_month:
               # then check if today's day is less than to its birthday
               if t_day < user_b_day:
                    # then subtract 1 to its age
                    age -= 1

          # handle zero and negative value
          if age <= 0:
               age = 1
          # then return age
          return age
