"""
TP DataViz N°1 - EXERCICE 2 : Dashboard Interactif STYLÉ
Dashboard moderne avec design gradient et animations
"""

import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

# ==============================================================================
# CHARGEMENT ET PRÉPARATION DES DONNÉES
# ==============================================================================
print("🔄 Chargement des données...")
df = pd.read_excel('data_dashboard_large.xlsx')

# Conversion du montant en numérique
df['Montant'] = pd.to_numeric(df['Montant'].astype(str).str.replace(',', '.'), errors='coerce')

# Conversion de la date
df['Date_Transaction'] = pd.to_datetime(df['Date_Transaction'])
df['Date'] = df['Date_Transaction'].dt.date

print(f"✅ Données chargées : {len(df)} transactions")
print(f"📅 Période : du {df['Date_Transaction'].min().date()} au {df['Date_Transaction'].max().date()}")

# ==============================================================================
# CALCUL DES KPI GLOBAUX
# ==============================================================================
def calculer_kpis(data):
    """Calcule les KPI globaux"""
    kpis = {
        'total_ventes': data['Montant'].sum(),
        'nb_transactions': len(data),
        'montant_moyen': data['Montant'].mean(),
        'satisfaction_moyenne': data['Satisfaction_Client'].mean()
    }
    return kpis

# ==============================================================================
# CRÉATION DE L'APPLICATION DASH
# ==============================================================================
app = dash.Dash(__name__)

