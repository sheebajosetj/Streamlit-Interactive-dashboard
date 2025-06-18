import streamlit as st # For building the app interface
import plotly.express as px #For creating interactive graphs
import warnings #It suppresses all warning messages in your Python program.
warnings.filterwarnings('ignore')
import os#For interacting with the file system
import pandas as pd #For data handling and manipulation

st.set_page_config(page_title = 'Superstore!!!', page_icon = ':bar_chart:', layout = 'wide')#page_title='Superstore!!!Sets the title that appears on the browser tab (like the tab name in Chrome)
#page_icon=':bar_chart:Sets an emoji icon (📊) on the browser tab using emoji shortcodes.
#layout='wide': Makes your app use the full width of the browser window instead of the default centered layout.
st.title(' :bar_chart: Sample SuperStore EDA')#This sets the main page title displayed at the top of your app: , :bar_chart: is an emoji that renders as 📊


st.markdown('<style>div.block-container{padding-top: 3rem;}</style>',unsafe_allow_html=True)#This line injects custom CSS styling to change the spacing at the top of the app.

# Upload a file
fl = st.file_uploader(":file_folder: Upload a file", type=["csv", "txt", "xlsx", "xls"])#This line creates a file upload widget in your Streamlit app and allows the user to upload a file of specific types.
#st.file_uploader(...) - This creates a file upload box in the app where users can select and upload a file
#:file_folder: Upload a file - This is the label shown above the upload box. The emoji :file_folder: 📁 makes it look nice.
#type=["csv", "txt", "xlsx", "xls"] This limits the allowed file types to:
if fl is not None: # Checks if a file was uploaded using the upload button.
    filename = fl.name # Extracts the file name and prints it on screen.
    st.write("Uploaded file:", filename)

    # Read file based on extension
    if filename.endswith(".csv") or filename.endswith(".txt"):#Runs only if the user uploads a file 
        df = pd.read_csv(fl, encoding="ISO-8859-1")#Read the file into a dataframe 
    elif filename.endswith((".xlsx", ".xls")):#if they are not the csv or txt then 
        df = pd.read_excel(fl)# reads the files as excel file and places it into a dataframe 
else: # Runs only if the user did not upload a file 
    # Fallback to local file if nothing is uploaded
    os.chdir(r"C:\Users\sheeb\Streamlit") # if not it takes the file on the computer 
    df = pd.read_csv("Superstore.csv", encoding="ISO-8859-1")#Reads them to the dataframe 

# Parse dates
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)#This line converts the "Order Date" column in your DataFrame df into actual date objects 
#When you load data from a CSV/Excel file, date columns often come in as plain text (like "24-05-2023").
#To work with them properly (like using filters or comparing dates), you must convert them into real date format.
#The date is written in day-month-year format.
# Get min and max date
startDate = df["Order Date"].min() #Gets the earliest date from the "Order Date" column
endDate = df["Order Date"].max() #Gets the latest date from the "Order Date" column

st.write(f"Date range: {startDate.date()} to {endDate.date()}")
# st.write(...)	Displays a message on the screen inside the app.
# f"...{...}..."	An f-string → allows inserting variables into a string.
# {startDate.date()}	Extracts just the date part (like 2023-05-10) from a full datetime object (removes the time part like 00:00:00).
# {endDate.date()}	Same as above — just gives the clean end date.

col1, col2 = st.columns((2)) #This line splits the Streamlit page into 2 side-by-side columns, and stores each column layout in col1 and col2.

with col1:#with col1
    date1 = pd.to_datetime(st.date_input("Start Date", startDate)) # creates start_date picker ,Do this action

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))#creates end_date picker, Do this action

# Filter the dataframe based on selected date range
df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()#It filters the dataframe to keep only the rows where the "Order Date" is between the selected start date (date1) and end date (date2).
# copy() Makes a clean, separate copy of the filtered data (to avoid warning/errors later if you modify it)

st.sidebar.header("Choose your filter: ")#It adds a bold heading called “Choose your filter:” to the left sidebar of your Streamlit app.
# Create for Region
region = st.sidebar.multiselect("Pick your Region", df["Region"].unique()) #It shows a multi-select dropdown in the left sidebar, where the user can choose one or more regions from the list in the data.

