# Importing libraries
import re
import io
import folium
import requests
import pandas as pd
import google.generativeai as genai
import streamlit as st
import speech_recognition as sr
from datetime import date
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium
from folium.plugins import LocateControl
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

# --- Configuration ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

st.set_page_config(page_title="FLITO: AI Traveling Blogger", page_icon="🌍", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('pages/countries.csv')
        df['Country'] = df['Country'].astype(str)
        df['City'] = df['City'].astype(str)
        df['Currency_Code'] = df['Currency_Code'].astype(str)
        return df
    except FileNotFoundError:
        st.error("Error: 'countries.csv' file not found.")
        return pd.DataFrame(columns=['Country', 'City', 'Currency_Code'])

df = load_data()

def get_countries():
    if not df.empty:
        return sorted(df['Country'].unique().tolist())
    return []

def get_cities(country):
    if not df.empty and country:
        return sorted(df[df['Country'] == country]['City'].unique().tolist())
    return []

def transcribe_audio(audio_file):
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language="en-US")
            return text
    except sr.UnknownValueError:
        return "Could not understand audio."
    except sr.RequestError as e:
        return f"Could not request results; {e}"
    except Exception as e:
        return f"Error processing audio: {e}"

st.markdown("""
<style>
    .stApp { background-color: #0C1B2A; color: #FFFFFF; }
    header[data-testid="stHeader"] { background-color: #0C1B2A !important; color: #FFFFFF !important; }
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown, div[data-testid="stMarkdownContainer"] > p { color: #FFFFFF !important; }
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #1F284A !important; color: #FFFFFF !important;
        border: 1px solid #CDA555 !important; caret-color: #FFFFFF !important;
    }
    .stDateInput > div > div, .stNumberInput > div > div { background-color: #1F284A !important; }
    .stDateInput input, .stNumberInput input { background-color: #1F284A !important; color: #FFFFFF !important; border: 1px solid #CDA555 !important; }
    .stSelectbox > div > div > div { background-color: #1F284A !important; color: #FFFFFF !important; border: 1px solid #CDA555 !important; }
    [data-baseweb="popover"], [data-baseweb="menu"], [role="listbox"] { background-color: #0C1B2A !important; border: 1px solid #CDA555 !important; }
    [role="option"] { background-color: #1F284A !important; color: #FFFFFF !important; }
    [role="option"]:hover, [role="option"][aria-selected="true"] { background-color: #CDA555 !important; color: #0C1B2A !important; }
    .stSelectbox svg { fill: #FFFFFF !important; }
    .stSelectbox div[data-baseweb="select"] > div { color: white !important; -webkit-text-fill-color: white !important; }
    div[data-baseweb="segmented-control"] { background-color: #1F284A !important; border: 1px solid #CDA555 !important; padding: 2px !important; }
    div[data-baseweb="segmented-control"] > div { color: #FFFFFF !important; background-color: transparent !important; font-weight: bold !important; }
    div[data-baseweb="segmented-control"] > div[aria-selected="true"] { background-color: #CDA555 !important; color: #0C1B2A !important; }
    div[data-baseweb="segmented-control"] > div:hover { color: #CDA555 !important; }
    div[data-testid="stAudioInput"] { background-color: #1F284A !important; border: 1px solid #CDA555 !important; border-radius: 8px !important; padding: 10px !important; color: #FFFFFF !important; }
    div[data-testid="stAudioInput"] button { background-color: #CDA555 !important; color: #0C1B2A !important; border: 1px solid #CDA555 !important; font-weight: bold !important; transition: all 0.3s ease; }
    div[data-testid="stAudioInput"] button:hover { background-color: #0C1B2A !important; color: #FFFFFF !important; border: 1px solid #CDA555 !important; }
    div[data-testid="stAudioInput"] > * { color: #FFFFFF !important; }
    .stButton > button, .stFormSubmitButton > button, .stDownloadButton > button,
    .stLinkButton > a, a[data-baseweb="link-button"] {
        background-color: #CDA555 !important; color: #0C1B2A !important;
        border: 1px solid #CDA555 !important; font-weight: bold !important;
        transition: all 0.3s ease !important; text-decoration: none !important;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover, .stDownloadButton > button:hover,
    .stLinkButton > a:hover, a[data-baseweb="link-button"]:hover {
        background-color: #1F284A !important; color: #FFFFFF !important;
        border: 1px solid #CDA555 !important; transform: scale(1.02);
    }
    div[data-testid="stDataFrame"] { border: 1px solid #CDA555; padding: 5px; background-color: #1F284A; }
    .stTabs [data-baseweb="tab-list"] { gap: 25px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: transparent; border-radius: 4px 4px 0px 0px; transition: color 0.3s, background-color 0.3s; }
    .stTabs [data-baseweb="tab"]:hover { color: #CDA555 !important; background-color: rgba(255,255,255,0.05); }
    .stTabs [aria-selected="true"] { background-color: rgba(255,255,255,0.1); color: #CDA555 !important; border-bottom-color: #CDA555 !important; }
    section[data-testid="stSidebar"] { background-color: #0C1B2A; border-right: 1px solid #CDA555; }
    [data-testid="stForm"] { background-color: #1F284A; padding: 20px; border-radius: 10px; border: 1px solid #CDA555; }
</style>
""", unsafe_allow_html=True)

