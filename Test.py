from __future__ import print_function
import numpy as np
import weio
import sys

# BadSignals=['PtfmRoll_[deg]', 'PtfmYaw_[deg]', 'HydroMzi_[N-m]']
BadSignals=[]


def compare_df(df_ref,df_cur,precision=1.e-3):

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
        print('[ OK ] {}/{} sensors passed'.format(nOK,len(df_ref.columns.values)))
    else:
        print('[FAIL] {}/{} sensors passed'.format(nOK,len(df_ref.columns.values)))
    if len(SensorSkipped)>0:
        print('[WARN] {}/{} sensors skipped'.format(len(SensorSkipped),len(df_ref.columns.values)))

    return len(SensorFailed)==0


if __name__=='__main__':
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
        precision=1.e-5

    print('Comparing: ',file_cur)
    print('  against: ',file_ref)

    df_ref = weio.read(file_ref).toDataFrame()
    df_cur = weio.read(file_cur).toDataFrame()


    OK =compare_df(df_ref,df_cur,precision)
    if OK:
        sys.exit(0)
    else :
        sys.exit(1)
