from django.shortcuts import render,HttpResponse
import mysql.connector as my
# customerid=[104,105,106,107,108,109,110,111]
fn=""
ln="" 
passs=""
email=""
city=""
state=""
apart=""
hno=0
mob=0
pin=0
room=0
description=""
complainid=""
room_type=""
auth=""
authid=0
custid=0
roomid=0
t=()
sample=""



# Create your views here.
def index(request):
    return render(request,'Home.html')
    # return HttpResponse("Hello")

def contact(request):
    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")

def user_dashboard(request,t):
    # s=t.remove('(',')')
    # if(t)
    data={"name":t[0][0]}
    return render(request,'userpage.html',data)

def login(request):
    global custid
    if request.method=="POST":
        m=my.connect(host="localhost",user="root",passwd="Yash@2001",database="dbms_project")
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key=="email":
                email=value
            if key=="password":
                passs=value
        if("--" in email or "'" in email):
            return render(request,"error.html")        
        q1="select * from login where email='{}' and password='{}'".format(email,passs)
        q2="select firstname,custid from customer where email='{}'".format(email)
        print(q1)
        cursor.execute(q1)
        
        t=tuple(cursor.fetchall())
        if(len(t)!=0):
            cursor.execute(q2)
            t=tuple(cursor.fetchall())
            x,custid=t[0]
            return user_dashboard(request,t)
        else:
            return render(request,"error.html")               
        

    return render(request,"login.html") 


def register(request):
    print("Hello")
    global customerid
    if request.method=="POST":
        m=my.connect(host="localhost",user="root",passwd="Yash@2001",database="dbms_project")
        cursor=m.cursor()
        d=request.POST
        
        for key,value in d.items():
            if key=="firstname":
                fn=value
            if key=="lastname":
                ln=value
            if key=="email":
                email=value
            if key=="password":
                passs=value
            if key=="phoneno":
                mob=value
            if key=="houseno":
                hno=value
            if key=="apartment":
                apart=value 
            if key=="city":
                city=value
            if key=="state":
                state=value
            if key=="pincode":
                pin=value

        print(d.items())        

        q1="insert into customer(firstname,lastname,email,phoneno,Houseno,apartment,city,state,pincode) values('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(fn,ln,email,mob,hno,apart,city,state,pin)

        q2="insert into login values('{}','{}')".format(email,passs)
        

        cursor.execute(q1)
        m.commit()
        cursor.execute(q2)
        m.commit()

    return render(request,"register.html")

adminid=""
admin_pass=""
def admin(request):
    if request.method=="POST":
        m=my.connect(host="localhost",user="root",passwd="Yash@2001",database="dbms_project")
        cursor=m.cursor()
        d=request.POST        
        for key,value in d.items():
            if(key=="adminid"):
                adminid=value
            if(key=="adminpass"):
                admin_pass=value
        q="select * from admin where adminid='{}' and password='{}'".format(adminid,admin_pass)
        cursor.execute(q)
        t=tuple(cursor.fetchall())
        if(t==()):
            return render(request,"error.html")
        else:
            return admin_dash(request)        

    return render(request,"Admin_login.html")


def services(request):
    m=my.connect(host="localhost",user="root",passwd="Yash@2001",database="dbms_project")
    cursor=m.cursor()
    data={}
    q="select name,mobile,timmings from service_nonpaid"
    cursor.execute(q)
    records=tuple(cursor.fetchall())
    print(records)
    i=1
    for rec in records:
        a,b,c,=rec
        # d="More Details"
        j=str(i)
        data["name"+j]=a
        data["mob"+j]=b
        data["time"+j]=c
        # data["receipt"+j]=d
        i=i+1
    q="select name,price,availability from service_paid"
    cursor.execute(q)
    records=tuple(cursor.fetchall())
    print(records)
    i=1
    for rec in records:
        a,b,c,=rec
        # d="More Details"
        j=str(i)
        data["n"+j]=a
        data["m"+j]=b
        data["t"+j]=c
        # data["receipt"+j]=d
        i=i+1    
    return render(request,'services.html',data) 