# --- Back to Home ---
if st.button("← Back to Web Stream"):
    st.switch_page("app.py")

st.title("FLITO: AI Traveling Blogger & Reviewer")
st.write("Discover hotels, restaurants, tourist attractions, transportation, plan your budget easily, and transfer your currencies!!!")

# --- Initialize session state ---
if "budget" not in st.session_state:
    st.session_state["budget"] = 1000
if "expenses" not in st.session_state:
    st.session_state["expenses"] = []

# --- PDF Helper Functions ---
def escape_html(text):
    return (text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))

def convert_markdown_to_html(text):
    text = escape_html(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'\[(.+?)\]\((https?://[^\)]+)\)', r'<a href="\2" color="blue">\1</a>', text)
    text = re.sub(r'(?<!href=")(https?://[^\s<>"]+)', r'<a href="\1" color="blue">\1</a>', text)
    return text

def generate_pdf_from_text(text_content):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()
    story = []
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor('#1a1a1a'), spaceAfter=14, spaceBefore=10, leading=20)
    heading2_style = ParagraphStyle('CustomHeading2', parent=styles['Heading2'], fontSize=13, textColor=colors.HexColor('#2c3e50'), spaceAfter=10, spaceBefore=8, leading=16, leftIndent=10)
    heading3_style = ParagraphStyle('CustomHeading3', parent=styles['Heading3'], fontSize=11, textColor=colors.HexColor('#34495e'), spaceAfter=8, spaceBefore=6, leading=14, leftIndent=15)
    bold_style = ParagraphStyle('BoldText', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#2c3e50'), spaceAfter=6, leading=14, leftIndent=20)
    normal_style = ParagraphStyle('CustomNormal', parent=styles['Normal'], fontSize=10, spaceAfter=6, leading=14, leftIndent=20)
    bullet_style = ParagraphStyle('BulletStyle', parent=styles['Normal'], fontSize=10, spaceAfter=4, leading=14, leftIndent=35, bulletIndent=25)

    lines = text_content.split('\n')
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped:
            story.append(Spacer(1, 8)); i += 1; continue
        if '|' in stripped and i + 1 < len(lines) and '|' in lines[i + 1]:
            table_data = []
            while i < len(lines) and '|' in lines[i].strip():
                row = lines[i].strip()
                if re.match(r'^[\|\s\-:]+$', row): i += 1; continue
                cells = [cell.strip() for cell in row.split('|') if cell]
                if cells: table_data.append(cells)
                i += 1
            if table_data:
                t = Table(table_data, hAlign='CENTER')
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('TOPPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
                ]))
                story.append(Spacer(1, 8)); story.append(t); story.append(Spacer(1, 12))
            continue
        if stripped.startswith('###'): story.append(Paragraph(convert_markdown_to_html(stripped.replace('###', '').strip()), heading3_style))
        elif stripped.startswith('##'): story.append(Paragraph(convert_markdown_to_html(stripped.replace('##', '').strip()), heading2_style))
        elif stripped.startswith('#'): story.append(Paragraph(convert_markdown_to_html(stripped.replace('#', '').strip()), title_style))
        elif stripped.startswith('**') and stripped.endswith('**'): story.append(Paragraph(f'<b>{escape_html(stripped.replace("**", "").strip())}</b>', bold_style))
        elif stripped.startswith(('*', '- ')): story.append(Paragraph(f'• {convert_markdown_to_html(stripped.lstrip("*-").strip())}', bullet_style))
        elif re.match(r'^\d+\.', stripped): story.append(Paragraph(convert_markdown_to_html(stripped), bold_style))
        else: story.append(Paragraph(convert_markdown_to_html(stripped), normal_style))
        i += 1
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def get_conversion_rates(base_currency):
    api_key = 'dfbe254500a0c3bf02a8c3df'
    request = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}'
    response = requests.get(request)
    if response.status_code == 200:
        return response.json()
    return None

