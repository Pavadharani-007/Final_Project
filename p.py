import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector
#from sqlalchemy import create_engine
import pickle
import sklearn
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sklearn.preprocessing import LabelEncoder


#------------------------------------------------------------------------------------------------------
 #Configuring Streamlit GUI 
st.set_page_config(layout='wide')

# Title
st.title(':green[EMPLOYEE ATTRITION PREDICTION]')
#model = pickle.load(open('rfc.pkl','rb'))
with open('C:\\Users\\HP\\Desktop\\vs code\\modelrfc.pkl', 'rb') as file:
                loaded_model = pickle.load(file)

# Tabs 
tab1, tab2 = st.tabs(["ATTRITION PREDICTION", "INSIGHTS"])
#---------------------------------------------------------------------------------------------------------

with tab1:
    st.title("Employee Details Form")

# Create input widgets for each field
    age = st.text_input("Age")
    business_travel = st.selectbox("Business Travel", [1,2,3,4,5])
    
    department = st.radio("Department", ["Human Resources", "Sales", "Research & Development"])
    distance_from_home = st.text_input("Distance From Home")
    st.write("1-Below college,2-college,3-Bachelor,4-Master,5-Doctor")
    education = st.selectbox("Education", [1, 2, 3, 4, 5])
    education_field = st.selectbox("Education Field", ["Life Sciences", "Medical", "Marketing", "Technical Degree","Human Resources", "Other"])
    st.write("1-Low,2-Medium,3-High,4-Very High")
    environment_satisfaction = st.selectbox("Environment Satisfaction", [1, 2, 3, 4])
    gender = st.radio("Gender", ["Male", "Female"])
    
    st.write("1-Low,2-Medium,3-High,4-Very High")
    job_involvement = st.selectbox("Job Involvement", [1, 2, 3, 4])
    job_level = st.selectbox("Job Level", [1, 2, 3, 4, 5])
    job_role = st.selectbox("Job Role", ["Sales Executive","Manufacturing Director","Healthcare Representative","Manager","Research Director","Labortory Technician","Sales Representative", "Research Scientist","Other"])
    job_satisfaction = st.selectbox("Job Satisfaction", [1, 2, 3, 4])
    marital_status = st.radio("Marital Status", ["Single", "Married", "Divorced"])
    monthly_income = st.text_input("Monthly Income")
    PercentSalaryHike=st.text_input("PercentSalaryHike")
    num_companies_worked = st.text_input("Number of Companies Worked ")
    #overtime = st.radio("Over Time", ["Yes", "No"])
    st.write("1-Low,2-Medium,3-High,4-Very High")
    performance_rating = st.selectbox("Performance Rating", [1,2,3, 4])
    
    stock_option_level = st.selectbox("Stock Option Level", [0, 1, 2, 3])
    total_working_years = st.text_input("Total Working Years")
    training_times_last_year = st.text_input("Training Times Last Year")
    #work_life_balance = st.selectbox("Work Life Balance", [1, 2, 3, 4])
    years_at_company = st.text_input("Years At Company")
    
    years_since_last_promotion = st.text_input("Years Since Last Promotion")
    years_with_curr_manager = st.text_input("Years With Curr Manager")
    Avg_Working_time = st.text_input("Avg_Working_time")


# Add a button to submit the form
    if st.button("Submit"):
        # Perform any data processing or analysis here
        final2= {
        'Age': int(age),
        #'Attrition' :int (attrition),
        'BusinessTravel': business_travel,
        'Department': department,
        'DistanceFromHome': int(distance_from_home),
        'Education': education,
        'EducationField': education_field,
        'Gender': gender,
        'JobLevel': job_level,
        'JobRole': job_role,
        'MaritalStatus':marital_status,
        'MonthlyIncome': int(monthly_income),
        'NumCompaniesWorked': int(num_companies_worked) ,
        'PercentSalaryHike': int(PercentSalaryHike),
        'StockOptionLevel': stock_option_level,
        'TotalWorkingYears': int(total_working_years)if total_working_years else None ,
        'TrainingTimesLastYear': int(training_times_last_year),
        'YearsAtCompany': int(years_at_company),
        'YearsSinceLastPromotion':int(years_since_last_promotion)if years_since_last_promotion else None,
        'TotalSatisfaction': job_satisfaction,
        'Avg_Working_time':int (Avg_Working_time)if Avg_Working_time else None 
        }
        
        df = pd.DataFrame ([final2])

        
        label_encoder = LabelEncoder()
        categorical_columns = ['BusinessTravel', 'Department', 'EducationField', 'Gender', 'JobRole', 'MaritalStatus']
        for col in categorical_columns:
            df[col] = label_encoder.fit_transform(df[col])
        st.write(df)
