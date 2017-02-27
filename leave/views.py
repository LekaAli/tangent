from django.shortcuts import render
from .models import Employee,Leave
from datetime import date,timedelta,datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.
def index(request):

    return render(request,'html/index.html')


def leaves(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')
        values = {'username': username, 'password': password}

        if username == "" or password == "":
            values = {'username': username, 'password': password}
            errorMsg = {'message': 'username and password are required'}
            return render(request, 'html/index.html', errorMsg)
            return render(request,'html/index.html')

        elif username != "" and password!="":
            user = authenticate(username=username, password=password) # check if user exist in the DB
            if user is not None:

                return render(request,'html/leaves.html',values)
            else:
                errorMsg = {'message': 'invalid username or password'}
                return render(request, 'html/index.html',errorMsg)

def remainingLeaves(request):

    if request.method == "GET":

        username = request.GET.get('username')
        employeeDB = Employee.objects.get(username=username)
        remainigDays = employeeDB.remainingLeaveDays
        values = {'remain':remainigDays,'username':username}
        return render(request,'html/checkRemainingLeaveDays.html',values)



def leaveRequest(request):

    if request.method == "POST":

        sDay = request.POST.get('startDay')
        sMonth = request.POST.get('startMonth')
        sYear = request.POST.get('startYear')

        eDay = request.POST.get('endDay')
        eMonth = request.POST.get('endMonth')
        eYear = request.POST.get('endYear')

        user = request.POST.get('username')

        dateInfo = {}
        dateInfo['day'] = range(1, 31)
        dateInfo['month'] = range(1, 13)
        dateInfo['year'] = range(2000, 2018)
        values = {'calender': dateInfo,'message': 'Leave start and end date not specified'}

        if ((sDay == None and sMonth == None and sYear == None) or (eDay == None and eMonth == None and eYear == None)) :

            return render(request, 'html/logLeaveRequest.html',values)

        else:
            start_date = date(int(sYear), int(sMonth), int(sDay))
            end_date = date(int(eYear), int(eMonth), int(eDay))

            weekdays = addLeave(request,start_date, end_date)

            #assign leave days to the employee
            employeeDB = Employee.objects.get(username=user)
            employeeStartDate = employeeDB.startDate


            currentLeaveRequestDate = date.today() #leave application day

            employeeDaysSinceAppointment = remainingLeave(request,employeeStartDate,currentLeaveRequestDate)

            if (int(employeeDaysSinceAppointment) > 0 and int(employeeDaysSinceAppointment) > weekdays):

                leaveDB = Leave(username=user,startDate=start_date, endDate=end_date, daysOfLeave=weekdays, status="Approved")
                leaveDB.save()

                employeeDB.remainingLeaveDays = (int(employeeDaysSinceAppointment) - int(weekdays))
                employeeDB.save()

                leaveStatus = {'status': 'Approved', 'other': employeeDaysSinceAppointment, 'week': weekdays}
                return render(request, 'html/leaveStatus.html',leaveStatus)
            else:

                leaveDB = Leave(username=user,startDate=start_date, endDate=end_date, daysOfLeave=weekdays, status="New")
                leaveDB.save()
                employeeDB.remainingLeaveDays = employeeDaysSinceAppointment
                employeeDB.save()
                leaveStatus = {'status': 'Declined','other':employeeDaysSinceAppointment,'week':weekdays}
                return render(request, 'html/leaveStatus.html', leaveStatus)
    else:
        username =  request.GET.get('username')
        dateInfo = {}
        dateInfo['day'] = range(1, 31)
        dateInfo['month'] = range(1, 13)
        dateInfo['year'] = range(2000, 2018)
        values = {'calender': dateInfo, 'message': 'Leave start and end date not specified','username':username}
        return render(request, 'html/logLeaveRequest.html',values)


def addLeave(request,start_date,end_date):

    all_days = []
    working_days = 0


    for x in range((end_date - start_date).days + 1):
        all_days.append(start_date + timedelta(days=x))

    for day in all_days:

        if day.weekday() < 5:
            working_days += 1

    return working_days

def remainingLeave(request,start_date,end_date):

    all_days = []
    working_days = 0
    remaingDays = 0
    carriedOverDays = 5

    for x in range((end_date - start_date).days + 1):
        all_days.append(start_date + timedelta(days=x))

    for day in all_days:

        if day.weekday() < 5:
            working_days += 1

    if working_days < 60 : # have less than 3 months working at the company
        remaingDays = 0
    elif working_days > 60 or working_days <= 240: # have more than 3 months working at the company
        remaingDays = 18
    elif working_days > 240: # have more than a year working at the company
        remaingDays = 18 + carriedOverDays


    return remaingDays