# --- Sidebar ---
with st.sidebar:
    st.header("Customize the app!")
    output_number = st.slider("How many outputs shall I suggest?:", 1, 10, 1, key="output_num")
    show_location = st.toggle("Show your location")
    st.divider()
    st.write('Rate us (out of 5):')
    rating = st.feedback('stars', key="trip_rating")
    #feedback = st.text_input("Any suggestions for improvement?")
    #if st.button('Send your Feedback', key='feedback'):
    #    st.write("Thanks For Your FeedBack!")
    #st.divider()
    #st.subheader('Would you like to go Premium?')
    #st.link_button('Subscribe now!', 'https://buy.stripe.com/test_3cIcN592b5iLfN93mU8so00')

# --- Tabs ---
map_tab, hotels_tab, food_tab, touristic_tab, transpotation_tab, shopping_tab, budget_tab, currency_tab, translate_tab, trip_builder_tab, extra_tab = st.tabs([
    "🗺️ Map", "🏨 Hotels", "🍝 Food", "🏝️ Tourism", "🚗 Transportation", "🛍️ Shopping",
    "💰 Budget", "💱 Currency", "🗣️ Translation", "✈️ Trip Builder (Premium)", "LINKS"
])

countries_list = get_countries()

# --- Map Tab ---
with map_tab:
    st.subheader("Your Location in the map!")
    if show_location:
        st.write("Check our interactive map...")
        col1, col2 = st.columns([3, 1])
        with col1:
            search_query = st.text_input("🔍 Search for a location", placeholder="Enter city, address, or landmark...", label_visibility="collapsed")
        default_lat, default_lon = 30.0444, 31.2357
        map_center = [default_lat, default_lon]
        zoom_level = 12
        if search_query:
            try:
                geolocator = Nominatim(user_agent="streamlit_map_app", timeout=10)
                with st.spinner(f"Searching for '{search_query}'..."):
                    location = geolocator.geocode(search_query)
                if location:
                    map_center = [location.latitude, location.longitude]
                    zoom_level = 15
                    st.success(f"📍 Found: {location.address}")
                else:
                    st.warning(f"Location '{search_query}' not found. Showing default location.")
            except Exception as e:
                st.error(f"Error searching location: {str(e)}")
        m = folium.Map(location=map_center, zoom_start=zoom_level)
        if search_query and 'location' in locals() and location:
            folium.Marker(
                [location.latitude, location.longitude],
                popup=location.address,
                tooltip="Searched Location",
                icon=folium.Icon(color='red', icon='search')
            ).add_to(m)
        LocateControl(auto_start=False).add_to(m)
        output = st_folium(m, height=700, use_container_width=True, returned_objects=["last_clicked"])
        if output["last_clicked"]:
            st.success(f"Your Location Selected:\nLatitude: {output['last_clicked']['lat']:.5f}, Longitude: {output['last_clicked']['lng']:.5f}")
        else:
            st.info("Click on the map or use the location button to specify your current location.")
    else:
        st.info("Select 'Show Location' in the sidebar to view your real-time location on the map.")

