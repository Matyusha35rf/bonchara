from schedule.schedule import get_schedule_by_name
from pprint import pprint
def update_subjects(group_name, week):
      subjects = []
      for week in range(0, 17):
          schedule = get_schedule_by_name("abs",group_name, week)
          for i in schedule:
              for j in schedule[i]:
                  subjects.append(j)


if __name__ == "__main__":
    update_subjects("ИСТ-341", 1)