def booking(request):
    if request.method=="POST":
        m=my.connect(host="localhost",user="root",passwd="Yash@2001",database="dbms_project")
        cursor=m.cursor()
        d=request.POST
        
        for key,value in d.items():
            if key=="firstname":
                fn=value
            if key=="lastname":
                ln=value
            if key=="email":
                email=value
            # if key=="password":
            #     passs=value
            if key=="mobile":
                mob=value
            if key=="checkin":
                hno=value
            if key=="checkout":
                apart=value 
            if key=="num_of_adult":
                city=value
            if key=="num_of_child":
                state=value
            if key=="num_of_rooms":
                pin=value
            if key=="type":
                room_type=value
            if key=="verification_type":
                auth=value
            if key=="verification_id":
                authid=value            

        print(d.items())        

        q1="insert into newbookings(first_name,last_name,mobile,num_of_adult,num_of_child,type_of_room,auth_type,auth_no,num_of_rooms,booking_from,booking_till,custid) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(fn,ln,mob,city,state,room_type,auth,authid,pin,hno,apart,custid)
        
        cursor.execute(q1)
        m.commit()
        q3="select bookingid from newbookings where auth_no='{}'".format(authid)
        cursor.execute(q3)
        t1=tuple(cursor.fetchall())
        bookid=t1[0][0]
        stat="Available"
        stat2="Booked"
        q4="select roomid from room where type='{}' and allotment_status='{}'".format(room_type,stat)
        cursor.execute(q4)
        
        t1=tuple(cursor.fetchall())
        roomid=t1[0][0]
        q5="update room set allotment_status='{}' where roomid='{}'".format(stat2,roomid)
        cursor.execute(q5)
        q2="insert into allotment(booked_from,booked_till,roomid,bookingid,custid) values('{}','{}','{}','{}','{}')".format(hno,apart,roomid,bookid,custid)      
        

        
        cursor.execute(q2)
        m.commit()     
    return render(request,"new_booking.html")

def booking_history(request):
    m=my.connect(host="localhost",user="root",passwd="Yash@2001",database="dbms_project")
    cursor=m.cursor()
    data={}
    q="select first_name,booking_from,bookingid from newbookings"
    cursor.execute(q)
    records=tuple(cursor.fetchall())
    print(records)
    i=1
    for rec in records:
        a,b,c,=rec
        d="More Details"
        j=str(i)
        data["name"+j]=a
        data["checkin"+j]=b
        data["id"+j]=c
        data["receip"+j]=d
        i=i+1

    q="select orderid,price,roomid from orders"
    cursor.execute(q)
    records=tuple(cursor.fetchall())
    print(records)
    i=1
    for rec in records:
        a,b,c,=rec
        d="More Details"
        j=str(i)
        data["order"+j]=a
        data["room"+j]=c
        data["price"+j]=b
        data["receipt"+j]=d
        i=i+1

    return render(request,"Mybookings.html",data)    
stat="Available"
def admin_dash(request):
    m=my.connect(host="localhost",user="root",passwd="Yash@2001",database="dbms_project")
    cursor=m.cursor()
    q1="select count(allotment_status) from room where allotment_status='{}'".format(stat)
    q2="select count(*) from complain"

    cursor.execute(q1)
    count=tuple(cursor.fetchall())
    c=count[0][0]
    cursor.execute(q2)
    count=tuple(cursor.fetchall())
    c2=count[0][0]
    rdata={"rooms":c,"complain":c2}
    return render(request,"admin_dash.html",rdata) 

def rooms(request):
    m=my.connect(host="localhost",user="root",passwd="Yash@2001",database="dbms_project")
    cursor=m.cursor()
    data={}
    q="select room.roomid,room.type,room.allotment_status,allotment.booked_from,allotment.booked_till,allotment.allotmentid from room left join allotment on room.roomid=allotment.roomid"
    cursor.execute(q)
    records=tuple(cursor.fetchall())
    print(records)
    i=1
    for rec in records:
        a,b,c,d,e,f=rec
        j=str(i)
        data["roomno"+j]=a
        data["type"+j]=b
        data["status"+j]=c
        data["from"+j]=d
        data["till"+j]=e
        i=i+1
    return render(request,"rooms.html",data)