# --- Hotels Tab ---
with hotels_tab:
    st.subheader("Search nearest and best hotels now!")
    col1, col2 = st.columns(2)
    with col1:
        hotel_country = st.selectbox('Country:', countries_list, key="h_country")
        hotel_price = st.selectbox('Price/night:', ['Cheap', 'Moderate', 'Expensive'], key="h_price")
    with col2:
        h_cities = get_cities(hotel_country)
        hotel_city = st.selectbox('City:', h_cities, key="h_city")
        st.write('Minimum star rating:')
        hotel_rating = st.feedback('stars', key="h_rating")
    st.write('---')
    hotel_extra = st.text_area('Extra details (optional)', key="h_extra")
    if st.button('🔎 Search now', key='hotel_search'):
        if not hotel_city or not hotel_country:
            st.error("Please select both a country and a city.")
        else:
            val_rating = hotel_rating + 1 if hotel_rating is not None else 3
            prompt = f"""Suggest for me a {val_rating}-stars hotel in {hotel_city} and in {hotel_country} with {hotel_price} price range.
Give me {output_number} options and consider the following details for each:
1. Name of the hotel
2. Address
3. People Rating (out of 5)
4. Price range per night formatted in a table if available
5. Facilities (e.g. swimming pool, gym, wifi, etc.)
6. Contact information (e.g. phone, hotline, etc.)

Extra notes: {hotel_extra}

Please format the response clearly with each hotel as a separate section.
Make your answer short and focused only on what I requested."""
            with st.spinner('Searching...'):
                response = model.generate_content(prompt)
                st.write(response.text)
                pdf_content = generate_pdf_from_text(response.text)
                st.download_button(label='Download PDF ⬇️', data=pdf_content, file_name='hotel_recommendations.pdf', mime="application/pdf")

# --- Food Tab ---
with food_tab:
    st.subheader("Search Restaurants & Cafes!")
    col1, col2 = st.columns(2)
    with col1:
        place = st.selectbox('Type of place:', ['Restaurant', 'Cafe', 'Restaurant & Cafe'], key='food_place')
        food_country = st.selectbox('Country:', countries_list, key='food_country')
        price = st.selectbox('Price level:', ['Cheap', 'Moderate', 'Expensive'], key='food_price')
    with col2:
        choice = st.text_input("What do you want eat/drink?", key="food_choice")
        f_cities = get_cities(food_country)
        food_city = st.selectbox('City:', f_cities, key='food_city')
        min_rating = st.slider('Minimum Rating:', 1, 5, 3, key='food_rating')
    st.write('---')
    extra = st.text_area('Extra details (optional):', key='food_extra')
    if st.button('Search now', key='food_search'):
        if not food_city or not food_country:
            st.error("Please select both a country and a city.")
        else:
            prompt = f"""Suggest for me a {place} for {choice} with a minimum rating of {min_rating} stars or more.
The place should be {price} in price.
Give me {output_number} options in {food_city}, {food_country} to consider with the following details for each:
1. Name of the place
2. Address
3. Rating (out of 5)
4. Price range and menu formatted in a table if available
5. Specialties
6. Brief description
7. Contact information (e.g. phone, hotline, etc.)

Extra notes: {extra}

Please format the response clearly with each restaurant as a separate section.
Make your answer short and focused only on what I requested."""
            with st.spinner('Searching...'):
                response = model.generate_content(prompt)
                st.write(response.text)
                pdf_content = generate_pdf_from_text(response.text)
                st.download_button(label='Download PDF ⬇️', data=pdf_content, file_name='food_recommendations.pdf', mime="application/pdf")

