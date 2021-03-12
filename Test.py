from __future__ import print_function
import numpy as np
import weio
import sys
import os

# BadSignals=['PtfmRoll_[deg]', 'PtfmYaw_[deg]', 'HydroMzi_[N-m]']
BadSignals=[]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def compare_df(df_ref,df_cur,precision=1.e-3,filename='', smallOK=False):

    SensorFailed=[]
    SensorSkipped=[]
    nOK=0

    if len(df_ref)!=len(df_cur):
        raise Exception('Different number of time steps. Current: {:d}, Reference:{:d}'.format(len(df_cur),len(df_ref)))

    for c in df_ref.columns.values:
        if c not in df_cur.columns.values:
            print('[WARN] Sensor missing in current version:',c)
        else:
            x0=df_ref[c].values
            x1=df_cur[c].values
            ma_ref=np.mean(np.abs(x0))
            min_val =np.min(x0)
            # We don't want to cross zero
            #x0=x0+min_val
            #x1=x1+min_val


            if ma_ref<1e-5:
                # Performing an aboslute test for such low signals
                ma_cur = np.mean(np.abs(x1))

                absdiff_mean = np.mean(np.abs(x0-x1))
                absdiff_max  = np.max(np.abs(x0-x1))
                fail = absdiff_mean>precision
                if fail:
                    print('{:15s} : abs mean {:.3e}, abs max {:.3e}'.format(c,absdiff_mean,absdiff_max))
            else:
                precision_loc=precision
                reldiff_mean = np.mean(np.abs(x0-x1)/ma_ref)
                reldiff_max  = np.max( np.abs(x0-x1)/ma_ref)
                fail = reldiff_mean>precision_loc
                if fail:
                    print('{:15s} : rel mean {:.3f}%, rel max {:.3f}%'.format(c,reldiff_mean*100,reldiff_max*100))
            if fail: 
                if c in BadSignals:
                    SensorSkipped.append(c)
                else:
                    SensorFailed.append(c)

            else:
                nOK+=1
            
    if len(SensorFailed)==0:
        # Font: Dot Matrix
        printOK(small=smallOK)
        print(bcolors.OKGREEN +"""{}""".format(filename)+bcolors.ENDC)
        print('[ OK ] {}/{} sensors passed - {}'.format(nOK,len(df_ref.columns.values),filename))
    else:
        printFAIL(small=smallOK)
        print(bcolors.FAIL+"""{}""".format(filename)+bcolors.ENDC)
        print('[FAIL] {}/{} sensors passed - {}'.format(nOK,len(df_ref.columns.values),filename))
    if len(SensorSkipped)>0:
        print('[WARN] {}/{} sensors skipped'.format(len(SensorSkipped),len(df_ref.columns.values)))

    return len(SensorFailed)==0


def printOK(small=False):
    if small:
        print(bcolors.OKGREEN +"""           OK           """+bcolors.ENDC)
    else:
        print(bcolors.OKGREEN +"""
                    _  _  _  _         _           _                               
                  _(_)(_)(_)(_)_      (_)       _ (_)                              
                 (_)          (_)     (_)    _ (_)                                 
                 (_)          (_)     (_) _ (_)                                    
                 (_)          (_)     (_)(_) _                                     
                 (_)          (_)     (_)   (_) _                                  
                 (_)_  _  _  _(_)     (_)      (_) _                               
                   (_)(_)(_)(_)       (_)         (_)                              
    """+bcolors.ENDC)

def printFAIL(small=False):
    print(bcolors.FAIL+"""
                                                                                    
   (_)(_)(_)(_)(_)           _(_)_              (_)(_)(_)         (_)            
   (_)                     _(_) (_)_               (_)            (_)            
   (_) _  _              _(_)     (_)_             (_)            (_)            
   (_)(_)(_)            (_) _  _  _ (_)            (_)            (_)            
   (_)                  (_)(_)(_)(_)(_)            (_)            (_)            
   (_)                  (_)         (_)          _ (_) _          (_) _  _  _  _ 
   (_)                  (_)         (_)         (_)(_)(_)         (_)(_)(_)(_)(_)
   """+bcolors.ENDC)        


def doCompare(file_ref, file_cur, precision, smallOK=False):
    filebase=os.path.splitext(os.path.basename(file_cur))[0]

    print('Comparing: ',file_cur)
    print('  against: ',file_ref)

    df_ref = weio.read(file_ref).toDataFrame()
    try:
        df_cur = weio.read(file_cur).toDataFrame()
    except:
        print('>>> File not found:', df_cur)
        printFAIL()
        return False

    return compare_df(df_ref,df_cur,precision,filebase, smallOK=smallOK)


# def log_OK(file_ref):
#     with open('STATUS','a') as f:
#         f.write('OK{}\n')

if __name__=='__main__':

    if len(sys.argv)>=1:
        if sys.argv[1]=='SUMMARY':
            print('>>> TODO')

    if len(sys.argv)<=2:
        print('')
        print('usage:   file_ref file_new [precision]')
        print('')
        raise Exception('This script requires two files')

    file_ref=sys.argv[1]
    file_cur=sys.argv[2]

    if len(sys.argv)==4:
        precision=sys.argv[3]
    else:
        precision=1.e-3

    if not os.path.exists(file_ref):
        f_ref, ext =os.path.splitext(file_ref)
        f_cur, ext =os.path.splitext(file_cur)
        OK = True

        if os.path.exists(f_cur+'.WT1_ref'+ext):
            # try to see if that's a multiple rotor case
            for i in np.arange(10):
                file_cur=f_cur+'.WT{}'.format(i+1)    +ext
                file_ref=f_cur+'.WT{}_ref'.format(i+1)+ext
                if os.path.exists(file_ref):
                    OK2 = doCompare(file_ref, file_cur, precision, smallOK=True)
                    OK = OK and OK2
        elif os.path.exists(f_cur+'.1_ref'+ext):
            # try to see if that's a combined case
            for i in np.arange(10):
                file_cur=f_cur+'.{}'.format(i+1)    +ext
                file_ref=f_cur+'.{}_ref'.format(i+1)+ext
                if os.path.exists(file_ref):
                    OK2 = doCompare(file_ref, file_cur, precision, smallOK=True)
                OK = OK and OK2

        else:
            raise Exception('Ref file not found: {}'.format(file_ref))
        if OK:
            printOK()
            print(f_cur)
        else:
            printFAIL()
            print(f_cur)

    else:
        OK = doCompare(file_ref, file_cur, precision)

    if OK:

        sys.exit(0)
    else :
        sys.exit(1)
