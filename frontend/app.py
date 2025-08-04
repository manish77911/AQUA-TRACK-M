

import streamlit as st
import requests
from datetime import datetime

API_URL = 'http://localhost:5000'

# --- Theme and Color Palette ---

# --- Only Dark Mode ---
THEME = {
    'primary': '#00CFC1',
    'accent': '#48CAE4',
    'background': '#121212',
    'card': '#1E1E2F',
    'text': '#FFFFFF',
    'secondary_text': '#A0A0A0',
    'progress': '#023E8A',
    'warning': '#FF7F7F',
}
theme = THEME

# --- Navigation ---

st.sidebar.title('AQUATRACK-M')
screen = st.sidebar.radio('Navigate', ['Onboarding', 'Dashboard', 'Reminders', 'History', 'Customization', 'Settings'])

# --- Custom CSS ---
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Roboto:wght@400&display=swap');
    html, body, [class^="css"] {{
        background-color: {theme['background']} !important;
        color: {theme['text']} !important;
        font-family: 'Roboto', 'Montserrat', sans-serif !important;
    }}
    /* Main content area */
    section.main {{
        background-color: {theme['background']} !important;
        color: {theme['text']} !important;
    }}
    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background-color: {theme['card']} !important;
        color: {theme['text']} !important;
    }}
    [data-testid="stSidebar"] .css-1v0mbdj, [data-testid="stSidebar"] .css-1lcbmhc {{
        color: {theme['text']} !important;
    }}
    .logo {{font-size:2.2rem; font-weight:700; color:{theme['primary']}; letter-spacing:1px; display:flex; align-items:center;}}
    .settings {{float:right; font-size:1.3rem; color:{theme['secondary_text']}; margin-top:-2.2rem; margin-right:0.5rem;}}
    .quote {{font-size:1.1rem; color:{theme['secondary_text']}; margin-bottom:1.5rem; font-style:italic;}}
    .card {{background:{theme['card']}; border-radius:16px; box-shadow:0 2px 8px #eee; padding:1.2rem 1.5rem; margin-bottom:1.2rem;}}
    .progress-label {{font-size:1.1rem; font-weight:600; margin-bottom:0.2rem;}}
    .progress-bar {{height:18px; border-radius:10px; background:{theme['progress']};}}
    .quick-btn {{background:{theme['progress']}; border:none; border-radius:12px; padding:0.8rem 2.2rem; font-size:1.1rem; margin:0.3rem; cursor:pointer;}}
    .quick-btn:hover {{background:{theme['accent']};}}
    .reminder-card {{background:{theme['background']}; border-radius:14px; box-shadow:0 1px 4px #eee; padding:1rem 1.2rem; margin-top:1.2rem;}}
    </style>
''', unsafe_allow_html=True)

# --- Header/logo and settings icon ---
st.markdown('<div class="logo">💧 AQUATRACK-M <span class="settings">⚙️</span></div>', unsafe_allow_html=True)
st.markdown('<div class="quote">"Drink water like your life depends on it — because it does."</div>', unsafe_allow_html=True)

# --- Screens ---
if screen == 'Onboarding':
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header('Welcome! Let’s set up your hydration profile.')
    st.write('Animated water waves coming soon...')
    gender = st.selectbox('Gender', ['Male', 'Female', 'Other'])
    age = st.number_input('Age', min_value=10, max_value=100, value=25)
    weight = st.number_input('Weight (kg)', min_value=30, max_value=200, value=60)
    activity = st.selectbox('Activity Level', ['Low', 'Moderate', 'High'])
    if st.button('Calculate Daily Goal'):
        resp = requests.post(f'{API_URL}/calculate_goal', json={'weight': weight})
        st.session_state['goal'] = resp.json()['daily_goal_ml']
        st.success(f"Your daily goal is {st.session_state['goal']} ml!")
    st.markdown('</div>', unsafe_allow_html=True)
    st.info('💡 Fun Fact: Up to 60% of the human body is water!')

elif screen == 'Dashboard':
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header('Daily Progress')
    total = st.session_state.get('total_today', 0)
    goal = st.session_state.get('goal', 1600)
    percent = min(total / goal, 1.0) if goal else 0
    st.markdown(f'<b>{total/1000:.1f}L / {goal/1000:.1f}L</b>', unsafe_allow_html=True)
    st.progress(percent)
    st.markdown(f'<span style="color:{theme['primary']};">{(goal-total)/1000:.1f}L remaining to reach your goal today.</span>', unsafe_allow_html=True)
    st.markdown(f'<span style="float:right;color:{theme['secondary_text']};font-size:0.95rem;">{int(percent*100)}% Complete</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header('Log Water Intake')
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('💧 150 ml', key='btn150', help='Log 150ml'):
            now = datetime.now().isoformat()
            requests.post(f'{API_URL}/log_intake', json={'amount_ml': 150, 'timestamp': now})
            st.session_state['total_today'] = st.session_state.get('total_today', 0) + 150
    with col2:
        if st.button('💧 250 ml', key='btn250', help='Log 250ml'):
            now = datetime.now().isoformat()
            requests.post(f'{API_URL}/log_intake', json={'amount_ml': 250, 'timestamp': now})
            st.session_state['total_today'] = st.session_state.get('total_today', 0) + 250
    with col3:
        if st.button('💧 500 ml', key='btn500', help='Log 500ml'):
            now = datetime.now().isoformat()
            requests.post(f'{API_URL}/log_intake', json={'amount_ml': 500, 'timestamp': now})
            st.session_state['total_today'] = st.session_state.get('total_today', 0) + 500

    custom_amount = st.text_input('Custom amount (ml)', '', key='custom_amt')
    if st.button('Log Custom', key='btnCustom'):
        try:
            amt = int(custom_amount)
            if amt > 0:
                now = datetime.now().isoformat()
                requests.post(f'{API_URL}/log_intake', json={'amount_ml': amt, 'timestamp': now})
                st.session_state['total_today'] = st.session_state.get('total_today', 0) + amt
                st.success(f'Logged {amt}ml!')
        except:
            st.error('Please enter a valid number.')
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="reminder-card">', unsafe_allow_html=True)
    st.markdown(f'<b>🔔 Reminders</b><br><span style="color:{theme['secondary_text']};">Reminders are active every 60 minutes between 6:00 am and 10:10 pm.</span><br><span style="color:{theme['secondary_text']};font-size:0.95rem;">Next check around: 7:05 PM</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif screen == 'Reminders':
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header('Reminder Schedule')
    st.write('Customize your reminder intervals and sounds.')
    interval = st.slider('Interval (minutes)', 30, 180, 60, 10)
    sound = st.selectbox('Sound', ['Water Droplet', 'Splash', 'Soft Bell'])
    st.button('Save Reminder Settings')
    st.markdown('</div>', unsafe_allow_html=True)

elif screen == 'History':
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header('Water Log History')
    st.write('View your hydration performance over time.')
    st.write('Calendar and stats coming soon...')
    st.line_chart([1200, 1600, 1800, 1400, 2000, 1700, 1500])
    st.markdown('</div>', unsafe_allow_html=True)

elif screen == 'Customization':
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header('Unique Features')
    st.write('Track your hydration streaks, mood, and set custom goals for each day.')
    # Hydration streak tracker
    if 'streak' not in st.session_state:
        st.session_state['streak'] = 0
    if st.button('Log Today as Goal Met'):
        st.session_state['streak'] += 1
    st.write(f"🔥 Hydration Streak: {st.session_state['streak']} days")
    # Mood tracker
    mood = st.selectbox('How do you feel today?', ['Energetic', 'Normal', 'Tired', 'Headache', 'Other'])
    st.write(f"Today's mood: {mood}")
    # Custom daily goal per day
    custom_goal = st.number_input('Set custom water goal for today (ml)', min_value=500, max_value=5000, value=st.session_state.get('goal', 1600))
    if st.button('Save Custom Goal'):
        st.session_state['goal'] = custom_goal
        st.success(f"Custom goal for today set to {custom_goal} ml!")
    st.markdown('</div>', unsafe_allow_html=True)

elif screen == 'Settings':
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header('Settings')
    st.write('Configure your app preferences below.')
    notif = st.checkbox('Enable notifications', value=True)
    sync = st.checkbox('Sync with Google Fit / Apple Health', value=False)
    lang = st.selectbox('Language', ['English', 'Spanish', 'French', 'Other'])
    time_fmt = st.radio('Time Format', ['12-hour', '24-hour'])
    st.write(f'Notifications: {notif}, Sync: {sync}, Language: {lang}, Time Format: {time_fmt}')
    st.markdown('</div>', unsafe_allow_html=True)