# --- Touristic Tab ---
with touristic_tab:
    st.subheader("Discover Tourist Attractions!")
    col1, col2 = st.columns(2)
    with col1:
        attraction_type = st.selectbox('Type of attraction', ['Museum', 'Historical Site', 'Natural Wonder', 'Theme Park', 'Monument', 'Beach', 'Temple/Religious Site'], key='tourism_type')
        tourist_country = st.selectbox('Country', countries_list, key='tourist_country')
        tourist_rating = st.slider('Min Rating', 1, 5, 3, key='tourist_rating')
    with col2:
        activity_preference = st.selectbox('Activity preference', ['Sightseeing', 'Adventure', 'Relaxation', 'Cultural Experience', 'Photography', 'Family Fun'], key='tourism_activity')
        t_cities = get_cities(tourist_country)
        tourist_city = st.selectbox('City', t_cities, key='tourist_city')
        tourist_price = st.selectbox('Cost', ['Free', 'Budget-friendly', 'Moderate', 'Premium'], key='tourist_price')
    st.write('---')
    tourist_extra = st.text_area('Extra details (optional)', key='tourist_extra')
    if st.button('Discover now', key='tourist_search'):
        if not tourist_city or not tourist_country:
            st.error("Please select both a country and a city.")
        else:
            prompt = f"""Suggest for me {attraction_type} tourist attractions for {activity_preference} in {tourist_city}, {tourist_country}.
The places should have a minimum rating of {tourist_rating} stars or more, be {tourist_price}.

Give me {output_number} options to consider with the following details for each:
1. Name of the attraction
2. Address
3. Rating (out of 5)
4. Entry fees/ticket prices in a table format if available
5. Best time to visit
6. Main highlights and activities
7. Brief description
8. Contact information and opening hours
9. Tips for visitors

Extra notes: {tourist_extra}

Please format the response clearly with each attraction as a separate section.
Make your answer short and focused only on what I requested."""
            with st.spinner('Discovering attractions...'):
                response = model.generate_content(prompt)
                st.write(response.text)
                pdf_content = generate_pdf_from_text(response.text)
                st.download_button(label='Download PDF ⬇️', data=pdf_content, file_name='tourist_recommendations.pdf', mime="application/pdf")

# --- Transportation Tab ---
with transpotation_tab:
    st.subheader("Know How To Go!")
    movement_type = st.selectbox('Type of Movement', ["Any", "Taxi", "Bus", "Train", "Flight", "Car Rental"], key='movement_type')
    st.markdown("#### Location of Transport / Destination")
    col1, col2 = st.columns(2)
    with col1:
        movement_country = st.selectbox('Country', countries_list, key='movement_country')
        movement_from = st.text_input("From (Specific Location/Landmark)", placeholder="e.g. Airport, Hotel X", key="movment_from")
        movement_rating = st.slider('Min Rating', 1, 5, 3, key='movement_rating')
    with col2:
        m_cities = get_cities(movement_country)
        movement_city = st.selectbox('City', m_cities, key='movement_city')
        movement_to = st.text_input("To (Specific Location/Landmark)", placeholder="e.g. City Center, Museum Y", key="movment_to")
        movement_price = st.selectbox('Cost', ['Free', 'Budget-friendly', 'Moderate', 'Premium'], key='movement_price')
    st.write('---')
    movement_extra = st.text_area('Extra details (optional)', key='movement_extra')
    if st.button('Move now', key='movement_search'):
        if not movement_city or not movement_country:
            st.error("Please select both a country and a city.")
        else:
            prompt = f"""Suggest for me a {movement_type} in {movement_city}, {movement_country}.
I need to go from {movement_from} to {movement_to}.
The {movement_type} should have a minimum rating of {movement_rating} stars or more, and its price should be {movement_price}.

Give me {output_number} options to consider with the following details for each:
1. Name of the vehicle/Service Provider
2. Rating (out of 5)
3. Price estimation
4. Brief description
5. Contact information and opening hours

Extra notes: {movement_extra}

Please format the response clearly with each option as a separate section.
Make your answer short and focused only on what I requested."""
            with st.spinner('Searching For Movement...'):
                response = model.generate_content(prompt)
                st.write(response.text)
                pdf_content = generate_pdf_from_text(response.text)
                st.download_button(label='Download PDF ⬇️', data=pdf_content, file_name='movement_recommendations.pdf', mime="application/pdf")

