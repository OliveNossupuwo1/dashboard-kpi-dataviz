"""
TP DataViz N°1 - EXERCICE 1 : DASHBOARD KPI STYLÉ
Dashboard interactif pour l'analyse des 6 KPI
"""

import dash
from dash import dcc, html, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ==============================================================================
# CHARGEMENT ET PRÉPARATION DES DONNÉES
# ==============================================================================
print("🔄 Chargement des données de l'Exercice 1...")
df = pd.read_excel('data_kpi.xlsx')

# Conversion du montant en numérique
df['Montant_Transaction'] = pd.to_numeric(df['Montant_Transaction'], errors='coerce')

print(f"✅ Données chargées : {len(df)} transactions")
print(f"📅 Période : du {df['Date_Transaction'].min().date()} au {df['Date_Transaction'].max().date()}")

# ==============================================================================
# CALCUL DES 6 KPI
# ==============================================================================

# KPI 1 : Valeur moyenne des transactions
moyenne_transactions = df['Montant_Transaction'].mean()
min_transaction = df['Montant_Transaction'].min()
max_transaction = df['Montant_Transaction'].max()
mediane_transaction = df['Montant_Transaction'].median()

# KPI 2 : Répartition des catégories de produits
ca_par_categorie = df.groupby('Categorie_Produit')['Montant_Transaction'].sum()
ca_total = ca_par_categorie.sum()
pourcentage_par_categorie = (ca_par_categorie / ca_total * 100).round(2)

# KPI 3 : Taux de récurrence des clients
transactions_par_client = df.groupby('ID_Client').size()
clients_recurrents = transactions_par_client[transactions_par_client > 1]
nombre_clients_recurrents = len(clients_recurrents)
nombre_total_clients = len(transactions_par_client)
taux_recurrence = (nombre_clients_recurrents / nombre_total_clients * 100)

# KPI 4 : Modes de paiement
modes_paiement = df['Mode_Paiement'].value_counts()
total_transactions = len(df)
pourcentage_modes = (modes_paiement / total_transactions * 100).round(2)
mode_plus_utilise = modes_paiement.index[0]

# KPI 5 : Customer Lifetime Value (CLV)
clv_par_client = df.groupby('ID_Client')['Montant_Transaction'].sum()
clv_moyenne = clv_par_client.mean()
clv_min = clv_par_client.min()
clv_max = clv_par_client.max()
clv_mediane = clv_par_client.median()
top_5_clients = clv_par_client.nlargest(5)

# KPI 6 : Indice de performance des catégories
categorie_top = ca_par_categorie.idxmax()
ca_top = ca_par_categorie.max()
part_ca_top = (ca_top / ca_total * 100)

print("\n✅ Tous les KPI ont été calculés !")

# ==============================================================================
# CRÉATION DE L'APPLICATION DASH
# ==============================================================================
app = dash.Dash(__name__)

