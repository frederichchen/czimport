alter table SCCZ.T_BDGMAIN modify TEXT10 VARCHAR2(1024);
alter table SCCZ.T_BDGSUB modify TEXT10 VARCHAR2(1024);
alter table SCCZ.T_PAYAPP modify TEXT10 VARCHAR2(1024);
alter table SCCZ.T_PAYVCH modify TEXT9 VARCHAR2(1024);
alter table SCCZ.T_PAYVCH modify TEXT10 VARCHAR2(1024);
alter table SCCZ.T_PLANMAIN modify TEXT10 VARCHAR2(1024);
alter table SCCZ.T_CARDINFO modify PAYMENTBANKACCTNAME VARCHAR2(512);
alter table SCCZ.T_CARDINFO modify PAYMENTBANKNAME VARCHAR2(512);
exit;