# --- Shopping Tab ---
with shopping_tab:
    st.subheader("Shop til you drop!")
    st.write("Find the best malls, stores, and markets.")
    col1, col2 = st.columns(2)
    with col1:
        shop_country = st.selectbox("Country", countries_list, key="shop_country")
        shop_type = st.selectbox("Type of Shopping", ["Shopping Mall", "Outlet", "Local Market", "Boutique", "Souvenir Shop", "Street Market"], key="shop_type")
    with col2:
        s_cities = get_cities(shop_country)
        shop_city = st.selectbox("City", s_cities, key="shop_city")
        shop_focus = st.text_input("What are you looking for?", placeholder="e.g. Clothes, Electronics, Local Crafts", key="shop_focus")
    st.write('---')
    shop_extra = st.text_area("Extra details (optional)", key="shop_extra")
    if st.button("Find Shopping Places", key="shop_search"):
        if not shop_city or not shop_country:
            st.error("Please select both a country and a city.")
        else:
            prompt = f"""I am looking for shopping recommendations in {shop_city}, {shop_country}.
I am specifically interested in {shop_type} and looking for {shop_focus}.

Please provide {output_number} recommendations. For each place include:
1. Name of the Place
2. Type (Mall, Market, etc.)
3. What they are best known for
4. Approximate price range (Budget-friendly/Moderate/Expensive)
5. Address
6. Opening Hours if available

Extra notes: {shop_extra}

Please format the response clearly with each shopping place as a separate section.
Make your answer short and focused only on what I requested."""
            with st.spinner('Finding the best places to shop...'):
                response = model.generate_content(prompt)
                st.write(response.text)
                pdf_content = generate_pdf_from_text(response.text)
                st.download_button(label='Download PDF ⬇️', data=pdf_content, file_name='shopping_recommendations.pdf', mime="application/pdf")

