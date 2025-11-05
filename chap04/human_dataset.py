# 중복된 피처명을 처리하는 함수, 계속 사용할꺼니까 / 중복된 컬럼명의 컬럼명 재지정 컬럼명_1, 컬럼명_2
import pandas as pd
import numpy as np

def get_new_feature_name_df(old_feature_name_df): 
    #old_feature_name_df <= feature_name_df
    feature_dup_df = pd.DataFrame(
        data=old_feature_name_df.groupby('column_name').cumcount(),
        columns = ['dup_cnt']
    )
    # feature_dup_df reset_index : 인덱스를 컬럼으로 뺀 것이다. => merge
    feature_dup_df = feature_dup_df.reset_index() # index col
    new_feature_name_df = pd.merge(
        old_feature_name_df.reset_index(),
        feature_dup_df,
        how='outer' # 여기까지하면 merge됨   
    )
    # 중복 컬럼의 새로운 컬럼명 부여한 데이터 프레임 추출
    new_feature_name_df['column_name'] = \
        new_feature_name_df[['column_name','dup_cnt']].apply(lambda x: x[0] +'_'+str(x[1]) if x[1]>0 else x[0], axis=1)
    
    return new_feature_name_df
    
    # index 컬럼을 삭제
    # new_feature_name_df = new_feature_name_df.drop(['index'],axis=1)
    
# 데이터 로딩
# 이책 특징: 함수처리가 많다,,,쉽지 않다...어렵다 그래도 도움되니까 봐용
def get_human_dataset(): #return X_train,X_test,y_train,y_test
    feature_name_df = pd.read_csv( # 변수명에 진한표시되있는거 ->사용함,회색->사용X
        './human_activity/features.txt'
        , sep = '\s+'
        ,header = None
        ,names= ['column_index','column_name']
    )
    # 중복된 피쳐명을 수정하는 함수, 신규피처명 
    new_feature_name_df = get_new_feature_name_df(feature_name_df)
    # 데이터프레임에서 피처명 추출
    # .tolist(): ndarray 로 나온걸 list 로 변환
    feature_name = new_feature_name_df.iloc[:,1].values.tolist()
    # 학습데이터, 데스트 데이터 => 데이터프레임으로 생성
    X_train = pd.read_csv('./human_activity/train/X_train.txt',sep='\s+',names = feature_name)
    X_test = pd.read_csv('./human_activity/test/X_test.txt',sep='\s+',names = feature_name)
    # 레이블 처리
    y_train = pd.read_csv('./human_activity/train/y_train.txt',sep='\s+',header=None,names=['action'])
    y_test = pd.read_csv('./human_activity/test/y_test.txt',sep='\s+',header=None,names=['action'])
    
    return X_train, X_test, y_train, y_test
    