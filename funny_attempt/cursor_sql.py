#-*-coding:utf-8-*-
import pyodbc
import os
def SelectInfo(hcon,hcur):
    hcur.execute('select * from PassMapT')
    ptitle=('ID','Item','Pwd','other')
    print(ptitle)
    result=hcur.fetchall()
    for item in result:
        print(item)
        print('')

def AddInfo(hcon,hcur):
    id=int(input('please input ID: '))
    item=str(input('please input Item: '))
    pwd=str(input('please input Tel 1: '))
    other=str(input('please input Other: '))
    sql="insert into PassMapT(id,item,pwd,other) values(?,?,?,?)"
    try:
        hcur.execute(sql,(id,item,pwd,other))
        hcon.commit()
    except:
        hcon.rollback()

def DeleteInfo(hcon,hcur):
    SelectInfo(hcon,hcur)
    did=int(input('please input id of delete: '))
    sql="delete from PassMapT where id=?"
    try:
        hcur.execute(sql,(did,))
        hcon.commit()
    except:
        hcon.rollback()

def UpdateInfo(hcon,hcur):
    SelectInfo(hcon,hcur)
    did=int(input('please input id of update: '))
    
    sqlitem="update PassMapT set item=? where id=?"
    item=str(input('please input Item: '))
    try:
        hcur.execute(sqlitem,(item,did))
        hcon.commit()
    except:
        hcon.rollback()
 
    sqlpwd="update PassMapT set pwd=? where id=?"
    pwd=str(input('please input Pwd: '))
    try:
        hcur.execute(sqlpwd,(pwd,did))
        hcon.commit()
    except:
        hcon.rollback()
    
    sqlother="update PassMapT set other=? where id=?"
    other=str(input('please input other: '))
    try:
        hcur.execute(sqlother,(other,did))
        hcon.commit()
    except:
        hcon.rollback()
 
def Meau():
    print('1.diaplay')
    print('2.add')
    print('3.update')
    print('4.delete')
    print('5.cls')
    print('0.exit')
    sel=9
    while(sel>5 or sel<0):
        sel=int(input('please choice: '))
        return sel

def main():
    hcon = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=127.0.0.1;DATABASE=PasswordMap;UID=sa;PWD=lptpwd')
    hcur=hcon.cursor()
    
    while(True):
        sel=Meau()
        if(sel==1):
            SelectInfo(hcon,hcur)
        elif(sel==2):
            AddInfo(hcon,hcur)
        elif(sel==3):
            UpdateInfo(hcon,hcur)
        elif(sel==4):
            DeleteInfo(hcon,hcur)
        elif(sel==5):
            os.system('cls')
        else:
            break
    hcur.close()
    hcon.close()

if __name__=='__main__':
    main()