# --- Budget Tab ---
with budget_tab:
    st.subheader("Make A Good Budget of your Trip!")
    st.session_state["budget"] = st.number_input("Enter your budget:", min_value=10, value=st.session_state["budget"], step=1)
    with st.form("add_expense_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            expense_name = st.text_input("Expense name", placeholder="e.g., Hotel night")
        with col2:
            expense_cost = st.number_input("Cost", min_value=0.0, value=0.0, step=1.0)
        submitted = st.form_submit_button("Add Expense")
        if submitted:
            if expense_name.strip():
                st.session_state["expenses"].append({"Expense": expense_name.strip(), "Cost": float(expense_cost)})
                st.success(f"Added: {expense_name.strip()} — ${expense_cost:.2f}")
            else:
                st.warning("Please enter a name and a non-negative cost.")
    if st.session_state["expenses"]:
        to_delete = st.selectbox("Delete an expense (optional)", ["—"] + [e["Expense"] for e in st.session_state["expenses"]], index=0)
        if to_delete != "—":
            st.session_state["expenses"] = [e for e in st.session_state["expenses"] if e["Expense"] != to_delete]
            st.success(f"Deleted: {to_delete}")
            st.rerun()
        df_expenses = pd.DataFrame(st.session_state["expenses"])
        styled_df = df_expenses.style.set_properties(**{'background-color': "#1F284A", 'color': "#ffffff", 'border-color': "#CDA555"})
        st.dataframe(styled_df, hide_index=True)
        total_spent = float(df_expenses["Cost"].sum()) if not df_expenses.empty else 0.0
        remaining = st.session_state["budget"] - total_spent
        st.write(f"**Total Spent:** ${total_spent:,.2f}")
        st.write(f"**Remaining:** ${remaining:,.2f}")
        if st.button("Clear all expenses"):
            st.session_state["expenses"].clear()
            st.info("All expenses cleared.")
            st.rerun()
    else:
        st.info("No expenses added yet.")

# --- Currency Tab ---
with currency_tab:
    st.subheader('💱 Currency Converter')
    st.write('Convert all currencies in real-time!')
    if not df.empty:
        all_currencies = sorted(df['Currency_Code'].dropna().unique().tolist())
        for c in ['USD', 'EUR', 'GBP']:
            if c not in all_currencies:
                all_currencies.append(c)
        all_currencies = sorted(list(set(all_currencies)))
    else:
        all_currencies = ['USD', 'EUR']
    col1, col2 = st.columns(2)
    with col1:
        idx_usd = all_currencies.index('USD') if 'USD' in all_currencies else 0
        base_currency = st.selectbox('From currency', all_currencies, index=idx_usd, key='base_curr')
    with col2:
        idx_eur = all_currencies.index('EUR') if 'EUR' in all_currencies else 0
        target_currency = st.selectbox('To currency', all_currencies, index=idx_eur, key='target_curr')
    amount = st.number_input('Enter the amount:', min_value=0.01, value=1.0, step=0.01)
    if st.button('Calculate Rate', key='currency_calc'):
        with st.spinner('Fetching exchange rates...'):
            result = get_conversion_rates(base_currency)
            if result and 'conversion_rates' in result:
                rates = result['conversion_rates']
                if target_currency in rates:
                    exchange_rate = rates[target_currency]
                    total = exchange_rate * amount
                    st.success(f'{amount:,.2f} {base_currency} = {total:,.2f} {target_currency}')
                    st.info(f'Exchange Rate: 1 {base_currency} = {exchange_rate:,.4f} {target_currency}')
                else:
                    st.error(f'Currency {target_currency} not found in conversion rates.')
            else:
                st.error('Failed to fetch exchange rates. Please try again later.')

# --- Translation Tab ---
languages = [
    "English", "Chinese", "Hindi", "Spanish", "Arabic", "French", "Greek", "Swedish", "Dutch",
    "Bengali", "Portuguese", "Russian", "Indonesian", "Urdu", "German", "Japanese",
    "Nigerian Pidgin", "Marathi", "Telugu", "Turkish", "Hausa", "Tamil", "Estonian",
    "Yue Chinese (Cantonese)", "Western Punjabi", "Swahili", "Tagalog", "Wu Chinese", "Iranian Persian",
    "Korean", "Thai", "Italian", "Gujarati", "Amharic", "Kannada", "Bhojpuri",
    "Polish", "Ukrainian", "Malayalam", "Odia", "Uzbek", "Sindhi", "Romanian", "Chittagonian",
    "Igbo", "Northern Pashto", "South Azerbaijani", "Saraiki", "Nepali", "Sinhalese",
    "Zhuang", "Somali", "Belarusian", "Czech", "Zulu"
]

with translate_tab:
    st.subheader("Translate Any Language!")
    col1, col2 = st.columns(2)
    with col1:
        From_Language = st.selectbox('From Which Language', options=languages, key='From_lang')
    with col2:
        To_Language = st.selectbox("To which Language", options=languages, key="To_lang")
    st.write('---')
    The_Word = st.text_area("Enter the sentence you need to translate:", key="which_word")
    if st.button('Translate now', key='Translate_search'):
        prompt = f"""I need the translation of the following word "{The_Word}" from the {From_Language} language to the {To_Language} language.
Please format the response clearly with the word and its pronunciation only.
1. Meaning:
2. Pronunciation:
Make your answer short and focused only on what I requested."""
        with st.spinner('Translating the sentence...'):
            response = model.generate_content(prompt)
            st.write(response.text)

# --- Trip Builder Tab (Premium) ---
with trip_builder_tab:
    st.subheader("✈️ Premium Trip Builder")
    st.write("Get a complete day-by-day itinerary tailored to your dates and budget.")
    trip_code = st.text_input("Enter Premium Code to access Trip Builder:", type="password", key="trip_code_input")
    if trip_code == "5555":
        st.success("Access Granted!")
        st.subheader("Step 1: Trip Mode")
        with st.container():
            trip_type = st.segmented_control(
                "Select Trip Mode",
                options=["One City", "Multiple Cities"],
                default="One City",
                key="trip_mode_segment"
            )
            st.subheader("Step 2: Trip Details")
            col1, col2 = st.columns(2)
            with col1:
                trip_dest_country = st.selectbox("Destination Country", countries_list, key="trip_country")
                trip_start_date = st.date_input("Start Date", min_value=date.today())
                trip_budget = st.number_input("Total Trip Budget in USD ($):", min_value=100, value=1000)
            with col2:
                if trip_type == "One City":
                    tb_cities = get_cities(trip_dest_country)
                    trip_dest_city = st.selectbox("Destination City", tb_cities, key="trip_city")
                else:
                    st.info("🗺️ AI will distribute your trip across the best cities.")
                    trip_dest_city = "Multiple Cities"
                trip_end_date = st.date_input("End Date", min_value=date.today())
            st.subheader("Step 3: Preferences")
            input_mode = st.radio("How would you like to input preferences?", ["Text", "Voice AI (English)"], horizontal=True)
            trip_extra_req = ""
            if input_mode == "Text":
                trip_extra_req = st.text_area("Any specific preferences? (e.g. Vegetarian food, love museums, hate hiking)")
            else:
                audio_value = st.audio_input("Record your preferences (Click microphone)")
                if audio_value:
                    with st.spinner("Transcribing your voice..."):
                        transcribed_text = transcribe_audio(audio_value)
                        st.success(f"Heard: {transcribed_text}")
                        trip_extra_req = transcribed_text
            if st.button("Generate Plan!"):
                valid_input = (trip_dest_country and trip_start_date and trip_end_date)
                if trip_type == "One City" and not trip_dest_city:
                    valid_input = False
                if valid_input:
                    if trip_end_date < trip_start_date:
                        st.error("End date cannot be before start date.")
                    else:
                        delta = trip_end_date - trip_start_date
                        num_days = delta.days
                        if trip_type == "One City":
                            location_context = f"to {trip_dest_city}, {trip_dest_country}"
                        else:
                            location_context = f"touring multiple cities in {trip_dest_country}. Please distribute these {num_days} days logically across the best cities in this country."
                        prompt = f"""I will travel from {trip_start_date} to {trip_end_date} ({num_days} days) {location_context}.
My budget is {trip_budget} USD.
The date of travel is crucial to identify if it's in winter or summer, so the activities must differ based on the season.

Recommend hotels/stays by stating:
1. Hotel name (If multiple cities, suggest one for each city)
2. Address
3. Price list of stay in a table
4. Contact phone number
5. Website (If available)

AND please generate a detailed trip plan for EACH day (Day 1 to Day {num_days}).
For each day include specific recommendations for:
1. Food (Mention specific restaurants to try and cafes)
2. Activities and tourism places (Appropriate for the season/weather)
3. Shopping malls or areas

Extra preferences: {trip_extra_req}

Format the output clearly by Day (e.g., **Day 1: [Date] - [City Name]**).
Make the response brief for each day, keep it simple and very readable."""
                        with st.spinner(f"Building your {num_days}-day plan for {trip_dest_country}..."):
                            response = model.generate_content(prompt)
                            st.write(response.text)
                            pdf_content = generate_pdf_from_text(response.text)
                            st.download_button(label='Download Plan PDF ⬇️', data=pdf_content, file_name=f'{trip_dest_country}_trip.pdf', mime="application/pdf")
                else:
                    st.warning("Please fill in all destination and date fields.")
    else:
        st.error("Enter the code first to access premium trip builder!")

with extra_tab:
    st.link_button('Youtube', 'https://youtube.com')

st.write('---')
st.caption('🌟 AI-powered recommendations using Google Gemini | Currency data from ExchangeRate-API')
