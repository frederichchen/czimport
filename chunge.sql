--insert SCCZ.T_BCTYPE
SELECT BCTYPEID
  ,CODE
  ,NAME
FROM T_BCTYPE;

--insert SCCZ.T_BDGMAIN
SELECT FROMCTRLID
  ,TOCTRLID
  ,FUNDTYPE
  ,BDGAGENCY
  ,EXPFUNC
  ,BDGVERSION
  ,BDGALLOW
  ,BDGLEVEL
  ,AMT
  ,REMARK
  ,CREATETIME
  ,TEXT2
  ,TEXT10
  ,BILLID
  ,BILLCODE
FROM T_BDGMAIN;

--insert SCCZ.T_BDGSUB
SELECT FROMCTRLID
  ,TOCTRLID
  ,FUNDTYPE
  ,BDGAGENCY
  ,EXPFUNC
  ,BDGVERSION
  ,BDGALLOW
  ,BDGLEVEL
  ,AMT
  ,REMARK
  ,CREATETIME
  ,TEXT2
  ,TEXT3
  ,TEXT10
  ,BILLID
  ,BILLCODE
  ,MAINID
FROM T_BDGSUB;

--insert SCCZ.T_CARDINFO
SELECT CARDNO
  ,BDGAGENCY
  ,OPENBANK
  ,PAYMENTBANKACCOUNT
  ,PAYMENTBANKACCTNAME
  ,PAYMENTBANKACCTCODE
  ,PAYMENTBANKNAME
  ,CARDOWNER
FROM T_CARDINFO;

--insert SCCZ.T_CONSUMEDETAIL
SELECT BILLNO
  ,CARDNO
  ,CONSUMEDATE
  ,CONSUMEAMT
  ,CONSUMESPOT
  ,CONSUMETYPE
  ,CURRENCYTYPE
FROM T_CONSUMEDETAIL;

--insert SCCZ.T_DICENUMITEM
SELECT ITEMID
  ,ELEMENTCODE
  ,CODE
  ,NAME
  ,WHOLENAME
FROM T_DICENUMITEM;

--insert SCCZ.T_FMCURRENCY
SELECT CYID
  ,CYCODE
  ,CYNAME
FROM T_FMCURRENCY;

--insert SCCZ.T_PAYAPP
SELECT BILLID
  ,BILLCODE
  ,FROMCTRLID
  ,TOCTRLID
  ,BDGAGENCY
  ,EXPFUNC
  ,BDGALLOW
  ,BDGLEVEL
  ,AMT
  ,DIGEST
  ,TEXT2
  ,TEXT3
  ,TEXT10
  ,PAYVCHID
  ,BCTYPEID
FROM T_PAYAPP;

--insert SCCZ.T_PAYVCH
SELECT BILLID
  ,BILLCODE
  ,CREATETIME
  ,VCHTYPEID
  ,FUNDTYPE
  ,BDGAGENCY
  ,DEPARTMENTDIVISION
  ,EXPFUNC
  ,EXPECONORMIC
  ,BDGVERSION
  ,PAYTYPE
  ,BCTYPEID
  ,BDGALLOW
  ,GATHERINGBANKACCOUNT
  ,GATHERINGBANKACCTNAME
  ,GATHERINGBANKACCTCODE
  ,GATHERINGBANKNAME
  ,PAYMENTBANKACCOUNT
  ,BDGLEVEL
  ,AMT
  ,DIGEST
  ,TEXT2
  ,TEXT3
  ,TEXT9
  ,TEXT10
  ,PROGRAM
  ,FROMCTRLID
  ,TOCTRLID
  ,PAYMENTBANKACCTNAME
  ,PAYMENTBANKACCTCODE
  ,PAYMENTBANKNAME
  ,CLEARBANKACCOUNT
  ,CLEARBANKACCTNAME
  ,CLEARBANKACCTCODE
  ,CLEARBANK
  ,CLEARBANKNAME
  ,GATHERINGBANKPROVINCE
  ,GATHERINGBANKCITY
  ,PAYMENTBANKPROVINCE
  ,PAYMENTBANKCITY
  ,PAYCLEARID
  ,FROMVCHID
  ,SETTLEMODE
  ,WFSTATUS
  ,ELEMENT02
  ,ELEMENT04
  ,ELEMENT11
  ,ELEMENT12
  ,INCOMEEXPMANAGE
FROM T_PAYVCH;

--insert SCCZ.T_PLANFROM
SELECT BILLID
  ,MAINID
  ,FROMCTRLID
  ,TOCTRLID
  ,AMT
FROM T_PLANFROM;

--insert SCCZ.T_PLANMAIN
 SELECT FROMCTRLID
  ,TOCTRLID
  ,BILLID
  ,BILLCODE
  ,AMT
  ,REMARK
  ,TEXT2
  ,TEXT3
  ,TEXT10
FROM T_PLANMAIN;

--insert SCCZ.T_PUBAGENCY
SELECT ITEMID
  ,CODE
  ,NAME
  ,WHOLENAME
FROM T_PUBAGENCY;

--insert SCCZ.T_PUBFUNC
SELECT ITEMID
  ,CODE
  ,NAME
  ,WHOLENAME
FROM T_PUBFUNC;

--insert SCCZ.T_PUBFUNDTYPE
SELECT ITEMID
  ,CODE
  ,NAME
  ,WHOLENAME
FROM T_PUBFUNDTYPE;

--insert SCCZ.T_PUBPAYTYPE
SELECT ITEMID
  ,CODE
  ,NAME
FROM T_PUBPAYTYPE;

--insert SCCZ.T_GLBDGCTRL
select CTRLID
,CURBAL
,ENDBAL
,FUNDTYPE
,BDGAGENCY
,EXPFUNC
,BDGVERSION
,BDGALLOW
,BDGLEVEL
,ORIGINALBAL
,STATUS
FROM T_GLBDGCTRL;

--insert SCCZ.T_PAVOUCHERTYPE
select VCHTYPEID, VCHCODE, NAME
from T_PAVOUCHERTYPE;

--insert SCCZ.T_PUBEXPECONORMIC
select ITEMID, CODE, NAME
from T_PUBEXPECONORMIC;

--insert SCCZ.T_PUBPROGRAM
select ITEMID, CODE, NAME
from T_PUBPROGRAM;

--insert SCCZ.T_WFSTATUS
select STATUS, NAME
from T_WFSTATUS;

--insert SCCZ.T_PUBINDSOURCE
select ITEMID, CODE, NAME
from T_PUBINDSOURCE;

--insert SCCZ.T_PUBINCOMEEXPMANAGE
select ITEMID, CODE, NAME
from T_PUBINCOMEEXPMANAGE;
