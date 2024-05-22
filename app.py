import streamlit as st
import http.client
import urllib

# Alkalmazás címe
st.title("Anna 10. szülinapi visszajelzés")

# Session state az űrlap adatainak tárolásához
if 'form_submitted' not in st.session_state:
    st.session_state['form_submitted'] = False
    st.session_state['name'] = ''
    st.session_state['attendance'] = ''

if st.session_state['form_submitted']:
    st.success(f"Köszönjük, {st.session_state['name']}! A visszajelzés elküldve!")
    st.session_state['form_submitted'] = False
else:
    # Form létrehozása
    with st.form(key='attendance_form'):
        # Név mező
        name = st.text_input("Név")
        
        # Radio button alapértelmezett érték nélkül
        attendance = st.radio("Részvétel", options=["Tudok jönni", "Nem tudok jönni"], index=None)
        
        # Mentés gomb
        submit_button = st.form_submit_button(label="Mentés")

    # Form eredmény kezelése
    if submit_button:
        if not name:
            st.warning("Kérjük, add meg a neved!")
        elif attendance is None:
            st.warning("Kérjük, válaszd ki, hogy tudsz-e jönni!")
        else:
            st.write("Köszönjük, hogy kitöltötted az űrlapot! Mentés folyamatban...")
            
            if attendance == "Tudok jönni":
                message = f"{name} tud jönni a bulira!"
            else:
                message = f"{name} nem tud jönni sajnos."
                
            # Pushover üzenet küldése
            conn = http.client.HTTPSConnection("api.pushover.net:443")
            conn.request("POST", "/1/messages.json",
              urllib.parse.urlencode({
                "token": "anw4j6o8ycyg2jou2iapr2u79avydq",
                "user": "urmeuez42s27uma7rqvx5av92hj2ad",
                "message": message,
              }), { "Content-type": "application/x-www-form-urlencoded" })
            response = conn.getresponse()
            
            # Az űrlap adatok tárolása session state-ben
            st.session_state['form_submitted'] = True
            st.session_state['name'] = name
            st.session_state['attendance'] = attendance

            # Visszajelzés az üzenet elküldéséről
            st.experimental_rerun()