# ==============================================================================
# CSS PERSONNALISÉ
# ==============================================================================
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Dashboard KPI - Exercice 1</title>
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
            
            /* Animations */
            @keyframes slideIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            
            @keyframes shine {
                0% { background-position: -200% center; }
                100% { background-position: 200% center; }
            }
            
            /* Conteneur principal */
            #react-entry-point > div {
                animation: slideIn 0.8s ease-out;
            }
            
            /* Titre principal */
            .main-title {
                background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
                border-radius: 20px;
                padding: 40px;
                margin-bottom: 30px;
                box-shadow: 0 15px 50px rgba(0,0,0,0.25);
                text-align: center;
            }
            
            .main-title h1 {
                font-size: 48px;
                font-weight: 700;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 15px;
            }
            
            .main-title p {
                color: #718096;
                font-size: 20px;
                font-weight: 400;
            }
            
            /* Cartes KPI principales */
            .kpi-card-main {
                background: linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(255,255,255,0.9) 100%);
                border-radius: 25px;
                padding: 30px;
                box-shadow: 0 15px 50px rgba(0,0,0,0.2);
                transition: all 0.4s ease;
                position: relative;
                overflow: hidden;
                border: 2px solid rgba(102, 126, 234, 0.2);
            }
            
            .kpi-card-main::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
                animation: shine 3s infinite;
            }
            
            .kpi-card-main:hover {
                transform: translateY(-15px) scale(1.03);
                box-shadow: 0 25px 70px rgba(0,0,0,0.3);
                border-color: #667eea;
            }
            
            .kpi-number {
                font-size: 48px;
                font-weight: 700;
                margin: 15px 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            
            .kpi-label {
                font-size: 16px;
                color: #718096;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .kpi-icon {
                font-size: 64px;
                margin-bottom: 15px;
                animation: pulse 2s infinite;
            }
            
            /* Sections */
            .section-card {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 25px;
                padding: 35px;
                margin-bottom: 30px;
                box-shadow: 0 15px 50px rgba(0,0,0,0.15);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.3);
                animation: slideIn 0.6s ease-out;
            }
            
            .section-title {
                font-size: 32px;
                font-weight: 700;
                color: #2d3748;
                margin-bottom: 25px;
                display: flex;
                align-items: center;
                gap: 15px;
            }
            
            .section-title::before {
                content: '';
                width: 6px;
                height: 40px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 10px;
            }
            
            /* Badges */
            .badge {
                display: inline-block;
                padding: 10px 20px;
                border-radius: 25px;
                font-weight: 700;
                font-size: 16px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                box-shadow: 0 5px 20px rgba(102, 126, 234, 0.5);
                margin: 5px;
            }
            
            .badge-success {
                background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
            }
            
            .badge-warning {
                background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
            }
            
            .badge-info {
                background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
            }
            
            /* Résumé KPI */
            .summary-box {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 25px;
                padding: 40px;
                margin: 30px 0;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            
            .summary-box h2 {
                font-size: 36px;
                margin-bottom: 25px;
                text-align: center;
                font-weight: 700;
            }
            
            .summary-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
                margin-top: 25px;
            }
            
            .summary-item {
                background: rgba(255, 255, 255, 0.15);
                padding: 20px 25px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
                border: 2px solid rgba(255, 255, 255, 0.3);
                transition: all 0.3s ease;
            }
            
            .summary-item:hover {
                background: rgba(255, 255, 255, 0.25);
                transform: scale(1.05);
            }
            
            .summary-item strong {
                display: block;
                font-size: 32px;
                margin-bottom: 8px;
                font-weight: 700;
            }
            
            .summary-item span {
                font-size: 14px;
                opacity: 0.9;
                font-weight: 500;
            }
            
            /* Détails mini */
            .detail-box {
                background: #f7fafc;
                border-radius: 15px;
                padding: 20px;
                margin-top: 20px;
                border-left: 5px solid #667eea;
            }
            
            .detail-item {
                display: flex;
                justify-content: space-between;
                padding: 12px 0;
                border-bottom: 1px solid #e2e8f0;
            }
            
            .detail-item:last-child {
                border-bottom: none;
            }
            
            .detail-label {
                color: #718096;
                font-weight: 600;
            }
            
            .detail-value {
                color: #2d3748;
                font-weight: 700;
                font-size: 18px;
            }
            
            /* Graphiques */
            .js-plotly-plot {
                border-radius: 20px;
                overflow: hidden;
            }
            
            /* Tableaux */
            .dash-table-container {
                border-radius: 20px;
                overflow: hidden;
                box-shadow: 0 8px 30px rgba(0,0,0,0.12);
            }
            
            /* Footer */
            .footer {
                text-align: center;
                padding: 25px;
                color: rgba(255,255,255,0.9);
                font-size: 16px;
                margin-top: 50px;
                font-weight: 500;
            }
            
            /* Scrollbar */
            ::-webkit-scrollbar {
                width: 12px;
            }
            
            ::-webkit-scrollbar-track {
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 10px;
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
# LAYOUT DU DASHBOARD
# ==============================================================================
app.layout = html.Div([
    
    # HEADER
    html.Div([
        html.H1('Exercice 1 : Calcul des KPI'),
        html.P('Analyse des Indicateurs Clés de Performance')
    ], className='main-title'),
    
    # ===========================================================================
    # RÉSUMÉ DES 6 KPI PRINCIPAUX
    # ===========================================================================
    html.Div([
        html.H2('Résumé des 6 KPI', style={'textAlign': 'center'}),
        html.Div([
            html.Div([
                
                html.Span('1. Valeur moyenne des transactions '), html.Strong(f'{moyenne_transactions:.2f} €')
            ], className='summary-item'),
            
            html.Div([
                
                html.Span('2. Catégorie la plus performante '), html.Strong(f'{categorie_top}')
            ], className='summary-item'),
            
            html.Div([
                
                html.Span('3. Taux de récurrence des clients '), html.Strong(f'{taux_recurrence:.2f}%')
            ], className='summary-item'),
            
            html.Div([
                
                html.Span('4. Mode de paiement le plus utilisé '), html.Strong(f'{mode_plus_utilise}')
            ], className='summary-item'),
            
            html.Div([
                
                html.Span('5. CLV moyenne '), html.Strong(f'{clv_moyenne:.2f} €')
            ], className='summary-item'),
            
            html.Div([
                
                html.Span('6. Chiffre d\'affaires total '), html.Strong(f'{ca_total:,.2f} €')
            ], className='summary-item'),
        ], className='summary-grid')
    ], className='summary-box'),
    
    # ===========================================================================
    # KPI 1 : VALEUR MOYENNE DES TRANSACTIONS
    # ===========================================================================
    html.Div([
        html.H2('KPI 1 : Valeur Moyenne des Transactions', className='section-title'),
        
        # Carte principale
        html.Div([
            html.Div([
                html.Div('💶', className='kpi-icon'),
                html.Div(f'{moyenne_transactions:.2f} €', className='kpi-number'),
                html.Div('Valeur Moyenne', className='kpi-label'),
                html.Div([
                    html.Span('✨ ', style={'fontSize': '20px'}),
                    html.Span('Montant moyen dépensé par transaction', 
                             style={'fontSize': '14px', 'color': '#718096'})
                ], style={'marginTop': '15px'})
            ], className='kpi-card-main', style={'textAlign': 'center', 'flex': '1'}),
        ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '25px'}),
        
        # Détails
        html.Div([
            html.Div([
                html.Span('Montant minimum', className='detail-label'),
                html.Span(f'{min_transaction:.2f} €', className='detail-value')
            ], className='detail-item'),
            html.Div([
                html.Span('Montant maximum', className='detail-label'),
                html.Span(f'{max_transaction:.2f} €', className='detail-value')
            ], className='detail-item'),
            html.Div([
                html.Span('Médiane', className='detail-label'),
                html.Span(f'{mediane_transaction:.2f} €', className='detail-value')
            ], className='detail-item'),
        ], className='detail-box'),
    ], className='section-card'),
    
    # ===========================================================================
    # KPI 2 : RÉPARTITION DES CATÉGORIES
    # ===========================================================================
    html.Div([
        html.H2(' KPI 2 : Répartition des Catégories de Produits', className='section-title'),
        
        # Graphique circulaire
        dcc.Graph(
            figure=px.pie(
                values=pourcentage_par_categorie.values,
                names=pourcentage_par_categorie.index,
                title='Répartition des ventes par catégorie',
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.RdBu
            ).update_traces(
                textposition='inside',
                textinfo='percent+label',
                textfont_size=14
            ).update_layout(
                font=dict(family='Poppins', size=13),
                showlegend=True,
                height=500
            ),
            config={'displayModeBar': False}
        ),
        
        # Tableau détails
        html.Div([
            html.H3(' Détails par catégorie', style={'marginBottom': '15px', 'color': '#2d3748'}),
            dash_table.DataTable(
                data=[
                    {
                        'Catégorie': cat,
                        'CA (€)': f'{ca_par_categorie[cat]:,.2f}',
                        'Part du CA': f'{pourcentage_par_categorie[cat]:.2f}%'
                    }
                    for cat in ca_par_categorie.index
                ],
                columns=[
                    {'name': 'Catégorie', 'id': 'Catégorie'},
                    {'name': 'Chiffre d\'affaires (€)', 'id': 'CA (€)'},
                    {'name': 'Part du CA total', 'id': 'Part du CA'}
                ],
                style_cell={
                    'textAlign': 'left',
                    'padding': '15px',
                    'fontFamily': 'Poppins',
                    'fontSize': '14px'
                },
                style_header={
                    'backgroundColor': '#667eea',
                    'color': 'white',
                    'fontWeight': '700',
                    'border': 'none',
                    'fontSize': '15px'
                },
                style_data_conditional=[
                    {'if': {'row_index': 'odd'}, 'backgroundColor': '#f7fafc'}
                ]
            )
        ], style={'marginTop': '30px'})
    ], className='section-card'),
    
    # ===========================================================================
    # KPI 3 : TAUX DE RÉCURRENCE
    # ===========================================================================
    html.Div([
        html.H2('KPI 3 : Taux de Récurrence des Clients', className='section-title'),
        
        html.Div([
            html.Div([
                html.Div('👥', className='kpi-icon'),
                html.Div(f'{taux_recurrence:.2f}%', className='kpi-number'),
                html.Div('Taux de Récurrence', className='kpi-label'),
                html.Div([
                    html.Span(f'{nombre_clients_recurrents} clients récurrents sur {nombre_total_clients}', 
                             style={'fontSize': '16px', 'color': '#718096', 'marginTop': '15px'})
                ])
            ], className='kpi-card-main', style={'textAlign': 'center'}),
        ], style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '25px'}),
        
        # Distribution
        html.Div([
            html.H3('Distribution des transactions par client', 
                   style={'marginBottom': '15px', 'color': '#2d3748'}),
            html.Div([
                html.Span('Clients avec 1 transaction', className='detail-label'),
                html.Span(f'{len(transactions_par_client[transactions_par_client == 1])}', 
                         className='detail-value')
            ], className='detail-item'),
            html.Div([
                html.Span('Clients avec 2 transactions', className='detail-label'),
                html.Span(f'{len(transactions_par_client[transactions_par_client == 2])}', 
                         className='detail-value')
            ], className='detail-item'),
            html.Div([
                html.Span('Clients avec 3+ transactions', className='detail-label'),
                html.Span(f'{len(transactions_par_client[transactions_par_client >= 3])}', 
                         className='detail-value')
            ], className='detail-item'),
            html.Div([
                html.Span('Maximum de transactions par client', className='detail-label'),
                html.Span(f'{transactions_par_client.max()}', className='detail-value')
            ], className='detail-item'),
        ], className='detail-box'),
        
        # Graphique distribution
        dcc.Graph(
            figure=px.histogram(
                x=transactions_par_client.values,
                nbins=20,
                title='Distribution du nombre de transactions par client',
                labels={'x': 'Nombre de transactions', 'y': 'Nombre de clients'},
                color_discrete_sequence=['#667eea']
            ).update_layout(
                font=dict(family='Poppins'),
                showlegend=False
            ),
            config={'displayModeBar': False},
            style={'marginTop': '25px'}
        )
    ], className='section-card'),
    
    # ===========================================================================
    # KPI 4 : MODES DE PAIEMENT
    # ===========================================================================
    html.Div([
        html.H2('KPI 4 : Modes de Paiement', className='section-title'),
        
        html.Div([
            # Graphique
            html.Div([
                dcc.Graph(
                    figure=px.bar(
                        x=pourcentage_modes.index,
                        y=pourcentage_modes.values,
                        title='Répartition des transactions par mode de paiement',
                        labels={'x': 'Mode de paiement', 'y': 'Pourcentage (%)'},
                        color=pourcentage_modes.values,
                        color_continuous_scale='Viridis'
                    ).update_layout(
                        font=dict(family='Poppins'),
                        showlegend=False
                    ),
                    config={'displayModeBar': False}
                )
            ], style={'width': '60%', 'display': 'inline-block'}),
            
            # KPI principal
            html.Div([
                html.Div([
                    html.Div('💳', style={'fontSize': '80px', 'marginBottom': '20px'}),
                    html.H3('Mode le plus utilisé', 
                           style={'color': '#718096', 'marginBottom': '15px', 'fontSize': '18px'}),
                    html.H1(mode_plus_utilise, 
                           style={'color': '#667eea', 'marginBottom': '15px', 'fontWeight': '700'}),
                    html.H2(f'{pourcentage_modes[mode_plus_utilise]:.1f}%', 
                           style={'color': '#48bb78', 'fontWeight': '700'}),
                    html.Div(f'{modes_paiement[mode_plus_utilise]} transactions', 
                            style={'color': '#718096', 'marginTop': '15px', 'fontSize': '16px'})
                ], style={'textAlign': 'center', 'padding': '40px'})
            ], style={'width': '38%', 'display': 'inline-block', 'float': 'right', 
                     'verticalAlign': 'top'})
        ])
    ], className='section-card'),
    
    # ===========================================================================
    # KPI 5 : CUSTOMER LIFETIME VALUE
    # ===========================================================================
    html.Div([
        html.H2('KPI 5 : Customer Lifetime Value (CLV)', className='section-title'),
        
        html.Div([
            html.Div([
                html.Div('💰', className='kpi-icon'),
                html.Div(f'{clv_moyenne:.2f} €', className='kpi-number'),
                html.Div('CLV Moyenne', className='kpi-label'),
                html.Div('Valeur moyenne générée par client', 
                        style={'fontSize': '14px', 'color': '#718096', 'marginTop': '15px'})
            ], className='kpi-card-main', style={'textAlign': 'center'}),
        ], style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '25px'}),
        
        # Statistiques CLV
        html.Div([
            html.Div([
                html.Span('CLV minimum', className='detail-label'),
                html.Span(f'{clv_min:.2f} €', className='detail-value')
            ], className='detail-item'),
            html.Div([
                html.Span('CLV maximum', className='detail-label'),
                html.Span(f'{clv_max:.2f} €', className='detail-value')
            ], className='detail-item'),
            html.Div([
                html.Span('CLV médiane', className='detail-label'),
                html.Span(f'{clv_mediane:.2f} €', className='detail-value')
            ], className='detail-item'),
        ], className='detail-box'),
        
        # Top 5 clients
        html.Div([
            html.H3('🏆 Top 5 des clients par CLV', 
                   style={'marginTop': '30px', 'marginBottom': '15px', 'color': '#2d3748'}),
            dash_table.DataTable(
                data=[
                    {
                        'Rang': f'🥇' if i == 0 else f'🥈' if i == 1 else f'🥉' if i == 2 else f'{i+1}',
                        'Client ID': client_id,
                        'CLV (€)': f'{clv:.2f}',
                        'Nb Trans.': transactions_par_client[client_id]
                    }
                    for i, (client_id, clv) in enumerate(top_5_clients.items())
                ],
                columns=[
                    {'name': 'Rang', 'id': 'Rang'},
                    {'name': 'ID Client', 'id': 'Client ID'},
                    {'name': 'CLV (€)', 'id': 'CLV (€)'},
                    {'name': 'Nombre de transactions', 'id': 'Nb Trans.'}
                ],
                style_cell={
                    'textAlign': 'center',
                    'padding': '15px',
                    'fontFamily': 'Poppins',
                    'fontSize': '14px'
                },
                style_header={
                    'backgroundColor': '#667eea',
                    'color': 'white',
                    'fontWeight': '700',
                    'border': 'none'
                },
                style_data_conditional=[
                    {'if': {'row_index': 0}, 'backgroundColor': '#fff3cd', 'fontWeight': '700'},
                    {'if': {'row_index': 1}, 'backgroundColor': '#e2e8f0', 'fontWeight': '700'},
                    {'if': {'row_index': 2}, 'backgroundColor': '#fed7d7', 'fontWeight': '700'},
                ]
            )
        ]),
        
        # Graphique distribution CLV
        dcc.Graph(
            figure=px.histogram(
                x=clv_par_client.values,
                nbins=30,
                title='Distribution de la CLV',
                labels={'x': 'CLV (€)', 'y': 'Nombre de clients'},
                color_discrete_sequence=['#764ba2']
            ).update_layout(
                font=dict(family='Poppins'),
                showlegend=False
            ),
            config={'displayModeBar': False},
            style={'marginTop': '25px'}
        )
    ], className='section-card'),
    
    # ===========================================================================
    # KPI 6 : PERFORMANCE DES CATÉGORIES
    # ===========================================================================
    html.Div([
        html.H2('KPI 6 : Indice de Performance des Catégories', className='section-title'),
        
        html.Div([
            html.Div([
                html.Div('🏆', className='kpi-icon'),
                html.Div(categorie_top, className='kpi-number', style={'fontSize': '36px'}),
                html.Div('Catégorie la Plus Performante', className='kpi-label'),
                html.Div([
                    html.Div(f'{ca_top:,.2f} €', 
                            style={'fontSize': '24px', 'color': '#48bb78', 
                                   'fontWeight': '700', 'marginTop': '15px'}),
                    html.Div(f'{part_ca_top:.2f}% du CA total', 
                            style={'fontSize': '16px', 'color': '#718096', 'marginTop': '10px'})
                ])
            ], className='kpi-card-main', style={'textAlign': 'center'}),
        ], style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '25px'}),
        
        # Graphique comparatif
        dcc.Graph(
            figure=go.Figure([
                go.Bar(
                    x=ca_par_categorie.index,
                    y=ca_par_categorie.values,
                    marker_color=['gold' if cat == categorie_top else '#667eea' 
                                 for cat in ca_par_categorie.index],
                    text=[f'{val:,.0f}€' for val in ca_par_categorie.values],
                    textposition='outside'
                )
            ]).update_layout(
                title='Performance des catégories de produits (Chiffre d\'affaires)',
                xaxis_title='Catégorie',
                yaxis_title='CA (€)',
                font=dict(family='Poppins', size=13),
                showlegend=False,
                height=500
            ),
            config={'displayModeBar': False}
        )
    ], className='section-card'),
    
    # ===========================================================================
    # CONCLUSION
    # ===========================================================================
    html.Div([
        html.H2('Résumé de l\'Analyse', className='section-title'),
        html.Div([
            html.P([
                html.Strong('Données analysées : '),
                f'{len(df)} transactions de {nombre_total_clients} clients'
            ], style={'fontSize': '16px', 'marginBottom': '15px'}),
            html.P([
                html.Strong('Chiffre d\'affaires total : '),
                f'{ca_total:,.2f} €'
            ], style={'fontSize': '16px', 'marginBottom': '15px'}),
            html.P([
                html.Strong('Catégorie leader : '),
                f'{categorie_top} ({part_ca_top:.2f}% du CA)'
            ], style={'fontSize': '16px', 'marginBottom': '15px'}),
            html.P([
                html.Strong('Fidélisation : '),
                f'{taux_recurrence:.2f}% de clients récurrents - Excellent !'
            ], style={'fontSize': '16px', 'marginBottom': '15px'}),
            html.P([
                html.Strong('Préférence de paiement : '),
                f'{mode_plus_utilise} ({pourcentage_modes[mode_plus_utilise]:.1f}%)'
            ], style={'fontSize': '16px', 'marginBottom': '15px'}),
            html.P([
                html.Strong('Valeur client : '),
                f'CLV moyenne de {clv_moyenne:.2f} €'
            ], style={'fontSize': '16px'}),
        ], style={'padding': '20px', 'background': '#f7fafc', 'borderRadius': '15px'})
    ], className='section-card'),
    
    # Footer
    html.Div([
        html.P('✨ Dashboard KPI créé avec Python Dash | © 2024 | Analyse Décisionnelle', 
               className='footer')
    ])
])

# ==============================================================================
# LANCEMENT DU SERVEUR
# ==============================================================================
server = app.server
if __name__ == '__main__':
    print("\n" + "="*80)
    print("🚀 DASHBOARD KPI EXERCICE 1 LANCÉ")
    print("="*80)
    print("\n📍 Ouvrez votre navigateur à l'adresse : http://127.0.0.1:8050/")
    print("\n📊 Tous les 6 KPI sont affichés de manière interactive !")
    print("⏹️  Appuyez sur Ctrl+C pour arrêter le serveur\n")
    
    app.run(debug=True, host='0.0.0.0', port=8050)