#if st.button("PREDICT"):
        prediction = loaded_model.predict(df)


        if prediction == 0:
            st.write('Employee Might Not Leave The Job')

        elif prediction == 1:
            st.write('Employee Might Leave The Job')
        else:
            st.write("error")
        #st.balloons()
#--------------------------------------------------------------------------------------------------
        mydb = mysql.connector.connect(host="localhost",user="root",password="pava12345S", )
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("CREATE DATABASE IF NOT EXISTS employee_details")
        mycursor.execute("USE employee_details")
        mycursor.execute("CREATE TABLE IF NOT EXISTS final(Age int,BusinessTravel int,Department int,DistanceFromHome int,Education int,EducationField int,Gender int,JobLevel int,JobRole int,MaritalStatus int,MonthlyIncome int,NumCompaniesWorked int,PercentSalaryHike int,StockOptionLevel int,TotalWorkingYears int,TrainingTimesLastYear int,YearsAtCompany int,YearsSinceLastPromotion int,TotalSatisfaction int,Avg_Working_time int,prediction_result varchar(255));")
        sql = """INSERT INTO final(Age,  BusinessTravel, Department, DistanceFromHome, Education, EducationField, 
                        Gender, JobLevel, JobRole, MaritalStatus, MonthlyIncome, 
                        NumCompaniesWorked, PercentSalaryHike, StockOptionLevel, TotalWorkingYears, 
                        TrainingTimesLastYear, YearsAtCompany,YearsSinceLastPromotion, TotalSatisfaction, Avg_Working_time,prediction_result) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        # data = tuple(df.values[0])+(prediction[0],)
        # data_list = data.tolist()
        # mycursor.execute(sql, data)
        # mydb.commit()
        data = tuple(df.values[0]) + (prediction[0],)
        data_list = [int(item) if isinstance(item, np.int64) else item for item in data]
        mycursor.execute(sql, data_list)
        mydb.commit()
with tab2:
    
    mydb = mysql.connector.connect(host="localhost",user="root",password="pava12345S", )
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("USE employee_details")
            
    question = st.selectbox('**Select your Question**',
                    ('1. Age Distribution by prediction_result Category',
                    '2. prediction_result by Gender',
                    '3. JobLevel vs prediction_result and JobRole vs prediction_result',
                    '4. Marital Status vs prediction_result',
                    '5. BusinessTravel and prediction_result',
                    "6. MonthlyIncome vs prediction_result",
                    "7. EducationField vs prediction_result",
                    "8. PercentSalaryHike and prediction_result",
                    "9. TotalSatisfaction vs prediction_result",
                    "10.Observations")
                    , key = 'collection_question')
    if question == '1. Age Distribution by prediction_result Category':
        mycursor.execute("SELECT prediction_result, Age, COUNT(*) as NumberOfEmployees FROM final GROUP BY prediction_result, Age ORDER BY prediction_result, Age;")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['prediction_result', 'Age',"NumberOfEmployees"])
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(df1)
        with col2:
            fig = px.bar(
            df1, 
                x='Age', 
                y='NumberOfEmployees', 
                color='prediction_result', 
                labels={'NumberOfEmployees': 'Number of Employees'},
                title='Age Distribution by prediction_result Category'
            )

            st.plotly_chart(fig)

    elif question == '2. prediction_result by Gender':
        mycursor.execute("SELECT prediction_result,Gender, COUNT(*) as NumberOfEmployees FROM final GROUP BY Gender, prediction_result ORDER BY prediction_result;")
        result = mycursor.fetchall()
        df1 = pd.DataFrame(result, columns=['Gender', 'prediction_result', 'NumberOfEmployees'])
                
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(df1)

        with col2:
            fig = px.bar(
                    df1,
                    x='Gender',  # Updated 'x' parameter
                    y='NumberOfEmployees', 
                    color='prediction_result',  # Updated 'color' parameter
                    labels={'NumberOfEmployees': 'Number of Employees'},
                    title='Gender by prediction_result'
                )
            st.plotly_chart(fig) 


    elif question== '3. JobLevel vs prediction_result and JobRole vs prediction_result':
               mycursor.execute("SELECT JobLevel, prediction_result, COUNT(*) as NumberOfEmployees FROM final GROUP BY JobLevel, prediction_result ORDER BY JobLevel, prediction_result;")
               result_job_level = mycursor.fetchall()
               df_job_level = pd.DataFrame(result_job_level, columns=['JobLevel', 'prediction_result', 'NumberOfEmployees']).reset_index(drop=True)

               mycursor.execute("SELECT JobRole, prediction_result, COUNT(*) as NumberOfEmployees FROM final GROUP BY JobRole, prediction_result ORDER BY JobRole, prediction_result;")
               result_job_role = mycursor.fetchall()
               df_job_role = pd.DataFrame(result_job_role, columns=['JobRole', 'prediction_result', 'NumberOfEmployees']).reset_index(drop=True)

            # Display the results in two columns
               col1, col2 = st.columns(2)

            #Column 1: JobLevel vs. Attrition with Line Chart
               with col1:
                st.header('JobLevel vs. prediction_result')
                st.dataframe(df_job_level)
                fig_job_level = px.line(
                    df_job_level, 
                    x='JobLevel', 
                    y='NumberOfEmployees', 
                    color='prediction_result', 
                    labels={'NumberOfEmployees': 'Number of Employees'},
                    title='prediction_result by JobLevel'
                )
                st.plotly_chart(fig_job_level)

         # Column 2: JobRole vs. Attrition with Pie Chart
               with col2:
                 st.header('JobRole vs. prediction_result')
                 st.dataframe(df_job_role)
                 colors = ['lightcoral', 'lightskyblue']
                 fig_job_role = go.Figure(go.Pie(
                 labels=df_job_role['JobRole'],
                 values=df_job_role['NumberOfEmployees'],
                 hole=0.3,
                 marker=dict(colors=colors),
                 title='prediction_result by JobRole'
             ))
               st.plotly_chart(fig_job_role)
            
    elif question=="4. Marital Status vs prediction_result":
             mycursor.execute("SELECT MaritalStatus, COUNT(*) as NumberOfEmployees FROM final GROUP BY MaritalStatus;")
             result_marital_status = mycursor.fetchall()
             df_marital_status = pd.DataFrame(result_marital_status, columns=['MaritalStatus', 'NumberOfEmployees']).reset_index(drop=True)
             col1,col2=st.columns(2)
             with col1:
              st.write(df_marital_status)
             with col2:
         # Display a Donut Chart for MaritalStatus
              fig_marital_status_donut = px.pie(
                 df_marital_status,
                 names='MaritalStatus',
                 values='NumberOfEmployees',
                 title='Marital Status Distribution',
                 hole=0.3
             )
             st.plotly_chart(fig_marital_status_donut)
    
    elif question=='5. BusinessTravel and prediction_result':
        
            mycursor.execute("SELECT BusinessTravel, prediction_result, COUNT(*) as NumberOfEmployees FROM final GROUP BY BusinessTravel, prediction_result ORDER BY BusinessTravel, prediction_result;")
            result_business_travel = mycursor.fetchall()
            df_business_travel = pd.DataFrame(result_business_travel, columns=['BusinessTravel', 'prediction_result', 'NumberOfEmployees']).reset_index(drop=True)

         # Display the Stacked Bar Chart for BusinessTravel vs. Attrition
            fig_business_travel = px.bar(
             df_business_travel,
             x='BusinessTravel',
             y='NumberOfEmployees',
             color='prediction_result',
             title='Business Travel vs. prediction_result',
             labels={'NumberOfEmployees': 'Number of Employees'},
             barmode='stack'
         )
            st.plotly_chart(fig_business_travel)

    elif question=="6. MonthlyIncome vs prediction_result":
            mycursor.execute("SELECT prediction_result, MonthlyIncome FROM final;")
            result_monthly_income = mycursor.fetchall()
            df_monthly_income = pd.DataFrame(result_monthly_income, columns=['prediction_result', 'MonthlyIncome']).reset_index(drop=True)

         # Display the Scatter Plot for MonthlyIncome vs. Attrition
            fig_monthly_income_scatter = px.scatter(
             df_monthly_income,
             x='MonthlyIncome',
             color='prediction_result',
             title='Monthly Income vs.prediction_result (Scatter Plot)',
             labels={'MonthlyIncome': 'Monthly Income'}
         )
            st.plotly_chart(fig_monthly_income_scatter)

    
    elif question=="7. EducationField vs prediction_result":
            mycursor.execute("SELECT EducationField, prediction_result, COUNT(*) as NumberOfEmployees FROM final GROUP BY EducationField, prediction_result ORDER BY EducationField, prediction_result;")
            result_education_field = mycursor.fetchall()
            df_education_field = pd.DataFrame(result_education_field, columns=['EducationField', 'prediction_result', 'NumberOfEmployees']).reset_index(drop=True)

         # Display the Sunburst Chart for EducationField vs. Attrition
            fig_education_field_sunburst = px.sunburst(
             df_education_field,
             path=['EducationField', 'prediction_result'],
             values='NumberOfEmployees',
             title='Education Field vs. prediction_result (Sunburst Chart)'
         )
            st.plotly_chart(fig_education_field_sunburst)


    elif question=="8. PercentSalaryHike and prediction_result":
            mycursor.execute("SELECT PercentSalaryHike, prediction_result, COUNT(*) as NumberOfEmployees FROM final GROUP BY PercentSalaryHike, prediction_result ORDER BY PercentSalaryHike, prediction_result;")
            result_salary_hike = mycursor.fetchall()
            df1 = pd.DataFrame(result_salary_hike, columns=['PercentSalaryHike', 'prediction_result', 'NumberOfEmployees']).reset_index(drop=True)

         # Display the Line Chart for PercentSalaryHike vs. Attrition
            fig_salary_hike_line = px.line(
             df1,
             x='PercentSalaryHike',
             y='NumberOfEmployees',
             color='prediction_result',
             title='Percent Salary Hike vs. prediction_result (Line Chart)',
             labels={'PercentSalaryHike': 'Percent Salary Hike', 'NumberOfEmployees': 'Number of Employees'}
         )
            st.plotly_chart(fig_salary_hike_line)
        
    elif question=="9. TotalSatisfaction vs prediction_result":
            mycursor.execute("SELECT TotalSatisfaction, prediction_result, COUNT(*) as NumberOfEmployees FROM final GROUP BY TotalSatisfaction, prediction_result ORDER BY TotalSatisfaction, prediction_result;")
            result_satisfaction = mycursor.fetchall()
            df_satisfaction = pd.DataFrame(result_satisfaction, columns=['TotalSatisfaction', 'prediction_result', 'NumberOfEmployees']).reset_index(drop=True)

         # Display the Stacked Bar Chart for TotalSatisfaction vs. Attrition
            fig_satisfaction_bar = px.bar(
             df_satisfaction,
             x='TotalSatisfaction',
             y='NumberOfEmployees',
             color='prediction_result',
             title='Total Satisfaction vs.prediction_result',
             labels={'NumberOfEmployees': 'Number of Employees', 'TotalSatisfaction': 'Total Satisfaction'},
             barmode='stack'
         )
            st.plotly_chart(fig_satisfaction_bar)
        
    elif question=="10.Observations":
         observations = [
         "With gender, males have a higher attrition rate of 68%.",
         "In job roles, Research Directors and Research Scientists have a high attrition rate.",
         "In job level, Level 2 has the highest attrition rate.",
         "Singles have a higher attrition count compared to married and divorced individuals.",
         "Those who travel rarely on business trips have a higher attrition rate.",
         "The age group from 25 to 35 has a high attrition rate.",
         "Individuals with low income have a higher attrition rate.",
         "Those from life science and medical fields are more likely to leave the job."
     ]

#     # Display observations in Streamlit
         for observation in observations:
          st.write(f"- {observation}")
         st.header('Factors Influencing Attrition Rate:')
         st.write("To decrease the attrition rate, the following factors play a key role:")
         st.write("- Monthly Income")
         st.write("- Percent Salary Hike")
         st.write("- Total Satisfaction")

