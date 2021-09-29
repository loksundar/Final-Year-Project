class scibot:
    def __init__(self):
        pass
    def analyze(filen,target,measure):
        strout = ""
        import numpy as np
        import pandas as pd
        from sklearn.preprocessing import LabelEncoder
        from scipy import stats
        from mlxtend.preprocessing import minmax_scaling
        import pyttsx3
        from pycaret.classification import setup
        from pycaret.classification import compare_models
        engine = pyttsx3.init()
        newVoiceRate = 150
        engine.setProperty('rate',newVoiceRate)
        vid = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
        engine.setProperty('voice', vid)
        df=pd.read_csv(filen)
        target = str(target)
        dtypedf = pd.DataFrame()
        dtypedf['Feature'] = df.dtypes.index
        dtypedf['dtype'] = [str(x) for x in df.dtypes]
        numdf = df.loc[:,df.dtypes!=np.object]
        catdf = df.loc[:,df.dtypes==np.object]
        cat = 0
        if df[target].dtypes==np.object:
            cat=1
        strn="There are "+str(df.shape[0])+" rows and "+str(df.shape[1])+"columns in the Data. "
        strn=strn + " There are xy Numerical features in dataframe. "
        strn = strn.replace("xy",str(len(numdf.columns)))
        engine.say(strn)
        strout = strout +strn
        strn="There are xy Categorical features in dataframe. "
        strn = strn.replace("xy",str(len(catdf.columns)))
        engine.say(strn)
        strout = strout +strn
        if(df.isnull().sum().sum()>0):
            strn = "There are "+str(df.isnull().sum().sum())+" Missing values in the data. Which will be Replaced by Mean Mode Imputaion Method."
            engine.say(strn)
            strout = strout +strn
        else:
            strn = "There are no Missing values in data"
            engine.say(strn)
            strout = strout +strn
        for i in numdf.columns:
            df[i].fillna(df[i].mean(skipna=True),inplace=True)
        for i in catdf.columns:
            df[i].fillna(df[i].mode()[0],inplace=True)
        for i in catdf.columns:
            le = LabelEncoder()
            le.fit(df[i])
            df[i]= pd.Series(le.transform(df[i]))
        for i in numdf.columns:
            df[i]=minmax_scaling(df[i], columns = [0])
        x = pd.DataFrame(setup(data = df, target = target, session_id=123,silent=True))
        j=0
        for i in range(len(x[0])):
            try:
                if(x[0][i][0][0]=="Setup Config"):
                    j=i
            except:
                pass
        setting_up = pd.DataFrame(setup(data = df, target = target, session_id=123,silent=True))[0][j][0][1]
        strn = "There is a imbalance in the data. to fix this we are using "+str(setting_up.set_index("Description").loc['Fix Imbalance Method'][0])+" method."
        engine.say(strn)
        strout = strout +strn
        strn="The Data-Scibot is running data on all the Models So Please wait for 2 minutes"
        engine.say(strn)
        strout = strout +strn
        engine.runAndWait()
        a = compare_models(exclude = [], sort = str(measure),n_select=3)
        model1 = a[0]
        model2 = a[1]
        model3 = a[2]
        strn = "The Top 3 models which performes best on the data are:  ."+str(model1).split()[0].split("(")[0]+".  "+str(model2).split()[0].split("(")[0]+".  "+str(model3).split()[0].split("(")[0]
        engine.say(strn)
        engine.runAndWait()
        strout = strout +strn
        print(strout)
        print(cat)
        if cat==1:
            from sklearn.ensemble import VotingClassifier
            model = VotingClassifier(estimators=[('1', model1), ('2', model2),('3', model3)], voting='hard')
        else:
            from sklearn.ensemble import VotingRegressor
            model = VotingRegressor(estimators=[('1', model1), ('2', model2),('3', model3)])
        return [df,model]