# ==============================================================================
# CSS PERSONNALISÉ ULTRA MODERNE
# ==============================================================================
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Dashboard Analytique Pro</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            /* Animation de pulsation */
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            
            /* Animation de glissement */
            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            /* Animation de brillance */
            @keyframes shine {
                0% { background-position: -200% center; }
                100% { background-position: 200% center; }
            }
            
            /* Conteneur principal */
            #react-entry-point > div {
                animation: slideIn 0.6s ease-out;
            }
            
            /* Cartes KPI stylées */
            .kpi-card {
                background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%);
                border-radius: 20px;
                padding: 25px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }
            
            .kpi-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
                animation: shine 3s infinite;
            }
            
            .kpi-card:hover {
                transform: translateY(-10px) scale(1.02);
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            
            /* Cartes de section */
            .section-card {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 25px;
                padding: 30px;
                margin-bottom: 30px;
                box-shadow: 0 15px 50px rgba(0,0,0,0.15);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.3);
                animation: slideIn 0.6s ease-out;
            }
            
            /* Titre principal */
            .main-title {
                background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
                border-radius: 20px;
                padding: 30px;
                margin-bottom: 30px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                text-align: center;
            }
            
            .main-title h1 {
                font-size: 42px;
                font-weight: 700;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 10px;
            }
            
            .main-title p {
                color: #666;
                font-size: 18px;
                font-weight: 300;
            }
            
            /* Section filtres */
            .filters-section {
                background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(240,240,255,0.95) 100%);
                border-radius: 20px;
                padding: 25px;
                margin-bottom: 30px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.15);
                border-left: 5px solid #667eea;
            }
            
            /* Titres de section */
            .section-title {
                font-size: 28px;
                font-weight: 600;
                color: #2d3748;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .section-title::before {
                content: '';
                width: 5px;
                height: 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 10px;
            }
            
            /* Dropdowns personnalisés */
            .Select-control {
                border-radius: 12px !important;
                border: 2px solid #e2e8f0 !important;
                transition: all 0.3s ease !important;
            }
            
            .Select-control:hover {
                border-color: #667eea !important;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
            }
            
            /* Graphiques */
            .js-plotly-plot {
                border-radius: 15px;
                overflow: hidden;
            }
            
            /* Tableaux */
            .dash-table-container {
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            }
            
            /* Badges */
            .badge {
                display: inline-block;
                padding: 8px 16px;
                border-radius: 20px;
                font-weight: 600;
                font-size: 14px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            }
            
            /* Icônes */
            .icon {
                font-size: 24px;
                margin-right: 10px;
            }
            
            /* Footer */
            .footer {
                text-align: center;
                padding: 20px;
                color: rgba(255,255,255,0.8);
                font-size: 14px;
                margin-top: 40px;
            }
            
            /* Scrollbar personnalisée */
            ::-webkit-scrollbar {
                width: 10px;
            }
            
            ::-webkit-scrollbar-track {
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 10px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# ==============================================================================
# LAYOUT DU DASHBOARD AVEC STYLE MODERNE
# ==============================================================================
app.layout = html.Div([
    
    # HEADER STYLÉ
    html.Div([
        html.H1(' Dashboard Analytique ', className='main-title'),
        html.P('Analyse des performances commerciales en temps réel', 
               style={'textAlign': 'center', 'color': 'rgba(255,255,255,0.9)', 
                      'fontSize': '18px', 'marginTop': '-15px'})
    ], className='main-title'),
    
    # ===========================================================================
    # FILTRES DYNAMIQUES STYLÉS
    # ===========================================================================
    html.Div([
        html.H3('🔍 Filtres de recherche', className='section-title'),
        
        html.Div([
            # Filtre Magasin
            html.Div([
                html.Label('🏪 Magasin', style={'fontWeight': '600', 'marginBottom': '8px', 
                                                 'color': '#2d3748', 'display': 'block'}),
                dcc.Dropdown(
                    id='filtre-magasin',
                    options=[{'label': '🌍 Tous les magasins', 'value': 'ALL'}] + 
                            [{'label': f'🏢 {m}', 'value': m} for m in sorted(df['Magasin'].unique())],
                    value='ALL',
                    clearable=False,
                    style={'borderRadius': '12px'}
                )
            ], style={'width': '23%', 'display': 'inline-block', 'marginRight': '2%', 'verticalAlign': 'top'}),
            
            # Filtre Catégorie
            html.Div([
                html.Label('📦 Catégorie', style={'fontWeight': '600', 'marginBottom': '8px', 
                                                   'color': '#2d3748', 'display': 'block'}),
                dcc.Dropdown(
                    id='filtre-categorie',
                    options=[{'label': '📊 Toutes les catégories', 'value': 'ALL'}] + 
                            [{'label': f'📦 {c}', 'value': c} for c in sorted(df['Categorie_Produit'].unique())],
                    value='ALL',
                    clearable=False,
                    style={'borderRadius': '12px'}
                )
            ], style={'width': '23%', 'display': 'inline-block', 'marginRight': '2%', 'verticalAlign': 'top'}),
            
            # Filtre Mode de paiement
            html.Div([
                html.Label('💳 Mode de paiement', style={'fontWeight': '600', 'marginBottom': '8px', 
                                                          'color': '#2d3748', 'display': 'block'}),
                dcc.Dropdown(
                    id='filtre-paiement',
                    options=[{'label': '💰 Tous', 'value': 'ALL'}] + 
                            [{'label': f'💳 {p}', 'value': p} for p in sorted(df['Mode_Paiement'].unique())],
                    value='ALL',
                    clearable=False,
                    style={'borderRadius': '12px'}
                )
            ], style={'width': '23%', 'display': 'inline-block', 'marginRight': '2%', 'verticalAlign': 'top'}),
            
            # Filtre Période
            html.Div([
                html.Label('📅 Période', style={'fontWeight': '600', 'marginBottom': '8px', 
                                                'color': '#2d3748', 'display': 'block'}),
                dcc.DatePickerRange(
                    id='filtre-periode',
                    start_date=df['Date_Transaction'].min(),
                    end_date=df['Date_Transaction'].max(),
                    display_format='DD/MM/YYYY',
                    style={'borderRadius': '12px'}
                )
            ], style={'width': '23%', 'display': 'inline-block', 'verticalAlign': 'top'})
        ])
    ], className='filters-section'),
    
    # ===========================================================================
    # SECTION 1 : VUE D'ENSEMBLE (KPI GLOBAUX)
    # ===========================================================================
    html.Div([
        html.H2('📈 Vue d\'ensemble', className='section-title'),
        
        # Cartes KPI
        html.Div(id='kpi-cards', style={'display': 'flex', 'justifyContent': 'space-between', 
                                         'marginBottom': '25px', 'gap': '20px'}),
        
        # Graphique ventes quotidiennes
        dcc.Graph(id='graph-ventes-quotidiennes', 
                  config={'displayModeBar': False},
                  style={'borderRadius': '15px'})
    ], className='section-card'),
    
    # ===========================================================================
    # SECTION 2 : ANALYSE PAR MAGASIN
    # ===========================================================================
    html.Div([
        html.H2('🏪 Analyse par magasin', className='section-title'),
        
        html.Div([
            # Graphique en secteurs
            html.Div([
                dcc.Graph(id='graph-repartition-magasins', config={'displayModeBar': False})
            ], style={'width': '48%', 'display': 'inline-block'}),
            
            # Graphique montant moyen
            html.Div([
                dcc.Graph(id='graph-montant-moyen-magasins', config={'displayModeBar': False})
            ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ]),
        
        # Tableau des ventes par magasin
        html.H3('📊 Détails par magasin', style={'color': '#2d3748', 'marginTop': '25px', 'marginBottom': '15px'}),
        html.Div(id='tableau-magasins')
    ], className='section-card'),
    
    # ===========================================================================
    # SECTION 3 : ANALYSE DES CATÉGORIES DE PRODUITS
    # ===========================================================================
    html.Div([
        html.H2('📦 Analyse des catégories de produits', className='section-title'),
        
        html.Div([
            # Histogramme quantités
            html.Div([
                dcc.Graph(id='graph-quantites-categories', config={'displayModeBar': False})
            ], style={'width': '48%', 'display': 'inline-block'}),
            
            # Graphique empilé
            html.Div([
                dcc.Graph(id='graph-ca-categories-magasins', config={'displayModeBar': False})
            ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ])
    ], className='section-card'),
    
    # ===========================================================================
    # SECTION 4 : ANALYSE DES MODES DE PAIEMENT
    # ===========================================================================
    html.Div([
        html.H2('💳 Analyse des modes de paiement', className='section-title'),
        
        html.Div([
            # Graphique secteurs
            html.Div([
                dcc.Graph(id='graph-modes-paiement', config={'displayModeBar': False})
            ], style={'width': '48%', 'display': 'inline-block'}),
            
            # KPI mode le plus utilisé
            html.Div(id='kpi-mode-paiement', 
                    style={'width': '48%', 'display': 'inline-block', 'float': 'right',
                           'textAlign': 'center', 'padding': '50px'})
        ])
    ], className='section-card'),
    
    # ===========================================================================
    # SECTION 5 : ANALYSE DE LA SATISFACTION CLIENT
    # ===========================================================================
    html.Div([
        html.H2('⭐ Analyse de la satisfaction client', className='section-title'),
        
        html.Div([
            # Satisfaction par magasin
            html.Div([
                dcc.Graph(id='graph-satisfaction-magasins', config={'displayModeBar': False})
            ], style={'width': '48%', 'display': 'inline-block'}),
            
            # Satisfaction par catégorie
            html.Div([
                dcc.Graph(id='graph-satisfaction-categories', config={'displayModeBar': False})
            ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ]),
        
        # Distribution des scores
        html.H3('📊 Distribution des scores', style={'color': '#2d3748', 'marginTop': '25px', 'marginBottom': '15px'}),
        html.Div(id='tableau-satisfaction')
    ], className='section-card'),
    
    # Footer
    html.Div([
        html.P('Dashboard créé avec ❤️ en Python Dash | © 2024 | Analyse Décisionnelle', 
               className='footer')
    ])
])

# ==============================================================================
# CALLBACKS POUR L'INTERACTIVITÉ
# ==============================================================================

@app.callback(
    [Output('kpi-cards', 'children'),
     Output('graph-ventes-quotidiennes', 'figure'),
     Output('graph-repartition-magasins', 'figure'),
     Output('graph-montant-moyen-magasins', 'figure'),
     Output('tableau-magasins', 'children'),
     Output('graph-quantites-categories', 'figure'),
     Output('graph-ca-categories-magasins', 'figure'),
     Output('graph-modes-paiement', 'figure'),
     Output('kpi-mode-paiement', 'children'),
     Output('graph-satisfaction-magasins', 'figure'),
     Output('graph-satisfaction-categories', 'figure'),
     Output('tableau-satisfaction', 'children')],
    [Input('filtre-magasin', 'value'),
     Input('filtre-categorie', 'value'),
     Input('filtre-paiement', 'value'),
     Input('filtre-periode', 'start_date'),
     Input('filtre-periode', 'end_date')]
)
def update_dashboard(magasin, categorie, paiement, start_date, end_date):
    # Filtrer les données
    df_filtered = df.copy()
    
    if magasin != 'ALL':
        df_filtered = df_filtered[df_filtered['Magasin'] == magasin]
    if categorie != 'ALL':
        df_filtered = df_filtered[df_filtered['Categorie_Produit'] == categorie]
    if paiement != 'ALL':
        df_filtered = df_filtered[df_filtered['Mode_Paiement'] == paiement]
    if start_date and end_date:
        df_filtered = df_filtered[
            (df_filtered['Date_Transaction'] >= start_date) & 
            (df_filtered['Date_Transaction'] <= end_date)
        ]
    
    # Calculer les KPI
    kpis = calculer_kpis(df_filtered)
    
    # ===========================================================================
    # 1. CARTES KPI STYLÉES
    # ===========================================================================
    kpi_cards = [
        html.Div([
            html.Div('💰', style={'fontSize': '40px', 'marginBottom': '10px'}),
            html.H4('Total des ventes', style={'color': '#718096', 'marginBottom': '10px', 'fontSize': '14px'}),
            html.H2(f"{kpis['total_ventes']:,.0f} €", style={'color': '#667eea', 'margin': '0', 'fontWeight': '700'})
        ], className='kpi-card', style={'flex': '1', 'textAlign': 'center'}),
        
        html.Div([
            html.Div('🛒', style={'fontSize': '40px', 'marginBottom': '10px'}),
            html.H4('Transactions', style={'color': '#718096', 'marginBottom': '10px', 'fontSize': '14px'}),
            html.H2(f"{kpis['nb_transactions']:,}", style={'color': '#48bb78', 'margin': '0', 'fontWeight': '700'})
        ], className='kpi-card', style={'flex': '1', 'textAlign': 'center'}),
        
        html.Div([
            html.Div('📊', style={'fontSize': '40px', 'marginBottom': '10px'}),
            html.H4('Montant moyen', style={'color': '#718096', 'marginBottom': '10px', 'fontSize': '14px'}),
            html.H2(f"{kpis['montant_moyen']:.2f} €", style={'color': '#ed8936', 'margin': '0', 'fontWeight': '700'})
        ], className='kpi-card', style={'flex': '1', 'textAlign': 'center'}),
        
        html.Div([
            html.Div('⭐', style={'fontSize': '40px', 'marginBottom': '10px'}),
            html.H4('Satisfaction', style={'color': '#718096', 'marginBottom': '10px', 'fontSize': '14px'}),
            html.H2(f"{kpis['satisfaction_moyenne']:.2f}/5", style={'color': '#f6ad55', 'margin': '0', 'fontWeight': '700'})
        ], className='kpi-card', style={'flex': '1', 'textAlign': 'center'})
    ]
    
    # ===========================================================================
    # 2. VENTES QUOTIDIENNES
    # ===========================================================================
    ventes_quotidiennes = df_filtered.groupby('Date')['Montant'].sum().reset_index()
    fig_ventes_quotidiennes = go.Figure()
    fig_ventes_quotidiennes.add_trace(go.Scatter(
        x=ventes_quotidiennes['Date'],
        y=ventes_quotidiennes['Montant'],
        mode='lines+markers',
        line=dict(color='#667eea', width=3),
        marker=dict(size=8, color='#764ba2'),
        fill='tonexty',
        fillcolor='rgba(102, 126, 234, 0.1)',
        name='Ventes'
    ))
    fig_ventes_quotidiennes.update_layout(
        title='Évolution des ventes quotidiennes',
        xaxis_title='Date',
        yaxis_title='Ventes (€)',
        template='plotly_white',
        hovermode='x unified',
        font=dict(family='Poppins', size=12),
        title_font=dict(size=18, color='#2d3748', family='Poppins')
    )
    
    # ===========================================================================
    # 3. ANALYSE PAR MAGASIN
    # ===========================================================================
    ventes_magasins = df_filtered.groupby('Magasin')['Montant'].sum().reset_index()
    fig_repartition = px.pie(
        ventes_magasins, values='Montant', names='Magasin',
        title='Répartition des ventes par magasin',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig_repartition.update_traces(textposition='inside', textinfo='percent+label', textfont_size=12)
    fig_repartition.update_layout(font=dict(family='Inter'))
    
    montant_moyen_magasins = df_filtered.groupby('Magasin')['Montant'].mean().reset_index()
    fig_montant_moyen = px.bar(
        montant_moyen_magasins, x='Magasin', y='Montant',
        title='Montant moyen par transaction et par magasin',
        labels={'Montant': 'Montant moyen (€)'},
        color='Montant',
        color_continuous_scale='Purples'
    )
    fig_montant_moyen.update_layout(showlegend=False, font=dict(family='Inter'))
    
    stats_magasins = df_filtered.groupby('Magasin').agg({
        'Montant': ['sum', 'count', 'mean']
    }).round(2)
    stats_magasins.columns = ['Ventes totales (€)', 'Nb transactions', 'Montant moyen (€)']
    stats_magasins = stats_magasins.reset_index()
    
    tableau_magasins = dash_table.DataTable(
        data=stats_magasins.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in stats_magasins.columns],
        style_cell={'textAlign': 'left', 'padding': '12px', 'fontFamily': 'Poppins'},
        style_header={
            'backgroundColor': "#66ea71",
            'color': 'white',
            'fontWeight': '600',
            'border': 'none'
        },
        style_data_conditional=[
            {'if': {'row_index': 'odd'}, 'backgroundColor': '#f7fafc'}
        ],
        style_table={'borderRadius': '10px', 'overflow': 'hidden'}
    )
    
    # ===========================================================================
    # 4. ANALYSE DES CATÉGORIES
    # ===========================================================================
    quantites_cat = df_filtered.groupby('Categorie_Produit')['Quantite'].sum().reset_index()
    fig_quantites = px.bar(
        quantites_cat, x='Categorie_Produit', y='Quantite',
        title='Quantités vendues par catégorie',
        labels={'Quantite': 'Quantité totale', 'Categorie_Produit': 'Catégorie'},
        color='Quantite',
        color_continuous_scale='Teal'
    )
    fig_quantites.update_layout(font=dict(family='Inter'))
    
    ca_cat_mag = df_filtered.groupby(['Magasin', 'Categorie_Produit'])['Montant'].sum().reset_index()
    fig_ca_empile = px.bar(
        ca_cat_mag, x='Magasin', y='Montant', color='Categorie_Produit',
        title='Chiffre d\'affaires par catégorie et magasin',
        labels={'Montant': 'CA (€)'},
        barmode='stack',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_ca_empile.update_layout(font=dict(family='Inter'))
    
    # ===========================================================================
    # 5. MODES DE PAIEMENT
    # ===========================================================================
    modes_paiement = df_filtered['Mode_Paiement'].value_counts().reset_index()
    modes_paiement.columns = ['Mode_Paiement', 'Count']
    
    fig_modes = px.pie(
        modes_paiement, values='Count', names='Mode_Paiement',
        title='Répartition des transactions par mode de paiement',
        hole=0.3,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_modes.update_layout(font=dict(family='Inter'))
    
    mode_plus_utilise = modes_paiement.iloc[0]['Mode_Paiement']
    pct_mode = (modes_paiement.iloc[0]['Count'] / modes_paiement['Count'].sum() * 100)
    
    kpi_mode = html.Div([
        html.Div('💳', style={'fontSize': '60px', 'marginBottom': '20px'}),
        html.H3('Mode de paiement le plus utilisé', style={'color': '#718096', 'marginBottom': '15px'}),
        html.H1(mode_plus_utilise, style={'color': '#667eea', 'margin': '10px 0', 'fontWeight': '700'}),
        html.H2(f'{pct_mode:.1f}%', style={'color': '#48bb78', 'fontWeight': '600'}),
        html.Div(className='badge', children=f'Leader du marché', 
                 style={'marginTop': '20px', 'display': 'inline-block'})
    ])
    
    # ===========================================================================
    # 6. SATISFACTION CLIENT
    # ===========================================================================
    satisfaction_mag = df_filtered.groupby('Magasin')['Satisfaction_Client'].mean().reset_index()
    fig_sat_mag = px.bar(
        satisfaction_mag, x='Magasin', y='Satisfaction_Client',
        title='Satisfaction moyenne par magasin',
        labels={'Satisfaction_Client': 'Score moyen'},
        color='Satisfaction_Client',
        color_continuous_scale='RdYlGn',
        range_color=[1, 5]
    )
    fig_sat_mag.update_layout(font=dict(family='Inter'))
    
    satisfaction_cat = df_filtered.groupby('Categorie_Produit')['Satisfaction_Client'].mean().reset_index()
    fig_sat_cat = px.bar(
        satisfaction_cat, x='Categorie_Produit', y='Satisfaction_Client',
        title='Satisfaction moyenne par catégorie',
        labels={'Satisfaction_Client': 'Score moyen', 'Categorie_Produit': 'Catégorie'},
        color='Satisfaction_Client',
        color_continuous_scale='RdYlGn',
        range_color=[1, 5]
    )
    fig_sat_cat.update_layout(font=dict(family='Inter'))
    
    dist_satisfaction = df_filtered['Satisfaction_Client'].value_counts().sort_index().reset_index()
    dist_satisfaction.columns = ['Score', 'Nombre de transactions']
    dist_satisfaction['Pourcentage'] = (dist_satisfaction['Nombre de transactions'] / 
                                        dist_satisfaction['Nombre de transactions'].sum() * 100).round(2)
    
    tableau_satisfaction = dash_table.DataTable(
        data=dist_satisfaction.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in dist_satisfaction.columns],
        style_cell={'textAlign': 'center', 'padding': '12px', 'fontFamily': 'Poppins'},
        style_header={
            'backgroundColor': '#f6ad55',
            'color': 'white',
            'fontWeight': '600',
            'border': 'none'
        },
        style_data_conditional=[
            {'if': {'row_index': 'odd'}, 'backgroundColor': '#f7fafc'},
            {'if': {'filter_query': '{Score} = 5'}, 'backgroundColor': '#c6f6d5', 'color': '#22543d', 'fontWeight': '600'},
            {'if': {'filter_query': '{Score} = 1'}, 'backgroundColor': '#fed7d7', 'color': '#742a2a', 'fontWeight': '600'}
        ],
        style_table={'borderRadius': '10px', 'overflow': 'hidden'}
    )
    
    return (kpi_cards, fig_ventes_quotidiennes, fig_repartition, fig_montant_moyen,
            tableau_magasins, fig_quantites, fig_ca_empile, fig_modes, kpi_mode,
            fig_sat_mag, fig_sat_cat, tableau_satisfaction)

# ==============================================================================
# LANCEMENT DU SERVEUR
# ==============================================================================
server = app.server
if __name__ == '__main__':
    print("\n" + "="*80)
    print("🚀 DASHBOARD INTERACTIF STYLÉ LANCÉ")
    print("="*80)
    print("\n📍 Ouvrez votre navigateur à l'adresse : http://127.0.0.1:8051/")
    print("\n💡 Design moderne avec animations et gradient")
    print("⏹️  Appuyez sur Ctrl+C pour arrêter le serveur\n")
    
    app.run(debug=True, host='0.0.0.0', port=8051)