title1=""
title2=""
desc1=""
desc2=""
def complain_rec(request):
    m=my.connect(host="localhost",user="root",passwd="Yash@2001",database="dbms_project")
    cursor=m.cursor()
    data={}
    q="select complain_title,description,roomno from complain"
    cursor.execute(q)
    records=tuple(cursor.fetchall())
    print(records)
    i=1
    for rec in records:
        a,b,c=rec
        d="Room No. - "+str(c)
        # d="More Details"
        j=str(i)
        data["title"+j]=a
        data["description"+j]=b
        data["room"+j]=d
        # data["receipt"+j]=d
        i=i+1

    return render(request,"Complain_rec.html",data)
titl=""
def complain_user(request):
    global title
    if request.method=="POST":
        m=my.connect(host="localhost",user="root",passwd="Yash@2001",database="dbms_project")
        cursor=m.cursor()
        d=request.POST
        print(d)        
        for key,value in d.items():
            if(key=="room"):
                room=value
            if(key=="description"):
                description=value
            if(key=="title"):
                titl=value    
        global complainid
              
        q="insert into complain(roomno,description,complain_title) values('{}','{}','{}')".format(room,description,titl)
        cursor.execute(q)
        m.commit()
        
    return render(request,"complain_send.html") 
price=0
t5=""
status="Available"
def addroom(request):
    global roomid,price,t5,status
    if request.method=="POST":
        m=my.connect(host="localhost",user="root",passwd="Yash@2001",database="dbms_project")
        cursor=m.cursor()
        d=request.POST        
        for key,value in d.items():
            if(key=="roomid"):
                roomid=int(value)
            if(key=="price"):
                price=int(value)
            if(key=="type"):
                t5=value
        q="insert into room values('{}','{}','{}','{}')".format(roomid,t5,status,price)
        cursor.execute(q)
        m.commit()             

    return render(request,"Add_room.html")

def payment(request):
    return render(request,"payment.html")

def receipt(request):
    return render(request,"receipt.html")  


roomno=0
item=""
quant=0
def order(request):
    global roomno,item
    if request.method=="POST":
        m=my.connect(host="localhost",user="root",passwd="Yash@2001",database="dbms_project")
        cursor=m.cursor()
        d=request.POST        
        for key,value in d.items():
            if(key=="roomno"):
                roomid=int(value)
            if(key=="item"):
                item=value
            if(key=="quantity"):
                quant=int(value)
                
        q="insert into orders(item,quantity,roomid) values('{}','{}','{}')".format(item,quant,roomno)
        cursor.execute(q)
        m.commit()             


    return render(request,"Getservice.html")

def last(request):
    return render(request,"lastbooking.html")

def admin_service(request):
    return render(request,"admin_service.html") 


name=""
desig=""
shift=""
contac=0
tim=""
def staff(request):
    global name,shift,desig,contac,tim
    m=my.connect(host="localhost",user="root",passwd="Yash@2001",database="dbms_project")
    cursor=m.cursor()
    data={}
    q="select * from staff"
    cursor.execute(q)
    records=tuple(cursor.fetchall())
    print(records)
    i=1
    for rec in records:
        a,b,c,d,e,f=rec
        j=str(i)
        data["id"+j]=a
        data["name"+j]=b
        data["designation"+j]=c
        data["contact"+j]=d
        data["shift"+j]=e
        data["timming"+j]=f
        i=i+1
    if request.method=="POST":
        m=my.connect(host="localhost",user="root",passwd="Yash@2001",database="dbms_project")
        cursor=m.cursor()
        d=request.POST        
        for key,value in d.items():
            if(key=="name"):
                name=value
            if(key=="desig"):
                desig=value
            if(key=="shift"):
                shift=value
            if(key=="contact"):
                contac=int(value)
            if(key=="timing"):
                tim=value    
            
        q="insert into staff(name,type,mobile,shift,Timmings) values('{}','{}','{}','{}','{}')".format(name,desig,contac,shift,tim)
        cursor.execute(q)
        m.commit()          
        

    
    return render(request,"Staff.html",data)
