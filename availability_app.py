import pandas as pd
import datetime
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
from PIL import Image

dft_read = pd.read_excel(r'D:\OneDrive - Blue Power Partners\Documents\Python Scripts\renato-mc-monthlyreport/W&S Task Planner1.xlsx')

m_avail_dft = dft_read[(dft_read['Task Name'].str.contains('Available '))
                     & (dft_read['Task Name'].str.contains('new '))][['Bucket Name','Task Name']]


w_avail_dft = dft_read[(dft_read['Task Name'].str.contains('Available '))
                     & (dft_read['Task Name'].str.contains('next '))][['Bucket Name','Task Name']]


m_current_avail = m_avail_dft[m_avail_dft['Task Name'].str.contains(str("Available for new task"))]

m_current_avail['Task Name'] = m_current_avail['Task Name'].str.rstrip()

m_current_avail['avail'] = m_current_avail['Task Name'].str.split(' ').str[-1]

m_avail=m_current_avail['avail']

m_name=m_current_avail['Bucket Name']



w_current_avail = w_avail_dft[w_avail_dft['Task Name'].str.contains(str("Available for next task"))]

w_current_avail['Task Name'] = w_current_avail['Task Name'].str.rstrip()

w_current_avail['avail'] = w_current_avail['Task Name'].str.split(' ').str[-1]

w_avail=w_current_avail['avail']

w_name=w_current_avail['Bucket Name']


df = pd.DataFrame(m_name)
df1 = pd.DataFrame(m_avail)
concatenated_df = pd.concat([df, df1], axis=1)



dg = pd.DataFrame(w_name)
dg1 = pd.DataFrame(w_avail)
n_df = pd.concat([dg, dg1], axis=1)
combined1_df = pd.concat([concatenated_df, n_df], ignore_index=True)
combined1_df.to_csv('modeling.csv', index=False)

ab=pd.read_csv('modeling.csv')
ab['avail'] = pd.to_datetime(ab['avail'])
today = datetime.date.today()
ab['match'] = ab['avail'].dt.date.eq(today).astype(int)
ab.to_csv('modeling.csv', index=False)


dft1_read = pd.read_excel(r'D:\OneDrive - Blue Power Partners\Documents\Python Scripts\renato-mc-monthlyreport/W&S Task Planner1.xlsx')

avail_dft1 = dft1_read[(dft1_read['Task Name'].str.contains('Week '))
                     & (dft1_read['Task Name'].str.contains('Available '))][['Bucket Name','Task Name']]

today_week_no = datetime.date.today().isocalendar()[1]
current_avail1 = avail_dft1[avail_dft1['Task Name'].str.contains(str(today_week_no))]

if len(current_avail1) == 0:
    current_avail1 = avail_dft1[avail_dft1['Task Name'].str.contains(str(today_week_no-1))]

# delete whitespace at the end of the string

current_avail1['Task Name'] = current_avail1['Task Name'].str.rstrip()

current_avail1['avail'] = current_avail1['Task Name'].str.split(' ').str[-1]

current_avail1['avail'] = current_avail1['avail'].str.split('%').str[0].astype(float)

name1=current_avail1['Bucket Name']
avail1=current_avail1['avail']

existing_df = pd.read_csv('modeling.csv')


# Modify the headers of the new columns
new_headers = ['Bucket name1', 'avail1']

updated_df = pd.concat([existing_df, pd.DataFrame({new_headers[0]: name1, new_headers[1]: avail1})], axis=1)

# Save the updated dataframe to the existing CSV file
updated_df.to_csv('WnS.csv', index=False)

ws = pd.read_csv('WnS.csv')
new_column_names = ['Name', 'Next Available Date \n (yyyy-mm-dd)', 'match', 'name1', 'avail1']

# Update the column names of the DataFrame
ws.columns = new_column_names

# Save the DataFrame back to a CSV file
ws.to_csv('updated_WnS.csv', index=False)

db = pd.read_csv('updated_WnS.csv')
replace_dict = {
    'Senthilnathan Kumarasamy': 'Senthil',
    'Suba Deve S': 'Suba',
    'Avinash Bhabu S D': 'Avinash',
    'Parvathy Anil': 'Parvathy',
    'Purushothaman Mani':'Puru',
    'Oscar Briz Lopez': 'Oscar',
    'Naveen N': 'Naveen',
    'Shaima': 'Shaima',
    'Anju V S': 'Anju',
    'Parvathy M': 'Parvathy',
    'Manikandan R': 'Mani',
    'Subramanian Vaidyanathan': 'Subra',
    'Vetrivel Pandiyan B': 'Vetri',
    'Velmurugan Karuppiah': 'Vel',
}
db = db.replace(replace_dict)

app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div(children=[
    html.H1('Availability of W&S Team Members', style={'text-align': 'center'}),
    
    html.Div(children=[
        dcc.Graph(
            id='scatter-plot',
            figure={
                'data': [
                    go.Scatter(
                        x=db['Name'],
                        y=db['match'],
                        mode='markers',
                        marker={
                            'size': 20,
                            'color': ['red' if marker == 0 else 'green' for marker in db['match']],
                        },
                    )
                ],
                'layout': go.Layout(
                    title="Today's Availability of Modeling Team Members",
                    xaxis={'tickfont': {'size': 16}},
                    yaxis={'tickmode': 'array',
                        'tickvals': [0, 1],
                        'ticktext': ['Not Available', 'Available'],
                        'tickfont': {'size': 12}
                    },
                    showlegend=False,
                
                    height=400
                )
            }
        ),
        
        html.Div(children=[
            dcc.Graph(
                id='bar-plot',
                figure={
                    'data': [
                        go.Bar(
                            x=db['name1'],
                            y=db['avail1'],
                            marker={'color': '#190157'},
                            width=0.2
                        )
                    ],
                    'layout': go.Layout(
                        title='Availability of MO Team Members',
                        xaxis={'title': 'Name','tickfont': {'size': 16}},
                        yaxis={'title': 'Availability (%)','tickfont': {'size': 16}},
                        showlegend=False,
                        height=400
                    )
                }
            )
        ], style={'margin-top': '50px'}),
        
        html.Div(children=[
            dcc.Markdown(
                """
                **Table: Next Available Date of Modeling Team Members**
                """
            ),
            dash_table.DataTable(
            id='availability-table',
            columns=[{'name': col, 'id': col} for col in db.columns[:-3]],  # Remove last two columns
            data=db.iloc[:, :-3].to_dict('records'),  # Remove last two columns from the data
            style_table={'height': '250px', 'overflowY': 'auto','font-size': '25px'},
            style_header={
                'backgroundColor': '#190157',
                'fontWeight': 'bold',
                'color': 'white',
                'padding': '8px'
            },
            style_cell={'textAlign': 'center', 'font-size': '20px', 'padding': '5px'}
        ),
       dcc.Markdown(
              
            )
        ])
    ], className='container')
])

if __name__ == '__main__':
    app.run_server(debug=False, port=8052)