# st.sidebar	Put this widget in the sidebar (left side)
# .multiselect()	Show a dropdown where user can pick multiple options
# "Pick your Region"	The label shown above the dropdown
# df["Region"].unique()	Pulls all the unique region names from your data (like East, West, South, etc.)
# region: It stores the selected values in a variable called region, so you can use it to filter your data later.

if not region:#If the user didn’t select any region, then show all data.
    df2 = df.copy()
else:#If they selected specific regions, then show only those rows
    df2 = df[df['Region'].isin(region)]
    
# create for State

state = st.sidebar.multiselect('Pick the State', df2['State'].unique())#This creates a multi-select dropdown in the sidebar
if not state:#If no state is selected...
    df3 = df2.copy()#Keep all states from the previous filtered data (df2)
else:#If user did select some states...
    df3 = df2[df2['State'].isin(state)]#Keep only rows with the selected states


    # Create for City
city = st.sidebar.multiselect("Pick the City",df3["City"].unique())#This shows a multi-select dropdown for cities,

# Filter the data based on Region, State and City

if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df = df[df["Region"].isin(region)]
elif not region and not city:
    filtered_df = df[df["State"].isin(state)]
elif state and city:
    filtered_df = df3[df["State"].isin(state) & df3["City"].isin(city)]
elif region and city:
    filtered_df = df3[df["Region"].isin(region) & df3["City"].isin(city)]
elif region and state:
    filtered_df = df3[df["Region"].isin(region) & df3["State"].isin(state)]
elif city:
    filtered_df = df3[df3["City"].isin(city)]
else:
    filtered_df = df3[df3["Region"].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]
    
    
category_df = filtered_df.groupby(by = ["Category"], as_index = False)["Sales"].sum()

with col1:
    st.subheader("Category wise Sales")
    fig = px.bar(category_df, x = "Category", y = "Sales", text = ['${:,.2f}'.format(x) for x in category_df["Sales"]],
                 template = "seaborn")
    st.plotly_chart(fig,use_container_width=True, height = 200)

with col2:
    st.subheader("Region wise Sales")
    fig = px.pie(filtered_df, values = "Sales", names = "Region", hole = 0.5)
    fig.update_traces(text = filtered_df["Region"], textposition = "outside")
    st.plotly_chart(fig,use_container_width=True)
    
cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("Category_ViewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Category.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')

with cl2:
    with st.expander("Region_ViewData"):
        region = filtered_df.groupby(by = "Region", as_index = False)["Sales"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Region.csv", mime = "text/csv",
                        help = 'Click here to download the data as a CSV file')

filtered_df["month_year"] = filtered_df["Order Date"].dt.to_period("M")
st.subheader('Time Series Analysis')

linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
fig2 = px.line(linechart, x = "month_year", y="Sales", labels = {"Sales": "Amount"},height=500, width = 1000,template="gridon")
st.plotly_chart(fig2,use_container_width=True)

with st.expander("View Data of TimeSeries:"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button('Download Data', data = csv, file_name = "TimeSeries.csv", mime ='text/csv')
    
import plotly.figure_factory as ff
st.subheader(":point_right: Month wise Sub-Category Sales Summary")
with st.expander("Summary_Table"):
    df_sample = df[0:5][["Region","State","City","Category","Sales","Profit","Quantity"]]
    fig = ff.create_table(df_sample, colorscale = "Cividis")
    st.plotly_chart(fig, use_container_width=True)
    
    
# Create a scatter plot
data1 = px.scatter(filtered_df, x = "Sales", y = "Profit", size = "Quantity")
data1.update_layout(
    title=dict(
        text="Relationship between Sales and Profits using Scatter Plot.",
        font=dict(size=20)
    ),
    xaxis=dict(
        title=dict(
            text="Sales",
            font=dict(size=19)
        )
    ),
    yaxis=dict(
        title=dict(
            text="Profit",
            font=dict(size=19)
        )
    )
)
with st.expander("View Data"):
    st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))

st.plotly_chart(data1, use_container_width=True)

# Download orginal DataSet
csv = df.to_csv(index = False).encode('utf-8')
st.download_button('Download Data', data = csv, file_name = "Data.csv",mime = "text/csv")