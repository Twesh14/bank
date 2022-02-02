# Bank Management System by Tarun
### mySQL Commands


create table account(Name varchar(20),Password varchar(20),Account_NO int,upi varchar(20),Balance int,upi_pin int);

create table transactions(TranNo int,Sender varchar(20),Reciever varchar(20),S_Close int,R_Close int,Amount varchar(20),Type varchar(10));

create table pending(No int,Requested varchar(20),Requester varchar(20),Amount int,status varchar(10));
